"""
🚀 main.py — FastAPI Application Entry Point
===============================================
📌 TV3 (Backend Developer) sẽ phát triển chính file này
📌 TV2 đã chuẩn bị sẵn agent_service & schema_service để TV3 gọi

Khởi chạy: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import app_config
from routers import query, health
from utils.logger import logger

# ====== KHỞI TẠO APP ======
app = FastAPI(
    title="AI Agent — Smart Data Analyst",
    description="Trợ lý phân tích dữ liệu thông minh trên Databricks",
    version="1.0.0",
)

# CORS — cho phép Frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: TV3/TV5 restrict trong production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== ĐĂNG KÝ ROUTERS ======
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(query.router, prefix="/api/v1", tags=["Query"])


@app.on_event("startup")
def warmup_dependencies() -> None:
    """
    Warm-up ngay khi backend khởi động:
    - Kết nối Databricks warehouse sớm để frontend vào là sẵn sàng query.
    """
    try:
        from services.agent_service import get_database

        db = get_database()
        db.run("SELECT 1")
        logger.info("Startup warm-up Databricks: OK")
    except Exception as exc:
        # Không crash app để vẫn truy cập được /health và đọc lỗi chi tiết.
        logger.warning("Startup warm-up Databricks failed: %s", exc)


@app.get("/")
def root():
    return {"message": "🤖 AI Agent — Smart Data Analyst API is running!"}
