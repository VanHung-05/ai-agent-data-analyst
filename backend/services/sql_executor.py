"""
⚡ sql_executor.py — Thực thi SQL trực tiếp trên Databricks
=============================================================
📌 Module backup cho TV2/TV3 — thực thi SQL trực tiếp (không qua LangChain)

Chức năng:
  - Kết nối trực tiếp Databricks qua databricks-sql-connector
  - Thực thi câu SQL thuần và trả kết quả dạng list[dict]
  - Dùng khi cần bypass LangChain (VD: export CSV, custom query)
"""

from databricks import sql as databricks_sql
from typing import Any

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import databricks_config, app_config
from utils.sql_validator import validate_sql


def get_connection():
    """
    Tạo kết nối trực tiếp tới Databricks SQL Warehouse

    💡 TV2 NOTE:
      - Khác với SQLDatabase (LangChain wrapper), đây là raw connection
      - Dùng khi cần control chi tiết hơn (streaming, large result sets)
    """
    return databricks_sql.connect(
        server_hostname=databricks_config.host,
        http_path=databricks_config.http_path,
        access_token=databricks_config.active_token,
    )


def execute_sql(query: str, max_rows: int | None = None) -> dict[str, Any]:
    """
    Thực thi câu SQL trực tiếp trên Databricks

    Args:
        query: Câu SQL cần thực thi
        max_rows: Giới hạn số dòng trả về (mặc định lấy từ config)

    Returns:
        dict: {
            "columns": list[str],    # Tên các cột
            "data": list[dict],      # Dữ liệu dạng list of dicts
            "row_count": int,
            "error": str | None
        }
    """
    if max_rows is None:
        max_rows = app_config.sql_max_limit

    # Validate SQL trước khi thực thi
    is_valid, error_msg = validate_sql(query)
    if not is_valid:
        return {
            "columns": [],
            "data": [],
            "row_count": 0,
            "error": f"SQL không an toàn: {error_msg}",
        }

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query)

        # Lấy tên cột từ cursor description
        columns = [desc[0] for desc in cursor.description] if cursor.description else []

        # Fetch kết quả
        rows = cursor.fetchmany(max_rows)

        # Chuyển thành list of dicts
        data = [dict(zip(columns, row)) for row in rows]

        cursor.close()
        connection.close()

        return {
            "columns": columns,
            "data": data,
            "row_count": len(data),
            "error": None,
        }

    except Exception as e:
        return {
            "columns": [],
            "data": [],
            "row_count": 0,
            "error": str(e),
        }


# ====== QUICK TEST ======
if __name__ == "__main__":
    print("⚡ Test SQL Executor...")
    result = execute_sql("SELECT 1 AS test_column")
    if result["error"]:
        print(f"❌ Lỗi: {result['error']}")
    else:
        print(f"✅ Kết quả: {result['data']}")
