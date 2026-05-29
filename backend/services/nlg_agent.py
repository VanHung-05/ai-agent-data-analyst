"""
nlg_agent.py — Natural Language Generation (NLG)
==================================================
📌 TV2: chuyển kết quả SQL (rows) thành câu trả lời tự nhiên qua LLM.
"""

import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from utils.logger import logger

NLG_SYSTEM_PROMPT = """Bạn là trợ lý phân tích dữ liệu. Nhiệm vụ: viết lại kết quả truy vấn thành câu trả lời cho người dùng cuối.

Quy tắc:
- Chỉ dựa trên dữ liệu JSON được cung cấp; không bịa thêm cột, dòng hay số liệu.
- Hệ thống chỉ đọc dữ liệu (SELECT). Không bao giờ hứa/thực hiện UPDATE/DELETE/INSERT/DROP hay bất kỳ thao tác ghi nào; nếu câu hỏi gợi ý sửa/xóa dữ liệu thì từ chối lịch sự và nhắc chỉ hỗ trợ truy vấn đọc.
- Giọng lịch sự, ngắn gọn, dễ hiểu. Ưu tiên tiếng Việt nếu câu hỏi chủ yếu bằng tiếng Việt; nếu câu hỏi hoàn toàn bằng tiếng Anh thì trả lời tiếng Anh.
- Định dạng số tiền, phần trăm, số lớn cho dễ đọc (ví dụ phân cách hàng nghìn).
- Ưu tiên nhắc tên/mô tả có ý nghĩa (danh mục, thành phố, bang…). Mã ID chỉ nhắc ngắn trong ngoặc nếu cần tham chiếu kỹ thuật.
- Không in lại nguyên khối JSON; không giải thích quy trình SQL.
"""


def _truncate_data_for_nlg(data: list[dict], max_rows: int) -> tuple[list[dict], int, bool]:
    total = len(data)
    if total <= max_rows:
        return data, total, False
    return data[:max_rows], total, True


EMPTY_RESULT_SYSTEM = """Bạn là trợ lý phân tích dữ liệu. Truy vấn được chạy thành công nhưng không có kết quả nào (empty result).

Nhiệm vụ:
- Giải thích ngắn gọn, lịch sự tại sao không có dữ liệu (dựa vào câu hỏi và SQL được cung cấp).
- Nếu có thể, đề xuất 1-2 câu hỏi thay thế phù hợp để người dùng có thể hỏi tiếp.
- Giọng lịch sự, ngắn gọn. Tiếng Việt nếu câu hỏi là tiếng Việt.
- Không nói "lỗi", không đổ lỗi hệ thống. Đây là kết quả hợp lệ (rỗng)."""


def _generate_empty_result_answer(question: str, sql: str, llm: Any) -> str:
    """Gọi LLM sinh giải thích hợp lý khi query empty, kèm gợi ý câu hỏi tiếp theo."""
    sql_hint = f"\n\nSQL đã chạy:\n{sql}" if sql else ""
    user_block = (
        f"Câu hỏi người dùng: {question}{sql_hint}\n\n"
        "Kết quả trả về: không có dữ liệu nào (empty result).\n"
        "Hãy giải thích lý do và đề xuất câu hỏi thay thế phù hợp."
    )
    messages = [
        SystemMessage(content=EMPTY_RESULT_SYSTEM.strip()),
        HumanMessage(content=user_block),
    ]
    try:
        response = llm.invoke(messages)
        text = (response.content or "").strip()
        if text:
            return text
    except Exception as e:
        logger.warning("NLG empty result invoke thất bại: %s", e)
    return "Hiện tại không có dữ liệu phù hợp với yêu cầu này. Bạn có thể thử mở rộng tiêu chí tìm kiếm hoặc đặt câu hỏi khác."



def generate_natural_language_answer(
    question: str,
    data: list[dict],
    llm: Any,
    *,
    max_rows: int = 80,
    sql: str = "",
) -> str:
    """
    Gửi câu hỏi gốc + mẫu dữ liệu cho LLM để sinh câu trả lời tự nhiên.

    Args:
        question: Câu hỏi người dùng.
        data: Kết quả đã parse (list[dict]).
        llm: Chat model LangChain (invoke messages).
        max_rows: Giới hạn số dòng đưa vào prompt để tránh context quá dài.
        sql: Câu SQL đã thực thi (dùng để giải thích empty result).
    """
    if not data:
        return _generate_empty_result_answer(question, sql, llm)

    slice_rows, total, truncated = _truncate_data_for_nlg(data, max_rows)
    try:
        data_json = json.dumps(slice_rows, ensure_ascii=False, default=str, indent=2)
    except (TypeError, ValueError) as e:
        logger.warning("NLG: không serialize JSON, fallback repr: %s", e)
        data_json = repr(slice_rows)

    trunc_note = ""
    if truncated:
        trunc_note = f"\n(Lưu ý nội bộ: chỉ có {max_rows}/{total} dòng đầu trong dữ liệu; hãy nói rõ là có thêm dòng nếu cần.)\n"

    user_block = (
        f"Câu hỏi: {question}\n\n"
        f"Dữ liệu trả về từ cơ sở dữ liệu (JSON):\n{data_json}\n"
        f"{trunc_note}\n"
        "Hãy trả lời người dùng một cách lịch sự, súc tích, dựa đúng trên dữ liệu trên."
    )

    messages = [
        SystemMessage(content=NLG_SYSTEM_PROMPT.strip()),
        HumanMessage(content=user_block),
    ]

    try:
        response = llm.invoke(messages)
        text = (response.content or "").strip()
        if text:
            return text
    except Exception as e:
        logger.warning("NLG invoke thất bại: %s", e)

    return _fallback_answer(total)


def _fallback_answer(row_count: int) -> str:
    return f"Đã lấy được {row_count} dòng dữ liệu; không tạo được bản tóm tắt tự nhiên lúc này. Xem bảng chi tiết bên dưới."
