"""
Health endpoint for API, Databricks, and LLM dependencies.
"""

from fastapi import APIRouter
from fastapi import Query

router = APIRouter()


def _check_databricks() -> tuple[str, str | None]:
    """Run a lightweight query to verify Databricks connectivity."""
    try:
        from services.agent_service import get_database

        db = get_database()
        db.run("SELECT 1")
        return "healthy", None
    except Exception as exc:
        return "unhealthy", str(exc)


def _check_llm(deep: bool = False) -> tuple[str, str | None]:
    """
    LLM health check.
    - deep=False (default): chỉ khởi tạo object LLM, không invoke model.
    - deep=True: invoke prompt nhỏ để kiểm tra end-to-end.
    """
    try:
        from config import llm_config

        provider = (llm_config.provider or "").lower().strip()
        if provider not in {"gemini", "openai", "databricks"}:
            return "unhealthy", f"LLM_PROVIDER không hợp lệ: {provider}"

        # lightweight check: chỉ validate config, không khởi tạo model
        if provider == "gemini" and not llm_config.gemini_api_key:
            return "unhealthy", "Thiếu GEMINI_API_KEY"
        if provider == "openai" and not llm_config.openai_api_key:
            return "unhealthy", "Thiếu OPENAI_API_KEY"
        if provider == "databricks" and not llm_config.databricks_llm_endpoint:
            return "unhealthy", "Thiếu DATABRICKS_LLM_ENDPOINT"

        if deep:
            from services.llm_service import get_llm
            llm = get_llm()
            llm.invoke("Reply with OK")
        return "healthy", None
    except Exception as exc:
        return "unhealthy", str(exc)


@router.get("/health")
def health_check(deep: bool = Query(default=False)):
    """Return overall service health and dependency details."""
    databricks_status, databricks_error = _check_databricks()
    llm_status, llm_error = _check_llm(deep=deep)

    overall = "ok" if databricks_status == "healthy" and llm_status == "healthy" else "degraded"

    return {
        "status": overall,
        "services": {
            "api": "healthy",
            "databricks": databricks_status,
            "llm": llm_status,
        },
        "errors": {
            "databricks": databricks_error,
            "llm": llm_error,
        },
    }
