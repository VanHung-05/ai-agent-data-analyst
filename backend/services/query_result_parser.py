"""
query_result_parser.py — Parse raw Databricks results
=======================================================
📌 TV2

Databricks trả về dạng string, thường chứa Decimal(...), datetime(...)
mà ast.literal_eval không xử lý được. Module này chuẩn hóa thành list[dict].
"""

from __future__ import annotations

import ast
import re
from datetime import date, datetime
from decimal import Decimal
from typing import Any


_DECIMAL_RE = re.compile(r"Decimal\(['\"]([^'\"]*?)['\"]\)")
_DATETIME_RE = re.compile(r"datetime\.datetime\((\d[\d\s,]*)\)")
_DATE_RE = re.compile(r"datetime\.date\((\d[\d\s,]*)\)")


def _sanitize_raw(raw: str) -> str:
    """Thay Decimal('...') → số; datetime.date/datetime → chuỗi ISO."""
    raw = _DECIMAL_RE.sub(r"\1", raw)

    def _date_replace(m: re.Match) -> str:
        parts = [int(x.strip()) for x in m.group(1).split(",")]
        if len(parts) >= 3:
            return "'{:04d}-{:02d}-{:02d}'".format(*parts[:3])
        return m.group(0)

    def _dt_replace(m: re.Match) -> str:
        parts = [int(x.strip()) for x in m.group(1).split(",")]
        if len(parts) >= 3:
            return "'{:04d}-{:02d}-{:02d}'".format(*parts[:3])
        return m.group(0)

    raw = _DATE_RE.sub(_date_replace, raw)
    raw = _DATETIME_RE.sub(_dt_replace, raw)
    return raw


def _is_pair(item: Any) -> bool:
    return isinstance(item, (tuple, list)) and len(item) == 2


def _is_series_of_pairs(items: Any) -> bool:
    if not isinstance(items, list) or len(items) < 2:
        return False
    return all(_is_pair(x) for x in items)


def _pairs_to_rows(pairs: list[Any]) -> list[dict[str, Any]]:
    return [
        {"col_0": _to_json_safe(p[0]), "col_1": _to_json_safe(p[1])}
        for p in pairs
    ]


def _try_parse_embedded_series(text: str) -> list[dict[str, Any]] | None:
    """Thử parse chuỗi nhúng kiểu '[(datetime.date(...), 120), ...]'."""
    candidate = text.strip()
    if not candidate.startswith("["):
        return None
    sanitized = _sanitize_raw(candidate)
    try:
        parsed = ast.literal_eval(sanitized)
    except (ValueError, SyntaxError):
        return None
    if _is_series_of_pairs(parsed):
        return _pairs_to_rows(parsed)
    if (
        isinstance(parsed, list)
        and len(parsed) == 1
        and _is_series_of_pairs(parsed[0])
    ):
        return _pairs_to_rows(parsed[0])
    return None


def _normalize_parsed_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Bung 1 dòng chứa cả series (list/tuple các cặp) thành nhiều dòng.
    Không đổi KPI một số / một cột đơn.
    """
    if not rows:
        return rows

    if len(rows) == 1:
        row = rows[0]
        keys = list(row.keys())

        if len(keys) == 1:
            val = row[keys[0]]
            if _is_series_of_pairs(val):
                return _pairs_to_rows(val)
            if isinstance(val, str):
                expanded = _try_parse_embedded_series(val)
                if expanded:
                    return expanded

        if len(keys) >= 2 and all(_is_pair(row[k]) for k in keys):
            pairs = [row[k] for k in keys]
            if _is_series_of_pairs(pairs):
                return _pairs_to_rows(pairs)

    return rows


def _rows_from_literal(parsed: Any) -> list[dict[str, Any]] | None:
    if not isinstance(parsed, list) or len(parsed) == 0:
        return [] if isinstance(parsed, list) else None

    if isinstance(parsed[0], dict):
        return [{k: _to_json_safe(v) for k, v in row.items()} for row in parsed]

    if isinstance(parsed[0], (tuple, list)):
        if (
            len(parsed) == 1
            and isinstance(parsed[0], list)
            and _is_series_of_pairs(parsed[0])
        ):
            return _pairs_to_rows(parsed[0])

        rows = [
            {f"col_{i}": _to_json_safe(val) for i, val in enumerate(row)}
            for row in parsed
        ]
        if len(rows) == 1:
            first = rows[0]
            values = list(first.values())
            if len(values) == 1 and _is_series_of_pairs(values[0]):
                return _pairs_to_rows(values[0])
            if len(values) >= 2 and all(_is_pair(v) for v in values):
                pairs = values
                if _is_series_of_pairs(pairs):
                    return _pairs_to_rows(pairs)
        return rows

    return [{"value": _to_json_safe(item)} for item in parsed]


def parse_query_result(raw_result: str) -> list[dict[str, Any]]:
    """Parse kết quả raw từ Databricks thành list[dict] chuẩn JSON."""
    if not raw_result or raw_result.strip() == "":
        return []

    raw = raw_result.strip()
    sanitized = _sanitize_raw(raw)

    try:
        parsed = ast.literal_eval(sanitized)
        rows = _rows_from_literal(parsed)
        if rows is not None:
            return _normalize_parsed_rows(rows)
    except (ValueError, SyntaxError):
        pass

    embedded = _try_parse_embedded_series(raw)
    if embedded:
        return embedded

    lines = raw.split("\n")
    if len(lines) >= 2 and ("\t" in lines[0] or "|" in lines[0]):
        sep = "\t" if "\t" in lines[0] else "|"
        headers = [h.strip() for h in lines[0].split(sep) if h.strip()]
        rows = []
        for line in lines[1:]:
            values = [v.strip() for v in line.split(sep) if v.strip()]
            if len(values) == len(headers):
                rows.append(dict(zip(headers, values)))
        if rows:
            return _normalize_parsed_rows(rows)

    return [{"result": raw}]


def _to_json_safe(val: Any) -> Any:
    """Decimal/date/datetime → JSON-friendly; giữ str/int/float."""
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(val, date):
        return val.isoformat()
    return val
