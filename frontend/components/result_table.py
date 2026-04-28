"""
result_table.py — Bảng kết quả component
==========================================
📌 TV4 (Frontend)

Hiển thị `data` (list[dict]) dưới dạng DataFrame tương tác trong Streamlit.
"""

from __future__ import annotations

import hashlib

import pandas as pd
import streamlit as st


def render_result_table(
    data: list[dict],
    *,
    max_display: int = 500,
    key_suffix: str = "",
) -> None:
    """Hiển thị bảng kết quả dạng `st.dataframe` với download CSV."""
    if not data:
        return

    df = pd.DataFrame(data)
    if df.empty:
        return

    total = len(df)

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except (ValueError, TypeError):
            pass

    st.dataframe(
        df.head(max_display),
        width="stretch",
        hide_index=True,
    )

    if total > max_display:
        st.caption(f"⚠️ Hiển thị {max_display}/{total} dòng. Tải CSV để xem đầy đủ.")

    csv = df.to_csv(index=False).encode("utf-8")
    # Mỗi bảng cần key duy nhất để tránh StreamlitDuplicateElementId
    content_hash = hashlib.md5(csv).hexdigest()[:10]
    button_key = f"download_csv_{content_hash}_{key_suffix}"

    st.download_button(
        "⬇️ Tải CSV",
        data=csv,
        file_name="query_result.csv",
        mime="text/csv",
        key=button_key,
    )
