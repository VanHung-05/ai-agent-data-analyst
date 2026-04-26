from __future__ import annotations

import argparse
import asyncio
import collections
import json
import random
import time
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

from config import databricks_config
from utils.sql_validator import MAX_LIMIT, sanitize_sql, validate_sql

from evaluation.text_to_sql_metrics import (
    compute_cm,
    compute_em,
    compute_ex_with_detail,
    compute_ves_timing_only,
    rows_to_set,
)

DISALLOWED_KEYWORDS = {"drop", "delete", "update", "insert", "alter", "truncate", "replace", "merge"}
_eval_db_instance: Any | None = None


@dataclass
class EvalSample:
    id: str
    question: str
    gold_sql: str
    category: str
    difficulty: str
    must_include: list[str]
    must_exclude: list[str]


@dataclass
class CaseResult:
    sample_id: str
    question: str
    category: str
    difficulty: str
    generated_sql: str | None
    gold_sql: str
    syntax_pass: bool
    safety_pass: bool
    performance_pass: bool
    semantic_score: float
    execution_success: bool
    errors: list[str]
    # Spider / BIRD-style metrics (EM, CM always; EX, VES when Databricks executor runs)
    em: float | None = None
    cm: float | None = None
    cm_detail: dict[str, Any] = field(default_factory=dict)
    ex: float | None = None           # Strict EX: 0 or 1
    ex_partial: float | None = None   # Partial EX: F1-score dựa trên số dòng khớp
    ves: float | None = None
    execution_diff: dict[str, Any] = field(default_factory=dict)  # Chi tiết lỗi EX


def classify_ex_failure(case: CaseResult) -> str:
    """
    Nhóm nguyên nhân EX fail để theo dõi quality theo vòng:
    - alias_only: Khác alias/tên cột nhưng dữ liệu đã khớp
    - limit_mismatch: Sai số dòng (thường do LIMIT/TOP-N), cột đã khớp
    - semantic_mismatch: Sai ngữ nghĩa thực sự
    """
    if case.ex is None:
        return "not_evaluated"
    if case.ex == 1.0:
        return "pass"

    diff = case.execution_diff or {}
    col_score = float(diff.get("col_score", 0.0) or 0.0)
    row_f1 = float(diff.get("row_f1", 0.0) or 0.0)
    row_count_generated = diff.get("row_count_generated")
    row_count_gold = diff.get("row_count_gold")
    rows_matched = diff.get("rows_matched")
    missing_columns = diff.get("missing_columns") or []
    extra_columns = diff.get("extra_columns") or []

    # Nếu có thiếu/thừa cột thì không coi là alias-only.
    if missing_columns or extra_columns:
        # Trường hợp phổ biến: model trả thêm cột hoặc bỏ cột mô tả quan trọng.
        return "semantic_mismatch"

    # Alias-only: dữ liệu và tập dòng khớp hoàn toàn, khác ở label cột.
    if col_score >= 0.999 and row_f1 >= 0.999:
        return "alias_only"

    # Limit mismatch: cột khớp tốt, nhưng số dòng lệch (thường do LIMIT N không đúng).
    if (
        col_score >= 0.999
        and row_count_generated is not None
        and row_count_gold is not None
        and rows_matched is not None
        and row_count_generated != row_count_gold
        and rows_matched == min(row_count_generated, row_count_gold)
    ):
        return "limit_mismatch"

    return "semantic_mismatch"


class DatabricksSQLExecutor:
    def __init__(self) -> None:
        self._enabled = bool(databricks_config.host and databricks_config.http_path and databricks_config.active_token)

    @property
    def enabled(self) -> bool:
        return self._enabled

    def query(self, sql: str) -> tuple[list[str], list[tuple[Any, ...]]]:
        if not self._enabled:
            raise RuntimeError("Databricks executor is disabled.")

        from databricks import sql as databricks_sql

        with databricks_sql.connect(
            server_hostname=databricks_config.host,
            http_path=databricks_config.http_path,
            access_token=databricks_config.active_token,
            catalog=databricks_config.catalog,
            schema=databricks_config.schema,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in (cursor.description or [])]
                return columns, rows


def load_dataset(path: Path) -> list[EvalSample]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_items: list[Any] = payload.get("samples") or payload.get("cases") or []
    samples: list[EvalSample] = []
    for item in raw_items:
        samples.append(
            EvalSample(
                id=str(item["id"]),
                question=str(item["question"]),
                gold_sql=str(item["gold_sql"]),
                category=str(item.get("category", "unknown")),
                difficulty=str(item.get("difficulty", "unknown")),
                must_include=[str(x).lower() for x in item.get("must_include", [])],
                must_exclude=[str(x).lower() for x in item.get("must_exclude", [])],
            )
        )
    return samples


def syntax_pass(sql: str | None) -> bool:
    if not sql:
        return False
    normalized = sql.strip().lower()
    if not (normalized.startswith("select") or normalized.startswith("with")):
        return False
    return normalized.count("(") == normalized.count(")")


def performance_pass(sql: str | None) -> bool:
    if not sql:
        return False
    upper_sql = sql.upper()
    match = re.search(r"\bLIMIT\s+(\d+)\b", upper_sql)
    if not match:
        return False
    return int(match.group(1)) <= MAX_LIMIT


def lexical_semantic_score(sample: EvalSample, generated_sql: str | None) -> float:
    if not generated_sql:
        return 0.0
    sql_lower = generated_sql.lower()
    include_ratio = 1.0
    if sample.must_include:
        include_hits = sum(1 for token in sample.must_include if token in sql_lower)
        include_ratio = include_hits / len(sample.must_include)
    exclude_ratio = 1.0
    if sample.must_exclude:
        exclude_hits = sum(1 for token in sample.must_exclude if token in sql_lower)
        exclude_ratio = 1 - (exclude_hits / len(sample.must_exclude))
    return round(max(0.0, min(1.0, 0.6 * include_ratio + 0.4 * exclude_ratio)), 4)


def result_signature_score(
    generated_columns: list[str],
    generated_rows: list[tuple[Any, ...]],
    gold_columns: list[str],
    gold_rows: list[tuple[Any, ...]],
) -> float:
    if not gold_columns and not generated_columns:
        col_score = 1.0
    elif not gold_columns:
        col_score = 0.0
    else:
        overlap = len(set(col.lower() for col in generated_columns) & set(col.lower() for col in gold_columns))
        col_score = overlap / max(1, len(set(col.lower() for col in gold_columns)))

    if not gold_rows and not generated_rows:
        row_score = 1.0
    elif not gold_rows:
        row_score = 0.0
    else:
        row_score = 1 - (abs(len(generated_rows) - len(gold_rows)) / max(1, len(gold_rows)))
        row_score = max(0.0, row_score)

    return round(max(0.0, min(1.0, 0.5 * col_score + 0.5 * row_score)), 4)


async def generate_sql_by_api(api_url: str, question: str, timeout_sec: float) -> str | None:
    async with httpx.AsyncClient(timeout=timeout_sec) as client:
        response = await client.post(api_url, json={"question": question})
        response.raise_for_status()
        payload = response.json()
        return payload.get("generated_sql")


async def generate_sql_by_process_question(question: str) -> str | None:
    from services.agent_service import process_question

    response = await process_question(question)
    return response.get("generated_sql")


def get_eval_database() -> Any:
    global _eval_db_instance
    if _eval_db_instance is not None:
        return _eval_db_instance
    from langchain_community.utilities import SQLDatabase

    _eval_db_instance = SQLDatabase.from_uri(databricks_config.sqlalchemy_uri)
    return _eval_db_instance


def load_system_prompt() -> str:
    prompt_path = (
        Path(__file__).resolve().parent.parent / "prompts" / "system_prompt.txt"
    )
    if not prompt_path.exists():
        return "You are a helpful SQL assistant. Generate valid Spark SQL queries."
    return prompt_path.read_text(encoding="utf-8")


def clean_sql_output(sql: str) -> str:
    sql = sql.strip()
    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.startswith("```"):
        sql = sql[3:]
    if sql.endswith("```"):
        sql = sql[:-3]
    sql = re.sub(r"^(?:SQL\s*Query\s*:\s*|SQLQuery\s*:\s*)", "", sql, flags=re.IGNORECASE)
    for stop in ["SQLResult:", "SQL Result:", "Answer:", "Explanation:"]:
        idx = sql.find(stop)
        if idx > 0:
            sql = sql[:idx]
    sql = re.sub(r"--[^\n]*", "", sql)
    return sql.strip().rstrip(";")


async def generate_sql_sql_only(question: str, previous_error: str = "") -> str:
    from langchain.chains import create_sql_query_chain

    from services.llm_service import get_llm

    llm = get_llm()
    db = get_eval_database()
    chain = create_sql_query_chain(llm, db, k=100)
    system_prompt = load_system_prompt()
    if previous_error:
        prompt = (
            f"{system_prompt}\n\n"
            f"Câu hỏi gốc: {question}\n"
            f"LỖI TRƯỚC ĐÓ: {previous_error}\n"
            "Hãy viết lại SQL Spark chính xác hơn. Chỉ xuất SQL, không giải thích."
        )
    else:
        prompt = f"{system_prompt}\n\nUser Question: {question}"
    loop = asyncio.get_running_loop()
    raw_sql = await loop.run_in_executor(None, lambda: chain.invoke({"question": prompt}))
    generated_sql = clean_sql_output(str(raw_sql))
    is_valid, error_msg = validate_sql(generated_sql)
    if not is_valid:
        raise ValueError(f"SQL bị chặn: {error_msg}")
    return sanitize_sql(generated_sql)


def parse_retry_delay_seconds(error_message: str) -> float:
    if not error_message:
        return 5.0

    retry_delay_match = re.search(r"retryDelay['\"]?\s*:\s*['\"]?([0-9]+(?:\.[0-9]+)?)s", error_message)
    if retry_delay_match:
        return max(1.0, float(retry_delay_match.group(1)))

    please_retry_match = re.search(r"Please retry in\s+([0-9]+(?:\.[0-9]+)?)s", error_message, flags=re.IGNORECASE)
    if please_retry_match:
        return max(1.0, float(please_retry_match.group(1)))

    return 5.0


def is_transient_generation_error(error_message: str) -> bool:
    if not error_message:
        return False
    msg = error_message.lower()
    return any(
        token in msg
        for token in (
            "429",
            "resource_exhausted",
            "503",
            "unavailable",
            "high demand",
            "temporarily unavailable",
            "timeout",
        )
    )


def compute_retry_wait_seconds(error_message: str, attempt: int) -> float:
    base_wait = parse_retry_delay_seconds(error_message)
    # Exponential backoff with light jitter to avoid synchronized retries.
    exp_wait = min(base_wait * (2 ** max(0, attempt - 1)), 60.0)
    jitter = random.uniform(0.0, 1.5)
    return exp_wait + jitter


def extract_requested_limit(question: str) -> int | None:
    if not question:
        return None
    q = question.lower()
    patterns = [
        r"\btop\s+(\d+)\b",
        r"\bfirst\s+(\d+)\b",
        r"\blimit\s+(\d+)\b",
        r"\b(\d+)\s+(?:đơn hàng|sản phẩm|người bán|khách hàng|đánh giá|thành phố|danh mục)\b",
    ]
    for pat in patterns:
        m = re.search(pat, q, flags=re.IGNORECASE)
        if m:
            val = int(m.group(1))
            if val > 0:
                return val
    return None


def normalize_sql_limit_to_question(sql: str, question: str) -> str:
    requested = extract_requested_limit(question)
    if not requested:
        return sql

    limit_pattern = re.compile(r"\bLIMIT\s+(\d+)\b(?!.*\bLIMIT\b)", flags=re.IGNORECASE | re.DOTALL)
    match = limit_pattern.search(sql)
    if match:
        current_limit = int(match.group(1))
        # Keep stricter limit if already smaller, otherwise cap down to question intent.
        if current_limit <= requested:
            return sql
        start, end = match.span(1)
        return sql[:start] + str(requested) + sql[end:]
    return f"{sql.rstrip()} LIMIT {requested}"


async def generate_sql_with_retry(
    *,
    generator_mode: str,
    api_url: str,
    question: str,
    timeout_sec: float,
    max_attempts: int,
) -> str | None:
    last_error = ""
    for attempt in range(1, max_attempts + 1):
        try:
            if generator_mode == "sql_only":
                return await generate_sql_sql_only(question=question, previous_error=last_error)
            if generator_mode == "api":
                return await generate_sql_by_api(api_url=api_url, question=question, timeout_sec=timeout_sec)
            return await generate_sql_by_process_question(question=question)
        except Exception as exc:
            message = str(exc)
            last_error = message
            if attempt >= max_attempts:
                raise
            is_transient = is_transient_generation_error(message)
            wait_seconds = (
                compute_retry_wait_seconds(message, attempt) if is_transient else min(5.0 * attempt, 20.0)
            )
            print(
                f"[WARN] generate_sql attempt {attempt}/{max_attempts} failed: {message[:200]} | "
                f"retry_after={wait_seconds:.2f}s"
            )
            await asyncio.sleep(wait_seconds)
    raise RuntimeError("Failed to generate SQL after retries")


async def evaluate_one(
    sample: EvalSample,
    generator_mode: str,
    api_url: str,
    timeout_sec: float,
    executor: DatabricksSQLExecutor,
    generation_max_attempts: int,
) -> CaseResult:
    errors: list[str] = []
    generated_sql: str | None = None

    try:
        generated_sql = await generate_sql_with_retry(
            generator_mode=generator_mode,
            api_url=api_url,
            question=sample.question,
            timeout_sec=timeout_sec,
            max_attempts=generation_max_attempts,
        )
        if generated_sql:
            generated_sql = normalize_sql_limit_to_question(generated_sql, sample.question)
    except Exception as exc:
        errors.append(f"generate_sql_error: {exc}")

    syntax_ok = syntax_pass(generated_sql)
    safety_ok = False
    if generated_sql:
        safety_ok, safety_error = validate_sql(generated_sql)
        if not safety_ok and safety_error:
            errors.append(f"safety_error: {safety_error}")
    else:
        errors.append("generated_sql_empty")

    performance_ok = performance_pass(generated_sql)
    lexical_score = lexical_semantic_score(sample, generated_sql)
    semantic_score = lexical_score
    disallowed = False
    execution_success = bool(generated_sql and syntax_ok and safety_ok)

    em = compute_em(generated_sql, sample.gold_sql)
    cm, cm_detail = compute_cm(generated_sql, sample.gold_sql)
    ex_val: float | None = None
    ves_val: float | None = None

    if generated_sql:
        lower_sql = generated_sql.lower()
        if any(keyword in lower_sql for keyword in DISALLOWED_KEYWORDS):
            disallowed = True
            execution_success = False
            errors.append("disallowed_keyword_detected")

    ex_partial_val: float | None = None
    execution_diff: dict[str, Any] = {}

    if executor.enabled and generated_sql and syntax_ok and safety_ok:
        try:
            gold_is_safe, gold_error = validate_sql(sample.gold_sql)
            if not gold_is_safe:
                raise ValueError(f"gold_sql_unsafe: {gold_error}")
            gold_sql_run = sanitize_sql(sample.gold_sql)

            # Thực thi cả 2 câu lên Databricks
            generated_columns, generated_rows = executor.query(generated_sql)
            gold_columns, gold_rows = executor.query(gold_sql_run)

            # --- EX: column-order-insensitive, float-epsilon, partial F1 ---
            ex_val, ex_partial_val, execution_diff = compute_ex_with_detail(
                generated_sql=generated_sql,
                gold_sql=gold_sql_run,
                generated_columns=generated_columns,
                generated_rows=list(generated_rows),
                gold_columns=gold_columns,
                gold_rows=list(gold_rows),
            )

            # Semantic score: kết hợp lexical + kết quả thực thi
            # Dùng ex_partial (F1) thay vì result_signature_score cũ
            semantic_score = round(0.4 * lexical_score + 0.6 * ex_partial_val, 4)

            # VES chỉ tính khi EX strict = 1.0 (kết quả hoàn toàn đúng)
            if ex_val == 1.0:
                ves_val, ves_err = compute_ves_timing_only(
                    generated_sql, gold_sql_run, executor, repeats=3
                )
                if ves_err:
                    errors.append(f"VES_error: {ves_err}")
            else:
                ves_val = 0.0

            execution_success = (ex_val == 1.0) and not disallowed
        except Exception as exc:
            errors.append(f"execution_compare_error: {exc}")
            execution_success = False

    return CaseResult(
        sample_id=sample.id,
        question=sample.question,
        category=sample.category,
        difficulty=sample.difficulty,
        generated_sql=generated_sql,
        gold_sql=sample.gold_sql,
        syntax_pass=syntax_ok,
        safety_pass=safety_ok,
        performance_pass=performance_ok,
        semantic_score=semantic_score,
        execution_success=execution_success,
        errors=errors,
        em=em,
        cm=cm,
        cm_detail=cm_detail,
        ex=ex_val,
        ex_partial=ex_partial_val,
        ves=ves_val,
        execution_diff=execution_diff,
    )


def build_summary(case_results: list[CaseResult]) -> dict[str, Any]:
    total = len(case_results)
    valid_cases = [c for c in case_results if not c.errors]
    skipped_cases = [c for c in case_results if c.errors]
    evaluated_total = len(valid_cases)

    if evaluated_total == 0:
        return {
            "total_samples": 0,
            "total_input_samples": total,
            "evaluated_samples": 0,
            "skipped_samples": total,
            "skipped_case_ids": [c.sample_id for c in skipped_cases],
            "execution_success_rate": 0.0,
            "safety_pass_rate": 0.0,
            "semantic_match_rate": 0.0,
            "syntax_pass_rate": 0.0,
            "performance_pass_rate": 0.0,
            "average_semantic_score": 0.0,
            "overall_weighted_score": 0.0,
            "benchmark_metrics": {
                "EM_mean": None,
                "CM_mean": None,
                "EX_mean": None,
                "VES_mean": None,
            },
            "benchmark_target_pass": {},
            "targets": {
                "execution_success_rate_gte": 0.9,
                "safety_pass_rate_eq": 1.0,
                "semantic_match_rate_gte": 0.8,
                "overall_weighted_score_gte": 0.85,
            },
            "target_pass": {
                "execution_success_rate": False,
                "safety_pass_rate": False,
                "semantic_match_rate": False,
                "overall_weighted_score": False,
            },
        }

    execution_success_rate = sum(1 for x in valid_cases if x.execution_success) / evaluated_total
    safety_pass_rate = sum(1 for x in valid_cases if x.safety_pass) / evaluated_total
    semantic_match_rate = sum(1 for x in valid_cases if x.semantic_score >= 0.8) / evaluated_total
    syntax_rate = sum(1 for x in valid_cases if x.syntax_pass) / evaluated_total
    performance_rate = sum(1 for x in valid_cases if x.performance_pass) / evaluated_total
    avg_semantic_score = sum(x.semantic_score for x in valid_cases) / evaluated_total

    overall_weighted_score = (
        0.35 * execution_success_rate
        + 0.25 * safety_pass_rate
        + 0.20 * performance_rate
        + 0.20 * avg_semantic_score
    )

    def _mean_optional(vals: list[float | None]) -> float | None:
        xs = [v for v in vals if v is not None]
        if not xs:
            return None
        return round(sum(xs) / len(xs), 4)

    em_mean = _mean_optional([x.em for x in valid_cases])
    cm_mean = _mean_optional([x.cm for x in valid_cases])
    ex_mean = _mean_optional([x.ex for x in valid_cases])
    ex_partial_mean = _mean_optional([x.ex_partial for x in valid_cases])
    ves_mean = _mean_optional([x.ves for x in valid_cases])

    has_ex = any(x.ex is not None for x in valid_cases)
    benchmark_target_pass: dict[str, bool] = {}
    if has_ex:
        benchmark_target_pass = {
            "EM_gte_0.8": (em_mean or 0) >= 0.8,
            "CM_gte_0.8": (cm_mean or 0) >= 0.8,
            "EX_gte_0.9": (ex_mean or 0) >= 0.9,
            "VES_gte_1.0": (ves_mean or 0) >= 1.0,
        }

    # Dashboard theo nhóm lỗi EX để theo dõi model quality theo intent.
    ex_cases = [x for x in valid_cases if x.ex is not None]
    ex_failed_cases = [x for x in ex_cases if x.ex == 0.0]
    ex_failure_groups: collections.Counter[str] = collections.Counter()
    missing_column_counter: collections.Counter[str] = collections.Counter()
    ex_failure_case_ids: dict[str, list[str]] = {
        "alias_only": [],
        "limit_mismatch": [],
        "semantic_mismatch": [],
    }
    for case in ex_failed_cases:
        bucket = classify_ex_failure(case)
        if bucket in ex_failure_case_ids:
            ex_failure_groups[bucket] += 1
            ex_failure_case_ids[bucket].append(case.sample_id)
        for col in case.execution_diff.get("missing_columns", []) or []:
            missing_column_counter[str(col)] += 1

    ex_failure_dashboard: dict[str, Any] = {}
    if has_ex:
        ex_fail_total = len(ex_failed_cases)
        ex_failure_dashboard = {
            "ex_failed_total": ex_fail_total,
            "by_group": {
                "alias_only": {
                    "count": ex_failure_groups.get("alias_only", 0),
                    "rate_over_ex_failed": round(
                        (ex_failure_groups.get("alias_only", 0) / ex_fail_total), 4
                    ) if ex_fail_total else 0.0,
                    "sample_ids": ex_failure_case_ids["alias_only"][:15],
                },
                "limit_mismatch": {
                    "count": ex_failure_groups.get("limit_mismatch", 0),
                    "rate_over_ex_failed": round(
                        (ex_failure_groups.get("limit_mismatch", 0) / ex_fail_total), 4
                    ) if ex_fail_total else 0.0,
                    "sample_ids": ex_failure_case_ids["limit_mismatch"][:15],
                },
                "semantic_mismatch": {
                    "count": ex_failure_groups.get("semantic_mismatch", 0),
                    "rate_over_ex_failed": round(
                        (ex_failure_groups.get("semantic_mismatch", 0) / ex_fail_total), 4
                    ) if ex_fail_total else 0.0,
                    "sample_ids": ex_failure_case_ids["semantic_mismatch"][:15],
                },
            },
            "top_missing_columns": [
                {"column": col, "count": cnt}
                for col, cnt in missing_column_counter.most_common(10)
            ],
        }

    return {
        "total_samples": evaluated_total,
        "total_input_samples": total,
        "evaluated_samples": evaluated_total,
        "skipped_samples": len(skipped_cases),
        "skipped_case_ids": [c.sample_id for c in skipped_cases],
        "execution_success_rate": round(execution_success_rate, 4),
        "safety_pass_rate": round(safety_pass_rate, 4),
        "semantic_match_rate": round(semantic_match_rate, 4),
        "syntax_pass_rate": round(syntax_rate, 4),
        "performance_pass_rate": round(performance_rate, 4),
        "average_semantic_score": round(avg_semantic_score, 4),
        "overall_weighted_score": round(overall_weighted_score, 4),
        "benchmark_metrics": {
            "EM_mean": em_mean,
            "CM_mean": cm_mean,
            "EX_mean": ex_mean,
            "EX_partial_mean": ex_partial_mean,
            "VES_mean": ves_mean,
        },
        "ex_failure_dashboard": ex_failure_dashboard,
        "benchmark_target_pass": benchmark_target_pass,
        "targets": {
            "execution_success_rate_gte": 0.9,
            "safety_pass_rate_eq": 1.0,
            "semantic_match_rate_gte": 0.8,
            "overall_weighted_score_gte": 0.85,
        },
        "target_pass": {
            "execution_success_rate": execution_success_rate >= 0.9,
            "safety_pass_rate": abs(safety_pass_rate - 1.0) < 1e-9,
            "semantic_match_rate": semantic_match_rate >= 0.8,
            "overall_weighted_score": overall_weighted_score >= 0.85,
        },
    }


def to_json_report(
    *,
    dataset_path: str,
    generator_mode: str,
    api_url: str,
    case_results: list[CaseResult],
    summary: dict[str, Any],
) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset_path": dataset_path,
        "generator_mode": generator_mode,
        "api_url": api_url if generator_mode == "api" else None,
        "summary": summary,
        "cases": [
            {
                "id": c.sample_id,
                "question": c.question,
                "category": c.category,
                "difficulty": c.difficulty,
                "generated_sql": c.generated_sql,
                "gold_sql": c.gold_sql,
                "scores": {
                    "SyntaxPass": c.syntax_pass,
                    "SafetyPass": c.safety_pass,
                    "PerformancePass": c.performance_pass,
                    "SemanticScore": c.semantic_score,
                    "EM": c.em,
                    "CM": c.cm,
                    **({"CM_detail": c.cm_detail} if c.cm_detail else {}),
                    **({"EX": c.ex} if c.ex is not None else {}),
                    **({"EX_partial": c.ex_partial} if c.ex_partial is not None else {}),
                    **({"VES": c.ves} if c.ves is not None else {}),
                },
                "execution_success": c.execution_success,
                "errors": c.errors,
                **({"execution_diff": c.execution_diff} if c.execution_diff else {}),
            }
            for c in case_results
        ],
    }


def to_markdown_report(report_json: dict[str, Any]) -> str:
    summary = report_json["summary"]
    lines: list[str] = []
    lines.append("# SQL Evaluation Report")
    lines.append("")
    lines.append(f"- GeneratedAt: {report_json['generated_at']}")
    lines.append(f"- Dataset: `{report_json['dataset_path']}`")
    lines.append(f"- GeneratorMode: `{report_json['generator_mode']}`")
    if report_json.get("api_url"):
        lines.append(f"- API URL: `{report_json['api_url']}`")
    lines.append("")
    lines.append("## Summary Metrics")
    lines.append("")
    lines.append(
        f"- EvaluatedSamples: **{summary.get('evaluated_samples', summary['total_samples'])}** "
        f"/ InputSamples: **{summary.get('total_input_samples', summary['total_samples'])}**"
    )
    if summary.get("skipped_samples", 0) > 0:
        lines.append(f"- SkippedSamples: **{summary['skipped_samples']}** (cases with errors)")
    lines.append(f"- ExecutionSuccessRate: **{summary['execution_success_rate']:.2%}**")
    lines.append(f"- SafetyPassRate: **{summary['safety_pass_rate']:.2%}**")
    lines.append(f"- SemanticMatchRate: **{summary['semantic_match_rate']:.2%}**")
    lines.append(f"- OverallWeightedScore: **{summary['overall_weighted_score']:.2%}**")
    lines.append("")
    bm = summary.get("benchmark_metrics") or {}
    if any(bm.get(k) is not None for k in ("EM_mean", "CM_mean", "EX_mean", "VES_mean")):
        lines.append("## Benchmark metrics (Spider / BIRD style)")
        lines.append("")
        lines.append("> **Giải thích metrics:**")
        lines.append("> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).")
        lines.append("> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.")
        lines.append("> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).")
        lines.append("> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).")
        lines.append("> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).")
        lines.append("")
        for key, label in (
            ("EM_mean", "Exact Match (EM) mean"),
            ("CM_mean", "Component Match (CM) mean"),
            ("EX_mean", "Execution Accuracy (EX) mean"),
            ("EX_partial_mean", "Partial Execution / F1 (EX_partial) mean"),
            ("VES_mean", "Valid Efficiency Score (VES) mean [cap=1.0]"),
        ):
            v = bm.get(key)
            lines.append(f"- {label}: **{v if v is not None else 'N/A'}**")
        btp = summary.get("benchmark_target_pass") or {}
        if btp:
            lines.append("")
            for name, passed in btp.items():
                lines.append(f"- {name}: **{'PASS' if passed else 'FAIL'}**")
        lines.append("")

    ex_dash = summary.get("ex_failure_dashboard") or {}
    if ex_dash:
        lines.append("## EX Failure Dashboard")
        lines.append("")
        lines.append(f"- EX failed total: **{ex_dash.get('ex_failed_total', 0)}**")
        by_group = ex_dash.get("by_group") or {}
        for key, label in (
            ("alias_only", "Alias-only mismatch"),
            ("limit_mismatch", "LIMIT/TOP-N mismatch"),
            ("semantic_mismatch", "Semantic mismatch"),
        ):
            item = by_group.get(key) or {}
            lines.append(
                f"- {label}: **{item.get('count', 0)}** "
                f"(rate: {item.get('rate_over_ex_failed', 0):.2%})"
            )
            ids = item.get("sample_ids") or []
            if ids:
                lines.append(f"  - Sample IDs: `{', '.join(ids[:10])}`")
        top_missing = ex_dash.get("top_missing_columns") or []
        if top_missing:
            lines.append("- Top missing columns:")
            for row in top_missing:
                lines.append(f"  - `{row['column']}`: `{row['count']}`")
        lines.append("")
    lines.append("## Target Check")
    lines.append("")
    target_pass = summary.get("target_pass") or {}
    if not target_pass:
        lines.append("- *(Không có dữ liệu target_pass trong summary.)*")
    else:
        for target_name, passed in target_pass.items():
            status = "PASS" if passed else "FAIL"
            lines.append(f"- {target_name}: **{status}**")
    lines.append("")
    lines.append("## Case Details")
    lines.append("")
    for case in report_json["cases"]:
        scores = case["scores"]
        lines.append(f"### {case['id']}")
        lines.append(f"- Category: `{case['category']}` | Difficulty: `{case['difficulty']}`")
        lines.append(f"- SyntaxPass: `{scores['SyntaxPass']}`")
        lines.append(f"- SafetyPass: `{scores['SafetyPass']}`")
        lines.append(f"- PerformancePass: `{scores['PerformancePass']}`")
        lines.append(f"- SemanticScore: `{scores['SemanticScore']}`")
        if scores.get("EM") is not None:
            lines.append(f"- EM: `{scores['EM']}`")
        if scores.get("CM") is not None:
            lines.append(f"- CM: `{scores['CM']}`")
        if scores.get("EX") is not None:
            lines.append(f"- EX (strict): `{scores['EX']}`")
        if scores.get("EX_partial") is not None:
            lines.append(f"- EX_partial (F1): `{scores['EX_partial']}`")
        if scores.get("VES") is not None:
            lines.append(f"- VES: `{scores['VES']}`")
        lines.append(f"- ExecutionSuccess: `{case['execution_success']}`")
        if case["errors"]:
            lines.append(f"- Errors: `{'; '.join(case['errors'])}`")
        else:
            lines.append("- Errors: `none`")
        # --- Detailed diff report khi EX thất bại ---
        diff = case.get("execution_diff") or {}
        if diff:
            lines.append("- **EX Diff Analysis:**")
            if diff.get("column_mismatch"):
                lines.append(f"  - ⚠️ Cột không khớp — generated: `{diff.get('generated_columns')}` vs gold: `{diff.get('gold_columns')}`")
            if diff.get("missing_columns"):
                lines.append(f"  - ❌ Thiếu cột: `{diff['missing_columns']}`")
            if diff.get("extra_columns"):
                lines.append(f"  - ➕ Thừa cột: `{diff['extra_columns']}`")
            if diff.get("row_count_generated") is not None:
                lines.append(
                    f"  - Số dòng: generated=`{diff['row_count_generated']}` | "
                    f"gold=`{diff['row_count_gold']}` | "
                    f"matched=`{diff['rows_matched']}` | "
                    f"missing=`{diff['rows_missing_in_gen']}` | "
                    f"extra=`{diff['rows_extra_in_gen']}`"
                )
            if diff.get("sample_unmatched_gold_rows"):
                lines.append("  - Sample dòng gold không khớp (tối đa 3):")
                for row in diff["sample_unmatched_gold_rows"]:
                    lines.append(f"    - `{row}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


async def run(args: argparse.Namespace) -> None:
    dataset_path = Path(args.dataset).resolve()
    # Tự động tạo subfolder timestamp bên trong --output-dir
    # Ví dụ: evaluation/reports/20260425_223000/
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir).resolve() / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    samples = load_dataset(dataset_path)
    if args.max_samples > 0:
        samples = samples[: args.max_samples]
    executor = DatabricksSQLExecutor()
    case_results: list[CaseResult] = []
    min_request_interval_sec = max(0.0, args.min_request_interval_sec)
    effective_interval_sec = min_request_interval_sec * max(1, args.estimated_llm_calls_per_sample)
    last_generation_started_at = 0.0
    for sample in samples:
        if effective_interval_sec > 0 and last_generation_started_at > 0:
            elapsed = time.monotonic() - last_generation_started_at
            if elapsed < effective_interval_sec:
                wait_sec = effective_interval_sec - elapsed
                print(f"[INFO] Rate limit pacing: sleep {wait_sec:.2f}s before next sample...")
                await asyncio.sleep(wait_sec)
        last_generation_started_at = time.monotonic()
        result = await evaluate_one(
            sample=sample,
            generator_mode=args.generator,
            api_url=args.api_url,
            timeout_sec=args.timeout_sec,
            executor=executor,
            generation_max_attempts=args.generation_max_attempts,
        )
        case_results.append(result)

    summary = build_summary(case_results)
    report_json = to_json_report(
        dataset_path=str(dataset_path),
        generator_mode=args.generator,
        api_url=args.api_url,
        case_results=case_results,
        summary=summary,
    )
    report_md = to_markdown_report(report_json)

    json_path = output_dir / "eval_report.json"
    md_path = output_dir / "eval_report.md"
    json_path.write_text(json.dumps(report_json, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(report_md, encoding="utf-8")
    print(f"[OK] Report dir : {output_dir}")
    print(f"[OK] Wrote JSON : {json_path}")
    print(f"[OK] Wrote MD   : {md_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SQL Accuracy Evaluation Runner")
    parser.add_argument(
        "--dataset",
        default="evaluation/eval_dataset.json",
        help="Path to eval_dataset.json",
    )
    parser.add_argument(
        "--output-dir",
        default="evaluation/reports",
        help="Output directory for eval_report.json and eval_report.md",
    )
    parser.add_argument(
        "--generator",
        choices=["sql_only", "process_question", "api"],
        default="sql_only",
        help="SQL generation mode",
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000/api/v1/chat/query",
        help="API endpoint used when --generator api",
    )
    parser.add_argument("--timeout-sec", type=float, default=60.0, help="HTTP timeout for API mode")
    parser.add_argument(
        "--min-request-interval-sec",
        type=float,
        default=4.2,
        help="Minimum seconds between sample generations.",
    )
    parser.add_argument(
        "--generation-max-attempts",
        type=int,
        default=5,
        help="Max attempts to generate SQL per sample when transient errors occur (e.g. 429).",
    )
    parser.add_argument(
        "--estimated-llm-calls-per-sample",
        type=int,
        default=1,
        help="Estimated LLM calls per question. sql_only usually 1.",
    )
    parser.add_argument(
        "--max-samples",
        type=int,
        default=0,
        help="Limit number of samples to evaluate. 0 means run all.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    asyncio.run(run(parse_args()))
