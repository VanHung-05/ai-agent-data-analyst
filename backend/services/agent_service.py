"""
🧠 agent_service.py — LangChain SQL Agent Pipeline
=====================================================
📌 FILE NÀY LÀ CỦA TV2 (AI/ML Engineer) — FILE QUAN TRỌNG NHẤT!

Chức năng:
  - Kết nối với Databricks qua SQLDatabase (LangChain wrapper)
  - Nhận câu hỏi ngôn ngữ tự nhiên → Sinh SQL → Thực thi → Trả kết quả
  - Xử lý Self-correction nếu SQL bị lỗi

Luồng xử lý:
  User question (NL) → System Prompt + Schema → LLM → SQL → Execute → Data
"""

import os
from typing import Any

from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

# Import các module nội bộ
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import databricks_config, app_config
from services.llm_service import get_llm
from utils.sql_validator import validate_sql, sanitize_sql


# ====== BIẾN TOÀN CỤC (Singleton Pattern) ======
_db_instance = None
_agent_chain = None


def get_database() -> SQLDatabase:
    """
    Khởi tạo kết nối SQLDatabase tới Databricks (Singleton)

    💡 TV2 NOTE:
      - Hàm này dùng credentials từ TV1 (trong .env) để kết nối
      - SQLDatabase tự động đọc toàn bộ schema/metadata từ Databricks
      - Chỉ khởi tạo 1 lần, sau đó cache lại để tái sử dụng

    Returns:
        SQLDatabase: Instance kết nối database
    """
    global _db_instance
    if _db_instance is None:
        # Kiểm tra có đủ credentials để kết nối không
        has_token = bool(databricks_config.token)
        has_sp = bool(databricks_config.client_id and databricks_config.client_secret)
        if not databricks_config.host or (not has_token and not has_sp):
            raise ConnectionError(
                "❌ Thiếu thông tin kết nối Databricks! "
                "Cần DATABRICKS_HOST + (TOKEN hoặc CLIENT_ID/CLIENT_SECRET) trong .env"
            )

        uri = databricks_config.sqlalchemy_uri
        _db_instance = SQLDatabase.from_uri(uri)
        print(f"✅ Đã kết nối Databricks: {databricks_config.host}")
        print(f"   Catalog: {databricks_config.catalog}")
        print(f"   Schema: {databricks_config.schema}")
        print(f"   Tables: {_db_instance.get_usable_table_names()}")

    return _db_instance


def get_schema_info() -> dict:
    """
    Lấy thông tin Schema từ Databricks (phục vụ API /schema cho TV3)

    Returns:
        dict: {
            "catalog": str,
            "schema": str,
            "tables": list[str],
            "table_info": str  # DDL + sample rows
        }
    """
    db = get_database()
    return {
        "catalog": databricks_config.catalog,
        "schema": databricks_config.schema,
        "tables": db.get_usable_table_names(),
        "table_info": db.get_table_info(),
    }


def _load_system_prompt() -> str:
    """
    Đọc system prompt từ file prompts/system_prompt.txt

    💡 TV2 NOTE:
      - Đây là nơi bạn định nghĩa "tính cách" và "quy tắc" cho AI
      - File system_prompt.txt chứa các hướng dẫn cho LLM
    """
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "prompts",
        "system_prompt.txt",
    )
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("⚠️ Không tìm thấy system_prompt.txt, dùng prompt mặc định.")
        return "You are a helpful SQL assistant. Generate valid Spark SQL queries."


async def process_question(question: str, max_retries: int = 3) -> dict[str, Any]:
    """
    🌟 HÀM CHÍNH (BẤT ĐỒNG BỘ) — Xử lý câu hỏi từ người dùng với Retry Loop linh hoạt

    Pipeline:
      1. Nhận câu hỏi
      2. Chạy Async Executor để sinh SQL
      3. Validate SQL an toàn
      4. Thực thi Databricks lấy data
      5. Nếu lỗi → Retry Loop (tối đa max_retries lần)
    """
    import asyncio
    import concurrent.futures

    async def run_in_executor(func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, lambda: func(*args, **kwargs))

    result = {
        "question": question,
        "generated_sql": None,
        "data": [],
        "row_count": 0,
        "visualization_recommendation": {"chart_type": "table"},
        "error": None,
    }

    try:
        db = await run_in_executor(get_database)
        llm = await run_in_executor(get_llm)
    except Exception as e:
        result["error"] = f"🚫 Lỗi khởi tạo kết nối: {str(e)}"
        return result

    # Load System Prompt từ file
    system_prompt_content = await run_in_executor(_load_system_prompt)

    retries = 0
    last_error_str = ""
    
    while retries < max_retries:
        try:
            # Tạo prompt kết hợp: System Prompt + Câu hỏi của người dùng
            if retries == 0:
                # Lần đầu: Nhúng nội dung system_prompt.txt vào câu hỏi
                prompt_input = {
                    "question": f"{system_prompt_content}\n\nUser Question: {question}"
                }
            else:
                # Các lần sau (Self-Correction): Nhúng thêm thông tin lỗi trước đó
                prompt_input = {
                    "question": (
                        f"{system_prompt_content}\n\n"
                        f"Câu hỏi gốc của người dùng: {question}\n"
                        f"❌ LỖI PHÁT SINH TRƯỚC ĐÓ: {last_error_str}\n"
                        f"HÀNH ĐỘNG CẦN LÀM: Hãy phân tích kỹ lỗi trên và viết lại câu lệnh SQL Spark chính xác hơn. "
                        f"Chỉ xuất SQL nguyên bản, không giải thích."
                    )
                }

            # Sinh SQL: Chain này sẽ tự động nhồi schema từ `db` vào prompt phía sau
            write_query = await run_in_executor(create_sql_query_chain, llm, db, k=100)
            raw_sql = await run_in_executor(write_query.invoke, prompt_input)
            generated_sql = await run_in_executor(_clean_sql_output, raw_sql)

            # Validate an toàn
            is_valid, error_msg = await run_in_executor(validate_sql, generated_sql)
            if not is_valid:
                raise ValueError(f"Câu lệnh DML bị chặn: {error_msg}")

            generated_sql = await run_in_executor(sanitize_sql, generated_sql)
            result["generated_sql"] = generated_sql

            # Thực thi
            execute_query = QuerySQLDataBaseTool(db=db)
            raw_result = await run_in_executor(execute_query.invoke, generated_sql)

            # Parse dữ liệu
            result["data"] = await run_in_executor(_parse_query_result, raw_result)
            result["row_count"] = len(result["data"])
            result["visualization_recommendation"] = await run_in_executor(
                _recommend_chart, question, generated_sql, result["data"]
            )
            result["error"] = None
            
            if retries > 0:
                print(f"✅ Retry lần {retries} thành công!")
            
            return result

        except Exception as e:
            retries += 1
            last_error_str = str(e)
            print(f"❌ Lỗi (thử lại {retries}/{max_retries}): {last_error_str}")
            if retries == max_retries:
                result["error"] = f"Thất bại sau {max_retries} lần thử: {last_error_str}"
                return result
            await asyncio.sleep(1) # Nghỉ 1 giây trước khi retry

    return result


def _clean_sql_output(sql: str) -> str:
    """
    Làm sạch SQL output từ LLM

    💡 TV2 NOTE:
      - LLM đôi khi trả SQL kèm markdown (```sql ... ```)
      - LangChain create_sql_query_chain yêu cầu trả dạng "SQLQuery: SELECT..."
      - Gemini 2.5 hay trả thêm SQLResult: và Answer: phía sau
      - Hàm này strip hết, chỉ giữ lại SQL thuần
    """
    import re
    sql = sql.strip()

    # Loại bỏ markdown code block
    if sql.startswith("```sql"):
        sql = sql[6:]
    if sql.startswith("```"):
        sql = sql[3:]
    if sql.endswith("```"):
        sql = sql[:-3]

    # Loại bỏ prefix "SQLQuery:" mà LangChain chain yêu cầu LLM output
    sql = re.sub(r'^(?:SQL\s*Query\s*:\s*|SQLQuery\s*:\s*)', '', sql, flags=re.IGNORECASE)

    # Cắt bỏ phần SAU SQL: SQLResult, Answer (Gemini hay trả thêm)
    for stop_word in ['SQLResult:', 'SQL Result:', 'Answer:', 'Explanation:']:
        idx = sql.find(stop_word)
        if idx > 0:
            sql = sql[:idx]

    # Loại bỏ SQL comment (-- ...) vì Gemini hay thêm comment giải thích
    sql = re.sub(r'--[^\n]*', '', sql)

    return sql.strip().rstrip(';')





def _parse_query_result(raw_result: str) -> list[dict]:
    """
    Parse kết quả raw từ Databricks thành list[dict] chuẩn JSON cho TV4 (Frontend)

    QuerySQLDataBaseTool trả về string dạng:
      "[(val1, val2), (val3, val4)]" hoặc "val1"
    Hàm này sẽ phân tích thành danh sách dictionary.
    """
    import ast
    import re

    if not raw_result or raw_result.strip() == "":
        return []

    raw = raw_result.strip()

    # --- Case 1: Kết quả dạng list of tuples ---
    # VD: "[(1, 'Alice', 100), (2, 'Bob', 200)]"
    try:
        parsed = ast.literal_eval(raw)
        if isinstance(parsed, list):
            if len(parsed) == 0:
                return []
            # Nếu mỗi phần tử là tuple/list → sinh key col_0, col_1...
            if isinstance(parsed[0], (tuple, list)):
                return [
                    {f"col_{i}": val for i, val in enumerate(row)}
                    for row in parsed
                ]
            # Nếu mỗi phần tử là dict → trả thẳng
            if isinstance(parsed[0], dict):
                return parsed
            # Nếu là list đơn giá trị → [{'value': x}, ...]
            return [{"value": item} for item in parsed]
    except (ValueError, SyntaxError):
        pass

    # --- Case 2: Kết quả dạng bảng text có header ---
    # VD: "col1\tcol2\nval1\tval2"
    lines = raw.split("\n")
    if len(lines) >= 2 and ("\t" in lines[0] or "|" in lines[0]):
        sep = "\t" if "\t" in lines[0] else "|"
        headers = [h.strip() for h in lines[0].split(sep) if h.strip()]
        rows = []
        for line in lines[1:]:
            vals = [v.strip() for v in line.split(sep) if v.strip()]
            if len(vals) == len(headers):
                rows.append(dict(zip(headers, vals)))
        if rows:
            return rows

    # --- Case 3: Kết quả đơn giá trị ---
    # VD: "42" hoặc "753.00"
    return [{"result": raw}]


def _recommend_chart(question: str, sql: str, data: list[dict]) -> dict:
    """
    Gợi ý loại biểu đồ phù hợp dựa trên:
    1. Ý định của câu hỏi (question)
    2. Cấu trúc SQL (sql)
    3. Dữ liệu thực tế trả về (data)

    💡 TV2 NOTE:
      - 1x1 data (COUNT, SUM) -> 'metric'
      - Time-based data -> 'line'
      - Distribution/Ratio -> 'pie'
      - Comparison -> 'bar'
    """
    if not data:
        return {"chart_type": "table", "reason": "No data"}

    columns = list(data[0].keys())
    row_count = len(data)
    question_lower = question.lower()
    sql_lower = sql.lower()

    # 🚀 CASE 1: Hiển thị dạng số đơn lẻ (Metric Card)
    # Ví dụ: "Bao nhiêu đơn hàng?" -> Kết quả 1 dòng 1 cột
    if row_count == 1 and len(columns) == 1:
        return {
            "chart_type": "metric",
            "label": columns[0],
            "value": data[0][columns[0]],
            "reason": "Single value result"
        }

    # CASE 2: Biểu đồ đường (Line) - Theo thời gian
    if any(kw in question_lower for kw in ["tháng", "ngày", "trend", "xu hướng", "over time"]) or \
       any(kw in sql_lower for kw in ["date", "timestamp", "year", "month"]):
        if len(columns) >= 2:
            return {"chart_type": "line", "x": columns[0], "y": columns[1], "reason": "Time series detected"}

    # CASE 3: Biểu đồ tròn (Pie) - Tỷ lệ
    if any(kw in question_lower for kw in ["tỷ lệ", "phần trăm", "ratio", "percentage"]):
        if len(columns) >= 2:
            return {"chart_type": "pie", "label": columns[0], "value": columns[1], "reason": "Proportions detected"}

    # CASE 4: Biểu đồ cột (Bar) - So sánh (Mặc định cho Group By)
    if any(kw in question_lower for kw in ["top", "so sánh", "ranking"]) or "group by" in sql_lower:
        if len(columns) >= 2:
            return {"chart_type": "bar", "x": columns[0], "y": columns[1], "reason": "Comparison detected"}

    return {"chart_type": "table", "reason": "Default list view"}


# ====== QUICK TEST ======
async def interactive_test():
    print("=" * 60)
    print("🧠 AI Agent — Smart Data Analyst | INTERACTIVE MODE (ASYNC)")
    print("=" * 60)

    # Test 1: Kiểm tra kết nối
    print("\n📡 Đang kết nối Databricks & Gemini...")
    try:
        schema = get_schema_info()
        print(f"✅ Đã kết nối Databricks Schema: {schema['tables']}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return

    # Test 2: Hỏi đáp tương tác
    print("\n🤖 Sẵn sàng! Hãy nhập câu hỏi bằng ngôn ngữ tự nhiên (Tắt: Ctrl+C)")
    print("Ví dụ: 'Có bao nhiêu đơn hàng đang chờ xử lý?'")

    while True:
        try:
            user_input = input("\n👉 Bạn hỏi: ")
            if not user_input.strip():
                continue
                
            response = await process_question(user_input)
            if response.get("error"):
                print(f"⚠️ Agent báo lỗi: {response['error']}")
            else:
                print(f"📝 SQL Agent sinh ra:\n\033[94m{response['generated_sql']}\033[00m")
                print(f"✅ Kết quả trả về ({response['row_count']} dòng):")
                
                # Hiển thị dữ liệu thực tế
                if response["data"]:
                    # Lấy 5 dòng đầu tiên để hiển thị cho gọn
                    for i, row in enumerate(response["data"][:5]):
                        print(f"   Row {i+1}: {row}")
                    if len(response["data"]) > 5:
                        print(f"   ... và {len(response['data']) - 5} dòng khác.")
                else:
                    print("   [Bảng rỗng]")
                    
                print(f"📊 Gợi ý vẽ biểu đồ: \033[92m{response['visualization_recommendation']['chart_type']}\033[00m")
                
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Đã thoát phiên Chat.")
            break

if __name__ == "__main__":
    import asyncio
    asyncio.run(interactive_test())
