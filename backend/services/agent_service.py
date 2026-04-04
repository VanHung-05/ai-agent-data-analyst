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


def process_question(question: str) -> dict[str, Any]:
    """
    🌟 HÀM CHÍNH — Xử lý câu hỏi từ người dùng

    Pipeline:
      1. Nhận câu hỏi ngôn ngữ tự nhiên
      2. Validate input
      3. AI sinh SQL dựa trên schema + prompt
      4. Validate SQL (chặn DML)
      5. Thực thi SQL trên Databricks
      6. Trả kết quả (hoặc retry nếu lỗi)

    Args:
        question: Câu hỏi bằng ngôn ngữ tự nhiên (VD: "Tổng doanh thu tháng 1?")

    Returns:
        dict: {
            "question": str,
            "generated_sql": str,
            "data": list[dict],
            "row_count": int,
            "visualization_recommendation": dict,
            "error": str | None
        }
    """
    result = {
        "question": question,
        "generated_sql": None,
        "data": [],
        "row_count": 0,
        "visualization_recommendation": {"chart_type": "table"},
        "error": None,
    }

    try:
        # --- Step 1: Khởi tạo Database & LLM ---
        db = get_database()
        llm = get_llm()

        # --- Step 2: Tạo chain sinh SQL ---
        # LangChain tự động nhồi schema vào prompt, ép limit mặc định = 5
        # Ta cần truyền k=100 để nó theo lời người dùng tới tối đa 100 dòng
        write_query = create_sql_query_chain(llm, db, k=100)

        # --- Step 3: AI sinh SQL ---
        generated_sql = write_query.invoke({"question": question})

        # Làm sạch SQL output (loại bỏ markdown formatting nếu có)
        generated_sql = _clean_sql_output(generated_sql)

        # --- Step 4: Validate SQL (bảo mật) ---
        is_valid, error_msg = validate_sql(generated_sql)
        if not is_valid:
            result["generated_sql"] = generated_sql
            result["error"] = f"🚫 SQL không an toàn: {error_msg}"
            return result

        # --- Step 4.5: Tự động thêm LIMIT nếu thiếu ---
        generated_sql = sanitize_sql(generated_sql)
        result["generated_sql"] = generated_sql

        # --- Step 5: Thực thi SQL trên Databricks ---
        execute_query = QuerySQLDataBaseTool(db=db)
        raw_result = execute_query.invoke(generated_sql)

        # --- Step 6: Parse kết quả ---
        result["data"] = _parse_query_result(raw_result)
        result["row_count"] = len(result["data"])

        # --- Step 7: Gợi ý loại biểu đồ ---
        result["visualization_recommendation"] = _recommend_chart(
            question, result["data"]
        )

    except Exception as e:
        error_str = str(e)
        print(f"❌ Lỗi lần 1: {error_str}")

        # --- FALLBACK: Self-correction (Retry tối đa 1 lần) ---
        try:
            result = _retry_with_correction(question, error_str, db, llm, result)
        except Exception as retry_err:
            print(f"❌ Retry cũng thất bại: {retry_err}")
            result["error"] = f"Lỗi xử lý: {error_str}"

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


def _retry_with_correction(
    question: str, error_msg: str, db, llm, result: dict
) -> dict:
    """
    Self-correction: Gửi lỗi SQL lại cho LLM để tự sửa (tối đa 1 lần retry)
    Tham khảo kỹ thuật từ Vi-RAG framework: nếu lần đầu thất bại,
    cung cấp thêm ngữ cảnh lỗi để LLM "học" và sửa.
    """
    print("🔄 Đang thử Self-correction...")

    correction_prompt = (
        f"Câu hỏi gốc: {question}\n"
        f"SQL trước đó bị lỗi với thông báo: {error_msg}\n"
        f"Hãy phân tích lỗi và viết lại câu SQL đúng. "
        f"Chỉ trả về SQL thuần, không giải thích."
    )

    write_query = create_sql_query_chain(llm, db)
    new_sql = write_query.invoke({"question": correction_prompt})
    new_sql = _clean_sql_output(new_sql)

    is_valid, err = validate_sql(new_sql)
    if not is_valid:
        result["error"] = f"Retry cũng không an toàn: {err}"
        return result

    new_sql = sanitize_sql(new_sql)
    result["generated_sql"] = new_sql

    execute_query = QuerySQLDataBaseTool(db=db)
    raw_result = execute_query.invoke(new_sql)

    result["data"] = _parse_query_result(raw_result)
    result["row_count"] = len(result["data"])
    result["visualization_recommendation"] = _recommend_chart(question, result["data"])
    result["error"] = None
    print("✅ Self-correction thành công!")
    return result


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


def _recommend_chart(question: str, data: list[dict]) -> dict:
    """
    Gợi ý loại biểu đồ phù hợp dựa trên câu hỏi & dữ liệu

    💡 TV2 NOTE (Phase 2):
      - Phân tích keyword trong câu hỏi để gợi ý chart
      - Có thể dùng LLM để recommend chart type thông minh hơn

    Returns:
        dict: {"chart_type": "bar"|"line"|"pie"|"table", ...}
    """
    question_lower = question.lower()

    # Rule-based recommendation (Phase 1 — đơn giản)
    if any(kw in question_lower for kw in ["theo tháng", "theo ngày", "trend", "xu hướng", "over time"]):
        return {"chart_type": "line", "reason": "Dữ liệu theo thời gian"}

    if any(kw in question_lower for kw in ["tỷ lệ", "phần trăm", "proportion", "ratio", "percentage"]):
        return {"chart_type": "pie", "reason": "Dữ liệu tỷ lệ"}

    if any(kw in question_lower for kw in ["so sánh", "compare", "top", "xếp hạng", "ranking", "theo loại"]):
        return {"chart_type": "bar", "reason": "Dữ liệu so sánh"}

    if any(kw in question_lower for kw in ["tổng", "total", "bao nhiêu", "count", "sum"]):
        # Nếu chỉ 1 giá trị → hiện bảng, nếu nhiều → bar chart
        if len(data) <= 1:
            return {"chart_type": "table", "reason": "Giá trị đơn lẻ"}
        return {"chart_type": "bar", "reason": "Tổng hợp nhiều nhóm"}

    return {"chart_type": "table", "reason": "Mặc định hiển thị bảng"}


# ====== QUICK TEST ======
if __name__ == "__main__":
    print("=" * 60)
    print("🧠 AI Agent — Smart Data Analyst | INTERACTIVE MODE")
    print("=" * 60)

    # Test 1: Kiểm tra kết nối
    print("\n📡 Đang kết nối Databricks & Gemini...")
    try:
        schema = get_schema_info()
        print(f"✅ Đã kết nối Databricks Schema: {schema['tables']}")
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        exit(1)

    # Test 2: Hỏi đáp tương tác
    print("\n🤖 Sẵn sàng! Hãy nhập câu hỏi bằng ngôn ngữ tự nhiên (Tắt: Ctrl+C)")
    print("Ví dụ: 'Có bao nhiêu đơn hàng đang chờ xử lý?'")

    while True:
        try:
            user_input = input("\n👉 Bạn hỏi: ")
            if not user_input.strip():
                continue
                
            response = process_question(user_input)
            if response.get("error"):
                print(f"⚠️ Agent báo lỗi: {response['error']}")
            else:
                print(f"📝 SQL Agent sinh ra:\n{response['generated_sql']}")
                print(f"✅ Số dòng dữ liệu Databricks trả về: {response['row_count']}")
                print(f"📊 Gợi ý vẽ biểu đồ: {response['visualization_recommendation']['chart_type']}")
                
        except KeyboardInterrupt:
            print("\n👋 Đã thoát phiên Chat.")
            break
