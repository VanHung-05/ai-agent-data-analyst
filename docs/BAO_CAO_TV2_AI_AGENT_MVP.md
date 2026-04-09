# BÁO CÁO TV2 - AI AGENT ENGINE (MVP)

## 1. Thông tin chung

- **Môn học:** Kiến trúc hướng dịch vụ và Điện toán đám mây
- **Đề tài:** AI Agent - Smart Data Analyst on Databricks
- **Vai trò:** TV2 (AI/ML Engineer)
- **Người thực hiện:** Nguyễn Văn Hùng
- **Phạm vi báo cáo:** Thiết kế và triển khai lõi Multi-Agent cho backend

---

## 2. Mục tiêu TV2

TV2 chịu trách nhiệm xây dựng AI Engine để chuyển câu hỏi tự nhiên thành kết quả dữ liệu có thể sử dụng ngay trên frontend:

1. Định tuyến câu hỏi theo intent (`conversation`, `sql`, `visualize`).
2. Sinh SQL Spark an toàn, chỉ đọc dữ liệu.
3. Tự phục hồi khi SQL lỗi (retry + self-correction).
4. Gợi ý trực quan hóa phù hợp với dữ liệu thực tế.
5. Sinh câu trả lời NLG dễ hiểu cho người dùng cuối.
6. Hỗ trợ progress realtime qua SSE cho frontend.

---

## 3. Công nghệ đã dùng

### Backend
- FastAPI
- LangChain (`create_sql_query_chain`, `QuerySQLDataBaseTool`)
- Databricks SQL Connector + SQLAlchemy
- Google Gemini qua `google-genai` wrapper
- Pydantic, asyncio

### Frontend liên quan đến TV2
- Streamlit tiêu thụ API JSON/SSE
- Plotly render chart từ chart spec backend

---

## 4. Kiến trúc triển khai

### 4.1 Multi-Agent pipeline

`User Question -> Router -> (Conversation | SQL -> Visualize -> NLG) -> Response`

### 4.2 Thành phần TV2 bàn giao

- `backend/services/agent_service.py` (orchestrator)
- `backend/services/router_agent.py`
- `backend/services/conversation_agent.py`
- `backend/services/visualize_agent.py`
- `backend/services/nlg_agent.py`
- `backend/services/query_result_parser.py`
- `backend/services/llm_service.py`
- `backend/prompts/system_prompt.txt`

---

## 5. Kết quả kỹ thuật chính

### 5.1 Router Agent

- Dùng LLM chấm confidence 3 nhánh intent.
- Parse JSON robust (kể cả output bẩn có markdown/text).
- Có fallback rule-based theo keyword khi LLM lỗi.

### 5.2 SQL Agent (an toàn + tự sửa lỗi)

- Sinh SQL từ câu hỏi tự nhiên.
- Bắt buộc qua `validate_sql` + `sanitize_sql` trước khi chạy.
- Retry tối đa 3 lần, đưa lỗi lần trước vào prompt để LLM sửa SQL.
- Chỉ chạy luồng read-only.

### 5.3 Query parser & dữ liệu chuẩn hóa

- Parse được raw result chứa `Decimal(...)`, tuple list, text table.
- Đổi `col_0`, `col_1` thành alias trong câu `SELECT` nếu khớp.

### 5.4 Visualize Agent thực tế

- Chặn case vẽ sai: dữ liệu 1 dòng/1 cột -> trả `table`.
- Chỉ cho pie chart khi đủ điều kiện (>=2 nhóm).
- Validate chart type theo hình thái dữ liệu để tránh chart 100% giả.

### 5.5 NLG Agent

- Diễn giải dữ liệu thành ngôn ngữ tự nhiên.
- Dựa đúng data trả về, không bịa thêm số liệu.

### 5.6 SSE realtime progress

- Thêm endpoint stream để frontend thấy tiến trình thật:
  - `llm_init`, `router`, `db_connect`, `sql_generate`, `sql_execute`, `visualize`, `nlg`, `done`.

---

## 6. Tối ưu hiệu năng & trải nghiệm

1. **Databricks warm-up khi startup** để giảm cold start query đầu tiên.
2. **DB singleton thread-safe** tránh connect lặp nhiều lần.
3. **LLM singleton cache** tránh khởi tạo model lại theo mỗi request.
4. **Health endpoint lightweight** không invoke model mặc định.

---

## 7. Rủi ro và hướng xử lý

- **Sai SQL / sai schema:** đã có self-correction + schema grounding.
- **Output LLM không chuẩn JSON:** đã có parse fallback.
- **Chart sai ngữ nghĩa:** đã có validate chart-vs-data.
- **Độ trễ:** đã thêm warm-up + caching + SSE progress.

---

## 8. Đối chiếu mục tiêu MVP

- Router đa nhánh: **Đạt**
- Text-to-SQL an toàn: **Đạt**
- Self-correction retry: **Đạt**
- NLG cho câu trả lời cuối: **Đạt**
- Visualize recommendation theo dữ liệu: **Đạt**
- Realtime progress stream: **Đạt**

---

## 9. Kết luận

TV2 đã hoàn thiện AI Agent Engine cho MVP theo kiến trúc microservice, đảm bảo an toàn SQL, khả năng tự sửa lỗi, trực quan hóa phù hợp và trải nghiệm realtime tốt hơn cho frontend.

**Trạng thái đề xuất nghiệm thu TV2: HOÀN THÀNH (MVP).**
