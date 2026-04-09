# AI Agent - Smart Data Analyst

Trợ lý phân tích dữ liệu thông minh cho bộ dữ liệu Olist E-Commerce, xây dựng theo kiến trúc **Multi-Agent** trên nền **FastAPI + LangChain + Databricks + Streamlit**.

## Giới thiệu

Dự án cho phép người dùng đặt câu hỏi bằng ngôn ngữ tự nhiên (Việt/Anh), hệ thống sẽ:

- Phân loại intent câu hỏi (chat thường / truy vấn dữ liệu / trực quan hóa)
- Sinh SQL Spark an toàn
- Chạy truy vấn trên Databricks SQL Warehouse
- Gợi ý biểu đồ phù hợp
- Diễn giải kết quả bằng ngôn ngữ tự nhiên (NLG)
- Hỗ trợ progress realtime qua SSE

## Công nghệ chính

### Backend
- Python 3.10+
- FastAPI
- LangChain (`create_sql_query_chain`, SQLDatabase tools)
- Databricks SQL Connector
- Gemini (google-genai wrapper)

### Frontend
- Streamlit
- Plotly

### Runtime
- Docker / Docker Compose

## Pipeline hệ thống

```text
User Question
    |
    v
FastAPI (/api/v1/chat/query | /api/v1/chat/query/stream)
    |
    v
Agent Orchestrator (agent_service)
    |
    +--> Router Agent (conversation | sql | visualize)
    |
    +--> Conversation Agent (nếu là câu chào/hỏi đáp)
    |
    +--> SQL Path:
    |      1) Generate SQL
    |      2) Validate/Sanitize SQL
    |      3) Execute Databricks
    |      4) Parse & Normalize result
    |      5) Visualize Agent (chart spec)
    |      6) NLG Agent (answer text)
    |
    v
JSON response / SSE progress events
```

## Các Agent chính

### 1) Router Agent
- **File:** `backend/services/router_agent.py`
- **Chức năng:** Xác định câu hỏi thuộc nhánh nào: `conversation`, `sql`, hoặc `visualize`.
- **Cách hoạt động:** Gọi LLM để chấm điểm confidence cho 3 intent, parse JSON robust (có fallback regex), sau đó chọn intent điểm cao nhất; nếu lỗi thì fallback keyword rule-based.
- **Ý nghĩa:** Tránh xử lý sai luồng, giúp hệ thống phản hồi đúng kiểu tác vụ ngay từ đầu.

### 2) Conversation Agent
- **File:** `backend/services/conversation_agent.py`
- **Chức năng:** Trả lời các câu chào hỏi/hội thoại chung và làm phương án fallback khi luồng SQL lỗi.
- **Cách hoạt động:** Nhận câu hỏi + ngữ cảnh lỗi (nếu có), sinh phản hồi tự nhiên, lịch sự, ngắn gọn.
- **Ý nghĩa:** Giữ trải nghiệm hội thoại mượt, tránh trả lỗi kỹ thuật thô cho người dùng cuối.

### 3) SQL Agent (trong Orchestrator)
- **File:** `backend/services/agent_service.py`
- **Chức năng:** Chuyển câu hỏi tự nhiên thành SQL Spark, truy vấn Databricks và trả dữ liệu chuẩn hóa.
- **Cách hoạt động:** `create_sql_query_chain` -> clean SQL -> `validate_sql/sanitize_sql` -> execute Databricks -> parse result; có retry self-correction tối đa 3 lần khi SQL lỗi.
- **Ý nghĩa:** Là lõi phân tích dữ liệu của hệ thống, đảm bảo vừa đúng nghiệp vụ vừa an toàn truy vấn.

### 4) Visualize Agent
- **File:** `backend/services/visualize_agent.py`
- **Chức năng:** Đề xuất cách trực quan hóa phù hợp (`chart_type`, `x`, `y`, `title`).
- **Cách hoạt động:** Dựa trên câu hỏi + SQL + shape dữ liệu để chọn chart bằng heuristic trước, LLM fallback sau; validate chart-vs-data để chặn case vẽ sai (ví dụ 1 dòng aggregate không ép pie 100%).
- **Ý nghĩa:** Biến kết quả số liệu thành hình ảnh dễ đọc, hỗ trợ người dùng ra quyết định nhanh hơn.

### 5) NLG Agent
- **File:** `backend/services/nlg_agent.py`
- **Chức năng:** Viết lại kết quả query thành câu trả lời tự nhiên cho người dùng.
- **Cách hoạt động:** Nhận câu hỏi gốc + dữ liệu JSON, gọi LLM để diễn giải súc tích, giữ đúng số liệu; có fallback nếu LLM gặp lỗi.
- **Ý nghĩa:** Tăng khả năng hiểu kết quả cho người không chuyên SQL, giảm phụ thuộc vào việc đọc bảng thô.

## Tóm tắt luồng hoạt động tổng thể

1. Frontend gửi câu hỏi vào backend
2. Router chọn nhánh xử lý
3. Nếu SQL/visualize:
   - LLM sinh SQL
   - SQL đi qua validator/sanitizer
   - Databricks trả dữ liệu
   - Hệ thống parse dữ liệu, gợi ý biểu đồ
   - NLG tạo câu trả lời
4. Frontend hiển thị answer + chart + table + SQL
5. Nếu dùng SSE thì frontend cập nhật tiến trình realtime theo step

## Cấu trúc thư mục

```text
ai-agent-data-analyst/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── routers/
│   │   ├── query.py
│   │   └── health.py
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── llm_service.py
│   │   ├── router_agent.py
│   │   ├── conversation_agent.py
│   │   ├── visualize_agent.py
│   │   ├── nlg_agent.py
│   │   └── query_result_parser.py
│   ├── prompts/
│   │   └── system_prompt.txt
│   └── utils/
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .streamlit/config.toml
│   ├── components/
│   │   ├── chat.py
│   │   ├── charts.py
│   │   └── result_table.py
│   └── assets/styles.css
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md
```

## Hướng dẫn cài đặt

## Cách 1: Chạy bằng Docker (khuyến nghị demo nhanh)

### Bước 1: chuẩn bị biến môi trường

Tạo file `backend/.env` từ `.env.example` và điền giá trị thật:

```bash
cp .env.example backend/.env
```

### Bước 2: chạy toàn bộ hệ thống

```bash
docker compose up --build
```

### Truy cập
- Frontend: `http://localhost:8501`
- Backend: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`

## Cách 2: Chạy bằng lệnh local (dev mode)

### A. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### B. Frontend

Mở terminal khác:

```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

> Dùng `.venv/bin/python -m streamlit` để tránh gọi nhầm streamlit từ Python hệ thống.

## API chính

- `GET /api/v1/health`
- `GET /api/v1/health?deep=true`
- `GET /api/v1/schema`
- `POST /api/v1/chat/query`
- `POST /api/v1/chat/query/stream` (SSE realtime)
- `POST /api/v1/chat/route`

## Ghi chú vận hành

- Backend có warm-up Databricks lúc startup.
- LLM được cache singleton để giảm khởi tạo lặp.
- `/health` mặc định lightweight (không invoke model).
- SQL được kiểm tra an toàn trước khi thực thi.

## Tài liệu liên quan

- `docs/KIEN_TRUC_CONG_NGHE_MULTI_AGENT.md`
- `docs/api_docs.md`
- `docs/TV2_PLAYBOOK_AI_AGENT.md`
- `SETUP_GUIDE.md`

