# API Documentation

Base URL:
- Local: `http://localhost:8000`
- Prefix: `/api/v1`

---

## 1) Health

### `GET /api/v1/health`

Kiểm tra trạng thái API, Databricks và LLM (lightweight).

Query params:
- `deep` (optional, default `false`)
  - `false`: chỉ check config LLM, không invoke model
  - `true`: kiểm tra sâu, có invoke model

Response 200:

```json
{
  "status": "ok",
  "services": {
    "api": "healthy",
    "databricks": "healthy",
    "llm": "healthy"
  },
  "errors": {
    "databricks": null,
    "llm": null
  }
}
```

---

## 2) Schema

### `GET /api/v1/schema`

Trả metadata schema hiện tại từ Databricks.

Response 200 (rút gọn):

```json
{
  "catalog": "ai_analyst",
  "schema": "ecommerce",
  "tables": ["olist_orders", "olist_order_items"],
  "table_info": "..."
}
```

---

## 3) Chat Query (JSON)

### `POST /api/v1/chat/query`

Nhận câu hỏi tự nhiên và trả kết quả hoàn chỉnh.

Request:

```json
{
  "question": "Top 10 danh mục doanh thu cao nhất"
}
```

Response 200:

```json
{
  "question": "Top 10 danh mục doanh thu cao nhất",
  "current_agent": "sql",
  "routing_info": {
    "intent": "sql",
    "scores": {
      "conversation": 0.0,
      "sql": 1.0,
      "visualize": 0.0
    },
    "selected_agents": ["sql"],
    "routing_method": "llm"
  },
  "answer": "Danh mục ...",
  "generated_sql": "SELECT ... LIMIT 1000",
  "data": [
    {"category": "housewares", "revenue": 12345.67}
  ],
  "row_count": 1,
  "visualization_recommendation": {
    "chart_type": "table",
    "x": null,
    "y": null,
    "title": null,
    "reason": "Single-row aggregate (KPI) -> table"
  },
  "error": null
}
```

Failure (vẫn 200 nhưng có `error`):

```json
{
  "question": "...",
  "current_agent": "conversation",
  "routing_info": {},
  "answer": "Xin lỗi...",
  "generated_sql": null,
  "data": [],
  "row_count": 0,
  "visualization_recommendation": {
    "chart_type": "conversation"
  },
  "error": "Thất bại sau 3 lần: ..."
}
```

---

## 4) Chat Query Streaming (SSE)

### `POST /api/v1/chat/query/stream`

Trả progress realtime theo event stream + kết quả cuối.

Request body giống `/chat/query`.

Event format:

```text
data: {"type":"progress","step":"router","message":"Router Agent phân loại intent..."}

data: {"type":"progress","step":"sql_execute","message":"Thực thi truy vấn SQL..."}

data: {"type":"result","data":{...QueryResponse...}}

data: {"type":"done"}
```

Các `step` thường gặp:
- `llm_init`
- `router`
- `conversation`
- `db_connect`
- `sql_generate`
- `sql_execute`
- `visualize`
- `nlg`
- `done`

---

## 5) Route Debug

### `POST /api/v1/chat/route`

Chỉ chạy router để debug intent.

Request:

```json
{ "question": "vẽ biểu đồ doanh thu theo tháng" }
```

Response:

```json
{
  "question": "vẽ biểu đồ doanh thu theo tháng",
  "routing_info": {
    "intent": "visualize",
    "scores": {
      "conversation": 0.0,
      "sql": 0.1,
      "visualize": 0.9
    },
    "selected_agents": ["visualize"],
    "routing_method": "llm"
  }
}
```

---

## 6) Root

### `GET /`

Response 200:

```json
{
  "message": "🤖 AI Agent — Smart Data Analyst API is running!"
}
```

---

## 7) HTTP lỗi chung

- `500 Internal Server Error`

```json
{
  "detail": "<error detail>"
}
```

---

## 8) Ghi chú quan trọng

- SQL luôn đi qua validator/sanitizer trước khi chạy.
- Pipeline ưu tiên read-only, chặn lệnh nguy hiểm.
- `/health` mặc định không invoke model để giảm chi phí và tăng tốc UI.
- Frontend có thể dùng `/chat/query` hoặc `/chat/query/stream` tùy nhu cầu realtime.
