"""
Health endpoint for API, Databricks, and LLM dependencies.
"""

from fastapi import APIRouter

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


def _check_llm() -> tuple[str, str | None]:
    """Initialize and ping LLM provider with a very small prompt."""
    try:
        from services.llm_service import get_llm

        llm = get_llm()
        llm.invoke("Reply with OK")
        return "healthy", None
    except Exception as exc:
        return "unhealthy", str(exc)


@router.get("/health")
def health_check():
    """Return overall service health and dependency details."""
    databricks_status, databricks_error = _check_databricks()
    llm_status, llm_error = _check_llm()

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
