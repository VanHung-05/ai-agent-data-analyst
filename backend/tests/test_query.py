"""
🧪 test_query.py — Unit tests cho Agent pipeline
===================================================
📌 TV2 viết test cho logic AI, TV5 bổ sung integration tests
"""

import pytest
from utils.sql_validator import validate_sql, sanitize_sql


class TestSQLValidator:
    """Test SQL Validator — đảm bảo chặn được lệnh nguy hiểm"""

    def test_valid_select(self):
        is_valid, error = validate_sql("SELECT * FROM olist_orders LIMIT 10")
        assert is_valid is True
        assert error is None

    def test_valid_with_cte(self):
        sql = "WITH cte AS (SELECT * FROM olist_orders) SELECT * FROM cte LIMIT 10"
        is_valid, error = validate_sql(sql)
        assert is_valid is True

    def test_block_drop(self):
        is_valid, error = validate_sql("DROP TABLE olist_orders")
        assert is_valid is False
        assert "DROP" in error

    def test_block_delete(self):
        is_valid, error = validate_sql("DELETE FROM olist_customers WHERE customer_id = 'abc'")
        assert is_valid is False
        assert "DELETE" in error

    def test_block_update(self):
        is_valid, error = validate_sql("UPDATE olist_orders SET order_status = 'canceled'")
        assert is_valid is False
        assert "UPDATE" in error

    def test_block_insert(self):
        is_valid, error = validate_sql("INSERT INTO olist_orders VALUES (1, 2, 3)")
        assert is_valid is False
        assert "INSERT" in error

    def test_block_excessive_limit(self):
        is_valid, error = validate_sql("SELECT * FROM olist_orders LIMIT 99999")
        assert is_valid is False
        assert "LIMIT" in error

    def test_empty_sql(self):
        is_valid, error = validate_sql("")
        assert is_valid is False

    def test_block_comment_injection(self):
        is_valid, error = validate_sql("SELECT * FROM olist_orders /* DROP TABLE olist_customers */")
        assert is_valid is False


class TestSanitizeSQL:
    """Test SQL sanitizer — tự động thêm LIMIT"""

    def test_add_limit_when_missing(self):
        result = sanitize_sql("SELECT * FROM olist_orders")
        assert "LIMIT" in result.upper()

    def test_keep_existing_limit(self):
        result = sanitize_sql("SELECT * FROM olist_orders LIMIT 50")
        assert "LIMIT 50" in result.upper()


class TestAgentService:
    """Test các hàm nghiệp vụ tiện ích (Utility) bên trong Agent Service"""

    def test_clean_sql_output(self):
        from services.agent_service import _clean_sql_output
        # markdown
        assert _clean_sql_output("```sql\nSELECT 1;\n```") == "SELECT 1"
        # langchain chain prefix
        assert _clean_sql_output("SQLQuery: SELECT 2;") == "SELECT 2"
        # gemini raw text noise
        assert _clean_sql_output("SELECT 1; SQLResult: [Row]") == "SELECT 1"
        assert _clean_sql_output("SELECT 1; Answer: Result is 1") == "SELECT 1"
        # inline comment strip
        assert _clean_sql_output("SELECT * FROM t -- comment of LLM") == "SELECT * FROM t"

    def test_recommend_chart(self):
        from services.agent_service import _recommend_chart

        # Test time-series -> line chart
        assert _recommend_chart("doanh thu theo thang", "SELECT month, sum(price) FROM x", [{"month": "2026-01", "revenue": 100}])["chart_type"] == "line"

        # Test proportion -> pie chart
        assert _recommend_chart("tỷ lệ đơn hàng bị hủy", "SELECT status, cnt FROM x", [{"status": "cancelled", "cnt": 10}])["chart_type"] == "pie"

        # Test top/ranking -> bar chart
        assert _recommend_chart("Top 5 san pham", "SELECT category, revenue FROM x GROUP BY category", [{"category": "a", "revenue": 1}])["chart_type"] == "bar"

        # Test single value -> metric
        assert _recommend_chart("tong doanh thu", "SELECT sum(price) FROM x", [{"total": 1}])["chart_type"] == "metric"

        # Default view when nothing special
        assert _recommend_chart("liet ke don hang", "SELECT id FROM x", [{"id": "o1"}, {"id": "o2"}])["chart_type"] == "table"

    def test_parse_query_result(self):
        from services.agent_service import _parse_query_result
        
        # Databricks RAW result as list of tuples (ast evaluable)
        raw = "[(1, 'Alice'), (2, 'Bob')]"
        res = _parse_query_result(raw)
        assert len(res) == 2
        assert res[0]["col_0"] == 1
        assert res[1]["col_1"] == "Bob"
        
        # Databricks RAW result as single value
        assert _parse_query_result("42")[0]["result"] == "42"
