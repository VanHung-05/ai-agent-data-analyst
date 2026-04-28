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
import json
import time
import uuid
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


def _new_conversation_id() -> str:
    return f"chat_{uuid.uuid4().hex[:8]}"


def _current_conversation() -> dict:
    cid = st.session_state.active_conversation_id
    return st.session_state.conversations[cid]


def _save_active_messages() -> None:
    conv = _current_conversation()
    conv["messages"] = list(st.session_state.messages)
    conv["updated_at"] = time.time()


def _load_conversation(conversation_id: str) -> None:
    st.session_state.active_conversation_id = conversation_id
    st.session_state.messages = list(
        st.session_state.conversations[conversation_id].get("messages", [])
    )


def _make_title_from_question(question: str) -> str:
    title = question.strip()
    if not title:
        return "Chat mới"
    return title[:42] + ("..." if len(title) > 42 else "")


def _short_text(text: str, max_len: int = 72) -> str:
    clean = " ".join(text.strip().split())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 3] + "..."


def _start_new_conversation() -> None:
    # Nếu chat hiện tại còn trống thì không tạo thêm chat trống mới.
    if not st.session_state.messages:
        return
    _save_active_messages()
    new_id = _new_conversation_id()
    st.session_state.conversations[new_id] = {
        "title": "Chat mới",
        "created_at": time.time(),
        "updated_at": time.time(),
        "messages": [],
    }
    _load_conversation(new_id)


def _init_conversation_state() -> None:
    if "conversations" not in st.session_state:
        st.session_state.conversations = {}

    if "active_conversation_id" not in st.session_state:
        first_id = _new_conversation_id()
        st.session_state.conversations[first_id] = {
            "title": "Chat mới",
            "created_at": time.time(),
            "updated_at": time.time(),
            "messages": [],
        }
        st.session_state.active_conversation_id = first_id
        st.session_state.messages = []
        return

    # Nếu có active conversation thì nạp messages tương ứng
    active_id = st.session_state.active_conversation_id
    if active_id in st.session_state.conversations:
        st.session_state.messages = list(
            st.session_state.conversations[active_id].get("messages", [])
        )
    else:
        # fallback khi id cũ không còn
        first_id = _new_conversation_id()
        st.session_state.conversations[first_id] = {
            "title": "Chat mới",
            "created_at": time.time(),
            "updated_at": time.time(),
            "messages": [],
        }
        st.session_state.active_conversation_id = first_id
        st.session_state.messages = []


_init_conversation_state()


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


def _api_post_query_stream(
    question: str,
    on_progress: Optional[Any] = None,
) -> dict:
    """Gọi SSE stream endpoint để nhận progress realtime + result cuối."""
    url = f"{BACKEND_URL}/chat/query/stream"
    try:
        with requests.post(url, json={"question": question}, stream=True, timeout=240) as r:
            r.raise_for_status()
            final_result: Optional[dict] = None
            for raw_line in r.iter_lines(decode_unicode=True):
                if not raw_line or not raw_line.startswith("data: "):
                    continue
                payload = raw_line[6:]
                try:
                    evt = json.loads(payload)
                except json.JSONDecodeError:
                    continue

                evt_type = evt.get("type")
                if evt_type == "progress":
                    if on_progress is not None:
                        on_progress(evt.get("step", ""), evt.get("message", ""))
                elif evt_type == "result":
                    final_result = evt.get("data", {})
                elif evt_type == "error":
                    return {
                        "error": evt.get("error", "Streaming error"),
                        "answer": "",
                        "data": [],
                        "row_count": 0,
                        "visualization_recommendation": {},
                        "current_agent": "error",
                        "routing_info": {},
                        "generated_sql": None,
                        "question": question,
                    }
                elif evt_type == "done":
                    break

            if final_result is not None:
                return final_result

    except Exception as e:
        return {
            "error": f"Streaming failed: {str(e)}",
            "answer": "",
            "data": [],
            "row_count": 0,
            "visualization_recommendation": {},
            "current_agent": "error",
            "routing_info": {},
            "generated_sql": None,
            "question": question,
        }

    return {
        "error": "Không nhận được kết quả stream.",
        "answer": "",
        "data": [],
        "row_count": 0,
        "visualization_recommendation": {},
        "current_agent": "error",
        "routing_info": {},
        "generated_sql": None,
        "question": question,
    }


@st.cache_data(ttl=20, show_spinner=False)
def _cached_health() -> Optional[Dict[str, Any]]:
    """Cache health để tránh gọi lại mỗi lần rerun UI."""
    return _api_get("/health")


@st.cache_data(ttl=300, show_spinner=False)
def _cached_schema() -> Optional[Dict[str, Any]]:
    """Schema ít đổi, cache 5 phút cho UI mượt hơn."""
    return _api_get("/schema")


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("AI Data Analyst")
    st.caption("Trợ lý phân tích dữ liệu thông minh — Olist E-Commerce")

    st.divider()

    # # Health check
    # health = _cached_health()
    # if health:
    #     status = health.get("status", "unknown")
    #     services = health.get("services", {})
    #     if status == "ok":
    #         st.success("🟢 Hệ thống hoạt động bình thường")
    #     else:
    #         st.warning(f"🟡 Hệ thống: {status}")
    #     cols = st.columns(3)
    #     for i, (svc, state) in enumerate(services.items()):
    #         emoji = "✅" if state == "healthy" else "❌"
    #         cols[i % 3].caption(f"{emoji} {svc}")
    #     st.session_state.backend_healthy = True
    # else:
    #     st.error("🔴 Backend không phản hồi")
    #     st.session_state.backend_healthy = False

    # st.divider()

    # Schema info
    with st.expander("Data Info", expanded=False):
        if st.button("Reload", key="load_schema_btn", width="stretch"):
            _cached_schema.clear()
        schema = _cached_schema()
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
            st.caption("Không tải được thông tin dữ liệu.")

    st.divider()

    # Conversations
    st.subheader("💬 Lịch sử chat")
    if st.button("➕ Chat mới", width="stretch"):
        _start_new_conversation()
        st.rerun()

    with st.expander("🕘 Mở cuộc trò chuyện", expanded=True):
        conversations = st.session_state.conversations
        sorted_items = sorted(
            conversations.items(),
            key=lambda x: x[1].get("updated_at", 0),
            reverse=True,
        )
        for cid, conv in sorted_items:
            messages = conv.get("messages", [])
            title = conv.get("title", "Chat mới")
            is_active = cid == st.session_state.active_conversation_id

            # Chỉ ẩn chat trống chưa dùng (nhưng vẫn giữ chat active).
            if (not messages) and (not is_active):
                continue

            if st.button(
                title,
                key=f"conv_{cid}",
                width="stretch",
                type="primary" if is_active else "secondary",
            ):
                _load_conversation(cid)
                st.rerun()

    st.divider()
    if st.button("🗑️ Xóa chat hiện tại", width="stretch"):
        st.session_state.messages = []
        _save_active_messages()
        st.rerun()


# ──────────────────────────────────────────────
# MAIN AREA
# ──────────────────────────────────────────────
st.header("📊 Trợ lý phân tích dữ liệu")

render_chat_history()


def _handle_question(question: str) -> None:
    """Gửi câu hỏi → Backend → hiển thị kết quả."""
    conv = _current_conversation()
    if conv.get("title", "Chat mới") == "Chat mới":
        conv["title"] = _make_title_from_question(question)

    append_user_message(question)
    render_user_bubble(question)

    with st.chat_message("assistant", avatar="🤖"):
        short_q = _short_text(question, 90)
        with st.status("Đang phân tích...", expanded=True) as status:
            step_placeholder = st.empty()
            step_placeholder.caption("Đang chờ backend...")

            def _on_progress(step: str, message: str) -> None:
                step_placeholder.caption(f"• {message}")

            resp = _api_post_query_stream(question, on_progress=_on_progress)
            status.update(label="Phân tích xong", state="complete")

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
    _save_active_messages()


# Chat input (bottom bar)
user_input = st.chat_input("Hỏi gì về dữ liệu Olist?")

question = user_input

if question:
    _handle_question(question)
