# Hướng dẫn cài đặt & chạy dự án

**AI Agent — Smart Data Analyst**
Trợ lý phân tích dữ liệu thông minh trên Databricks

---

## Yêu cầu hệ thống

| Thành phần | Phiên bản tối thiểu |
|---|---|
| Python | 3.8+ (khuyến nghị 3.10+) |
| pip | 23+ |
| Git | 2.x |
| Docker *(tùy chọn)* | 24+ |

---

## Cấu trúc thư mục chính

```
ai-agent-data-analyst/
├── backend/                ← FastAPI + LangChain + Databricks
│   ├── main.py             ← Entry point (uvicorn)
│   ├── config.py           ← Đọc biến môi trường
│   ├── requirements.txt
│   ├── routers/            ← API endpoints
│   ├── services/           ← Multi-Agent logic (Router, SQL, NLG, Visualize, Conversation)
│   ├── prompts/            ← System prompt cho LLM
│   └── utils/              ← SQL validator, logger
├── frontend/               ← Streamlit UI
│   ├── app.py              ← Entry point (streamlit run)
│   ├── requirements.txt
│   ├── components/         ← Chat, Charts, Result Table
│   └── assets/             ← CSS
├── .env.example            ← Mẫu biến môi trường
├── docker-compose.yml      ← Chạy bằng Docker (tùy chọn)
└── SETUP_GUIDE.md          ← File này
```

---

## Cách 1: Chạy thủ công (khuyến nghị khi phát triển)

### Bước 1 — Cấu hình biến môi trường

```bash
# Ở thư mục gốc dự án
cp .env.example .env
```

Mở file `.env` và điền thông tin thật:

```env
# Databricks (TV1 cấp)
DATABRICKS_HOST=dbc-xxxxx.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxx
DATABRICKS_CLIENT_ID=<client-id>
DATABRICKS_CLIENT_SECRET=<secret>
DATABRICKS_CATALOG=ai_analyst
DATABRICKS_SCHEMA=ecommerce

# LLM (TV2 cấp)
LLM_PROVIDER=gemini
GEMINI_API_KEY=<api-key>
GEMINI_MODEL=gemini-2.5-flash

# App
APP_ENV=development
APP_PORT=8000
LOG_LEVEL=INFO
```

> **⚠️ KHÔNG commit file `.env` lên Git!** File đã có trong `.gitignore`.

---

### Bước 2 — Chạy Backend (Terminal 1)

```bash
cd backend

# Tạo venv (chỉ lần đầu)
python3 -m venv .venv

# Kích hoạt venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# Cài dependencies (chỉ lần đầu hoặc khi thay đổi)
pip install --upgrade pip
pip install -r requirements.txt

# Chạy server
python -m uvicorn main:app --reload --port 8000
```

Kiểm tra: mở http://localhost:8000 → thấy `{"message": "🤖 AI Agent — Smart Data Analyst API is running!"}`

Kiểm tra health: http://localhost:8000/api/v1/health

API docs (auto): http://localhost:8000/docs

---

### Bước 3 — Chạy Frontend (Terminal 2)

```bash
cd frontend

# Tạo venv (chỉ lần đầu)
python3 -m venv .venv

# Kích hoạt venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

# Cài dependencies (chỉ lần đầu hoặc khi thay đổi)
pip install --upgrade pip
pip install -r requirements.txt

# Chạy Streamlit
.venv/bin/python -m streamlit run app.py
```

> **Lưu ý quan trọng:** Dùng `.venv/bin/python -m streamlit run app.py` thay vì `streamlit run app.py` để đảm bảo chạy đúng Python trong venv (tránh xung đột với streamlit cài ở system Python).

Mở http://localhost:8501 → giao diện chat AI Data Analyst.

---

## Cách 2: Chạy bằng Docker Compose

```bash
# Ở thư mục gốc dự án (cần có .env đã cấu hình ở Bước 1)
docker-compose up --build
```

| Service | URL |
|---|---|
| Backend API | http://localhost:8000 |
| Backend Docs | http://localhost:8000/docs |
| Frontend UI | http://localhost:8501 |

Dừng:

```bash
docker-compose down
```

---

## API Endpoints chính

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/api/v1/health` | Kiểm tra trạng thái hệ thống |
| `GET` | `/api/v1/schema` | Xem metadata database |
| `POST` | `/api/v1/chat/query` | Gửi câu hỏi → nhận SQL + data + chart + NLG answer |
| `POST` | `/api/v1/chat/route` | Chỉ chạy Router Agent (debug) |

### Ví dụ gọi API

```bash
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Tổng doanh thu là bao nhiêu?"}'
```

---

## Kiến trúc Multi-Agent

```
User Question
    │
    ▼
┌─────────────┐
│ Router Agent│  ← Phân loại intent: conversation / sql / visualize
└──────┬──────┘
       │
  ┌────┴─────┐
  │          │
  ▼          ▼
┌────┐  ┌────────┐
│Chat│  │SQL Agent│  ← Sinh SQL + thực thi trên Databricks
└────┘  └───┬────┘
            │
       ┌────┴─────┐
       │          │
       ▼          ▼
  ┌─────────┐ ┌───────┐
  │Visualize│ │  NLG  │  ← Đề xuất chart + Viết câu trả lời tự nhiên
  │  Agent  │ │ Agent │
  └─────────┘ └───────┘
```

---

## Xử lý sự cố thường gặp

### Backend không kết nối Databricks
- Kiểm tra `.env`: `DATABRICKS_HOST`, `DATABRICKS_HTTP_PATH`, `CLIENT_ID/SECRET` đúng chưa.
- Gọi `GET /api/v1/health` xem chi tiết lỗi.

### Frontend báo "Backend không phản hồi"
- Đảm bảo backend đang chạy trên port 8000.
- Nếu backend ở URL khác: `export BACKEND_URL=http://<host>:<port>/api/v1` trước khi chạy streamlit.

### Lỗi "No module named ..."
- Đảm bảo đang trong đúng venv: `which python` phải trỏ vào `.venv/bin/python`.
- Chạy lại `pip install -r requirements.txt`.

### Lỗi "streamlit" gọi nhầm Python hệ thống
- Dùng `.venv/bin/python -m streamlit run app.py` thay vì `streamlit run app.py`.

---

## Phân công nhóm

| Vai trò | Thư mục chính | Mô tả |
|---|---|---|
| TV1 — Data Engineer | `data/` | Schema, SQL scripts, Databricks config |
| TV2 — AI/ML Engineer | `backend/services/`, `backend/prompts/`, `backend/utils/` | Multi-Agent logic, LLM, SQL validator |
| TV3 — Backend Dev | `backend/routers/`, `backend/main.py` | REST API endpoints |
| TV4 — Frontend Dev | `frontend/` | Streamlit UI |
| TV5 — DevOps & QA | `docker-compose.yml`, `Dockerfile`, tests | CI/CD, Docker, testing |
