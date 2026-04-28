"""
Text-to-SQL evaluation metrics: CM, EM, EX, VES (Spider / BIRD style).

Spec chuẩn:
  - EM (Exact Match):          String-level so khớp sau normalize & alias stripping.
  - CM (Component Matching):   So khớp từng clause SQL với Jaccard similarity, weighted average.
  - EX (Execution Accuracy):   1.0 nếu result set giống hệt gold (row-wise), 0.0 nếu khác.
                                Hỗ trợ: column-order-insensitive, float epsilon, partial F1-score.
  - VES (Valid Efficiency Score): sqrt(T_gold / T_gen) khi EX == 1.0, cap tại 1.0.
                                  (Theo spec BIRD: VES ∈ [0, 1], không phải [0, 2])

Cải tiến v2 (linh hoạt hơn, bớt khắt khe):
  1. Data Normalization: collapse \n/\t/multi-space thành 1 space; normalize timezone datetime.
  2. Value-based Column Mapping: khi alias khác nhau, tự tìm cặp cột qua data similarity
     thay vì dựa vào positional (dễ nhầm khi thứ tự cột khác).
  3. Two-dimensional F1 (Column × Row): EX_partial = col_score × row_score.
     Nếu chọn đúng 3/4 cột và rows khớp 100%, partial = 0.75 thay vì 0.
  4. Subset / LIMIT-aware precision: nếu gen là tập con hoàn toàn hợp lệ của gold,
     precision = 1.0 (không phạt vì LIMIT ngầm định).
  5. VES cap = 1.0 (theo chuẩn BIRD), không phải 2.0.
  6. Trả về execution_diff để báo cáo "tại sao EX thất bại".
"""

from __future__ import annotations

import math
import re
import time
from typing import Any

# ---------------------------------------------------------------------------
# Clause definitions for CM
# ---------------------------------------------------------------------------
CLAUSE_KEYWORDS = [
    "SELECT",
    "FROM",
    "JOIN",
    "LEFT JOIN",
    "RIGHT JOIN",
    "INNER JOIN",
    "FULL JOIN",
    "CROSS JOIN",
    "WHERE",
    "GROUP BY",
    "HAVING",
    "ORDER BY",
    "LIMIT",
    "UNION",
    "UNION ALL",
    "WITH",
]

CLAUSE_WEIGHTS: dict[str, float] = {
    "SELECT":   0.20,
    "FROM":     0.10,
    "JOIN":     0.10,
    "WHERE":    0.20,
    "GROUP BY": 0.15,
    "HAVING":   0.10,
    "ORDER BY": 0.10,
    "LIMIT":    0.05,
}

CLAUSE_ALIASES: dict[str, str] = {
    "LEFT JOIN":  "JOIN",
    "RIGHT JOIN": "JOIN",
    "INNER JOIN": "JOIN",
    "FULL JOIN":  "JOIN",
    "CROSS JOIN": "JOIN",
    "UNION ALL":  "UNION",
    "WITH":       "SELECT",
}

_RESERVED_ALIAS_FOLLOWERS = (
    "where|group|order|limit|join|left|right|inner|full|cross|on|having|union|"
    "with|select|from"
)
_FROM_JOIN_ALIAS_PATTERN = re.compile(
    rf"\b(from|join)\s+([a-z_][a-z0-9_\.]*)\s+(?:as\s+)?(?!{_RESERVED_ALIAS_FOLLOWERS}\b)([a-z_][a-z0-9_]*)\b"
)

_FLOAT_EPSILON = 1e-6  # Ngưỡng sai số cho so sánh số thực


# ---------------------------------------------------------------------------
# SQL normalization helpers
# ---------------------------------------------------------------------------

def normalize_sql(sql: str) -> str:
    """Lowercase, collapse whitespace, strip SQL comments."""
    if not sql:
        return ""
    s = sql.strip()
    s = re.sub(r"--[^\n]*", " ", s)
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.DOTALL)
    s = re.sub(r"\s+", " ", s)
    s = s.lower()
    s = re.sub(r"\s*(=|!=|<>|<=|>=|<|>)\s*", r" \1 ", s)
    s = re.sub(r"\s*,\s*", ", ", s)
    return s.strip()


def normalize_sql_for_match(sql: str) -> str:
    """
    Normalize for EM-style matching with relaxed alias handling.
    Strips table alias qualifiers from column references.
    """
    s = normalize_sql(sql)
    aliases = {m.group(3) for m in _FROM_JOIN_ALIAS_PATTERN.finditer(s)}
    s = _FROM_JOIN_ALIAS_PATTERN.sub(r"\1 \2", s)
    for alias in sorted(aliases, key=len, reverse=True):
        s = re.sub(rf"\b{re.escape(alias)}\.([a-z_][a-z0-9_]*)\b", r"\1", s)
    return s


def _split_top_level_csv(expr: str) -> list[str]:
    """Split biểu thức theo dấu phẩy ở mức top-level (không split trong hàm)."""
    parts: list[str] = []
    buff: list[str] = []
    depth = 0
    for ch in expr:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if ch == "," and depth == 0:
            part = "".join(buff).strip()
            if part:
                parts.append(part)
            buff = []
            continue
        buff.append(ch)
    tail = "".join(buff).strip()
    if tail:
        parts.append(tail)
    return parts


def _sort_csv_clause_items(clause_body: str) -> str:
    """Sort danh sách item trong SELECT/GROUP BY/ORDER BY để bỏ qua thứ tự."""
    items = _split_top_level_csv(clause_body)
    if len(items) <= 1:
        return clause_body.strip()
    return ", ".join(sorted(i.strip() for i in items if i.strip()))


def _sort_where_predicates(where_body: str) -> str:
    """
    Canonical hóa WHERE theo kiểu nhẹ:
    - Tách các predicate bởi AND ở top-level
    - Sort để bỏ qua thứ tự điều kiện
    """
    # Tách theo AND ở mức top-level (không tách trong ngoặc đơn).
    parts: list[str] = []
    buff: list[str] = []
    depth = 0
    i = 0
    s = where_body
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == "(":
            depth += 1
            buff.append(ch)
            i += 1
            continue
        if ch == ")":
            depth = max(0, depth - 1)
            buff.append(ch)
            i += 1
            continue

        if depth == 0 and i + 3 <= n and s[i:i + 3].lower() == "and":
            prev_ok = (i == 0) or (not (s[i - 1].isalnum() or s[i - 1] == "_"))
            next_ok = (i + 3 == n) or (not (s[i + 3].isalnum() or s[i + 3] == "_"))
            if prev_ok and next_ok:
                piece = "".join(buff).strip()
                if piece:
                    parts.append(piece)
                buff = []
                i += 3
                continue

        buff.append(ch)
        i += 1

    tail = "".join(buff).strip()
    if tail:
        parts.append(tail)
    if len(parts) <= 1:
        return where_body.strip()
    return " and ".join(sorted(parts))


def canonicalize_sql_for_semantic_match(sql: str) -> str:
    """
    Canonical SQL cho semantic matching:
    - Bỏ newline/tab/comment + normalize whitespace
    - Bỏ table alias qualifier (a.col -> col)
    - Bỏ ảnh hưởng thứ tự item trong SELECT/GROUP BY/ORDER BY và predicate AND của WHERE
    """
    norm = normalize_sql_for_match(sql)
    clauses = _merge_clause_aliases(extract_clauses(norm))

    canonical_clauses: dict[str, str] = {}
    for clause, body in clauses.items():
        clean_body = body.strip()
        if clause in {"SELECT", "GROUP BY", "ORDER BY"}:
            clean_body = _sort_csv_clause_items(clean_body)
        elif clause == "WHERE":
            clean_body = _sort_where_predicates(clean_body)
        canonical_clauses[clause] = clean_body

    ordered = ["SELECT", "FROM", "JOIN", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT", "UNION"]
    chunks: list[str] = []
    for kw in ordered:
        val = canonical_clauses.get(kw, "")
        if val:
            chunks.append(f"{kw} {val}")
    return " | ".join(chunks)


# ---------------------------------------------------------------------------
# Clause extraction for CM
# ---------------------------------------------------------------------------

def extract_clauses(sql: str) -> dict[str, str]:
    """Split SQL into clause buckets for Component Matching."""
    sql_upper = sql.upper()
    clauses: dict[str, str] = {}
    positions: list[tuple[int, str]] = []

    for kw in CLAUSE_KEYWORDS:
        pattern = re.compile(r"\b" + kw.replace(" ", r"\s+") + r"\b")
        for m in pattern.finditer(sql_upper):
            positions.append((m.start(), kw))

    positions.sort(key=lambda x: x[0])

    for i, (pos, kw) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(sql)
        content = sql[pos:end].strip()
        content_body = re.sub(
            r"^" + kw.replace(" ", r"\s+"),
            "",
            content,
            flags=re.IGNORECASE,
        ).strip()
        clauses[kw] = normalize_sql(content_body)

    return clauses


def _merge_clause_aliases(clauses: dict[str, str]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for k, v in clauses.items():
        canonical = CLAUSE_ALIASES.get(k, k)
        merged[canonical] = (merged.get(canonical, "") + " " + v).strip()
    return merged


def _clause_similarity(a: str, b: str) -> float:
    """Jaccard token similarity between two clause bodies."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    tokens_a = set(re.split(r"\W+", a)) - {""}
    tokens_b = set(re.split(r"\W+", b)) - {""}
    if not tokens_a and not tokens_b:
        return 1.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)


# ---------------------------------------------------------------------------
# EM — Exact Match
# ---------------------------------------------------------------------------

def compute_em(generated_sql: str | None, gold_sql: str) -> float:
    """
    Exact Match: 1.0 nếu normalized SQL khớp hoàn toàn, 0.0 nếu không.
    Đây là metric khắt khe nhất — khác 1 từ là trả về 0.
    """
    gen = generated_sql or ""
    return float(
        canonicalize_sql_for_semantic_match(gen)
        == canonicalize_sql_for_semantic_match(gold_sql)
    )


# ---------------------------------------------------------------------------
# CM — Component Match
# ---------------------------------------------------------------------------

def compute_cm(generated_sql: str | None, gold_sql: str) -> tuple[float, dict[str, float]]:
    """
    Component Match: Đánh giá từng mệnh đề SQL (SELECT, WHERE, GROUP BY, ...)
    độc lập nhau bằng Jaccard similarity, sau đó tổng hợp weighted average.
    Không yêu cầu thứ tự clause giống nhau.
    """
    gen = generated_sql or ""
    gen_clauses = _merge_clause_aliases(extract_clauses(normalize_sql_for_match(gen)))
    gold_clauses = _merge_clause_aliases(extract_clauses(normalize_sql_for_match(gold_sql)))

    detail: dict[str, float] = {}
    total_weight = 0.0
    weighted_score = 0.0

    for clause, weight in CLAUSE_WEIGHTS.items():
        gold_val = gold_clauses.get(clause, "")
        gen_val = gen_clauses.get(clause, "")

        if not gold_val and not gen_val:
            continue

        sim = _clause_similarity(gen_val, gold_val)
        detail[clause] = round(sim, 4)
        weighted_score += weight * sim
        total_weight += weight

    if total_weight == 0:
        return 0.0, detail

    cm_score = weighted_score / total_weight
    return round(cm_score, 4), detail


# ---------------------------------------------------------------------------
# Row comparison helpers (dùng cho EX & VES)
# ---------------------------------------------------------------------------

def _try_float(v: Any) -> float | None:
    """Thử ép kiểu về float. Trả về None nếu không thể."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


_DATETIME_STRIP_TZ = re.compile(
    r"^(\d{4}-\d{2}-\d{2})[t ](\d{2}:\d{2}:\d{2})(?:\.\d+)?(?:z|[+-]\d{2}:?\d{2})?$"
)


def _normalize_value(v: Any) -> str:
    """
    [Ý tưởng 1] Chuẩn hóa triệt để một giá trị text trước khi so sánh:
    - Collapse tất cả whitespace (\n, \t, dấu cách kép) thành 1 dấu cách.
    - Normalize timezone datetime: bỏ phần timezone/microsecond để chỉ giữ
      yyyy-mm-dd HH:MM:SS, tránh mismatch '2016-09-05 04:15:19' vs '2016-09-05 04:15:19+00:00'.
    """
    s = re.sub(r"\s+", " ", str(v)).strip().lower()
    m = _DATETIME_STRIP_TZ.match(s)
    if m:
        # Normalize về 'yyyy-mm-dd HH:MM:SS' (bỏ T-separator, timezone, microseconds)
        return f"{m.group(1)} {m.group(2)}"
    return s


def _values_equal(a: Any, b: Any, epsilon: float = _FLOAT_EPSILON) -> bool:
    """
    So sánh 2 giá trị:
    - Nếu cả 2 là số thực: dùng ngưỡng epsilon.
    - Nếu không: normalize text (whitespace collapse + datetime normalization) rồi so sánh.
    """
    fa, fb = _try_float(a), _try_float(b)
    if fa is not None and fb is not None:
        return abs(fa - fb) <= epsilon
    return _normalize_value(a) == _normalize_value(b)


def _row_to_comparable(row: tuple[Any, ...], col_names: list[str]) -> dict[str, Any]:
    """Chuyển 1 dòng thành dict {tên_cột: giá_trị} để so sánh độc lập với thứ tự cột."""
    return {col.lower(): val for col, val in zip(col_names, row)}


def _rows_match(
    gen_row: dict[str, Any],
    gold_row: dict[str, Any],
    keys: list[str] | None = None,
    epsilon: float = _FLOAT_EPSILON,
) -> bool:
    """
    So sánh 2 dòng (dưới dạng dict) — column-order-insensitive.
    Nếu `keys` được truyền vào, chỉ so sánh trên tập cột đó (dùng cho partial column matching).
    """
    compare_keys = keys if keys is not None else list(gold_row.keys())
    if not compare_keys:
        return False
    return all(
        k in gen_row and k in gold_row and _values_equal(gen_row[k], gold_row[k], epsilon)
        for k in compare_keys
    )


def rows_to_set(rows: list[tuple[Any, ...]] | None) -> set[tuple[str, ...]]:
    """Chuyển rows về set tuple-string (dùng cho EX strict)."""
    return {tuple(str(v) for v in row) for row in (rows or [])}


def _build_value_column_mapping(
    gen_cols: list[str],
    gold_cols: list[str],
    gen_rows: list[tuple[Any, ...]],
    gold_rows: list[tuple[Any, ...]],
    epsilon: float = _FLOAT_EPSILON,
    min_similarity: float = 0.5,
) -> dict[str, str]:
    """
    [Ý tưởng 2] Value-based Column Mapping.

    Khi tên cột gen và gold khác nhau (alias mismatch), tự động tìm cặp (gen_col, gold_col)
    có giá trị dữ liệu giống nhau cao nhất. Trả về dict {gen_col: gold_col}.

    Thuật toán: Greedy matching — với mỗi gold_col, tìm gen_col chưa được ghép cặp
    có tỷ lệ giá trị trùng khớp cao nhất. Ghép nếu similarity >= min_similarity.
    """
    if not gen_rows or not gold_rows:
        return {}

    n_sample = min(len(gen_rows), len(gold_rows), 50)  # giới hạn sample để tránh chậm
    gen_dicts = [_row_to_comparable(r, gen_cols) for r in gen_rows[:n_sample]]
    gold_dicts = [_row_to_comparable(r, gold_cols) for r in gold_rows[:n_sample]]

    # similarity[gi][goi] = tỷ lệ dòng gen_col gi giống gold_col goi
    def col_similarity(gc: str, godc: str) -> float:
        matches = sum(
            1 for gd, god in zip(gen_dicts, gold_dicts)
            if gc in gd and godc in god and _values_equal(gd[gc], god[godc], epsilon)
        )
        return matches / n_sample

    used_gen_cols: set[str] = set()
    mapping: dict[str, str] = {}  # gold_col -> gen_col

    for gold_c in gold_cols:
        best_sim = min_similarity
        best_gen_c = None
        for gen_c in gen_cols:
            if gen_c in used_gen_cols:
                continue
            sim = col_similarity(gen_c, gold_c)
            if sim > best_sim:
                best_sim = sim
                best_gen_c = gen_c
        if best_gen_c is not None:
            mapping[gold_c] = best_gen_c
            used_gen_cols.add(best_gen_c)

    return mapping  # {gold_col: gen_col}


# ---------------------------------------------------------------------------
# EX — Execution Accuracy (với partial score + diff report)
# ---------------------------------------------------------------------------

def compute_ex_with_detail(
    generated_sql: str,
    gold_sql: str,
    generated_columns: list[str],
    generated_rows: list[tuple[Any, ...]],
    gold_columns: list[str],
    gold_rows: list[tuple[Any, ...]],
    epsilon: float = _FLOAT_EPSILON,
) -> tuple[float, float, dict[str, Any]]:
    """
    Tính EX (strict 0/1) và EX_partial (two-dimensional F1) kèm diff report.

    Trả về:
        ex_strict  (float): 1.0 nếu result sets khớp hoàn toàn, 0.0 nếu không.
        ex_partial (float): col_score × row_f1 (partial credit cho cả cột lẫn dòng).
        diff       (dict):  Chi tiết "tại sao thất bại".

    Pipeline so sánh:
      1. Tên cột khớp hoàn toàn (set match)  → so sánh theo tên (column-order-insensitive).
      2. Tên cột khác nhau                    → [Ý tưởng 2] value-based column mapping.
      3. Partial score                         → [Ý tưởng 3] EX_partial = col_score × row_f1.
      4. LIMIT-aware precision                 → [Ý tưởng 4] nếu gen ⊂ gold, precision = 1.0.
    """
    diff: dict[str, Any] = {}

    gen_cols = [c.lower() for c in generated_columns]
    gold_cols = [c.lower() for c in gold_columns]

    col_names_match = (set(gen_cols) == set(gold_cols))

    # -----------------------------------------------------------------------
    # Xác định tập cột dùng để so sánh và column_score
    # -----------------------------------------------------------------------
    if col_names_match:
        # Mode 1: tên cột khớp hoàn toàn
        active_gold_cols = gold_cols          # cột gold cần so sánh
        col_mapping: dict[str, str] = {c: c for c in gold_cols}  # gold_col -> gen_col
        col_score = 1.0
        diff_gen_cols = gen_cols
        diff_gold_cols = gold_cols
    else:
        # Mode 2: [Ý tưởng 2] value-based column mapping
        col_mapping = _build_value_column_mapping(
            gen_cols, gold_cols, generated_rows, gold_rows, epsilon
        )
        mapped_gold_cols = list(col_mapping.keys())
        # Tập gold chưa ánh xạ được → vẫn thử tìm theo tên cột trùng nhau
        for gc in gold_cols:
            if gc not in col_mapping and gc in gen_cols:
                col_mapping[gc] = gc
                mapped_gold_cols.append(gc)

        active_gold_cols = list(col_mapping.keys())

        # [Ý tưởng 3] col_score = tỷ lệ cột gold được ánh xạ thành công
        n_matched_cols = len(active_gold_cols)
        n_gold_cols = len(gold_cols)
        col_score = n_matched_cols / n_gold_cols if n_gold_cols > 0 else 0.0

        missing_cols = [c for c in gold_cols if c not in active_gold_cols]
        extra_cols   = [c for c in gen_cols  if c not in col_mapping.values()]
        if missing_cols:
            diff["missing_columns"] = missing_cols
        if extra_cols:
            diff["extra_columns"] = extra_cols
        if set(gen_cols) != set(gold_cols):
            diff["generated_columns"] = gen_cols
            diff["gold_columns"] = gold_cols
            diff["value_based_col_mapping"] = col_mapping

        if not active_gold_cols:
            # Không ánh xạ được cột nào → thất bại hoàn toàn
            diff["column_mismatch"] = True
            return 0.0, 0.0, diff

    # -----------------------------------------------------------------------
    # So sánh các dòng chỉ trên tập cột đã ánh xạ
    # -----------------------------------------------------------------------
    gen_dicts = [
        {gold_c: row[gen_cols.index(col_mapping[gold_c])] for gold_c in active_gold_cols
         if col_mapping[gold_c] in gen_cols}
        for row in generated_rows
    ]
    gold_dicts = [
        {gold_c: row[gold_cols.index(gold_c)] for gold_c in active_gold_cols}
        for row in gold_rows
    ]

    gen_count  = len(gen_dicts)
    gold_count = len(gold_dicts)
    matched_count = 0
    gold_unmatched = list(enumerate(gold_dicts))  # (original_idx, dict)

    for gd in gen_dicts:
        for pos, (_, gld) in enumerate(gold_unmatched):
            if _rows_match(gd, gld, keys=active_gold_cols, epsilon=epsilon):
                matched_count += 1
                gold_unmatched.pop(pos)
                break

    gold_unmatched_dicts = [
        {k: str(v) for k, v in row.items()}
        for _, row in gold_unmatched[:3]
    ]

    # -----------------------------------------------------------------------
    # Strict EX theo execution semantics:
    # - Không bắt buộc tên cột giống nhau (alias khác vẫn chấp nhận)
    # - Cần map đủ toàn bộ cột gold và số lượng cột tương đương
    # - Toàn bộ row phải khớp
    # -----------------------------------------------------------------------
    full_column_coverage = (len(active_gold_cols) == len(gold_cols) == len(gen_cols))
    ex_strict = 1.0 if (full_column_coverage and matched_count == gold_count == gen_count) else 0.0

    # -----------------------------------------------------------------------
    # [Ý tưởng 4] LIMIT-aware precision:
    # Nếu gen là tập con hợp lệ của gold (gen_count < gold_count, matched == gen_count),
    # coi precision = 1.0 (không phạt vì LIMIT ngầm định của AI).
    # -----------------------------------------------------------------------
    is_valid_subset = (gen_count < gold_count and matched_count == gen_count)

    if is_valid_subset:
        precision = 1.0
        diff["limit_subset_detected"] = True
        diff["note"] = (
            f"gen ({gen_count} rows) là tập con hợp lệ của gold ({gold_count} rows) — "
            "có thể do AI thêm LIMIT ngầm định. Precision = 1.0."
        )
    else:
        precision = matched_count / gen_count if gen_count > 0 else 0.0

    recall = matched_count / gold_count if gold_count > 0 else 0.0

    # [Ý tưởng 3] row_f1 rồi nhân col_score → EX_partial hai chiều
    row_f1 = (
        round(2 * precision * recall / (precision + recall), 4)
        if (precision + recall) > 0 else 0.0
    )
    ex_partial = round(col_score * row_f1, 4)
    if ex_strict == 1.0:
        # Bất biến metric: strict đúng hoàn toàn thì partial phải = 1.0
        ex_partial = 1.0

    if ex_strict < 1.0:
        diff["col_score"]           = round(col_score, 4)
        diff["row_f1"]              = row_f1
        diff["row_count_generated"] = gen_count
        diff["row_count_gold"]      = gold_count
        diff["rows_matched"]        = matched_count
        diff["rows_missing_in_gen"] = gold_count - matched_count
        diff["rows_extra_in_gen"]   = max(gen_count - matched_count, 0)
        if gold_unmatched_dicts:
            diff["sample_unmatched_gold_rows"] = gold_unmatched_dicts

    return ex_strict, ex_partial, diff


# ---------------------------------------------------------------------------
# VES — Valid Efficiency Score
# ---------------------------------------------------------------------------

def compute_ves_timing_only(
    generated_sql: str,
    gold_sql: str,
    executor: Any,
    repeats: int = 3,
) -> tuple[float, str]:
    """
    BIRD-style VES (timing only) — caller phải đảm bảo EX == 1.0.

    VES = min(sqrt(T_gold / T_gen), 1.0)
    - VES = 1.0: generated SQL nhanh hơn hoặc bằng gold SQL (tối ưu)
    - VES < 1.0: generated SQL chậm hơn gold SQL
    - VES = 0.0: generated SQL lỗi khi chạy

    Khác với phiên bản cũ (cap = 2.0), spec BIRD chuẩn cap tại 1.0.
    Lý do: VES không nên "thưởng" SQL nhanh hơn gold; SQL nhanh = tối ưu = 1.0 là đủ.
    """

    def best_time(sql: str) -> float:
        best = float("inf")
        for _ in range(repeats):
            t0 = time.perf_counter()
            executor.query(sql)
            best = min(best, time.perf_counter() - t0)
        return best

    try:
        gold_time = best_time(gold_sql)
        gen_time = best_time(generated_sql)
        gen_time = max(gen_time, 1e-6)
        gold_time = max(gold_time, 1e-6)
        r_time = gold_time / gen_time
        # Cap tại 1.0 theo chuẩn BIRD (không thưởng SQL nhanh hơn gold)
        return round(min(math.sqrt(r_time), 1.0), 4), ""
    except Exception as exc:
        return 0.0, str(exc)


def compute_ves_from_executor(
    generated_sql: str,
    gold_sql: str,
    executor: Any,
    repeats: int = 3,
) -> tuple[float, str]:
    """
    VES full: kiểm tra EX trước, nếu EX=1.0 thì tính VES timing.
    Trả về (ves_score, error_message).
    """
    try:
        _, gold_rows = executor.query(gold_sql)
        _, gen_rows = executor.query(generated_sql)
        if rows_to_set(gen_rows) != rows_to_set(gold_rows):
            return 0.0, "result mismatch — VES=0"
        return compute_ves_timing_only(generated_sql, gold_sql, executor, repeats)
    except Exception as exc:
        return 0.0, str(exc)
