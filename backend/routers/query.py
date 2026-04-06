"""
💬 query.py — Query & Chat Endpoints
=======================================
📌 TV3 phụ trách route, TV2 cung cấp logic qua agent_service

POST /api/v1/chat/query → Nhận câu hỏi NL, trả SQL + data
GET  /api/v1/schema     → Trả metadata schema
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


# ====== REQUEST / RESPONSE MODELS ======
class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    generated_sql: str | None
    data: list
    row_count: int
    visualization_recommendation: dict
    error: str | None


# ====== ENDPOINTS ======

@router.post("/chat/query", response_model=QueryResponse)
async def chat_query(request: QueryRequest):
    """
    Nhận câu hỏi ngôn ngữ tự nhiên, trả về SQL + kết quả

    📌 TV3 gọi agent_service.process_question() của TV2 ở đây
    """
    try:
        from services.agent_service import process_question
        result = await process_question(request.question)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schema")
def get_schema():
    """
    Trả về thông cấu trúc database

    📌 TV3 gọi schema_service.get_full_schema() của TV2 ở đây
    """
    try:
        from services.schema_service import get_full_schema
        return get_full_schema()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
