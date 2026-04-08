"""
app.py — Streamlit Frontend: AI Agent Smart Data Analyst
==========================================================
📌 TV4 (Frontend Developer)

Giao diện chat hỏi đáp dữ liệu:
  - Chat input → POST /api/v1/chat/query
  - Hiển thị: NLG answer + biểu đồ Plotly + bảng data + SQL đã sinh
  - Sidebar: trạng thái hệ thống, schema, gợi ý câu hỏi mẫu
"""

import os
from typing import Any, Dict, Optional

import requests
import streamlit as st

from components.chat import (
    append_assistant_message,
    append_user_message,
    render_chat_history,
    render_user_bubble,
)
from components.charts import render_chart
from components.result_table import render_result_table

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")

SAMPLE_QUESTIONS_SQL = [
    "Tổng doanh thu là bao nhiêu?",
    "Top 10 danh mục sản phẩm bán chạy nhất?",
    "Số đơn hàng theo tháng năm 2017?",
    "Phương thức thanh toán phổ biến nhất?",
    "Điểm đánh giá trung bình theo bang?",
    "Top 5 thành phố có nhiều người bán nhất?",
]

SAMPLE_QUESTIONS_VISUALIZE = [
    "Vẽ biểu đồ doanh thu theo tháng năm 2017",
    "Vẽ biểu đồ tỷ lệ phương thức thanh toán",
    "Vẽ chart top 10 danh mục có doanh thu cao nhất",
    "Vẽ biểu đồ trend đơn hàng theo quý",
    "Vẽ đồ thị so sánh doanh thu theo bang",
    "Vẽ biểu đồ phân bố điểm đánh giá",
]


# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

_css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.isfile(_css_path):
    with open(_css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "backend_healthy" not in st.session_state:
    st.session_state.backend_healthy = None


# ──────────────────────────────────────────────
# API HELPERS
# ──────────────────────────────────────────────
def _api_get(path: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
    try:
        r = requests.get(f"{BACKEND_URL}{path}", timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def _api_post_query(question: str) -> dict:
    try:
        r = requests.post(
            f"{BACKEND_URL}/chat/query",
            json={"question": question},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Không thể kết nối Backend. Kiểm tra server đang chạy?", "answer": "", "data": [], "row_count": 0, "visualization_recommendation": {}, "current_agent": "error", "routing_info": {}, "generated_sql": None, "question": question}
    except Exception as e:
        return {"error": str(e), "answer": "", "data": [], "row_count": 0, "visualization_recommendation": {}, "current_agent": "error", "routing_info": {}, "generated_sql": None, "question": question}


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("AI Data Analyst")
    st.caption("Trợ lý phân tích dữ liệu thông minh — Olist E-Commerce")

    st.divider()

    # Health check
    health = _api_get("/health")
    if health:
        status = health.get("status", "unknown")
        services = health.get("services", {})
        if status == "ok":
            st.success("🟢 Hệ thống hoạt động bình thường")
        else:
            st.warning(f"🟡 Hệ thống: {status}")
        cols = st.columns(3)
        for i, (svc, state) in enumerate(services.items()):
            emoji = "✅" if state == "healthy" else "❌"
            cols[i % 3].caption(f"{emoji} {svc}")
        st.session_state.backend_healthy = True
    else:
        st.error("🔴 Backend không phản hồi")
        st.session_state.backend_healthy = False

    st.divider()

    # Schema info
    with st.expander("📂 Database Schema", expanded=False):
        schema = _api_get("/schema")
        if schema:
            tables = schema.get("tables", [])
            if isinstance(tables, list) and tables:
                if isinstance(tables[0], str):
                    for t in tables:
                        st.markdown(f"- `{t}`")
                else:
                    for t in tables:
                        name = t.get("name", t) if isinstance(t, dict) else t
                        st.markdown(f"- `{name}`")
            st.caption(f"Catalog: `{schema.get('catalog', '?')}` · Schema: `{schema.get('schema', '?')}`")
        else:
            st.caption("Không lấy được schema.")

    st.divider()

    # Sample questions — SQL Agent
    st.subheader("🗃️ Truy vấn dữ liệu")
    for q in SAMPLE_QUESTIONS_SQL:
        if st.button(q, key=f"sql_{q}", use_container_width=True):
            st.session_state["_pending_question"] = q

    st.divider()

    # Sample questions — Visualize Agent
    st.subheader("📊 Vẽ biểu đồ")
    for q in SAMPLE_QUESTIONS_VISUALIZE:
        if st.button(q, key=f"viz_{q}", use_container_width=True):
            st.session_state["_pending_question"] = q

    st.divider()
    if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ──────────────────────────────────────────────
# MAIN AREA
# ──────────────────────────────────────────────
st.header("📊 Trợ lý phân tích dữ liệu")

render_chat_history()


def _handle_question(question: str) -> None:
    """Gửi câu hỏi → Backend → hiển thị kết quả."""
    append_user_message(question)
    render_user_bubble(question)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Đang phân tích..."):
            resp = _api_post_query(question)

        agent = resp.get("current_agent", "")
        answer = resp.get("answer", "")
        error = resp.get("error")
        data = resp.get("data", [])
        viz = resp.get("visualization_recommendation", {})
        sql = resp.get("generated_sql")
        routing = resp.get("routing_info", {})

        # Routing badge
        if routing:
            scores = routing.get("scores", {})
            badge_parts = [f"**{k}** {v:.0%}" for k, v in scores.items() if v > 0]
            if badge_parts:
                st.caption(f"🔀 Router → {' · '.join(badge_parts)}")

        # Error
        if error:
            st.error(f"⚠️ {error}")

        # NLG answer
        if answer:
            st.markdown(answer)

        # Chart
        if data and viz.get("chart_type") not in (None, "table", "conversation"):
            render_chart(data, viz)

        # Data table
        if data and agent != "conversation":
            with st.expander(f"📋 Dữ liệu ({resp.get('row_count', len(data))} dòng)", expanded=False):
                render_result_table(data, key_suffix="current")

        # SQL
        if sql:
            with st.expander("🔍 SQL đã sinh", expanded=False):
                st.code(sql, language="sql")

    append_assistant_message(
        answer or error or "Không có phản hồi.",
        agent=agent,
        sql=sql,
        data=data,
        viz=viz,
        row_count=resp.get("row_count", len(data)),
        error=error,
        routing_info=routing,
    )


# Chat input (bottom bar)
user_input = st.chat_input("Hỏi gì về dữ liệu Olist?")

pending = st.session_state.pop("_pending_question", None)
question = user_input or pending

if question:
    _handle_question(question)
