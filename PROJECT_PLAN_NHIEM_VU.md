# 🚀 KẾ HOẠCH DỰ ÁN: AI AGENT — SMART DATA ANALYST ON DATABRICKS

> **Môn học:** Kiến trúc hướng dịch vụ và Điện toán đám mây  
> **Ngày bắt đầu:** 30/03/2026  
> **Deadline:** 15/04/2026 *(16 ngày)*  
> **Số thành viên:** 5 người

---

## 📋 1. TỔNG QUAN DỰ ÁN

### 1.1. Mục tiêu
Xây dựng một **AI Agent** đóng vai trò "Trợ lý phân tích dữ liệu thông minh", cho phép người dùng **không cần biết SQL** vẫn có thể truy vấn và phân tích dữ liệu từ Data Warehouse thông qua **ngôn ngữ tự nhiên** (tiếng Việt/Anh).

### 1.2. Luồng hoạt động chính

```
Người dùng nhập câu hỏi (NL) 
    → Agent Orchestrator nhận yêu cầu
    → Schema Provider cung cấp metadata (tên bảng, cột, kiểu dữ liệu)
    → LLM sinh câu SQL dựa trên prompt + schema
    → SQL được thực thi trên Databricks SQL Warehouse
    → Kết quả trả về dạng bảng / biểu đồ trên Frontend
```

### 1.3. Kiến trúc Microservices (SOA)

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Service 1)                  │
│              Streamlit / React + Chart.js                │
│         ┌──────────────────────────────────┐             │
│         │  Chat UI  │  Result Table/Chart  │             │
│         └──────────────────────────────────┘             │
└────────────────────────┬────────────────────────────────┘
                         │ REST API (HTTP/JSON)
┌────────────────────────▼────────────────────────────────┐
│              AGENT ORCHESTRATOR (Service 2)              │
│                   FastAPI / Flask                        │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ LangChain   │  │ Prompt Engine│  │ SQL Validator  │  │
│  │ Agent Logic │  │              │  │               │  │
│  └──────┬──────┘  └──────────────┘  └───────────────┘  │
└─────────┼───────────────────────────────────────────────┘
          │                          │
    ┌─────▼──────┐          ┌───────▼────────┐
    │  SCHEMA    │          │  DATABRICKS    │
    │  PROVIDER  │          │  SQL WAREHOUSE │
    │ (Service 3)│          │  (Data Layer)  │
    │            │          │                │
    │ Unity      │          │  Delta Lake    │
    │ Catalog API│          │  Tables        │
    └────────────┘          └────────────────┘
```

---

## 🔧 2. CHI TIẾT KỸ THUẬT & PHÂN CÔNG THEO MODULE

### 2.1. Khối 1: Tầng Dữ liệu & Cloud (Data Layer) — Phụ trách: TV1 - **TUẤN ANH**
*Mục tiêu: Xây dựng trung tâm lưu trữ, bảo đảm dữ liệu sạch, có đầy đủ metadata cho AI phân tích.*
- **Công nghệ/Framework:** Databricks (Community / Azure / AWS), Delta Lake, Spark SQL.
- **Nhiệm vụ chi tiết:**
  - Thiết lập Dataset (Ví dụ: E-commerce với Orders, Users, Products).
  - Tối ưu `COMMENT` bằng tiếng Việt/Anh chuẩn mực vào Column của Delta Table để Schema Provider lấy thông tin mớm cho AI.
  - Thiết lập Unity Catalog: Phân quyền rành mạch cho credentials được Backend dùng (chỉ `SELECT`).
  - Quản trị cluster/Warehouse SQL, cấu hình auto-terminate tránh phung phí tài nguyên.

### 2.2. Khối 2: Lõi AI & Agent (AI/ML Engine) — Phụ trách: TV2 - **VĂN HÙNG**
*Mục tiêu: Trái tim của dự án, chịu trách nhiệm hiểu ngữ nghĩa của prompt và chuyển thành mã SQL chuẩn xác.*
- **Công nghệ/Framework:** LangChain (đặc biệt là `create_sql_agent` hoặc custom chain).
- **Mô hình (LLM):** OpenAI GPT-4o (qua API) hoặc Llama-3/DBRX (Databricks Model Serving).
- **Nhiệm vụ chi tiết:**
  - **Prompt Engineering:** Xây dựng `system_prompt.txt` định tuyến (Ví dụ chặn LIMIT lớn, hiểu các quy luật Business logic...).
  - **Few-Shot Prompting:** Tạo danh sách các cặp câu hỏi - SQL chuẩn làm ngữ cảnh cho AI.
  - **Fallback Mechanism:** Setup LangChain tự sửa lỗi (Self-correction) nếu SQL trả về báo sai.
  - Tối ưu ngữ cảnh: Đảm bảo nhồi đúng Schema liên quan vào prompt, không nhét dư thừa gây tốn token chết API.

### 2.3. Khối 3: Backend API & Schema Provider — Phụ trách: TV3 - **ĐỨC TRÍ**
*Mục tiêu: Đóng vai trò là "Nhà ga", điều phối Frontend, AI, Databricks xử lý xuyên suốt bằng REST API.*
- **Công nghệ/Framework:** FastAPI (Python), Uvicorn, SQLAlchemy, Databricks-SQL-Connector.
- **Nhiệm vụ chi tiết:**
  - Xây dựng **Schema Provider**: Móc nối Unity Catalog API lấy Metadata, tạo cơ chế Cache Schema.
  - Xây dựng **API RESTful**: Chuẩn hóa input/output giữa hệ thống (chi tiết bên dưới).
  - **SQL Validator:** Hàm Regex chặn đứng DML (`UPDATE, INSERT, DROP`) trước khi đẩy xuống Databricks.
  - Quản lý dữ liệu session cho Phase 2.

> **📌 ĐẶC TẢ REST API CHI TIẾT (Giao tiếp giữa TV3 và TV4):**
> 
> **Nhóm API Core (Phase 1):**
> - `GET /api/v1/health`: Kiểm tra kết nối AI, Databricks.
> - `GET /api/v1/schema`: Trả sơ đồ cấu trúc Database (Schema, catalogs, tables, columns, type).
> - `POST /api/v1/chat/query`: Nhận `{"question": "..."}`, Trả về `{"generated_sql": "...", "data": [...], "visualization_recommendation": {"chart_type": "bar"}}`.
> 
> **Nhóm API Nâng cao (Phase 2):**
> - `GET /api/v1/chat/sessions`: Lấy danh sách phiên chat củ (làm sidebar history).
> - `GET /api/v1/chat/sessions/{session_id}/history`: Lấy chi tiết lịch sử tin nhắn của 1 phiên.
> - `POST /api/v1/export`: Nhận SQL và xuất trả về streaming file `.csv` / `.xlsx`.

### 2.4. Khối 4: Giao diện người dùng (Frontend) — Phụ trách: TV4 - **NHỰT HÀO**
*Mục tiêu: Xây dựng cầu nối tương tác giữa người dùng và toàn bộ hệ thống.*
- **Công nghệ/Framework:** Streamlit (Phase 1) -> React.js (Phase 2, nếu team đủ lực).
- **Thư viện biểu đồ:** Plotly, Altair, hoặc Chart.js.
- **Đầu vào (Input):** Nhận JSON data, generated SQL, và gợi ý vẽ biểu đồ từ Backend.
- **Nhiệm vụ chi tiết:**
  - Xây dựng ô Chatbox thân thiện để nhập ngôn ngữ tự nhiên (NL).
  - Hiển thị "Loading State" (Spinner) trong lúc chờ AI phân tích (từ 5-10s).
  - Quản lý hiển thị linh hoạt: Thể hiện Dữ liệu (Bảng), Mã SQL (Code snippet), và Biểu đồ tự render dựa trên `chart_type` trả về.
  - Quản lý giao diện Lịch sử phiên chat như ChatGPT (nếu dùng Streamlit thì quản lý qua `st.session_state`).

### 2.5. Khối 5: Vận hành, Triển khai & Kiểm thử (DevOps / QA) — Phụ trách: TV5 - **ANH HUY**
*Mục tiêu: Gói trọn toàn bộ dự án, bảo vệ quy trình làm việc, đảm bảo chạy ổn định trên mọi máy ảo.*
- **Công nghệ/Framework:** Docker, Docker Compose, Git, Postman / PyTest.
- **Nhiệm vụ chi tiết:**
  - Viết `Dockerfile` cho Frontend, Backend, kết nối E2E hoàn chỉnh trong `docker-compose.yml`.
  - Quản lý chung tệp `.env` / Configurations (Không commit API keys).
  - **System QA:** Đóng vai Hacker/User kiểm thử hệ thống qua Postman (VD: Thử SQL Injection, lỗi quá tải).
  - Hỗ trợ báo cáo và tài liệu: Tổng hợp API Docs, Slides, README hướng dẫn thầy cô/chấm thi gõ 1 lệnh `docker-compose up -d`.

---

## 📅 3. PHÂN CHIA PHASE

### ⚡ PHASE 1: MVP — Sản phẩm khả dụng tối thiểu
> **Thời gian:** 30/03 → 07/04 (9 ngày)  
> **Mục tiêu:** Hệ thống chạy được end-to-end: người dùng nhập câu hỏi → nhận kết quả

| # | Công việc | Kết quả cần đạt |
|---|---|---|
| 1.1 | Setup Databricks Workspace + tạo Delta Tables với sample data | Có database với ≥3 bảng, dữ liệu mẫu sẵn sàng |
| 1.2 | Xây dựng Schema Provider — đọc metadata từ Unity Catalog | API `/schema` trả JSON metadata chính xác |
| 1.3 | Xây dựng Agent Orchestrator — tích hợp LLM + LangChain | Nhận câu hỏi NL → sinh SQL → thực thi → trả kết quả |
| 1.4 | Prompt Engineering — thiết kế system prompt + few-shot | LLM sinh SQL chính xác ≥70% các câu hỏi cơ bản |
| 1.5 | Xây dựng Frontend cơ bản (Streamlit) | Chat UI + hiển thị kết quả bảng |
| 1.6 | Kết nối end-to-end: Frontend → Backend → Databricks | Demo được luồng hoàn chỉnh |
| 1.7 | Docker hóa tất cả services + docker-compose | `docker-compose up` chạy toàn bộ hệ thống |

### 🚀 PHASE 2: Nâng cao & Hoàn thiện
> **Thời gian:** 08/04 → 14/04 (7 ngày)  
> **Mục tiêu:** Nâng cấp UX, tính năng, hiệu năng và hoàn thiện báo cáo

| # | Công việc | Kết quả cần đạt |
|---|---|---|
| 2.1 | Trực quan hóa dữ liệu — tự động sinh biểu đồ phù hợp | Kết quả hiển thị biểu đồ (bar, line, pie) tự động |
| 2.2 | Lịch sử hội thoại — lưu và hiển thị các câu hỏi trước | Sidebar hiển thị history, click để xem lại |
| 2.3 | SQL Validation & Security — chặn truy vấn nguy hiểm | Chặn DML, giới hạn LIMIT, timeout |
| 2.4 | Cải thiện Prompt Engineering — multi-turn, xử lý edge cases | Xử lý được câu hỏi mơ hồ, lỗi, tiếng Việt |
| 2.5 | Cải thiện UI/UX — loading states, error handling, responsive | Giao diện mượt mà, thân thiện |
| 2.6 | Kiểm thử toàn diện — unit test, integration test | Test coverage cho các flow chính |
| 2.7 | Viết báo cáo + chuẩn bị slide thuyết trình | Báo cáo đầy đủ + slide demo |
| 2.8 | (Bonus) Export kết quả CSV/Excel | Nút download kết quả |
| 2.9 | (Bonus) Nâng cấp Frontend lên React | Giao diện hiện đại, SPA |
| 2.10 | (Bonus) Auto-scaling demo trên Cloud | Chứng minh khả năng scale |

---

## 👥 4. PHÂN CÔNG NHÓM 5 THÀNH VIÊN

### Vai trò tổng quan

| Thành viên | Vai trò | Phụ trách chính |
|---|---|---|
| **TV1** | 🏗️ Data Engineer & Cloud | Databricks, Delta Lake, Unity Catalog, SQL Warehouse |
| **TV2** | 🤖 AI/ML Engineer | LangChain Agent, Prompt Engineering, LLM integration |
| **TV3** | ⚙️ Backend Developer | FastAPI, API design, Schema Provider, SQL Validation |
| **TV4** | 🎨 Frontend Developer | Streamlit/React UI, biểu đồ, UX |
| **TV5** | 🔧 DevOps & QA + Docs | Docker, deployment, testing, báo cáo, slide |

---

### 📋 BẢNG PHÂN CÔNG CHI TIẾT THEO NGÀY

#### PHASE 1: MVP (30/03 → 07/04)

| Ngày | TV1 🏗️ | TV2 🤖 | TV3 ⚙️ | TV4 🎨 | TV5 🔧 |
|---|---|---|---|---|---|
| **30/03** | Tạo Databricks Workspace, cấu hình cluster | Nghiên cứu LangChain SQL Agent, chọn LLM | Khởi tạo project FastAPI, cấu trúc thư mục | Nghiên cứu Streamlit, thiết kế wireframe | Setup Git repo, cấu trúc monorepo, Dockerfile base |
| **31/03** | Tạo Delta Tables, load sample data (≥3 bảng) | Thiết kế System Prompt v1 | Xây dựng Schema Provider module | Thiết kế mockup UI | Viết docker-compose.yml skeleton |
| **01/04** | Cấu hình Unity Catalog, test SQL Warehouse | Tích hợp LLM API (Databricks/OpenAI) | API `/schema` — trả metadata JSON | Xây dựng Chat UI component | Setup logging & env config |
| **02/04** | Test truy vấn qua databricks-sql-connector | Xây dựng LangChain Agent pipeline | API `/query` — nhận NL, trả kết quả | Xây dựng Result Table component | Viết unit test cho Schema Provider |
| **03/04** | Tối ưu schema, thêm descriptions cho cột/bảng | Few-shot examples, test prompt | Kết nối Backend ↔ Databricks SQL | Kết nối Frontend ↔ Backend API | Test API endpoints (Postman/pytest) |
| **04/04** | Review SQL output, fix data issues | Tinh chỉnh prompt cho accuracy | SQL Validation — chặn DML, LIMIT | Hiển thị SQL generated + loading | Integration test Frontend-Backend |
| **05/04** | *Buffer / hỗ trợ đồng đội* | *Buffer / hỗ trợ đồng đội* | *Buffer / hỗ trợ đồng đội* | *Buffer / hỗ trợ đồng đội* | *Buffer / hỗ trợ đồng đội* |
| **06/04** | Hỗ trợ debug kết nối Cloud | Fix bugs Agent logic | Fix bugs API | Fix bugs UI | Docker compose — chạy E2E |
| **07/04** | ✅ **MVP Demo** — chạy thử E2E toàn nhóm | ✅ **MVP Demo** | ✅ **MVP Demo** | ✅ **MVP Demo** | ✅ **MVP Demo** |

> [!IMPORTANT]
> **Milestone MVP (07/04):** Hệ thống phải chạy được end-to-end bằng `docker-compose up`. Người dùng nhập câu hỏi tiếng Anh → nhận kết quả dạng bảng.

---

#### PHASE 2: Nâng cao & Hoàn thiện (08/04 → 14/04)

| Ngày | TV1 🏗️ | TV2 🤖 | TV3 ⚙️ | TV4 🎨 | TV5 🔧 |
|---|---|---|---|---|---|
| **08/04** | Thêm dataset phức tạp hơn (JOIN nhiều bảng) | Multi-turn conversation context | API lưu lịch sử hội thoại | Tích hợp biểu đồ (Plotly) | Viết test cases toàn diện |
| **09/04** | Tài liệu hóa schema cho báo cáo | Xử lý tiếng Việt, câu hỏi mơ hồ | API export CSV/Excel | Auto-detect loại biểu đồ | Test trên Docker, fix bugs |
| **10/04** | Demo auto-scaling (nếu có trial) | Tối ưu prompt — giảm hallucination | Error handling toàn diện, rate limit | Conversation history sidebar | Performance testing |
| **11/04** | Viết phần Cloud/Databricks trong báo cáo | Viết phần AI/Prompt trong báo cáo | Viết phần Backend/API trong báo cáo | Viết phần Frontend/UX trong báo cáo | Tổng hợp, format báo cáo chung |
| **12/04** | Review báo cáo, bổ sung screenshot | Review + cải thiện accuracy | Code cleanup, API documentation | Polish UI, responsive design | Finalize Docker + README |
| **13/04** | Chuẩn bị demo dataset | Chuẩn bị demo queries mẫu | Chuẩn bị demo API flow | Chuẩn bị demo UI walkthrough | Chuẩn bị slide thuyết trình |
| **14/04** | ✅ **Rehearsal** — tập demo toàn nhóm | ✅ **Rehearsal** | ✅ **Rehearsal** | ✅ **Rehearsal** | ✅ **Rehearsal** |

> [!WARNING]
> **Deadline 15/04:** Ngày 14/04 là ngày cuối cùng để rehearsal. Không để công việc dồn sang ngày 15.

---

## 📁 5. CẤU TRÚC THƯ MỤC DỰ ÁN

```
ai-smart-analyst/
├── docker-compose.yml
├── README.md
├── .env.example
├── .gitignore
│
├── backend/                    # Service 2: Agent Orchestrator
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Environment variables & settings
│   ├── routers/
│   │   ├── query.py            # POST /query endpoint
│   │   └── health.py           # GET /health endpoint
│   ├── services/
│   │   ├── agent_service.py    # LangChain Agent logic
│   │   ├── llm_service.py      # LLM integration (Databricks/OpenAI)
│   │   ├── schema_service.py   # Service 3: Schema Provider
│   │   └── sql_executor.py     # Databricks SQL execution
│   ├── prompts/
│   │   └── system_prompt.txt   # System prompt template
│   ├── utils/
│   │   ├── sql_validator.py    # SQL safety checks
│   │   └── logger.py           # Logging config
│   └── tests/
│       ├── test_query.py
│       └── test_schema.py
│
├── frontend/                   # Service 1: User Interface
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py                  # Streamlit main app
│   ├── components/
│   │   ├── chat.py             # Chat UI component
│   │   ├── result_table.py     # Data table display
│   │   └── charts.py          # Chart visualization
│   └── assets/
│       └── styles.css
│
├── data/                       # Sample data & scripts
│   ├── sample_data/
│   │   └── *.csv
│   └── init_tables.sql         # SQL to create Delta tables
│
└── docs/                       # Documentation
    ├── report.md               # Báo cáo dự án
    ├── api_docs.md             # API documentation
    └── presentation.pptx       # Slide thuyết trình
```

---

## ✅ 6. DEFINITION OF DONE (DoD)

### Phase 1 — MVP ✓
- [ ] Databricks Workspace hoạt động, có ≥3 Delta Tables với dữ liệu mẫu
- [ ] Backend API `/query` nhận câu hỏi NL, trả kết quả SQL + data
- [ ] Backend API `/schema` trả metadata đúng
- [ ] Frontend hiển thị chat box, gửi query, nhận kết quả dạng bảng
- [ ] Toàn bộ hệ thống chạy được bằng `docker-compose up`
- [ ] LLM sinh SQL chính xác ≥70% cho các câu hỏi đơn giản (SELECT, WHERE, GROUP BY)

### Phase 2 — Advanced ✓
- [ ] Biểu đồ tự động (bar/line/pie) dựa trên loại dữ liệu
- [ ] Lịch sử hội thoại hoạt động
- [ ] SQL Validation chặn được câu lệnh nguy hiểm
- [ ] Xử lý lỗi graceful (thông báo lỗi thân thiện)
- [ ] Báo cáo dự án hoàn chỉnh
- [ ] Slide thuyết trình sẵn sàng
- [ ] README.md hướng dẫn cài đặt & chạy

---

## ⚠️ 7. RỦI RO & GIẢI PHÁP

| Rủi ro | Mức độ | Giải pháp |
|---|---|---|
| Databricks trial hết hạn / bị giới hạn | 🔴 Cao | Backup plan: dùng SQLite local + mock schema |
| LLM sinh SQL sai / hallucination | 🟡 TB | Few-shot prompting, SQL validation, fallback query |
| Thành viên không hoàn thành đúng hạn | 🟡 TB | Daily standup 15 phút, deadline từng task rõ ràng |
| Docker không chạy được trên máy cá nhân | 🟢 Thấp | Hỗ trợ cài đặt, dùng Codespaces/Gitpod |
| API key LLM hết quota | 🟡 TB | Dùng Databricks Model Serving (miễn phí trong trial) |

---

## 🤝 8. QUY TẮC LÀM VIỆC NHÓM

### Communication
- **Daily standup:** 15 phút mỗi tối (online) — báo cáo: đã làm gì, sẽ làm gì, khó khăn gì
- **Tool:** Zalo/Discord group chat + Google Meet cho standup
- **Code review:** Mỗi PR cần ít nhất 1 người review

### Git Workflow
- **Branch naming:** `feature/<tên-tính-năng>` (vd: `feature/chat-ui`, `feature/langchain-agent`)
- **Commit message:** Rõ ràng, prefix: `feat:`, `fix:`, `docs:`, `chore:`
- **Main branch:** Protected — chỉ merge qua PR

### Deliverables cho mỗi thành viên
Mỗi thành viên **phải** có:
1. Code đã merge vào `main`
2. Phần báo cáo riêng (viết phần mình phụ trách)
3. Ít nhất 1 slide trong bài thuyết trình

---

## 📞 9. CÁC MỐC KIỂM TRA (Checkpoints)

| Ngày | Checkpoint | Nội dung kiểm tra |
|---|---|---|
| **02/04** | 🔍 Check 1 | Databricks OK? Schema Provider OK? FastAPI skeleton OK? |
| **05/04** | 🔍 Check 2 | Agent sinh SQL được? API hoạt động? Frontend prototype? |
| **07/04** | 🎯 **MVP Demo** | Chạy E2E demo cho cả nhóm |
| **10/04** | 🔍 Check 3 | Biểu đồ OK? History OK? Validation OK? |
| **14/04** | 🎯 **Final Rehearsal** | Tập thuyết trình + demo hoàn chỉnh |
| **15/04** | 🏁 **DEADLINE** | Nộp sản phẩm + báo cáo |

---

> [!TIP]
> **Lời khuyên:** Ưu tiên làm cho luồng E2E chạy được trước (dù đơn giản), rồi mới nâng cấp từng phần. Đừng cầu toàn từng service riêng lẻ mà quên kết nối chúng lại!
