# Kiến trúc công nghệ & thiết kế Multi-Agent

Tài liệu mô tả đầy đủ kiến trúc kỹ thuật cho dự án **AI Agent - Smart Data Analyst**: stack công nghệ, luồng xử lý, mô tả từng agent, cách triển khai, và hướng mở rộng production.

---

## 1) Mục tiêu hệ thống

Xây dựng trợ lý phân tích dữ liệu bằng ngôn ngữ tự nhiên cho dữ liệu e-commerce trên Databricks, với định hướng:

- Người dùng hỏi bằng tiếng Việt/Anh tự nhiên.
- Hệ thống tự chọn luồng xử lý phù hợp (chat thường, SQL, visualize).
- Trả kết quả dễ hiểu (NLG), có thể trực quan hóa bằng biểu đồ.
- Bảo toàn an toàn SQL: chỉ đọc dữ liệu, chặn lệnh biến đổi.

---

## 2) Stack công nghệ

### Backend
- **Python 3.10+**
- **FastAPI**: cung cấp REST API
- **LangChain**: orchestration LLM + SQL chain
- **Databricks SQL Warehouse**: nguồn dữ liệu chính
- **google-genai (Gemini)**: mô hình LLM mặc định
- **Pydantic**: model request/response

### Frontend
- **Streamlit**: giao diện chat + bảng dữ liệu + biểu đồ
- **Plotly**: vẽ chart theo chart spec từ backend

### Hạ tầng & vận hành
- **Docker / Docker Compose**: chạy local dạng container
- **.env**: quản lý biến môi trường
- **Logging**: `backend/utils/logger.py`

---

## 3) Kiến trúc tổng thể

```text
User (Streamlit UI)
        |
        v
FastAPI Router (/api/v1/chat/query, /api/v1/chat/query/stream)
        |
        v
Agent Orchestrator (backend/services/agent_service.py)
        |
        +--> Router Agent (intent: conversation/sql/visualize)
        |
        +--> Conversation Agent (nếu intent conversation)
        |
        +--> SQL Agent (LLM -> SQL -> validate -> execute Databricks)
        |         |
        |         +--> Query Result Parser (chuẩn hóa raw result)
        |         +--> Visualize Agent (chart_type + x/y/title)
        |         +--> NLG Agent (diễn giải tự nhiên)
        |
        v
Response JSON / SSE stream events
        |
        v
Streamlit render: answer + chart + table + SQL + chat history
```

---

## 4) Luồng xử lý end-to-end

### 4.1 REST tiêu chuẩn (`POST /api/v1/chat/query`)
1. Frontend gửi câu hỏi.
2. Backend khởi tạo (hoặc lấy cache) LLM.
3. Router Agent phân loại intent.
4. Nếu `conversation` -> trả lời trực tiếp.
5. Nếu `sql`/`visualize`:
   - sinh SQL bằng LangChain
   - validate/sanitize SQL
   - chạy SQL trên Databricks
   - parse kết quả
   - đề xuất chart spec
   - sinh câu trả lời NLG
6. Trả JSON cho frontend.

### 4.2 SSE realtime (`POST /api/v1/chat/query/stream`)
Backend phát sự kiện theo bước:
- `llm_init`
- `router`
- `db_connect`
- `sql_generate`
- `sql_execute`
- `visualize`
- `nlg`
- `done`

Frontend nhận event và cập nhật tiến trình realtime trong khung trạng thái.

---

## 5) Mô tả chi tiết các Agent

## 5.1 Router Agent
**File:** `backend/services/router_agent.py`

**Mục đích**
- Chọn đường đi xử lý: `conversation`, `sql`, hoặc `visualize`.

**Cách hoạt động**
- Gọi LLM để chấm điểm confidence cho 3 nhãn.
- Parse JSON robust (có fallback regex nếu output bẩn).
- Normalize tổng điểm về 1.0.
- Nếu lỗi LLM -> fallback keyword rule-based.

**Output chính**
- `intent`
- `scores`
- `selected_agents`
- `routing_method` (`llm` hoặc `rule_based`)

---

## 5.2 Conversation Agent
**File:** `backend/services/conversation_agent.py`

**Mục đích**
- Xử lý lời chào/hỏi đáp chung, hoặc fallback khi SQL thất bại.

**Đặc điểm**
- Trả lời ngắn gọn, lịch sự.
- Có thể dùng ngữ cảnh lỗi để phản hồi dễ hiểu hơn.

---

## 5.3 SQL Agent (trong Orchestrator)
**File chính:** `backend/services/agent_service.py`

**Mục đích**
- Chuyển câu hỏi tự nhiên thành SQL, chạy trên Databricks, trả dữ liệu.

**Các bước kỹ thuật**
1. `create_sql_query_chain(llm, db, k=100)`
2. Lấy SQL từ chain và làm sạch output markdown/prefix.
3. Qua `validate_sql` + `sanitize_sql`.
4. Chạy SQL bằng `QuerySQLDataBaseTool`.
5. Parse dữ liệu qua `query_result_parser`.
6. Rename `col_0, col_1...` bằng alias trong `SELECT`.

**Cơ chế retry**
- Retry tối đa 3 lần khi sinh/chạy SQL lỗi.
- Có đưa lỗi lần trước vào prompt để LLM sửa SQL.

---

## 5.4 Visualize Agent
**File:** `backend/services/visualize_agent.py`

**Mục đích**
- Đề xuất loại biểu đồ phù hợp với dữ liệu và câu hỏi.

**Nguyên tắc hiện tại**
- Không vẽ chart khi dữ liệu quá ít (1 dòng/1 cột) -> `table`.
- Ưu tiên chart người dùng yêu cầu rõ (line/bar/pie/...)
- Validate chart theo dữ liệu thực:
  - Pie cần >= 2 nhóm
  - Line/bar/scatter/area cần >= 2 điểm
  - Y-axis nên numeric
- Fallback LLM nếu heuristic không chắc chắn.

**Output**
- `chart_type`, `x`, `y`, `title`, `reason`

---

## 5.5 NLG Agent
**File:** `backend/services/nlg_agent.py`

**Mục đích**
- Biến dữ liệu query thành câu trả lời tự nhiên dễ hiểu cho người dùng.

**Đặc điểm**
- Nhận câu hỏi + dữ liệu JSON.
- Ưu tiên ngôn ngữ người dùng (Việt/Anh).
- Có fallback nếu LLM lỗi.
- Không “bịa” số liệu ngoài dữ liệu đầu vào.

---

## 6) Các thành phần hỗ trợ quan trọng

### 6.1 Query Result Parser
**File:** `backend/services/query_result_parser.py`

- Chuẩn hóa raw output từ Databricks thành `list[dict]`.
- Xử lý các dạng đặc biệt như `Decimal(...)`, bảng text, tuple list.

### 6.2 Health Router
**File:** `backend/routers/health.py`

- `GET /health` (mặc định lightweight):
  - check API + Databricks + config LLM (không invoke model).
- `GET /health?deep=true`:
  - kiểm tra sâu, có invoke LLM.

### 6.3 LLM Service
**File:** `backend/services/llm_service.py`

- Factory theo provider (`gemini`, `openai`, `databricks`).
- Có singleton cache để tránh khởi tạo model lặp lại nhiều lần.

### 6.4 Warm-up lúc startup
**File:** `backend/main.py`

- Startup hook kết nối Databricks sớm (`SELECT 1`) để giảm cold start khi user vừa vào UI.

---

## 7) Thiết kế Frontend (Streamlit)

**File chính:** `frontend/app.py`

### Tính năng chính
- Chat UI: user bên phải, assistant bên trái.
- Lưu nhiều cuộc hội thoại (chat history trong sidebar).
- Nút `Chat mới`.
- Hiển thị:
  - trạng thái hệ thống
  - câu trả lời NLG
  - chart Plotly
  - bảng dữ liệu + download CSV
  - SQL đã sinh

### Realtime progress
- Dùng SSE endpoint `/chat/query/stream`.
- Hiển thị các bước xử lý đang chạy ngay trong assistant status.

---

## 8) API contract chính

- `POST /api/v1/chat/query`: trả kết quả hoàn chỉnh dạng JSON.
- `POST /api/v1/chat/query/stream`: trả SSE event stream.
- `POST /api/v1/chat/route`: debug routing.
- `GET /api/v1/schema`: metadata schema.
- `GET /api/v1/health`: trạng thái dịch vụ.

---

## 9) An toàn & chất lượng

- SQL bắt buộc qua validator/sanitizer.
- Chỉ cho phép query đọc dữ liệu.
- Không hardcode secret, đọc qua env.
- Log đầy đủ các bước chính để debug.
- Hạn chế gọi LLM thừa (cache + health lightweight).

---

## 10) Cách triển khai

### Local (2 terminal)
1. Chạy backend (`uvicorn main:app --reload --port 8000`)
2. Chạy frontend (`streamlit run app.py` hoặc `.venv/bin/python -m streamlit run app.py`)

### Docker
- `docker-compose up --build`

---

## 11) Hướng mở rộng đề xuất

- Thêm persistence cho chat history (SQLite/Redis/Postgres).
- Thêm auth cho API.
- Bổ sung guardrails và observability (request id, latency per step).
- Tách worker queue cho query nặng.
- Thêm test integration cho các luồng agent chính.

---

## 12) Danh sách file cốt lõi

- `backend/main.py`
- `backend/routers/query.py`
- `backend/routers/health.py`
- `backend/services/agent_service.py`
- `backend/services/router_agent.py`
- `backend/services/conversation_agent.py`
- `backend/services/visualize_agent.py`
- `backend/services/nlg_agent.py`
- `backend/services/query_result_parser.py`
- `backend/services/llm_service.py`
- `frontend/app.py`
- `frontend/components/chat.py`
- `frontend/components/charts.py`
- `frontend/components/result_table.py`

