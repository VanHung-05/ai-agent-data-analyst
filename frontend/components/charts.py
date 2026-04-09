"""
charts.py — Chart rendering component
========================================
📌 TV4 (Frontend)

Nhận `visualization_recommendation` + `data` từ API → vẽ Plotly chart trong Streamlit.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st


_CHART_BUILDERS = {}


def _register(name: str):
    def decorator(fn):
        _CHART_BUILDERS[name] = fn
        return fn
    return decorator


def render_chart(data: list[dict], viz: dict) -> None:
    """Entry point: dispatch chart theo `viz["chart_type"]`."""
    if not data:
        return

    chart_type = viz.get("chart_type", "table")
    if chart_type in ("table", "conversation"):
        return

    df = pd.DataFrame(data)
    if df.empty:
        return

    builder = _CHART_BUILDERS.get(chart_type)
    if builder is None:
        st.info(f"Loại biểu đồ `{chart_type}` chưa hỗ trợ. Hiển thị dạng bảng.")
        return

    title = viz.get("title") or ""
    reason = viz.get("reason") or ""
    if reason:
        st.caption(f"💡 {reason}")

    fig = builder(df, viz, title)
    if fig is not None:
        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=40, r=20, t=50, b=40),
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)


def _resolve_axes(df: pd.DataFrame, viz: dict, chart_type: str = "") -> tuple[str, str]:
    cols = [str(c) for c in df.columns]
    numeric_cols = _get_numeric_columns(df)
    non_numeric_cols = [c for c in cols if c not in numeric_cols]

    x_hint = str(viz.get("x")) if viz.get("x") else None
    y_hint = str(viz.get("y")) if viz.get("y") else None

    # Ưu tiên trục x theo hint nếu tồn tại
    if x_hint in cols:
        x = x_hint
    elif chart_type in {"line", "area"}:
        time_cols = [c for c in cols if _is_time_like_col(c)]
        if time_cols:
            x = time_cols[0]
        elif non_numeric_cols:
            x = non_numeric_cols[0]
        else:
            x = cols[0]
    elif non_numeric_cols:
        x = non_numeric_cols[0]
    else:
        x = cols[0]

    # Ưu tiên trục y là metric numeric (tránh chọn nhầm year/qtr/state)
    if y_hint in numeric_cols and y_hint != x and not _is_time_like_col(y_hint):
        y = y_hint
    else:
        y_candidates = [c for c in numeric_cols if c != x and not _is_time_like_col(c)]
        if not y_candidates:
            y_candidates = [c for c in numeric_cols if c != x]
        if y_candidates:
            y = _pick_metric_col(y_candidates)
        else:
            y = cols[1] if len(cols) > 1 else cols[0]
    return x, y


def _get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """
    Xác định cột numeric (kể cả numeric nhưng đang ở dạng string).
    Cột được coi là numeric nếu >= 80% giá trị parse được thành số.
    """
    numeric_cols: list[str] = []
    for col in df.columns:
        series = pd.to_numeric(df[col], errors="coerce")
        non_null = series.notna().sum()
        total = len(series)
        if total > 0 and (non_null / total) >= 0.8:
            numeric_cols.append(str(col))
            # Ép kiểu về numeric để Plotly vẽ ổn định hơn
            df[col] = series
    return numeric_cols


@_register("bar")
def _bar(df: pd.DataFrame, viz: dict, title: str):
    x, y = _resolve_axes(df, viz, "bar")
    text_auto = ".2s" if pd.api.types.is_numeric_dtype(df[y]) else None
    return px.bar(df, x=x, y=y, title=title, text_auto=text_auto)


@_register("line")
def _line(df: pd.DataFrame, viz: dict, title: str):
    x, y = _resolve_axes(df, viz, "line")
    work_df = df.copy()

    # Nếu có year + quarter, ghép thành period để line chart mượt hơn.
    year_col = _find_col_by_keywords(work_df.columns, ["year", "yr"])
    quarter_col = _find_col_by_keywords(work_df.columns, ["quarter", "qtr"])
    if year_col and quarter_col and y not in {year_col, quarter_col}:
        year_series = pd.to_numeric(work_df[year_col], errors="coerce")
        quarter_series = pd.to_numeric(work_df[quarter_col], errors="coerce")
        if year_series.notna().any() and quarter_series.notna().any():
            work_df["__period"] = (
                year_series.fillna(0).astype(int).astype(str)
                + "-Q"
                + quarter_series.fillna(0).astype(int).astype(str)
            )
            x = "__period"
    return px.line(work_df, x=x, y=y, title=title, markers=True)


@_register("pie")
def _pie(df: pd.DataFrame, viz: dict, title: str):
    x, y = _resolve_axes(df, viz, "pie")
    return px.pie(df, names=x, values=y, title=title)


@_register("scatter")
def _scatter(df: pd.DataFrame, viz: dict, title: str):
    x, y = _resolve_axes(df, viz, "scatter")
    return px.scatter(df, x=x, y=y, title=title)


@_register("area")
def _area(df: pd.DataFrame, viz: dict, title: str):
    x, y = _resolve_axes(df, viz, "area")
    return px.area(df, x=x, y=y, title=title)


@_register("histogram")
def _histogram(df: pd.DataFrame, viz: dict, title: str):
    x, _ = _resolve_axes(df, viz, "histogram")
    return px.histogram(df, x=x, title=title)


@_register("metric")
def _metric(df: pd.DataFrame, viz: dict, title: str):
    label = viz.get("label") or title or "Kết quả"
    value = viz.get("value")
    if value is None and not df.empty:
        value = df.iloc[0, -1]
    st.metric(label=label, value=value)
    return None


def _is_time_like_col(col: str) -> bool:
    name = str(col).lower()
    return any(k in name for k in ["date", "time", "month", "year", "yr", "quarter", "qtr", "day"])


def _pick_metric_col(cols: list[str]) -> str:
    score_keywords = ["total", "count", "revenue", "amount", "value", "sales", "orders", "sum", "avg"]
    scored = sorted(
        cols,
        key=lambda c: sum(1 for kw in score_keywords if kw in c.lower()),
        reverse=True,
    )
    return scored[0]


def _find_col_by_keywords(columns: Any, keywords: list[str]) -> str | None:
    for c in columns:
        name = str(c).lower()
        if any(kw == name or kw in name for kw in keywords):
            return str(c)
    return None
