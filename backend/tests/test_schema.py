"""
🧪 test_schema.py — Unit tests cho Schema Service
====================================================
📌 TV2/TV3 viết test cho Schema Provider
"""

# TODO: TV2 implement sau khi có kết nối Databricks thực tế
# Hoặc dùng mock database để test offline

import pytest
from services.schema_service import get_table_names, get_full_schema

class TestSchemaService:
    """Test Schema Provider (Yêu cầu M2M Auth tới Databricks hoạt động)"""

    def test_get_table_names(self):
        tables = get_table_names()
        # Dataset Olist có ít nhất 8 bảng
        assert isinstance(tables, list)
        assert len(tables) >= 3

    def test_get_full_schema(self):
        schema = get_full_schema()
        assert "tables" in schema
        assert "catalog" in schema
        assert "schema" in schema
        assert len(schema["tables"]) >= 3
        # Cache works?
        assert "cached_at" in schema
