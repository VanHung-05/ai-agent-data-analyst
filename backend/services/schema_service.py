"""
🔗 schema_service.py — Schema Provider (Đọc metadata từ Databricks)
=====================================================================
📌 TV2 kết nối Databricks, TV3 sẽ dùng module này để expose API /schema

Chức năng:
  - Đọc danh sách tables, columns, data types từ Databricks
  - Cache schema để giảm số lần gọi API
  - Cung cấp metadata cho prompt engineering (TV2) và API (TV3)
"""

import time
from typing import Any

from services.agent_service import get_database
from config import databricks_config


# ====== CACHE SCHEMA (tránh gọi Databricks liên tục) ======
_schema_cache: dict | None = None
_cache_timestamp: float = 0
CACHE_TTL = 300  # Cache 5 phút


def get_full_schema(force_refresh: bool = False) -> dict[str, Any]:
    """
    Lấy toàn bộ thông tin schema từ Databricks

    💡 TV2/TV3 NOTE:
      - Kết quả được cache 5 phút để tránh gọi Databricks quá nhiều
      - Set force_refresh=True để bỏ qua cache

    Returns:
        dict: {
            "catalog": str,
            "schema": str,
            "tables": [
                {
                    "name": str,
                    "columns": [...],
                    "ddl": str
                }
            ],
            "raw_info": str,
            "cached_at": float
        }
    """
    global _schema_cache, _cache_timestamp

    # Kiểm tra cache
    if not force_refresh and _schema_cache and (time.time() - _cache_timestamp < CACHE_TTL):
        return _schema_cache

    db = get_database()
    tables = db.get_usable_table_names()

    schema_data = {
        "catalog": databricks_config.catalog,
        "schema": databricks_config.schema,
        "tables": [],
        "raw_info": db.get_table_info(),
        "cached_at": time.time(),
    }

    for table_name in tables:
        # Lấy metadata cột từ SQLAlchemy Inspector
        columns_info = []
        try:
            inspector = db._inspector
            cols = inspector.get_columns(table_name, schema=databricks_config.schema)
            for c in cols:
                columns_info.append({
                    "name": c["name"],
                    "type": str(c["type"]),
                    "comment": c.get("comment", "")
                })
        except Exception:
            # Fallback nếu lỗi permission
            pass

        table_info = {
            "name": table_name,
            "columns": columns_info,
            "ddl": db.get_table_info([table_name]),
        }
        schema_data["tables"].append(table_info)

    # Update cache
    _schema_cache = schema_data
    _cache_timestamp = time.time()

    return schema_data


def get_table_names() -> list[str]:
    """Lấy danh sách tên bảng"""
    db = get_database()
    return list(db.get_usable_table_names())


def get_table_detail(table_name: str) -> str:
    """Lấy chi tiết DDL + sample data của 1 bảng cụ thể"""
    db = get_database()
    return db.get_table_info([table_name])
