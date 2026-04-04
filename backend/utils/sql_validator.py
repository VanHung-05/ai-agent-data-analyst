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
