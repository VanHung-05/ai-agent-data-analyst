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
from decimal import Decimal
from typing import Any


_DECIMAL_RE = re.compile(r"Decimal\(['\"]([^'\"]*?)['\"]\)")
_DATETIME_RE = re.compile(
    r"datetime\.datetime\((\d[\d\s,]*)\)"
)


def _sanitize_raw(raw: str) -> str:
    """Thay Decimal('...') → số, datetime.datetime(...) → string ISO."""
    raw = _DECIMAL_RE.sub(r"\1", raw)

    def _dt_replace(m: re.Match) -> str:
        parts = [int(x.strip()) for x in m.group(1).split(",")]
        if len(parts) >= 3:
            return "'{:04d}-{:02d}-{:02d}'".format(*parts[:3])
        return m.group(0)

    raw = _DATETIME_RE.sub(_dt_replace, raw)
    return raw


def parse_query_result(raw_result: str) -> list[dict[str, Any]]:
    """Parse kết quả raw từ Databricks thành list[dict] chuẩn JSON."""
    if not raw_result or raw_result.strip() == "":
        return []

    raw = raw_result.strip()
    sanitized = _sanitize_raw(raw)

    try:
        parsed = ast.literal_eval(sanitized)
        if isinstance(parsed, list):
            if len(parsed) == 0:
                return []
            if isinstance(parsed[0], (tuple, list)):
                return [{f"col_{i}": _to_json_safe(val) for i, val in enumerate(row)} for row in parsed]
            if isinstance(parsed[0], dict):
                return [{k: _to_json_safe(v) for k, v in row.items()} for row in parsed]
            return [{"value": _to_json_safe(item)} for item in parsed]
    except (ValueError, SyntaxError):
        pass

    lines = raw.split("\n")
    if len(lines) >= 2 and ("\t" in lines[0] or "|" in lines[0]):
        sep = "\t" if "\t" in lines[0] else "|"
        headers = [h.strip() for h in lines[0].split(sep) if h.strip()]
        rows: list[dict[str, Any]] = []
        for line in lines[1:]:
            values = [v.strip() for v in line.split(sep) if v.strip()]
            if len(values) == len(headers):
                rows.append(dict(zip(headers, values)))
        if rows:
            return rows

    return [{"result": raw}]


def _to_json_safe(val: Any) -> Any:
    """Decimal/float/int → float cho JSON; giữ nguyên str."""
    if isinstance(val, Decimal):
        return float(val)
    return val
