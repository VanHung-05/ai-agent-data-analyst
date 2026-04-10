"""
agent_service.py — Multi-Agent Orchestrator
=============================================
📌 FILE NÀY LÀ CỦA TV2 (AI/ML Engineer)

Kiến trúc Multi-Agent:
  1. Router Agent    → Phân loại intent (conversation / sql / visualize)
  2. Conversation Agent → Xử lý chào hỏi, giải thích lỗi
  3. SQL Agent       → Sinh SQL + thực thi trên Databricks (logic có sẵn)
  4. Visualize Agent → Đề xuất chart spec sau khi có data
  5. NLG Agent      → LLM diễn giải rows thành câu trả lời tự nhiên (`answer`)

Luồng xử lý:
  User question → Router → [Conversation | SQL → Visualize → NLG] → Response
"""

import asyncio
import concurrent.futures
import os
import re
import threading
from typing import Any, Awaitable, Callable, TypedDict

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langgraph.graph import END, StateGraph

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import databricks_config, app_config
from services.conversation_agent import conversation_response
from services.llm_service import get_llm
from services.query_result_parser import parse_query_result
from services.router_agent import route_detail
from services.nlg_agent import generate_natural_language_answer
from services.visualize_agent import recommend_chart
from utils.sql_validator import validate_sql, sanitize_sql
from utils.logger import logger


# ====== SINGLETON ======
_db_instance: SQLDatabase | None = None
_db_lock = threading.Lock()
_workflow = None
_workflow_lock = threading.Lock()


def get_database() -> SQLDatabase:
    """Khởi tạo kết nối SQLDatabase tới Databricks (Singleton, thread-safe)."""
    global _db_instance
    if _db_instance is not None:
        return _db_instance
    with _db_lock:
        if _db_instance is None:
            has_token = bool(databricks_config.token)
            has_sp = bool(databricks_config.client_id and databricks_config.client_secret)
            if not databricks_config.host or (not has_token and not has_sp):
                raise ConnectionError(
                    "Thiếu thông tin kết nối Databricks! "
                    "Cần DATABRICKS_HOST + (TOKEN hoặc CLIENT_ID/CLIENT_SECRET) trong .env"
                )
            uri = databricks_config.sqlalchemy_uri
            _db_instance = SQLDatabase.from_uri(uri)
            logger.info("Đã kết nối Databricks: %s | Tables: %s",
                        databricks_config.host, _db_instance.get_usable_table_names())
    return _db_instance


def get_schema_info() -> dict:
    """Lấy thông tin Schema từ Databricks (phục vụ API /schema)."""
    db = get_database()
    return {
        "catalog": databricks_config.catalog,
        "schema": databricks_config.schema,
        "tables": db.get_usable_table_names(),
        "table_info": db.get_table_info(),
    }


def _load_system_prompt() -> str:
    """Đọc system prompt từ file prompts/system_prompt.txt."""
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "prompts", "system_prompt.txt",
    )
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("system_prompt.txt not found, using default.")
        return "You are a helpful SQL assistant. Generate valid Spark SQL queries."


# ====== ASYNC HELPER ======
async def _run_in_executor(func: Any, *args: Any) -> Any:
    """Chạy hàm blocking trong thread pool."""
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, lambda: func(*args))


async def _emit_progress(
    progress_hook: Callable[[str, str], Awaitable[None] | None] | None,
    step: str,
    message: str,
) -> None:
    """Phát progress event (nếu có hook)."""
    if progress_hook is None:
        return
    try:
        maybe = progress_hook(step, message)
        if asyncio.iscoroutine(maybe):
            await maybe
    except Exception:
        # Không để lỗi progress làm hỏng luồng xử lý chính
        return


def _create_sql_query_chain(llm: Any, db: SQLDatabase) -> Any:
    """create_sql_query_chain(llm, db, 100) SAI: tham số thứ 3 là prompt, không phải k."""
    return create_sql_query_chain(llm, db, k=100)


def _extract_select_aliases(sql: str) -> list[str]:
    """
    Trích tên cột từ SELECT list để thay `col_0`, `col_1` thành tên có nghĩa.
    Ưu tiên alias sau AS; nếu không có thì lấy token cuối của expression.
    """
    m = re.search(r"\bselect\b(.*?)\bfrom\b", sql, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return []

    select_part = m.group(1).strip()
    if not select_part:
        return []

    # Tách theo dấu phẩy ở level ngoài cùng (không tách trong hàm)
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    for ch in select_part:
        if ch == "(":
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
        if ch == "," and depth == 0:
            expr = "".join(buf).strip()
            if expr:
                parts.append(expr)
            buf = []
            continue
        buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        parts.append(tail)

    aliases: list[str] = []
    for expr in parts:
        expr_clean = expr.strip()
        # Bỏ modifier DISTINCT ở đầu expression
        expr_clean = re.sub(r"^\s*distinct\s+", "", expr_clean, flags=re.IGNORECASE)

        as_match = re.search(r"\bas\s+([`\"\[]?[A-Za-z_][\w$]*[`\"\]]?)\s*$", expr_clean, flags=re.IGNORECASE)
        if as_match:
            name = as_match.group(1).strip("`\"[]")
            aliases.append(name)
            continue

        token_match = re.search(r"([A-Za-z_][\w$]*)\s*$", expr_clean)
        if token_match:
            aliases.append(token_match.group(1))
        else:
            aliases.append(f"col_{len(aliases)}")
    return aliases


def _rename_parsed_columns(data: list[dict[str, Any]], sql: str) -> list[dict[str, Any]]:
    """Đổi `col_i` -> tên cột từ SELECT aliases nếu khớp số lượng cột."""
    if not data:
        return data

    first_keys = list(data[0].keys())
    if not first_keys or not all(k.startswith("col_") for k in first_keys):
        return data

    aliases = _extract_select_aliases(sql)
    if len(aliases) != len(first_keys):
        return data

    renamed: list[dict[str, Any]] = []
    for row in data:
        new_row: dict[str, Any] = {}
        for idx, old_key in enumerate(first_keys):
            new_row[aliases[idx]] = row.get(old_key)
        renamed.append(new_row)
    return renamed


class WorkflowState(TypedDict, total=False):
    """State dùng cho LangGraph workflow."""

    question: str
    max_retries: int
    llm: Any
    progress_hook: Callable[[str, str], Awaitable[None] | None] | None
    route: str
    result: dict[str, Any]


async def _node_router(state: WorkflowState) -> WorkflowState:
    """Node Router: phân loại intent và cập nhật routing_info."""
    question = state["question"]
    llm = state["llm"]
    result = state["result"]
    progress_hook = state.get("progress_hook")

    await _emit_progress(progress_hook, "router", "Router Agent phân loại intent...")
    routing = await _run_in_executor(route_detail, question, llm)
    route = routing["intent"]
    result["routing_info"] = routing
    result["current_agent"] = route
    return {"route": route, "result": result}


async def _node_conversation(state: WorkflowState) -> WorkflowState:
    """Node Conversation: trả lời hội thoại, không truy vấn DB."""
    question = state["question"]
    llm = state["llm"]
    result = state["result"]
    progress_hook = state.get("progress_hook")

    await _emit_progress(progress_hook, "conversation", "Conversation Agent đang phản hồi...")
    message = await _run_in_executor(conversation_response, question, None, llm)
    result["answer"] = message
    result["data"] = [{"assistant_response": message}]
    result["row_count"] = 1
    result["visualization_recommendation"] = {
        "chart_type": "conversation",
        "reason": "Routed to Conversation Agent",
    }
    result["error"] = None
    await _emit_progress(progress_hook, "done", "Hoàn tất.")
    return {"result": result}


async def _node_sql_pipeline(state: WorkflowState) -> WorkflowState:
    """Node SQL pipeline: SQL -> Execute -> Visualize -> NLG."""
    question = state["question"]
    llm = state["llm"]
    max_retries = state["max_retries"]
    result = state["result"]
    route = state.get("route", "sql")
    progress_hook = state.get("progress_hook")

    try:
        await _emit_progress(progress_hook, "db_connect", "Kết nối Databricks...")
        db = await _run_in_executor(get_database)
    except Exception as e:
        result["error"] = f"Lỗi kết nối Databricks: {str(e)}"
        result["answer"] = await _run_in_executor(conversation_response, question, str(e), llm)
        result["current_agent"] = "conversation"
        logger.exception("Database connection error")
        return {"result": result}

    system_prompt = await _run_in_executor(_load_system_prompt)
    retries = 0
    last_error_str = ""

    while retries < max_retries:
        try:
            await _emit_progress(progress_hook, "sql_generate", f"Sinh SQL (lần {retries + 1}/{max_retries})...")
            if retries == 0:
                prompt_input = {
                    "question": f"{system_prompt}\n\nUser Question: {question}"
                }
            else:
                prompt_input = {
                    "question": (
                        f"{system_prompt}\n\n"
                        f"Câu hỏi gốc: {question}\n"
                        f"LỖI TRƯỚC ĐÓ: {last_error_str}\n"
                        f"Hãy viết lại SQL Spark chính xác hơn. Chỉ xuất SQL, không giải thích."
                    )
                }

            write_query = await _run_in_executor(_create_sql_query_chain, llm, db)
            raw_sql = await _run_in_executor(write_query.invoke, prompt_input)
            generated_sql = _clean_sql_output(raw_sql)

            is_valid, error_msg = validate_sql(generated_sql)
            if not is_valid:
                raise ValueError(f"SQL bị chặn: {error_msg}")

            generated_sql = sanitize_sql(generated_sql)
            result["generated_sql"] = generated_sql

            await _emit_progress(progress_hook, "sql_execute", "Thực thi truy vấn SQL...")
            execute_tool = QuerySQLDataBaseTool(db=db)
            raw_result = await _run_in_executor(execute_tool.invoke, generated_sql)

            result["data"] = parse_query_result(raw_result)
            result["data"] = _rename_parsed_columns(result["data"], generated_sql)
            result["row_count"] = len(result["data"])

            await _emit_progress(progress_hook, "visualize", "Đề xuất trực quan hóa dữ liệu...")
            chart_rec = await _run_in_executor(
                recommend_chart, question, generated_sql, result["data"], llm
            )
            chart_rec["routed_agent"] = route
            result["visualization_recommendation"] = chart_rec

            await _emit_progress(progress_hook, "nlg", "Tạo câu trả lời tự nhiên...")
            result["answer"] = await _run_in_executor(
                generate_natural_language_answer, question, result["data"], llm
            )
            result["error"] = None

            if retries > 0:
                logger.info("Retry lần %s thành công", retries)
            await _emit_progress(progress_hook, "done", "Hoàn tất.")
            return {"result": result}

        except Exception as e:
            retries += 1
            last_error_str = str(e)
            logger.warning("Lỗi SQL (thử %s/%s): %s", retries, max_retries, last_error_str)

            if retries >= max_retries:
                await _emit_progress(progress_hook, "fallback", "SQL thất bại, chuyển sang Conversation Agent...")
                fallback_msg = await _run_in_executor(
                    conversation_response, question, last_error_str, llm
                )
                result["error"] = f"Thất bại sau {max_retries} lần: {last_error_str}"
                result["answer"] = fallback_msg
                result["current_agent"] = "conversation"
                result["visualization_recommendation"] = {
                    "chart_type": "conversation",
                    "reason": "SQL failed, fallback to Conversation Agent",
                }
                return {"result": result}

            await asyncio.sleep(1)

    return {"result": result}


def _next_after_router(state: WorkflowState) -> str:
    """Router edge: chọn node tiếp theo theo intent."""
    route = state.get("route", "conversation")
    return "conversation" if route == "conversation" else "sql_pipeline"


def _get_workflow():
    """Khởi tạo LangGraph workflow một lần (singleton)."""
    global _workflow
    if _workflow is not None:
        return _workflow

    with _workflow_lock:
        if _workflow is None:
            workflow = StateGraph(WorkflowState)
            workflow.add_node("router", _node_router)
            workflow.add_node("conversation", _node_conversation)
            workflow.add_node("sql_pipeline", _node_sql_pipeline)
            workflow.set_entry_point("router")
            workflow.add_conditional_edges(
                "router",
                _next_after_router,
                {
                    "conversation": "conversation",
                    "sql_pipeline": "sql_pipeline",
                },
            )
            workflow.add_edge("conversation", END)
            workflow.add_edge("sql_pipeline", END)
            _workflow = workflow.compile()

    return _workflow


# ====== MAIN ORCHESTRATOR ======
async def process_question(
    question: str,
    max_retries: int = 3,
    progress_hook: Callable[[str, str], Awaitable[None] | None] | None = None,
) -> dict[str, Any]:
    """
    Hàm chính: điều phối Multi-Agent pipeline.

    Response format (cho Frontend):
        {
            "question": str,
            "current_agent": "conversation" | "sql" | "visualize",
            "routing_info": { "intent", "scores", "selected_agents", "routing_method" },
            "answer": str,              # NLG: câu trả lời tự nhiên từ LLM (không phải raw rows)
            "generated_sql": str | None,
            "data": list[dict],
            "row_count": int,
            "visualization_recommendation": dict,
            "error": str | None
        }
    """
    result: dict[str, Any] = {
        "question": question,
        "current_agent": "conversation",
        "routing_info": {},
        "answer": "",
        "generated_sql": None,
        "data": [],
        "row_count": 0,
        "visualization_recommendation": {"chart_type": "table"},
        "error": None,
    }

    # ── Bước 1: Khởi tạo LLM ──
    try:
        await _emit_progress(progress_hook, "llm_init", "Khởi tạo LLM...")
        llm = await _run_in_executor(get_llm)
    except Exception as e:
        result["error"] = f"Lỗi khởi tạo LLM: {str(e)}"
        result["answer"] = "Hệ thống đang gặp sự cố kết nối LLM. Vui lòng thử lại sau."
        logger.exception("LLM init error")
        return result

    workflow = _get_workflow()
    final_state = await workflow.ainvoke(
        {
            "question": question,
            "max_retries": max_retries,
            "llm": llm,
            "progress_hook": progress_hook,
            "result": result,
            "route": "conversation",
        }
    )
    return final_state.get("result", result)


def _clean_sql_output(sql: str) -> str:
    """Làm sạch SQL output từ LLM (markdown, prefix, trailing comments)."""
    sql = sql.strip()

    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.startswith("```"):
        sql = sql[3:]
    if sql.endswith("```"):
        sql = sql[:-3]

    sql = re.sub(r'^(?:SQL\s*Query\s*:\s*|SQLQuery\s*:\s*)', '', sql, flags=re.IGNORECASE)

    for stop in ['SQLResult:', 'SQL Result:', 'Answer:', 'Explanation:']:
        idx = sql.find(stop)
        if idx > 0:
            sql = sql[:idx]

    sql = re.sub(r'--[^\n]*', '', sql)
    return sql.strip().rstrip(';')


# ====== QUICK TEST ======
async def interactive_test() -> None:
    print("=" * 60)
    print("AI Agent — Smart Data Analyst | INTERACTIVE MODE")
    print("=" * 60)

    try:
        schema = get_schema_info()
        print(f"Đã kết nối. Tables: {schema['tables']}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        return

    print("Nhập câu hỏi (Ctrl+C để thoát):")
    while True:
        try:
            user_input = input("\n> ")
            if not user_input.strip():
                continue
            resp = await process_question(user_input)
            print(f"[Agent: {resp['current_agent']}]")
            print(f"Answer: {resp['answer']}")
            if resp.get("generated_sql"):
                print(f"SQL: {resp['generated_sql']}")
            if resp.get("error"):
                print(f"Error: {resp['error']}")
            chart = resp["visualization_recommendation"]
            print(f"Chart: {chart.get('chart_type')} | Reason: {chart.get('reason')}")
        except (KeyboardInterrupt, EOFError):
            print("\nThoát.")
            break


if __name__ == "__main__":
    asyncio.run(interactive_test())
