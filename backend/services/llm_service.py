"""
🤖 llm_service.py — Khởi tạo & quản lý LLM Model
=====================================================
📌 FILE NÀY LÀ CỦA TV2 (AI/ML Engineer)

Chức năng:
  - Khởi tạo LLM dựa trên provider được chọn (OpenAI / Gemini / Databricks)
  - Cung cấp instance LLM cho agent_service.py sử dụng
  - Gemini dùng SDK mới `google-genai` thay vì thư viện deprecated

Hướng dẫn:
  1. Cấu hình LLM_PROVIDER trong file .env ("openai", "gemini" hoặc "databricks")
  2. Điền API key tương ứng
  3. Gọi get_llm() từ các module khác để lấy instance LLM
"""

from langchain_openai import ChatOpenAI

# Import config
import sys
import os
import threading
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import llm_config, databricks_config

_llm_instance = None
_llm_lock = threading.Lock()


def get_llm():
    """
    Factory function: Trả về instance LLM dựa trên cấu hình .env

    Returns:
        BaseChatModel: Instance của LLM đã được khởi tạo

    Raises:
        ValueError: Nếu LLM_PROVIDER không hợp lệ

    Ví dụ sử dụng:
        >>> llm = get_llm()
        >>> response = llm.invoke("Xin chào!")
    """
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    with _llm_lock:
        if _llm_instance is not None:
            return _llm_instance

        provider = llm_config.provider.lower()

        if provider == "openai":
            _llm_instance = _init_openai()
        elif provider == "gemini":
            _llm_instance = _init_gemini()
        elif provider == "databricks":
            _llm_instance = _init_databricks()
        else:
            raise ValueError(
                f"❌ LLM_PROVIDER không hợp lệ: '{provider}'. "
                f"Chỉ chấp nhận 'openai', 'gemini' hoặc 'databricks'."
            )
        return _llm_instance


def _init_openai():
    """
    Khởi tạo ChatOpenAI (GPT-4o / GPT-4o-mini / GPT-3.5-turbo)
    """
    if not llm_config.openai_api_key:
        raise ValueError("❌ OPENAI_API_KEY chưa được set trong file .env")

    return ChatOpenAI(
        model=llm_config.openai_model,
        api_key=llm_config.openai_api_key,
        temperature=0,
    )


def _init_gemini():
    """
    Khởi tạo Gemini (Google) Model bằng SDK mới google-genai
    Wrapper thành LangChain BaseChatModel để tương thích với create_sql_query_chain

    💡 TV2 NOTE (Tham khảo Vi-RAG framework):
      - Dùng google.genai SDK mới thay vì google.generativeai (deprecated)
      - Wrap thành class GeminiLangChainWrapper để LangChain gọi được
      - temperature=0 → Gen SQL chính xác, không ảo giác
    """
    if not llm_config.gemini_api_key:
        raise ValueError("❌ GEMINI_API_KEY chưa được set trong file .env")

    from google import genai
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import BaseMessage, AIMessage
    from langchain_core.outputs import ChatResult, ChatGeneration
    from pydantic import Field
    from typing import Any, List, Optional

    class GeminiLangChainWrapper(BaseChatModel):
        """Wrapper biến google-genai SDK thành LangChain ChatModel"""

        client: Any = Field(default=None, exclude=True)
        model_name: str = "gemini-2.0-flash"

        class Config:
            arbitrary_types_allowed = True

        def __init__(self, api_key: str, model: str = "gemini-2.0-flash", **kwargs):
            super().__init__(**kwargs)
            self.client = genai.Client(api_key=api_key)
            self.model_name = model

        @property
        def _llm_type(self) -> str:
            return "google-gemini"

        def _generate(
            self,
            messages: List[BaseMessage],
            stop: Optional[List[str]] = None,
            **kwargs,
        ) -> ChatResult:
            # Gộp tất cả messages thành 1 prompt duy nhất
            prompt = "\n".join([m.content for m in messages])

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "temperature": 0,
                    "max_output_tokens": 2048,
                },
            )

            text = response.text.strip() if response.text else ""
            return ChatResult(
                generations=[ChatGeneration(message=AIMessage(content=text))]
            )

    print(f"   🤖 Khởi tạo Gemini model: {llm_config.gemini_model}")
    return GeminiLangChainWrapper(
        api_key=llm_config.gemini_api_key,
        model=llm_config.gemini_model,
    )


def _init_databricks():
    """
    Khởi tạo LLM từ Databricks Model Serving (DBRX / Llama-3)
    """
    raise NotImplementedError(
        "⚠️ Databricks LLM chưa được implement. "
        "TV2 cần hoàn thiện hàm _init_databricks()."
        "không cần vì đã để LLM_PROVIDER = gemini trong .env"
        "cần nâng cấp thì thêm"
    )


# ====== QUICK TEST ======
if __name__ == "__main__":
    print("🔄 Đang khởi tạo LLM...")
    try:
        llm = get_llm()
        print(f"✅ LLM đã sẵn sàng! Provider: {llm_config.provider}")
        print(f"   Model: {llm_config.gemini_model}")

        # Test nhanh
        response = llm.invoke("Xin chào, bạn là AI gì?")
        print(f"🤖 Response: {response.content[:200]}")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
