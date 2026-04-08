"""
chat.py — Chat UI component
==============================
📌 TV4 (Frontend)

Hiển thị lịch sử hội thoại: user bên PHẢI, assistant bên TRÁI.
Dùng HTML/CSS inline vì Streamlit st.chat_message không hỗ trợ align right.
"""

from typing import Any, Dict, List, Optional

import streamlit as st

from components.charts import render_chart
from components.result_table import render_result_table

AGENT_ICONS = {
    "sql": "🗃️",
    "conversation": "💬",
    "visualize": "📊",
}

_USER_BUBBLE_CSS = (
    "background:rgba(79,139,249,0.15); color:#FAFAFA; "
    "padding:0.7rem 1rem; border-radius:12px 12px 0 12px; "
    "display:inline-block; max-width:75%; text-align:left; "
    "font-size:0.95rem; line-height:1.5;"
)


def render_user_bubble(text: str) -> None:
    """Render tin nhắn user dạng HTML sát bên phải."""
    st.markdown(
        f'<div style="text-align:right; margin:0.4rem 0;">'
        f'<span style="{_USER_BUBBLE_CSS}">{text}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_chat_history() -> None:
    """Render toàn bộ tin nhắn: user bên phải (HTML), assistant bên trái (st.chat_message)."""
    for idx, msg in enumerate(st.session_state.get("messages", [])):
        role = msg["role"]

        if role == "user":
            render_user_bubble(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])

                agent = msg.get("agent")
                if agent:
                    icon = AGENT_ICONS.get(agent, "🤖")
                    st.caption(f"{icon} Agent: **{agent}**")

                routing = msg.get("routing_info") or {}
                if routing:
                    scores = routing.get("scores", {})
                    badge_parts = [f"**{k}** {v:.0%}" for k, v in scores.items() if v > 0]
                    if badge_parts:
                        st.caption(f"🔀 Router → {' · '.join(badge_parts)}")

                error = msg.get("error")
                if error:
                    st.error(f"⚠️ {error}")

                data = msg.get("data") or []
                viz = msg.get("viz") or {}
                if data and viz.get("chart_type") not in (None, "table", "conversation"):
                    render_chart(data, viz)

                if data and agent != "conversation":
                    row_count = msg.get("row_count", len(data))
                    with st.expander(f"📋 Dữ liệu ({row_count} dòng)", expanded=False):
                        render_result_table(data, key_suffix=f"history_{idx}")

                sql = msg.get("sql")
                if sql:
                    with st.expander("🔍 SQL đã sinh", expanded=False):
                        st.code(sql, language="sql")


def append_user_message(question: str) -> None:
    st.session_state.messages.append({"role": "user", "content": question})


def append_assistant_message(
    answer: str,
    *,
    agent: Optional[str] = None,
    sql: Optional[str] = None,
    data: Optional[List[Dict[str, Any]]] = None,
    viz: Optional[Dict[str, Any]] = None,
    row_count: int = 0,
    error: Optional[str] = None,
    routing_info: Optional[Dict[str, Any]] = None,
) -> None:
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "agent": agent,
        "sql": sql,
        "data": data or [],
        "viz": viz or {},
        "row_count": row_count,
        "error": error,
        "routing_info": routing_info or {},
    })
