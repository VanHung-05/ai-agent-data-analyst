"""
❤️ health.py — Health Check Endpoint
======================================
📌 TV3 phụ trách

GET /api/v1/health → Kiểm tra trạng thái kết nối AI, Databricks
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """Kiểm tra kết nối hệ thống"""
    status = {
        "status": "ok",
        "services": {
            "api": "healthy",
            "databricks": "unknown",  # TODO: TV3 kiểm tra kết nối thực
            "llm": "unknown",         # TODO: TV3 kiểm tra kết nối thực
        },
    }

    # TODO: TV3 implement kiểm tra thực tế
    # try:
    #     from services.agent_service import get_database
    #     db = get_database()
    #     status["services"]["databricks"] = "healthy"
    # except Exception:
    #     status["services"]["databricks"] = "unhealthy"

    return status
