"""
query.py — Query, Chat & Routing Endpoints
=============================================
📌 TV3 phụ trách route, TV2 cung cấp logic qua agent_service

POST /api/v1/chat/query  → Nhận câu hỏi NL, trả SQL + data + chart spec
POST /api/v1/chat/route  → Chỉ chạy Router Agent, trả routing info (cho debug/frontend)
GET  /api/v1/schema      → Trả metadata schema
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


# ====== REQUEST / RESPONSE MODELS ======

class QueryRequest(BaseModel):
    question: str


class RoutingInfo(BaseModel):
    intent: str
    scores: dict[str, float]
    selected_agents: list[str]
    routing_method: str


class VisualizationRecommendation(BaseModel):
    chart_type: str
    x: str | None = None
    y: str | None = None
    title: str | None = None
    label: str | None = None
    value: str | None = None
    reason: str | None = None
    routed_agent: str | None = None

    class Config:
        extra = "allow"


class QueryResponse(BaseModel):
    question: str
    current_agent: str
    routing_info: dict
    answer: str
    generated_sql: str | None
    data: list
    row_count: int
    visualization_recommendation: dict
    error: str | None


class RouteResponse(BaseModel):
    question: str
    routing_info: RoutingInfo


# ====== ENDPOINTS ======

@router.post("/chat/query", response_model=QueryResponse)
async def chat_query(request: QueryRequest):
    """
    Endpoint chính: nhận câu hỏi NL → Multi-Agent pipeline → trả kết quả.

    Response bao gồm:
    - current_agent: agent nào đã xử lý (conversation/sql/visualize)
    - routing_info: chi tiết routing (scores, method)
    - answer: câu trả lời tổng hợp dạng text
    - generated_sql: SQL đã sinh (None nếu conversation)
    - data: dữ liệu dạng list[dict]
    - visualization_recommendation: chart spec cho frontend
    """
    try:
        from services.agent_service import process_question
        result = await process_question(request.question)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/route", response_model=RouteResponse)
async def chat_route(request: QueryRequest):
    """
    Chỉ chạy Router Agent, không query DB.
    Dùng cho frontend hiển thị "đang phân tích..." hoặc debug routing.
    """
    try:
        from services.llm_service import get_llm
        from services.router_agent import route_detail
        llm = get_llm()
        routing = route_detail(request.question, llm)
        return RouteResponse(question=request.question, routing_info=RoutingInfo(**routing))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schema")
def get_schema():
    """Trả về cấu trúc database."""
    try:
        from services.schema_service import get_full_schema
        return get_full_schema()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
