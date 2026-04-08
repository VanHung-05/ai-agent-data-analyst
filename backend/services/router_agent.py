"""
Router Agent — Phân loại intent câu hỏi người dùng
=====================================================
Vai trò: Lễ tân / Người điều phối
  - Nhận input đầu tiên từ người dùng
  - Phân loại thành 1 trong 3 nhóm: conversation / sql / visualize
  - Trả confidence scores cho từng nhóm
  - Fallback rule-based nếu LLM lỗi
"""

import json
import re
from typing import Any

from utils.logger import logger

_ROUTER_LABELS = {"conversation", "sql", "visualize"}

_CONVERSATION_KEYWORDS = [
    "xin chào", "chào bạn", "chào", "hello", "hi", "hey", "alo",
    "bạn là ai", "bạn có thể làm gì", "giúp tôi", "hướng dẫn",
    "cảm ơn", "thank", "tạm biệt", "bye",
]

_VISUALIZE_KEYWORDS = [
    "biểu đồ", "chart", "vẽ", "visualize", "trực quan",
    "plot", "đồ thị", "graph", "hình ảnh hóa", "histogram",
    "pie chart", "bar chart", "line chart",
]


def rule_based_intent(question: str) -> str:
    """
    Fallback: phân loại intent bằng keyword matching.
    Dùng khi LLM router gặp lỗi hoặc trả kết quả không hợp lệ.
    """
    q = question.lower().strip()
    if not q:
        return "conversation"

    if any(kw in q for kw in _CONVERSATION_KEYWORDS):
        return "conversation"
    if any(kw in q for kw in _VISUALIZE_KEYWORDS):
        return "visualize"
    return "sql"


def route_detail(question: str, llm: Any) -> dict[str, Any]:
    """
    Router Agent chính: dùng LLM để chấm confidence score cho 3 intent.

    Args:
        question: Câu hỏi từ người dùng
        llm: Instance LLM (Gemini/OpenAI) đã khởi tạo

    Returns:
        dict: {
            "intent": "conversation" | "sql" | "visualize",
            "scores": {"conversation": 0.1, "sql": 0.8, "visualize": 0.1},
            "selected_agents": ["sql"],
            "routing_method": "llm" | "rule_based"
        }
    """
    fallback_intent = rule_based_intent(question)
    default_scores = {"conversation": 0.0, "sql": 0.0, "visualize": 0.0}
    default_scores[fallback_intent] = 1.0

    prompt = (
        "Bạn là Router Agent cho hệ thống phân tích dữ liệu trên Databricks.\n"
        "Nhiệm vụ: chấm điểm confidence cho 3 intent.\n\n"
        "Quy tắc phân loại:\n"
        '- "conversation": chào hỏi, hỏi khả năng, xã giao, không cần truy vấn dữ liệu\n'
        '- "sql": cần truy vấn/tra cứu/thống kê dữ liệu từ database\n'
        '- "visualize": yêu cầu vẽ biểu đồ, trực quan hóa, plot, chart\n\n'
        "Yêu cầu:\n"
        "- Mỗi giá trị trong [0, 1], tổng = 1.0\n"
        "- visualize bao gồm cả việc query dữ liệu rồi vẽ\n"
        "- Chỉ trả JSON thuần, không giải thích\n\n"
        'Format: {"conversation":0.1,"sql":0.1,"visualize":0.8}\n\n'
        f"Câu hỏi: {question}"
    )

    try:
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)

        json_match = re.search(r"\{[^{}]+\}", content)
        raw_json = json_match.group(0) if json_match else content.strip()
        parsed = json.loads(raw_json)

        scores: dict[str, float] = {}
        for label in _ROUTER_LABELS:
            val = float(parsed.get(label, 0.0))
            scores[label] = max(0.0, min(1.0, val))

        total = sum(scores.values())
        if total <= 0:
            scores = default_scores
        else:
            scores = {k: round(v / total, 4) for k, v in scores.items()}

        selected = max(scores, key=scores.get)  # type: ignore[arg-type]

        logger.info("Router LLM → intent=%s scores=%s", selected, scores)
        return {
            "intent": selected,
            "scores": scores,
            "selected_agents": [selected],
            "routing_method": "llm",
        }

    except Exception as exc:
        logger.warning("Router LLM failed, fallback rule-based: %s", exc)
        return {
            "intent": fallback_intent,
            "scores": default_scores,
            "selected_agents": [fallback_intent],
            "routing_method": "rule_based",
        }
