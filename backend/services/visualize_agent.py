"""
Visualize Agent — Chuyên gia hình ảnh hóa
============================================
Vai trò:
  - Nhận kết quả từ SQL Agent (data + columns)
  - Phân tích dữ liệu và quyết định loại biểu đồ phù hợp
  - Trả chart spec (chart_type, x, y, title) để Frontend vẽ hình
  - Heuristic rules xử lý nhanh các case rõ ràng
  - LLM xử lý các case mơ hồ mà heuristic không bắt được
"""

import json
import re
from typing import Any

from utils.logger import logger

_SUPPORTED_CHART_TYPES = {
    "metric", "line", "bar", "pie", "table", "scatter", "histogram", "area"
}

_CHART_KEYWORDS = {
    "line": ["line chart", "line", "đường", "xu hướng", "trend", "over time"],
    "bar": ["bar chart", "bar", "cột", "so sánh", "ranking", "xếp hạng", "top"],
    "pie": ["pie chart", "pie", "tròn", "tỷ lệ", "phần trăm", "ratio", "proportion"],
    "scatter": ["scatter", "phân tán", "correlation", "tương quan"],
    "histogram": ["histogram", "phân bố", "distribution", "tần suất"],
    "area": ["area chart", "area", "miền"],
}


def recommend_chart(
    question: str,
    sql: str,
    data: list[dict],
    llm: Any | None = None,
) -> dict:
    """
    Phân tích dữ liệu và đề xuất loại biểu đồ phù hợp.

    Args:
        question: Câu hỏi gốc của người dùng
        sql: Câu SQL đã thực thi
        data: Dữ liệu trả về từ Databricks (list of dicts)
        llm: Instance LLM. Nếu None, chỉ dùng heuristic.

    Returns:
        dict: {
            "chart_type": "metric"|"line"|"bar"|"pie"|"table",
            "x": str | None,
            "y": str | None,
            "title": str | None,
            "reason": str
        }
    """
    if not data:
        return {"chart_type": "table", "reason": "No data"}

    columns = list(data[0].keys())
    row_count = len(data)
    q = question.lower()
    sql_lower = sql.lower()
    x_col, y_col = _choose_axes(data, columns)

    # Người dùng chỉ định loại biểu đồ rõ ràng -> ưu tiên
    forced_chart = _detect_forced_chart_type(q)
    if forced_chart is not None:
        if forced_chart == "histogram":
            return {
                "chart_type": forced_chart,
                "x": y_col or x_col,
                "y": None,
                "title": _suggest_title(question, forced_chart),
                "reason": "User explicitly requested chart type",
            }
        return {
            "chart_type": forced_chart,
            "x": x_col,
            "y": y_col,
            "title": _suggest_title(question, forced_chart),
            "reason": "User explicitly requested chart type",
        }

    # === HEURISTIC: các case rõ ràng ===

    if row_count == 1 and len(columns) == 1:
        return {
            "chart_type": "metric",
            "x": None,
            "y": columns[0],
            "title": None,
            "label": columns[0],
            "value": data[0][columns[0]],
            "reason": "Single value result → metric card",
        }

    time_kw_question = ["tháng", "ngày", "trend", "xu hướng", "over time", "theo thời gian"]
    time_kw_sql = ["date", "timestamp", "year", "month", "day"]
    if any(kw in q for kw in time_kw_question) or any(kw in sql_lower for kw in time_kw_sql):
        if len(columns) >= 2:
            return {
                "chart_type": "line",
                "x": x_col,
                "y": y_col,
                "title": _suggest_title(question, "line"),
                "reason": "Time series detected",
            }

    if any(kw in q for kw in ["tỷ lệ", "phần trăm", "ratio", "percentage", "proportion"]):
        if len(columns) >= 2:
            return {
                "chart_type": "pie",
                "x": x_col,
                "y": y_col,
                "title": _suggest_title(question, "pie"),
                "reason": "Proportions/ratio detected",
            }

    if any(kw in q for kw in ["top", "so sánh", "ranking", "xếp hạng"]) or "group by" in sql_lower:
        if len(columns) >= 2:
            return {
                "chart_type": "bar",
                "x": x_col,
                "y": y_col,
                "title": _suggest_title(question, "bar"),
                "reason": "Comparison/ranking detected",
            }

    # === LLM: xử lý case mơ hồ mà heuristic không match ===
    if llm is not None:
        llm_result = _llm_recommend(question, sql, data, columns, llm)
        if llm_result is not None:
            return llm_result

    return {"chart_type": "table", "x": None, "y": None, "title": None, "reason": "Default table view"}


def _llm_recommend(
    question: str,
    sql: str,
    data: list[dict],
    columns: list[str],
    llm: Any,
) -> dict | None:
    """Dùng LLM để chọn chart type khi heuristic không xác định được."""
    try:
        sample_rows = data[:5]
        prompt = (
            "Bạn là Visualize Agent. Dựa vào câu hỏi, SQL, và dữ liệu mẫu, "
            "hãy chọn loại biểu đồ PHÙ HỢP NHẤT.\n"
            "Chỉ dùng 1 trong: metric, line, bar, pie, scatter, histogram, area, table.\n"
            "Trả JSON thuần đúng format, KHÔNG giải thích:\n"
            '{"chart_type":"...","x":"column_name","y":"column_name",'
            '"title":"Tiêu đề biểu đồ","reason":"Lý do ngắn"}\n\n'
            f"Question: {question}\n"
            f"SQL: {sql}\n"
            f"Columns: {columns}\n"
            f"Sample ({len(data)} rows total): {sample_rows}"
        )
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)

        json_match = re.search(r"\{[^{}]+\}", content)
        raw_json = json_match.group(0) if json_match else content.strip()
        parsed = json.loads(raw_json)

        chart_type = str(parsed.get("chart_type", "")).strip().lower()
        if chart_type not in _SUPPORTED_CHART_TYPES:
            return None

        logger.info("Visualize LLM → chart_type=%s", chart_type)
        return {
            "chart_type": chart_type,
            "x": parsed.get("x"),
            "y": parsed.get("y"),
            "title": parsed.get("title"),
            "reason": parsed.get("reason", "LLM suggestion"),
        }
    except Exception as exc:
        logger.warning("Visualize LLM failed, using table default: %s", exc)
        return None


def _detect_forced_chart_type(question_lower: str) -> str | None:
    for chart_type, kws in _CHART_KEYWORDS.items():
        if any(kw in question_lower for kw in kws):
            return chart_type
    return None


def _is_numeric_like(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        cleaned = value.replace(",", "").replace("_", "").strip()
        if cleaned == "":
            return False
        try:
            float(cleaned)
            return True
        except ValueError:
            return False
    return False


def _choose_axes(data: list[dict], columns: list[str]) -> tuple[str | None, str | None]:
    if not columns:
        return None, None

    numeric_cols: list[str] = []
    for col in columns:
        values = [row.get(col) for row in data]
        non_null = [v for v in values if v is not None]
        if not non_null:
            continue
        ratio = sum(1 for v in non_null if _is_numeric_like(v)) / len(non_null)
        if ratio >= 0.7:
            numeric_cols.append(col)

    non_numeric_cols = [c for c in columns if c not in numeric_cols]

    if non_numeric_cols and numeric_cols:
        return non_numeric_cols[0], numeric_cols[0]
    if len(numeric_cols) >= 2:
        return numeric_cols[0], numeric_cols[1]
    if len(columns) >= 2:
        return columns[0], columns[1]
    return columns[0], columns[0]


def _suggest_title(question: str, chart_type: str) -> str:
    q = question.strip().rstrip("?")
    if not q:
        return f"{chart_type.title()} chart"
    return q[:120]
