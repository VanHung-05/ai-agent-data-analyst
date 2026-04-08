"""
Conversation Agent — Chuyên gia giao tiếp
============================================
Vai trò:
  - Chào hỏi, giới thiệu khả năng hệ thống
  - Giải thích lỗi kỹ thuật cho người dùng một cách khéo léo
  - Hướng dẫn cách đặt câu hỏi đúng để agent SQL/Visualize xử lý được
"""

from typing import Any

from utils.logger import logger


def conversation_response(
    question: str,
    error_context: str | None = None,
    llm: Any | None = None,
) -> str:
    """
    Tạo phản hồi hội thoại cho người dùng.

    Args:
        question: Câu hỏi/tin nhắn gốc của người dùng
        error_context: Nếu có, đây là thông báo lỗi từ SQL Agent cần giải thích
        llm: Instance LLM (Gemini). Nếu None, dùng phản hồi tĩnh.

    Returns:
        str: Tin nhắn phản hồi bằng tiếng Việt
    """
    if error_context:
        return _handle_error(question, error_context, llm)
    return _handle_chat(question, llm)


def _handle_error(question: str, error_context: str, llm: Any | None) -> str:
    """Giải thích lỗi SQL/kỹ thuật cho người dùng."""
    fallback = (
        "Mình chưa lấy được dữ liệu do truy vấn gặp lỗi kỹ thuật. "
        "Bạn có thể thử diễn đạt lại câu hỏi rõ hơn, ví dụ: "
        "'Cho tôi <chỉ số> theo <thời gian/nhóm>'."
    )
    if llm is None:
        return fallback

    try:
        prompt = (
            "Bạn là Conversation Agent cho trợ lý phân tích dữ liệu Databricks.\n"
            "SQL Agent vừa gặp lỗi khi xử lý câu hỏi của người dùng.\n"
            "Hãy giải thích lỗi một cách ngắn gọn, KHÔNG đề cập chi tiết kỹ thuật, "
            "và gợi ý cách đặt lại câu hỏi.\n"
            "Trả lời bằng tiếng Việt, thân thiện, 2-3 câu.\n\n"
            f"Câu hỏi gốc: {question}\n"
            f"Lỗi kỹ thuật: {error_context}"
        )
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        return content.strip() or fallback
    except Exception as exc:
        logger.warning("Conversation error-handler LLM failed: %s", exc)
        return fallback


def _handle_chat(question: str, llm: Any | None) -> str:
    """Xử lý hội thoại thông thường (chào hỏi, hướng dẫn)."""
    q = question.lower()
    if any(greet in q for greet in ["xin chào", "chào", "hello", "hi", "hey"]):
        static_greeting = (
            "Chào bạn! Mình là trợ lý phân tích dữ liệu thông minh. "
            "Mình có thể giúp bạn:\n"
            "• Truy vấn dữ liệu bằng ngôn ngữ tự nhiên\n"
            "• Vẽ biểu đồ trực quan từ dữ liệu\n"
            "Hãy đặt câu hỏi để bắt đầu!"
        )
        if llm is None:
            return static_greeting

    fallback = (
        "Mình sẵn sàng hỗ trợ! Bạn có thể hỏi theo dạng:\n"
        "• 'Top 10 sản phẩm doanh thu cao nhất tháng này'\n"
        "• 'Vẽ biểu đồ doanh thu theo tháng trong năm 2025'"
    )
    if llm is None:
        return fallback

    try:
        prompt = (
            "Bạn là Conversation Agent cho trợ lý phân tích dữ liệu Databricks.\n"
            "Hệ thống có 3 khả năng: truy vấn SQL, vẽ biểu đồ, và hội thoại.\n"
            "Phản hồi ngắn gọn (2-4 câu), lịch sự, bằng tiếng Việt.\n"
            "Nếu câu hỏi không liên quan đến dữ liệu, hãy hướng dẫn cách đặt câu hỏi.\n\n"
            f"Tin nhắn: {question}"
        )
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)
        return content.strip() or fallback
    except Exception as exc:
        logger.warning("Conversation chat LLM failed: %s", exc)
        return fallback
