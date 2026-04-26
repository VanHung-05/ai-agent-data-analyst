import json

import pytest

from evaluation.sql_eval_runner import (
    EvalSample,
    build_summary,
    extract_requested_limit,
    is_transient_generation_error,
    lexical_semantic_score,
    load_dataset,
    normalize_sql_limit_to_question,
    parse_retry_delay_seconds,
    performance_pass,
    syntax_pass,
)


def test_syntax_pass():
    assert syntax_pass("SELECT * FROM olist_orders LIMIT 10") is True
    assert syntax_pass("WITH cte AS (SELECT 1) SELECT * FROM cte LIMIT 1") is True
    assert syntax_pass("DELETE FROM olist_orders") is False


def test_performance_pass():
    assert performance_pass("SELECT * FROM olist_orders LIMIT 1000") is True
    assert performance_pass("SELECT * FROM olist_orders LIMIT 1001") is False
    assert performance_pass("SELECT * FROM olist_orders") is False


def test_lexical_semantic_score():
    sample = EvalSample(
        id="x",
        question="q",
        gold_sql="SELECT 1",
        category="basic_select",
        difficulty="easy",
        must_include=["olist_orders", "limit"],
        must_exclude=["drop", "delete"],
    )
    good_sql = "SELECT * FROM olist_orders LIMIT 10"
    bad_sql = "SELECT * FROM random_table"
    assert lexical_semantic_score(sample, good_sql) > lexical_semantic_score(sample, bad_sql)


def test_build_summary():
    from evaluation.sql_eval_runner import CaseResult

    cases = [
        CaseResult(
            sample_id="1",
            question="q1",
            category="basic_select",
            difficulty="easy",
            generated_sql="SELECT 1 LIMIT 1",
            gold_sql="SELECT 1 LIMIT 1",
            syntax_pass=True,
            safety_pass=True,
            performance_pass=True,
            semantic_score=0.9,
            execution_success=True,
            errors=[],
        ),
        CaseResult(
            sample_id="2",
            question="q2",
            category="join",
            difficulty="hard",
            generated_sql=None,
            gold_sql="SELECT 1 LIMIT 1",
            syntax_pass=False,
            safety_pass=False,
            performance_pass=False,
            semantic_score=0.1,
            execution_success=False,
            errors=["generated_sql_empty"],
        ),
    ]
    summary = build_summary(cases)
    assert summary["total_input_samples"] == 2
    assert summary["total_samples"] == 1
    assert summary["evaluated_samples"] == 1
    assert summary["skipped_samples"] == 1
    assert summary["skipped_case_ids"] == ["2"]
    assert 0.0 <= summary["overall_weighted_score"] <= 1.0


def test_load_dataset_accepts_cases_key(tmp_path):
    p = tmp_path / "ds.json"
    p.write_text(
        json.dumps(
            {
                "metadata": {},
                "cases": [
                    {
                        "id": "a1",
                        "question": "q?",
                        "gold_sql": "SELECT 1 LIMIT 1",
                        "category": "basic_select",
                        "difficulty": "easy",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    rows = load_dataset(p)
    assert len(rows) == 1
    assert rows[0].id == "a1"
    assert rows[0].must_include == []
    assert rows[0].must_exclude == []


def test_parse_retry_delay_seconds():
    msg_1 = "429 RESOURCE_EXHAUSTED ... retryDelay': '27s'"
    msg_2 = "Please retry in 12.5s."
    assert parse_retry_delay_seconds(msg_1) == 27.0
    assert parse_retry_delay_seconds(msg_2) == 12.5


def test_is_transient_generation_error():
    assert is_transient_generation_error("503 UNAVAILABLE high demand") is True
    assert is_transient_generation_error("429 RESOURCE_EXHAUSTED") is True
    assert is_transient_generation_error("Some syntax error in SQL") is False


def test_extract_requested_limit():
    assert extract_requested_limit("Top 10 sản phẩm bán chạy") == 10
    assert extract_requested_limit("Liệt kê first 5 orders") == 5
    assert extract_requested_limit("Có bao nhiêu khách hàng?") is None


def test_normalize_sql_limit_to_question():
    sql = "SELECT order_id FROM olist_orders ORDER BY order_purchase_timestamp DESC LIMIT 1000"
    q = "Liệt kê 10 đơn hàng gần nhất"
    assert normalize_sql_limit_to_question(sql, q).endswith("LIMIT 10")

    sql_small = "SELECT order_id FROM olist_orders LIMIT 5"
    assert normalize_sql_limit_to_question(sql_small, q).endswith("LIMIT 5")


def test_compute_em_cm():
    from evaluation.text_to_sql_metrics import compute_cm, compute_em

    gold = "SELECT a, b FROM t WHERE x = 1 LIMIT 10"
    assert compute_em(gold, gold) == 1.0
    assert compute_em("SELECT a, b FROM t WHERE x = 1 LIMIT 10", gold) == 1.0
    assert compute_em("SELECT a,b FROM t WHERE x=1 LIMIT 10", gold) == 1.0
    assert compute_em("SELECT b, a FROM t WHERE x = 1 LIMIT 10", gold) == 0.0

    cm_same, _ = compute_cm(gold, gold)
    assert cm_same == 1.0
    cm_partial, detail = compute_cm("SELECT a FROM t LIMIT 10", gold)
    assert 0.0 < cm_partial < 1.0
    assert "WHERE" in detail


@pytest.mark.parametrize(
    ("generated_sql", "gold_sql"),
    [
        (
            "SELECT p.product_id FROM products p WHERE p.product_id = 10 LIMIT 1",
            "SELECT product_id FROM products WHERE product_id = 10 LIMIT 1",
        ),
        (
            "SELECT p.id, p.name FROM products AS p ORDER BY p.id LIMIT 5",
            "SELECT id, name FROM products ORDER BY id LIMIT 5",
        ),
        (
            "SELECT o.order_id FROM orders o JOIN users u ON o.user_id = u.user_id LIMIT 3",
            "SELECT order_id FROM orders JOIN users ON user_id = user_id LIMIT 3",
        ),
    ],
)
def test_compute_em_ignores_table_aliases(generated_sql, gold_sql):
    from evaluation.text_to_sql_metrics import compute_em

    assert compute_em(generated_sql, gold_sql) == 1.0
