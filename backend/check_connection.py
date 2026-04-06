"""
🔍 check_connection.py — Kiểm tra toàn bộ kết nối hệ thống
=========================================================
Sử dụng script này để xác minh:
1. File .env đã được load đúng hay chưa.
2. Kết nối tới Databricks (Host, Token, Catalog, Schema).
3. Kết nối tới Google Gemini API.
4. Danh sách các bảng dữ liệu hiện có.
"""

import os
import sys
from dotenv import load_dotenv

# Thêm thư mục hiện tại vào path để import các module nội bộ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import databricks_config, llm_config
from services.agent_service import get_database, get_schema_info
from services.llm_service import get_llm

def redact(text: str, visible: int = 4) -> str:
    """Ẩn bớt các ký tự nhạy cảm của API Key/Secret"""
    if not text or len(text) <= visible:
        return "[TRỐNG]"
    return text[:visible] + "********" + text[-visible:]

def run_diagnostic():
    print("=" * 60)
    print("🚀 BẮT ĐẦU KIỂM TRA HỆ THỐNG (DIAGNOSTIC MODE)")
    print("=" * 60)

    # --- 1. KIỂM TRA BIẾN MÔI TRƯỜNG ---
    print("\n[1] Kiểm tra cấu hình .env:")
    print(f"   🔹 Databricks Host: {databricks_config.host}")
    print(f"   🔹 Databricks Catalog: {databricks_config.catalog}")
    print(f"   🔹 Databricks Schema: {databricks_config.schema}")
    print(f"   🔹 Client ID: {redact(databricks_config.client_id)}")
    print(f"   🔹 Client Secret: {redact(databricks_config.client_secret)}")
    print(f"   🔹 Gemini Model: {llm_config.gemini_model}")
    print(f"   🔹 Gemini API Key: {redact(llm_config.gemini_api_key)}")

    # --- 2. KIỂM TRA DATABRICKS ---
    print("\n[2] Kiểm tra kết nối Databricks:")
    try:
        db = get_database()
        
        # Thử dùng SQL thuần để liệt kê bảng (tránh bộ lọc của LangChain)
        print("   🔹 Đang truy vấn danh sách bảng bằng SQL thuần...")
        raw_tables = db.run("SHOW TABLES")
        print(f"   🔎 Kết quả SHOW TABLES từ Databricks: {raw_tables}")

        tables = db.get_usable_table_names()
        print(f"   ✅ LangChain nhận diện được {len(tables)} bảng: {tables}")
        
        # Kiểm tra thử quyền truy cập vào bảng Olist
        print("\n   🔹 Kiểm tra quyền truy cập bảng Olist thực tế...")
        try:
            test_query = "SELECT * FROM olist_orders LIMIT 1"
            db.run(test_query)
            print("   ✅ CHÚC MỪNG: Service Principal CÓ QUYỀN đọc bảng olist_orders!")
        except Exception as perm_err:
            print(f"   ❌ CẢNH BÁO: Service Principal KHÔNG CÓ QUYỀN đọc bảng olist_orders. Lỗi: {str(perm_err)[:100]}...")

        print("\n   --- Chi tiết Metadata các bảng nhận diện được ---")
        schema_info = get_schema_info()
        print(schema_info["table_info"])
    except Exception as e:
        print(f"   ❌ LỖI KẾT NỐI DATABRICKS: {str(e)}")

    # --- 3. KIỂM TRA LLM (GEMINI) ---
    print("\n[3] Kiểm tra kết nối Gemini API:")
    try:
        llm = get_llm()
        print(f"   ✅ Đã khởi tạo Gemini Model.")
        print(f"   📡 Gửi câu hỏi thử nghiệm: 'Who are you?'")
        response = llm.invoke("Who are you? Answer in 1 short sentence.")
        print(f"   🤖 Trả lời: {response.content}")
    except Exception as e:
        print(f"   ❌ LỖI KẾT NỐI GEMINI: {str(e)}")

    print("\n" + "=" * 60)
    print("🏁 HOÀN TẤT KIỂM TRA!")
    print("=" * 60)

if __name__ == "__main__":
    run_diagnostic()
