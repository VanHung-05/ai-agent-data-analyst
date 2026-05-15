"""
Visualize Agent — Chuyên gia hình ảnh hóa
============================================
Vai trò:
  - Nhận kết quả từ SQL Agent (data + columns)
  - Phân tích dữ liệu và quyết định loại biểu đồ phù hợp
  - Trả chart spec (chart_type, x, y, title) để Frontend vẽ hình
  - Heuristic rules xử lý nhanh các case rõ ràng
  - LLM xử lý các case mơ hồ mà heuristic không bắt được
"""

import json
import re
from typing import Any

from utils.logger import logger

_SUPPORTED_CHART_TYPES = {
    "metric", "line", "bar", "pie", "table", "scatter", "histogram", "area"
}

_CHART_KEYWORDS = {
    "line": ["line chart", "line", "đường", "xu hướng", "trend", "over time"],
    "bar": ["bar chart", "bar", "cột", "so sánh", "ranking", "xếp hạng", "top"],
    # Không map "tỷ lệ/phần trăm" → ép pie: thường là 1 dòng KPI (late/total/%) → pie sai 100%
    "pie": ["pie chart", "pie", "biểu đồ tròn", "chart tròn"],
    "scatter": ["scatter", "phân tán", "correlation", "tương quan"],
    "histogram": ["histogram", "phân bố", "distribution", "tần suất"],
    "area": ["area chart", "area", "miền"],
}


def recommend_chart(
    question: str,
    sql: str,
    data: list[dict],
    llm: Any | None = None,
) -> dict:
    """
    Phân tích dữ liệu và đề xuất loại biểu đồ phù hợp.

    Args:
        question: Câu hỏi gốc của người dùng
        sql: Câu SQL đã thực thi
        data: Dữ liệu trả về từ Databricks (list of dicts)
        llm: Instance LLM. Nếu None, chỉ dùng heuristic.

    Returns:
        dict: {
            "chart_type": "metric"|"line"|"bar"|"pie"|"table",
            "x": str | None,
            "y": str | None,
            "title": str | None,
            "reason": str
        }
    """
    if not data:
        return {"chart_type": "table", "reason": "No data"}

    columns = list(data[0].keys())
    row_count = len(data)
    q = question.lower()
    sql_lower = sql.lower()
    x_col, y_col = _choose_axes(data, columns)

    # === Không vẽ chart khi x-axis là UUID/hash và không có cột thay thế ===
    if x_col and _is_id_column(x_col, data):
        # Thử tìm cột khác làm x-axis thay thế
        alt_x = _find_non_id_x(data, columns, x_col)
        if alt_x:
            x_col = alt_x
        else:
            return {
                "chart_type": "table",
                "x": None,
                "y": None,
                "title": None,
                "reason": f"x-axis '{x_col}' is an ID/hash column — chart would be unreadable",
            }

    # === Ưu tiên: không vẽ khi dữ liệu không đủ ý nghĩa cho chart ===
    if len(columns) <= 1:
        return {
            "chart_type": "table",
            "x": None,
            "y": None,
            "title": None,
            "reason": "Single-column result → table is clearer",
        }

    if row_count <= 1:
        return {
            "chart_type": "table",
            "x": None,
            "y": None,
            "title": None,
            "reason": "Single-row aggregate (KPI) → text/NLG + table, not chart",
        }

    # Người dùng chỉ định loại biểu đồ — chỉ áp dụng nếu dữ liệu khớp
    forced_chart = _detect_forced_chart_type(q)
    if forced_chart is not None:
        spec = _build_chart_spec(forced_chart, question, x_col, y_col)
        ok, _why = _validate_chart_for_data(
            spec["chart_type"], data, columns, spec.get("x"), spec.get("y")
        )
        if ok:
            spec["reason"] = "User explicitly requested chart type"
            return spec

    # === HEURISTIC: các case rõ ràng ===

    time_kw_question = ["tháng", "ngày", "trend", "xu hướng", "over time", "theo thời gian"]
    time_kw_sql = ["date", "timestamp", "year", "month", "day"]
    if any(kw in q for kw in time_kw_question) or any(kw in sql_lower for kw in time_kw_sql):
        if len(columns) >= 2:
            spec = _build_chart_spec("line", question, x_col, y_col)
            ok, _why = _validate_chart_for_data(
                "line", data, columns, spec.get("x"), spec.get("y")
            )
            if ok:
                spec["reason"] = "Time series detected"
                return spec

    # Pie: tỉ lệ / phần trăm / proportion — ưu tiên trước bar/ranking
    pie_kws = [
        "tỉ lệ", "tỷ lệ", "phần trăm", "ratio", "percentage",
        "proportion", "share", "cơ cấu", "phân bổ",
    ]
    if any(kw in q for kw in pie_kws):
        if len(columns) >= 2 and row_count >= 2:
            spec = _build_chart_spec("pie", question, x_col, y_col)
            ok, _why = _validate_chart_for_data(
                "pie", data, columns, spec.get("x"), spec.get("y")
            )
            if ok:
                spec["reason"] = "Proportions/ratio with multiple categories"
                return spec

    # === Câu hỏi tìm cực trị ("nhất") → bảng đủ, không cần chart ===
    # Ví dụ: "cao nhất", "nhiều nhất", "lớn nhất", "thấp nhất"...
    # Ngoại lệ: user đã chỉ định chart type ở trên (forced_chart) hoặc có "top N so sánh"
    if _is_superlative_question(q):
        return {
            "chart_type": "table",
            "x": None,
            "y": None,
            "title": None,
            "reason": "Superlative question (nhất/most/least) — table + NLG answer is sufficient",
        }

    if any(kw in q for kw in ["top", "so sánh", "ranking", "xếp hạng", "comparison", "liệt kê"]):
        if len(columns) >= 2:
            spec = _build_chart_spec("bar", question, x_col, y_col)
            ok, _why = _validate_chart_for_data(
                "bar", data, columns, spec.get("x"), spec.get("y")
            )
            if ok:
                spec["reason"] = "Comparison/ranking detected"
                return spec

    # group by + time → line đã bắt ở trên, không fallback bar cho mọi GROUP BY

    # === LLM: xử lý case mơ hồ mà heuristic không match ===
    if llm is not None:
        llm_result = _llm_recommend(question, sql, data, columns, llm)
        if llm_result is not None:
            ct = str(llm_result.get("chart_type", "table")).lower()
            ok, why = _validate_chart_for_data(
                ct, data, columns, llm_result.get("x"), llm_result.get("y")
            )
            if ok:
                return llm_result
            logger.info("Visualize LLM downgraded to table: %s", why)

    return {"chart_type": "table", "x": None, "y": None, "title": None, "reason": "Default table view"}


def _build_chart_spec(
    chart_type: str,
    question: str,
    x_col: str | None,
    y_col: str | None,
) -> dict[str, Any]:
    if chart_type == "histogram":
        return {
            "chart_type": chart_type,
            "x": y_col or x_col,
            "y": None,
            "title": _suggest_title(question, chart_type),
            "reason": "",
        }
    return {
        "chart_type": chart_type,
        "x": x_col,
        "y": y_col,
        "title": _suggest_title(question, chart_type),
        "reason": "",
    }


def _validate_chart_for_data(
    chart_type: str,
    data: list[dict],
    columns: list[str],
    x_col: str | None,
    y_col: str | None,
) -> tuple[bool, str]:
    """
    Quy tắc thực tế:
    - Pie: cần ≥2 hạng mục (dòng); 1 dòng KPI + nhiều cột số → không pie.
    - Line/bar/area/scatter: cần ≥2 điểm.
    - Histogram: ≥2 mẫu.
    """
    n = len(data)
    ct = chart_type.lower().strip()
    if ct == "table" or ct == "conversation" or ct == "metric":
        return True, ""

    if ct == "pie":
        if n < 2:
            return False, "pie requires ≥2 rows (categories)"
        if not x_col or not y_col or x_col == y_col:
            return False, "pie needs distinct label (x) and value (y)"
        if not _column_is_numericish(data, y_col):
            return False, "pie value column must be numeric"
        return True, ""

    if ct in {"line", "bar", "area", "scatter"}:
        if n < 2:
            return False, f"{ct} requires ≥2 rows"
        if not x_col or not y_col or x_col == y_col:
            return False, f"{ct} needs distinct x and y"
        if not _column_is_numericish(data, y_col):
            return False, "y axis should be numeric"
        return True, ""

    if ct == "histogram":
        if n < 2:
            return False, "histogram requires ≥2 samples"
        hx = x_col or y_col
        if not hx:
            return False, "histogram needs a column"
        return True, ""

    return True, ""


def _column_is_numericish(data: list[dict], col: str) -> bool:
    vals = [row.get(col) for row in data if row.get(col) is not None]
    if not vals:
        return False
    ok = sum(1 for v in vals if _is_numeric_like(v))
    return ok / len(vals) >= 0.7


def _llm_recommend(
    question: str,
    sql: str,
    data: list[dict],
    columns: list[str],
    llm: Any,
) -> dict | None:
    """Dùng LLM để chọn chart type khi heuristic không xác định được."""
    try:
        sample_rows = data[:5]
        prompt = (
            "Bạn là Visualize Agent. Dựa vào câu hỏi, SQL, và dữ liệu mẫu, "
            "hãy chọn loại biểu đồ PHÙ HỢP NHẤT.\n"
            "Chỉ dùng 1 trong: metric, line, bar, pie, scatter, histogram, area, table.\n"
            "Quy tắc bắt buộc:\n"
            "- Nếu chỉ có 1 dòng kết quả (aggregate KPI: tổng, tỷ lệ %, late/total...) → chart_type=table.\n"
            "- Pie chỉ khi có ≥2 dòng (mỗi dòng là một nhóm: ví dụ payment_type + count).\n"
            "- Line/bar cần ≥2 điểm dữ liệu (≥2 dòng).\n"
            "Trả JSON thuần đúng format, KHÔNG giải thích:\n"
            '{"chart_type":"...","x":"column_name","y":"column_name",'
            '"title":"Tiêu đề biểu đồ","reason":"Lý do ngắn"}\n\n'
            f"Question: {question}\n"
            f"SQL: {sql}\n"
            f"Columns: {columns}\n"
            f"Sample ({len(data)} rows total): {sample_rows}"
        )
        response = llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)

        json_match = re.search(r"\{[^{}]+\}", content)
        raw_json = json_match.group(0) if json_match else content.strip()
        parsed = json.loads(raw_json)

        chart_type = str(parsed.get("chart_type", "")).strip().lower()
        if chart_type not in _SUPPORTED_CHART_TYPES:
            return None

        logger.info("Visualize LLM → chart_type=%s", chart_type)
        return {
            "chart_type": chart_type,
            "x": parsed.get("x"),
            "y": parsed.get("y"),
            "title": parsed.get("title"),
            "reason": parsed.get("reason", "LLM suggestion"),
        }
    except Exception as exc:
        logger.warning("Visualize LLM failed, using table default: %s", exc)
        return None


def _detect_forced_chart_type(question_lower: str) -> str | None:
    for chart_type, kws in _CHART_KEYWORDS.items():
        if any(kw in question_lower for kw in kws):
            return chart_type
    return None


def _is_numeric_like(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        cleaned = value.replace(",", "").replace("_", "").strip()
        if cleaned == "":
            return False
        try:
            float(cleaned)
            return True
        except ValueError:
            return False
    return False


def _is_id_column(col_name: str, data: list[dict]) -> bool:
    """
    Phát hiện cột ID/UUID không phù hợp để làm trục x biểu đồ.
    Trả về True nếu:
    - Tên cột chứa '_id' và không phải cột phân tích có ý nghĩa
    - Hơn 60% giá trị trông như UUID/MD5 hex hash (32 ký tự hex)
    """
    import re as _re
    _ID_COL_NAMES = {
        "seller_id", "customer_id", "customer_unique_id", "order_id",
        "product_id", "review_id", "geolocation_zip_code_prefix",
    }
    if col_name.lower() in _ID_COL_NAMES:
        return True

    # Kiểm tra giá trị có phải hex hash 32 ký tự (MD5-like UUID)
    _UUID_RE = _re.compile(r'^[a-f0-9]{32}$')
    vals = [str(row.get(col_name, "")).strip() for row in data if row.get(col_name) is not None]
    if not vals:
        return False
    uuid_count = sum(1 for v in vals if _UUID_RE.match(v))
    return uuid_count / len(vals) >= 0.6




def _is_superlative_question(question_lower: str) -> bool:
    """
    Phát hiện câu hỏi tìm cực trị ("nhất") không cần vẽ biểu đồ.
    Ví dụ: "cao nhất", "nhiều nhất", "lớn nhất", "thấp nhất", "highest", "most"...
    Ngoại lệ: nếu câu có từ khoá so sánh nhiều đối tượng thì vẫn chart.
    """
    vi_superlatives = [
        "nhất", "cao nhất", "thấp nhất", "nhiều nhất", "ít nhất",
        "lớn nhất", "nhỏ nhất", "nhanh nhất", "chậm nhất",
        "tốt nhất", "kém nhất", "đắt nhất", "rẻ nhất",
        "dài nhất", "ngắn nhất", "nặng nhất", "nhẹ nhất",
    ]
    en_superlatives = [
        "highest", "lowest", "most", "least", "greatest",
        "smallest", "largest", "fastest", "slowest", "best", "worst",
        "maximum", "minimum", "max", "min",
    ]
    # Từ khoá so sánh → vẫn cần chart (ngoại lệ)
    comparison_kws = ["so sánh", "xếp hạng", "ranking", "top", "comparison", "liệt kê"]

    has_superlative = any(kw in question_lower for kw in vi_superlatives + en_superlatives)
    has_comparison = any(kw in question_lower for kw in comparison_kws)
    return has_superlative and not has_comparison


def _choose_axes(data: list[dict], columns: list[str]) -> tuple[str | None, str | None]:
    if not columns:
        return None, None

    numeric_cols: list[str] = []
    for col in columns:
        values = [row.get(col) for row in data]
        non_null = [v for v in values if v is not None]
        if not non_null:
            continue
        ratio = sum(1 for v in non_null if _is_numeric_like(v)) / len(non_null)
        if ratio >= 0.7:
            numeric_cols.append(col)

    non_numeric_cols = [c for c in columns if c not in numeric_cols]
    # Ưu tiên cột không phải ID làm x-axis
    non_id_non_numeric = [c for c in non_numeric_cols if not _is_id_column(c, data)]

    x_candidates = non_id_non_numeric if non_id_non_numeric else non_numeric_cols

    if x_candidates and numeric_cols:
        return x_candidates[0], numeric_cols[0]
    if non_numeric_cols and numeric_cols:
        return non_numeric_cols[0], numeric_cols[0]
    if len(numeric_cols) >= 2:
        return numeric_cols[0], numeric_cols[1]
    if len(columns) >= 2:
        return columns[0], columns[1]
    return columns[0], columns[0]


def _find_non_id_x(data: list[dict], columns: list[str], current_x: str) -> str | None:
    """Tìm cột non-numeric, non-ID thay thế x-axis khi x hiện tại là ID."""
    numeric_cols = set()
    for col in columns:
        vals = [row.get(col) for row in data if row.get(col) is not None]
        if vals and sum(1 for v in vals if _is_numeric_like(v)) / len(vals) >= 0.7:
            numeric_cols.add(col)

    for col in columns:
        if col == current_x:
            continue
        if col in numeric_cols:
            continue
        if not _is_id_column(col, data):
            return col
    return None


def _suggest_title(question: str, chart_type: str) -> str:
    q = question.strip().rstrip("?")
    if not q:
        return f"{chart_type.title()} chart"
    return q[:120]
