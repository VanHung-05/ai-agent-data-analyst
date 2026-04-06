"""
⚙️ config.py — Quản lý cấu hình & biến môi trường
====================================================
Load tất cả credentials từ file .env
TV2 cần đảm bảo file .env đã được tạo từ .env.example
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()


import requests

@dataclass
class DatabricksConfig:
    """Cấu hình kết nối Databricks — 4 thông tin từ TV1"""
    host: str = os.getenv("DATABRICKS_HOST", "")
    http_path: str = os.getenv("DATABRICKS_HTTP_PATH", "")
    token: str = os.getenv("DATABRICKS_TOKEN", "") # Dùng cho Personal Access Token (Neu co)
    client_id: str = os.getenv("DATABRICKS_CLIENT_ID", "") # Dùng cho Service Principal
    client_secret: str = os.getenv("DATABRICKS_CLIENT_SECRET", "")
    catalog: str = os.getenv("DATABRICKS_CATALOG", "hive_metastore")
    schema: str = os.getenv("DATABRICKS_SCHEMA", "default")

    def _fetch_oauth_token(self) -> str:
        """Tu dong lay Access Token qua OAuth (tuong tu code TV1 chay)"""
        token_url = f"https://{self.host}/oidc/v1/token"
        payload = {"grant_type": "client_credentials", "scope": "all-apis"}
        response = requests.post(token_url, data=payload, auth=(self.client_id, self.client_secret), timeout=10)
        response.raise_for_status()
        return response.json().get("access_token")

    @property
    def active_token(self) -> str:
        """Lấy token (ẩn chứa logic xin tự động qua Service Principal M2M)"""
        if not self.token and self.client_id and self.client_secret:
            print("🔄 Đang xin cấp Token từ Databricks qua M2M Service Principal...")
            self.token = self._fetch_oauth_token()
        return self.token

    @property
    def sqlalchemy_uri(self) -> str:
        """Tạo chuỗi kết nối SQLAlchemy cho LangChain SQLDatabase"""
        return (
            f"databricks://token:{self.active_token}@{self.host}"
            f"?http_path={self.http_path}"
            f"&catalog={self.catalog}"
            f"&schema={self.schema}"
        )


@dataclass
class LLMConfig:
    """Cấu hình LLM — OpenAI, Databricks Model Serving, hoặc Gemini"""
    provider: str = os.getenv("LLM_PROVIDER", "gemini")

    # Gemini (Google)
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Databricks Model Serving
    databricks_llm_endpoint: str = os.getenv("DATABRICKS_LLM_ENDPOINT", "")


@dataclass
class AppConfig:
    """Cấu hình chung của ứng dụng"""
    env: str = os.getenv("APP_ENV", "development")
    port: int = int(os.getenv("APP_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    sql_max_limit: int = int(os.getenv("SQL_MAX_LIMIT", "1000"))
    sql_query_timeout: int = int(os.getenv("SQL_QUERY_TIMEOUT", "30"))


# ====== KHỞI TẠO CÁC CONFIG INSTANCE ======
databricks_config = DatabricksConfig()
llm_config = LLMConfig()
app_config = AppConfig()
