"""
🛡️ sql_validator.py — Kiểm tra an toàn SQL trước khi thực thi
================================================================
📌 TV2 xây dựng, TV3 sử dụng trong API layer

Chức năng:
  - Chặn các lệnh DML nguy hiểm (INSERT, UPDATE, DELETE, DROP...)
  - Kiểm tra LIMIT để tránh truy vấn quá lớn
  - Tầng bảo vệ thứ 2 (sau Prompt + sau Unity Catalog permission)
"""

import re
import unicodedata


# Danh sách các keyword DML bị cấm
BLOCKED_KEYWORDS = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bCREATE\b",
    r"\bREPLACE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bMERGE\b",
]

# Giới hạn LIMIT tối đa
MAX_LIMIT = 1000

# --- Chặn yêu cầu ghi/sửa/xóa dữ liệu bằng ngôn ngữ tự nhiên (trước khi sinh SQL) ---
WRITE_REQUEST_REFUSAL_VI: str = (
    "Hệ thống chỉ hỗ trợ đọc dữ liệu (truy vấn SELECT). "
    "Không thực hiện được các thao tác sửa, xóa, thêm hay thay đổi dữ liệu trên kho "
    "(UPDATE/DELETE/INSERT/DROP/…). "
    "Nếu bạn cần phân tích hoặc xem thống kê, hãy đặt câu hỏi dạng “cho biết / thống kê / top / theo tháng …”."
)


def _normalize_question_for_policy(question: str) -> str:
    """Chuẩn hóa chữ thường + bỏ dấu tiếng Việt để so khớp policy đơn giản."""
    s = question.strip().lower()
    s = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in s if unicodedata.category(ch) != "Mn")


def is_natural_language_write_request(question: str) -> bool:
    """
    Phát hiện ý định sửa/xóa/ghi dữ liệu từ câu hỏi tự nhiên (không cần là câu SQL).

    Dùng để từ chối sớm, tránh LLM/NLG diễn đạt như sẽ thực hiện UPDATE/DELETE
    trong khi backend chỉ có thể chạy SELECT.

    Args:
        question: Câu hỏi gốc của người dùng.

    Returns:
        True nếu nên chặn theo chính sách read-only.
    """
    if not question or not question.strip():
        return False

    raw = question.strip()
    raw_upper = raw.upper()
    n = _normalize_question_for_policy(raw)

    # Mảnh SQL / DDL lộ liễu trong câu hỏi
    sql_fragments = [
        r"\bDELETE\s+FROM\b",
        r"\bINSERT\s+INTO\b",
        r"\bDROP\s+TABLE\b",
        r"\bTRUNCATE\b",
        r"\bALTER\s+TABLE\b",
        r"\bMERGE\s+INTO\b",
        r"\bUPDATE\s+\w+\s+SET\b",
    ]
    for pat in sql_fragments:
        if re.search(pat, raw_upper):
            return True

    # Tiếng Việt / Anh: từ khóa thao tác ghi + đối tượng dữ liệu
    nl_patterns = [
        # update / set giá (bắt buộc có tín hiệu gán giá trị hoặc số 0)
        r"\bupdate\b.*\b(price|prices)\b.*(\bset\b|=|\bto\b|\bve\b|\bthan[hg]\b|0\b)",
        r"\b(set|dat)\b.*\b(price|prices|gia)\b.*(=|\bto\b|\bve\b|\bthan[hg]\b|0\b)",
        # cập nhật / sửa / xóa dữ liệu
        r"\b(cap nhat|sua|thay doi|doi)\b.*(toan bo|tat ca)\b.*\b(gia|price)\b",
        r"\b(cap nhat|sua)\b.*\b(gia|price)\b.*(\bve\b|\bthan[hg]\b|=|0\b)",
        r"\b(xoa|xóa)\b.*(tat ca|toan bo|du lieu|bang|table|dong|hang)\b",
        r"\b(delete|remove|erase|wipe)\b.*(\b(all|every|full)\b|toan bo|tat ca|rows?|data)\b",
        r"\b(overwrite|purge)\b.*\b(data|database|table)\b",
        r"\b(empty|clear)\b.*\b(table|database|bang)\b",
    ]
    for pat in nl_patterns:
        if re.search(pat, n, flags=re.IGNORECASE):
            return True

    return False


def validate_sql(sql: str) -> tuple[bool, str | None]:
    """
    Kiểm tra SQL có an toàn để thực thi không

    Args:
        sql: Câu SQL cần kiểm tra

    Returns:
        tuple: (is_valid: bool, error_message: str | None)
               - (True, None) nếu SQL an toàn
               - (False, "lý do") nếu SQL nguy hiểm

    Ví dụ:
        >>> validate_sql("SELECT * FROM orders LIMIT 10")
        (True, None)
        >>> validate_sql("DROP TABLE orders")
        (False, "Phát hiện lệnh nguy hiểm: DROP")
    """
    if not sql or not sql.strip():
        return False, "SQL rỗng"

    sql_upper = sql.upper().strip()

    # --- Check 1: Chặn DML keywords ---
    for pattern in BLOCKED_KEYWORDS:
        if re.search(pattern, sql_upper):
            keyword = re.search(pattern, sql_upper).group()
            return False, f"Phát hiện lệnh nguy hiểm: {keyword}"

    # --- Check 2: Phải bắt đầu bằng SELECT hoặc WITH (CTE) ---
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return False, f"Chỉ chấp nhận câu lệnh SELECT. Phát hiện: {sql_upper[:20]}..."

    # --- Check 3: Kiểm tra LIMIT ---
    limit_match = re.search(r"\bLIMIT\s+(\d+)", sql_upper)
    if limit_match:
        limit_value = int(limit_match.group(1))
        if limit_value > MAX_LIMIT:
            return False, f"LIMIT quá lớn ({limit_value}). Tối đa cho phép: {MAX_LIMIT}"

    # --- Check 4: Chặn block comment injection (/* ... */) ---
    # Note: Single-line comment (--) đã được strip ở _clean_sql_output()
    if "/*" in sql:
        return False, "Phát hiện SQL block comment (có thể là injection)"

    return True, None


def sanitize_sql(sql: str) -> str:
    """
    Tự động thêm LIMIT nếu câu SQL chưa có

    💡 TV2 NOTE:
      - Gọi hàm này SAU khi validate_sql() đã pass
      - Đảm bảo không bao giờ trả về quá nhiều dữ liệu
    """
    sql = sql.strip().rstrip(";")
    sql_upper = sql.upper()

    if "LIMIT" not in sql_upper:
        sql += f" LIMIT {MAX_LIMIT}"

    return sql


# ====== QUICK TEST ======
if __name__ == "__main__":
    test_cases = [
        ("SELECT * FROM orders LIMIT 10", True),
        ("DROP TABLE orders", False),
        ("DELETE FROM users WHERE id = 1", False),
        ("SELECT * FROM orders", True),
        ("UPDATE orders SET status = 'done'", False),
        ("WITH cte AS (SELECT * FROM orders) SELECT * FROM cte", True),
        ("SELECT * FROM orders LIMIT 99999", False),
    ]

    print("🛡️ Testing SQL Validator...")
    for sql, expected in test_cases:
        is_valid, error = validate_sql(sql)
        status = "✅" if is_valid == expected else "❌ FAILED"
        print(f"  {status} | Valid={is_valid:5} | {sql[:50]}")
        if error:
            print(f"         Reason: {error}")
