"""
🧪 test_query.py — Unit tests cho Agent pipeline
===================================================
📌 TV2 viết test cho logic AI, TV5 bổ sung integration tests
"""

import pytest
from utils.sql_validator import (
    is_natural_language_write_request,
    sanitize_sql,
    validate_sql,
)


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


class TestNaturalLanguageWritePolicy:
    """Chặn yêu cầu ghi/sửa/xóa bằng ngôn ngữ tự nhiên (trước khi sinh SQL)."""

    def test_block_update_all_prices_to_zero_vi(self):
        assert is_natural_language_write_request("Hãy update toàn bộ price về 0") is True

    def test_block_update_prices_english(self):
        assert is_natural_language_write_request("UPDATE all prices to 0 please") is True

    def test_block_delete_from_table(self):
        assert is_natural_language_write_request("DELETE FROM olist_orders WHERE 1=1") is True

    def test_allow_select_analytics(self):
        assert is_natural_language_write_request("Thống kê doanh thu theo tháng năm 2017") is False

    def test_allow_read_only_question_with_update_word(self):
        # “cập nhật” theo nghĩa báo cáo / hiển thị — không có tín hiệu ghi
        assert is_natural_language_write_request("Cập nhật cho tôi top 5 bang có điểm review cao nhất") is False


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

    def test_chart_sql_retry_policy(self):
        from services.visualize_agent import (
            needs_chart_sql_retry,
            parse_recent_days_count,
            sql_has_wrong_today_only_filter,
        )

        q = "vẽ biểu đồ đơn hàng 7 ngày gần đây"
        assert parse_recent_days_count(q) == 7
        bad_sql = (
            "SELECT DATE(order_purchase_timestamp + INTERVAL 7 HOURS) AS ngay_vn, COUNT(order_id) "
            "FROM bronze_rt_orders_sim "
            "WHERE DATE(order_purchase_timestamp + INTERVAL 7 HOURS) >= DATE(CURRENT_TIMESTAMP()) "
            "GROUP BY DATE(order_purchase_timestamp + INTERVAL 7 HOURS) LIMIT 7"
        )
        assert sql_has_wrong_today_only_filter(bad_sql) is True
        good_sql = (
            "WHERE DATE(order_purchase_timestamp + INTERVAL 7 HOURS) >= "
            "DATE(CURRENT_TIMESTAMP() + INTERVAL 7 HOURS - INTERVAL 6 DAYS)"
        )
        assert sql_has_wrong_today_only_filter(good_sql) is False

        should_retry, msg = needs_chart_sql_retry(
            q,
            bad_sql,
            [{"ngay_vn": "2026-05-27", "so_don": 120}],
            {"chart_type": "table", "reason": "Single-row aggregate → table + NLG answer is sufficient"},
            route="visualize",
        )
        assert should_retry is True
        assert "INTERVAL 6 DAYS" in msg
        assert "GROUP BY" in msg

        ok, _ = needs_chart_sql_retry(
            q,
            good_sql,
            [{"ngay_vn": f"2026-05-{20+i}", "so_don": 100 + i} for i in range(7)],
            {"chart_type": "line", "reason": "Time series detected"},
            route="visualize",
        )
        assert ok is False

    def test_recommend_chart(self):
        from services.visualize_agent import recommend_chart

        # Test time-series -> line chart (≥2 điểm thời gian)
        assert recommend_chart(
            "doanh thu theo thang",
            "SELECT month, sum(price) FROM x",
            [{"month": "2026-01", "revenue": 100}, {"month": "2026-02", "revenue": 200}],
            None,
        )["chart_type"] == "line"

        # Test proportion -> pie chart (≥2 nhóm)
        assert recommend_chart(
            "tỷ lệ đơn hàng bị hủy",
            "SELECT status, cnt FROM x",
            [{"status": "cancelled", "cnt": 10}, {"status": "delivered", "cnt": 90}],
            None,
        )["chart_type"] == "pie"

        # Test top/ranking -> bar chart
        assert recommend_chart(
            "Top 5 san pham",
            "SELECT category, revenue FROM x GROUP BY category",
            [{"category": "a", "revenue": 1}, {"category": "b", "revenue": 2}],
            None,
        )["chart_type"] == "bar"

        # Một dòng KPI → table (NLG answer đủ rõ, không cần chart)
        assert recommend_chart(
            "tong doanh thu",
            "SELECT sum(price) AS total FROM x",
            [{"total": 1}],
            None,
        )["chart_type"] == "table"

        # Default view when nothing special
        assert recommend_chart(
            "liet ke don hang",
            "SELECT id FROM x",
            [{"id": "o1"}, {"id": "o2"}],
            None,
        )["chart_type"] == "table"

    def test_parse_query_result(self):
        from services.query_result_parser import parse_query_result

        # Databricks RAW result as list of tuples (ast evaluable)
        raw = "[(1, 'Alice'), (2, 'Bob')]"
        res = parse_query_result(raw)
        assert len(res) == 2
        assert res[0]["col_0"] == 1
        assert res[1]["col_1"] == "Bob"

        # datetime.date trong list tuple (GROUP BY ngày)
        raw_dates = (
            "[(datetime.date(2026, 5, 22), 120), (datetime.date(2026, 5, 23), 120), "
            "(datetime.date(2026, 5, 24), 180)]"
        )
        res_dates = parse_query_result(raw_dates)
        assert len(res_dates) == 3
        assert res_dates[0]["col_0"] == "2026-05-22"
        assert res_dates[0]["col_1"] == 120
        assert res_dates[2]["col_1"] == 180

        # Một dòng bọc cả series (nested list)
        raw_nested = "[[(datetime.date(2026, 5, 22), 120), (datetime.date(2026, 5, 23), 90)]]"
        res_nested = parse_query_result(raw_nested)
        assert len(res_nested) == 2
        assert res_nested[1]["col_1"] == 90

        # Fallback result string chứa series (screenshot UI)
        raw_wrapped = (
            "[(datetime.date(2026, 5, 22), 120), (datetime.date(2026, 5, 23), 120)]"
        )
        res_wrapped = parse_query_result(raw_wrapped)
        assert len(res_wrapped) == 2

        # KPI một số — giữ 1 dòng
        assert parse_query_result("42")[0]["result"] == "42"
        assert len(parse_query_result("[(120,)]")) == 1
        assert parse_query_result("[{'total': 999}]")[0]["total"] == 999
