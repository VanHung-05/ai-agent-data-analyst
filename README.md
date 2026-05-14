<h1 align="center">🤖 AI Agent — Smart Data Analyst</h1>

<p align="center">
  <strong>Trợ lý phân tích dữ liệu thông minh sử dụng kiến trúc Multi-Agent</strong><br>
  Chuyển đổi câu hỏi ngôn ngữ tự nhiên (Việt/Anh) thành truy vấn SQL, thực thi trên Databricks và trả về kết quả trực quan.
</p>

<p align="center">
  <a href="#-tính-năng-chính">Tính năng</a> •
  <a href="#-kiến-trúc-hệ-thống">Kiến trúc</a> •
  <a href="#-đánh-giá-benchmark">Benchmark</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-cài-đặt">Cài đặt</a> •
  <a href="#-api-reference">API</a> 
  
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React_19-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>


<a id="-tính-năng-chính"></a>
## ✨ Tính năng chính

| Tính năng | Mô tả |
|---|---|
| 🗣️ **Natural Language to SQL** | Đặt câu hỏi bằng tiếng Việt/Anh, AI tự sinh SQL Spark chính xác |
| 🤖 **Multi-Agent Orchestration** | 5 Agent chuyên biệt phối hợp qua LangGraph workflow |
| 📊 **Auto Visualization** | Tự động đề xuất biểu đồ phù hợp (Bar, Line, Pie, Area, Scatter) |
| 💬 **NLG Response** | Diễn giải kết quả bằng ngôn ngữ tự nhiên, không cần đọc bảng thô |
| ⚡ **Real-time Streaming** | Progress tracking từng bước qua Server-Sent Events (SSE) |
| 🔒 **SQL Safety** | Validate & sanitize SQL trước khi thực thi, chặn mọi thao tác ghi/xóa |
| 📥 **Export CSV** | Xuất kết quả truy vấn ra file CSV |
| 💾 **Session Persistence** | Lưu lịch sử hội thoại tự động, không mất khi refresh trang |

---

<a id="-kiến-trúc-hệ-thống"></a>
## 🏗 Kiến trúc hệ thống

### Tổng quan

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React 19)                      │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌─────────────┐  │
│  │ ChatInput│  │MessageList│  │DynamicChart│  │  DataTable   │  │
│  └────┬─────┘  └───────────┘  └────────────┘  └─────────────┘  │
│       │              ▲               ▲               ▲          │
│       │              └───────────────┴───────────────┘          │
│       │                    Zustand Store                        │
│       ▼                    (auto-persist)                       │
│  SSE Stream ─────────────────────────────────────────────────── │
└───────┬─────────────────────────────────────────────────────────┘
        │ HTTP POST /api/v1/chat/query/stream
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                            │
│                                                                 │
│  ┌──────────────── Agent Orchestrator (LangGraph) ────────────┐ │
│  │                                                             │ │
│  │  ┌─────────┐    ┌────────────────┐    ┌─────────────────┐  │ │
│  │  │ Router  │───▶│ Conversation   │    │   SQL Pipeline   │  │ │
│  │  │ Agent   │    │ Agent          │    │                   │  │ │
│  │  └─────────┘    └────────────────┘    │ Generate SQL      │  │ │
│  │       │                                │ Validate/Sanitize │  │ │
│  │       └───────────────────────────────▶│ Execute Databricks│  │ │
│  │                                        │ Visualize Agent   │  │ │
│  │                                        │ NLG Agent         │  │ │
│  │                                        └─────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                   │
└──────────────────────────────┼───────────────────────────────────┘
                               ▼
                ┌──────────────────────────┐
                │  Databricks SQL Warehouse │
                │  (Olist E-Commerce Data)  │
                └──────────────────────────┘
```

### Multi-Agent Pipeline

```
User Question
     │
     ▼
 ┌─────────┐
 │ Router  │──── conversation ────▶ Conversation Agent ──▶ Response
 │ Agent   │
 └────┬────┘
      │ sql / visualize
      ▼
 Generate SQL (LLM + System Prompt)
      │
      ▼
 Validate & Sanitize (sql_validator)
      │
      ▼
 Execute on Databricks SQL Warehouse
      │
      ▼
 Visualize Agent (chart recommendation)
      │
      ▼
 NLG Agent (natural language answer)
      │
      ▼
 JSON Response + SSE Progress Events
```

### Các Agent

| # | Agent | File | Chức năng |
|---|---|---|---|
| 1 | **Router** | `router_agent.py` | Phân loại intent: `conversation` / `sql` / `visualize`. Dùng LLM scoring + fallback keyword rule-based |
| 2 | **Conversation** | `conversation_agent.py` | Trả lời chào hỏi, hội thoại chung. Fallback khi SQL pipeline lỗi |
| 3 | **SQL** | `agent_service.py` | Sinh SQL Spark từ NL, thực thi Databricks, retry self-correction (tối đa 3 lần) |
| 4 | **Visualize** | `visualize_agent.py` | Đề xuất chart spec (`chart_type`, `x`, `y`, `title`). Heuristic-first, LLM fallback |
| 5 | **NLG** | `nlg_agent.py` | Diễn giải kết quả thành câu trả lời tự nhiên, giữ đúng số liệu |

---

<a id="-đánh-giá-benchmark"></a>
## 📈 Đánh giá (Benchmark)

Hệ thống được đánh giá trên **100 test cases** với 4 chỉ số chuẩn từ bài survey *"From Natural Language to SQL"* (Mohammadjafari et al., 2024):

| Chỉ số | Kết quả | Mô tả |
|---|---|---|
| **EX** (Execution Accuracy) ⭐ | **91.0%** | Tỷ lệ SQL sinh ra cho kết quả khớp với Gold SQL |
| **CM** (Component Match) | **91.5%** | Tỷ lệ clause SQL khớp cấu trúc |
| **EM** (Exact Match) | **50.0%** | Tỷ lệ khớp chuỗi SQL hoàn toàn |
| **VES** (Valid Efficiency Score) | **90.4%** | Hiệu năng thực thi so với Gold SQL |

**Chỉ số bổ sung:**

| Chỉ số | Kết quả |
|---|---|
| Syntax Pass Rate | **100%** |
| Semantic Match Rate | **92.0%** |
| Overall Weighted Score | **96.07%** |

> Chi tiết quá trình tối ưu 12 vòng: [`evaluation/prompt_fix_log.md`](backend/evaluation/prompt_fix_log.md)

---

<a id="-tech-stack"></a>
## 🛠 Tech Stack

### Backend
| Công nghệ | Phiên bản | Vai trò |
|---|---|---|
| Python | 3.10+ | Runtime |
| FastAPI | 0.115 | Web framework + SSE |
| LangChain | 0.3.0 | SQL chain + LLM orchestration |
| LangGraph | latest | Multi-agent workflow |
| Gemini | gemini-2.5-flash | LLM provider (default) |
| Databricks SQL | Connector 3.6 | Data warehouse |
| SQLAlchemy | 2.0.35 | Database abstraction |

### Frontend
| Công nghệ | Phiên bản | Vai trò |
|---|---|---|
| React | 19 | UI framework |
| Vite | 8 | Build tool |
| TypeScript | 6.0 | Type safety |
| Zustand | 5.0 | State management + persistence |
| Recharts | 3.8 | Chart rendering |
| TailwindCSS | 3.4 | Styling |
| Nginx | latest | Production static server + reverse proxy |

### Infrastructure
| Công nghệ | Vai trò |
|---|---|
| Docker Compose | Container orchestration |
| Databricks Unity Catalog | Data governance |
| Olist E-Commerce Dataset | 10 tables, ~100K orders |


---

<a id="-cài-đặt"></a>
## 🚀 Cài đặt

### Yêu cầu

- Docker & Docker Compose (khuyến nghị)
- Hoặc: Python 3.10+ & Node.js 18+
- Databricks workspace với SQL Warehouse
- Gemini API key (hoặc OpenAI API key)

### Cách 1: Docker Compose (khuyến nghị)

**Bước 1:** Cấu hình biến môi trường

```bash
cp .env.example backend/.env
# Mở backend/.env và điền credentials thật
```

**Bước 2:** Khởi chạy hệ thống

```bash
docker compose up --build
```

**Bước 3:** Truy cập

| Service | URL |
|---|---|
| 🌐 Frontend | http://localhost |
| ⚙️ Backend API | http://localhost:8000 |
| 📖 API Docs (Swagger) | http://localhost:8000/docs |

### Cách 2: Dev Mode (local)

**Backend:**

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend-react
npm install
npm run dev
# → http://localhost:5173
```

---

## 🔑 Biến môi trường

| Biến | Mô tả | Bắt buộc |
|---|---|---|
| `DATABRICKS_HOST` | Hostname workspace Databricks | ✅ |
| `DATABRICKS_HTTP_PATH` | HTTP path của SQL Warehouse | ✅ |
| `DATABRICKS_CLIENT_ID` | Service Principal Application ID | ✅* |
| `DATABRICKS_CLIENT_SECRET` | Service Principal OAuth Secret | ✅* |
| `DATABRICKS_CATALOG` | Unity Catalog name | ✅ |
| `DATABRICKS_SCHEMA` | Schema chứa tables | ✅ |
| `LLM_PROVIDER` | `gemini` hoặc `openai` | ✅ |
| `GEMINI_API_KEY` | Google Gemini API key | ✅** |
| `GEMINI_MODEL` | Model name (default: `gemini-2.5-flash`) | |
| `SQL_MAX_LIMIT` | Max rows per query (default: 1000) | |

> \* Hoặc dùng `DATABRICKS_TOKEN` (Personal Access Token) thay cho Service Principal  
> \** Bắt buộc khi `LLM_PROVIDER=gemini`

---

<a id="-api-reference"></a>
## 📡 API Reference

### Health & Schema

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/api/v1/health` | Health check (lightweight) |
| `GET` | `/api/v1/health?deep=true` | Deep health check (test LLM connection) |
| `GET` | `/api/v1/schema` | Lấy thông tin schema Databricks |

### Chat & Query

| Method | Endpoint | Mô tả |
|---|---|---|
| `POST` | `/api/v1/chat/query` | Truy vấn đồng bộ (JSON response) |
| `POST` | `/api/v1/chat/query/stream` | Truy vấn streaming (SSE real-time) |
| `POST` | `/api/v1/chat/route` | Chỉ phân loại intent (không thực thi) |

**Request body:**

```json
{
  "question": "Top 5 thành phố có nhiều khách hàng nhất?"
}
```

**Response format:**

```json
{
  "question": "Top 5 thành phố có nhiều khách hàng nhất?",
  "current_agent": "sql",
  "answer": "Dựa trên dữ liệu, 5 thành phố có nhiều khách hàng nhất là...",
  "generated_sql": "SELECT ... FROM ... LIMIT 5",
  "data": [{"city": "sao paulo", "count": 15540}, ...],
  "row_count": 5,
  "visualization_recommendation": {
    "chart_type": "bar",
    "x": "city",
    "y": "count",
    "title": "Top 5 thành phố theo số khách hàng"
  },
  "error": null
}
```

---

<a id="-bảo-mật"></a>
## 🛡 Bảo mật

- **Read-only policy**: Chặn mọi yêu cầu `INSERT`, `UPDATE`, `DELETE`, `DROP` ở cả 2 tầng (NL detection + SQL validation)
- **SQL Sanitize**: Loại bỏ comments, nested queries nguy hiểm, giới hạn `LIMIT`
- **No credentials in code**: Tất cả secrets qua biến môi trường (`.env`)
- **CORS configurable**: Có thể restrict origins trong production

---

<a id="-cấu-trúc-dự-án"></a>
## 📁 Cấu trúc dự án

```
ai-agent-data-analyst/
├── backend/                          # FastAPI Backend
│   ├── main.py                       # Entry point, CORS, startup warm-up
│   ├── config.py                     # Databricks / LLM / App config
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile
│   ├── routers/
│   │   ├── health.py                 # GET /health, /schema
│   │   └── query.py                  # POST /chat/query, /chat/query/stream
│   ├── services/
│   │   ├── agent_service.py          # Multi-Agent Orchestrator (LangGraph)
│   │   ├── router_agent.py           # Intent classification
│   │   ├── conversation_agent.py     # Conversation handler
│   │   ├── visualize_agent.py        # Chart recommendation
│   │   ├── nlg_agent.py              # Natural language generation
│   │   ├── llm_service.py            # LLM provider factory (Gemini/OpenAI)
│   │   ├── query_result_parser.py    # Raw result → JSON parser
│   │   └── schema_service.py         # Schema introspection
│   ├── prompts/
│   │   └── system_prompt.txt         # System prompt (27 rules + few-shot examples)
│   ├── utils/
│   │   ├── sql_validator.py          # SQL safety: validate, sanitize, block writes
│   │   └── logger.py                 # Structured logging
│   └── evaluation/                   # Benchmark & Evaluation module
│       ├── sql_eval_runner.py        # Evaluation runner
│       ├── text_to_sql_metrics.py    # CM, EM, EX, VES metrics
│       ├── eval_dataset.json         # 100 test cases (gold SQL)
│       ├── prompt_fix_log.md         # Optimization history (12 rounds)
│       └── reports/                  # Auto-generated evaluation reports
│
├── frontend-react/                   # React 19 + Vite Frontend
│   ├── src/
│   │   ├── App.tsx                   # Root layout (Sidebar + Chat)
│   │   ├── components/
│   │   │   ├── chat/
│   │   │   │   ├── ChatWindow.tsx    # Message list + auto-scroll
│   │   │   │   ├── ChatInput.tsx     # Input bar + message queue
│   │   │   │   └── MessageBubble.tsx # User/AI message renderer
│   │   │   ├── charts/
│   │   │   │   └── DynamicChart.tsx  # Recharts renderer (6 chart types)
│   │   │   └── shared/
│   │   │       ├── Sidebar.tsx       # Session history + grouped by date
│   │   │       ├── DataTable.tsx     # Paginated result table + CSV export
│   │   │       └── SQLViewer.tsx     # Syntax-highlighted SQL viewer
│   │   ├── hooks/
│   │   │   └── useChatStream.ts      # SSE stream handler + task queue
│   │   ├── store/
│   │   │   └── chatStore.ts          # Zustand store + auto-persist sessions
│   │   ├── api/
│   │   │   └── config.ts             # API base URL config
│   │   └── types/                    # TypeScript type definitions
│   ├── Dockerfile                    # Multi-stage: build → nginx
│   ├── nginx.conf                    # Reverse proxy → backend
│   └── package.json
│
├── docs/                             # Team documentation
├── docker-compose.yml                # Full-stack deployment
├── .env.example                      # Environment template
└── README.md
```

---


## 📚 Tài liệu liên quan

| Tài liệu | Đường dẫn |
|---|---|
| Kiến trúc Multi-Agent | [`docs/KIEN_TRUC_CONG_NGHE_MULTI_AGENT.md`](docs/KIEN_TRUC_CONG_NGHE_MULTI_AGENT.md) |
| API Documentation | [`docs/api_docs.md`](docs/api_docs.md) |
| Setup Guide | [`SETUP_GUIDE.md`](SETUP_GUIDE.md) |
| Evaluation README | [`backend/evaluation/README.md`](backend/evaluation/README.md) |
| Prompt Optimization Log | [`backend/evaluation/prompt_fix_log.md`](backend/evaluation/prompt_fix_log.md) |

---

<p align="center">
  <sub>Built with ❤️ using LangChain + Databricks + React</sub>
</p>
