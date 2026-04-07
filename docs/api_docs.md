# API Documentation (Phase 1)

Base URL:
- Local: http://localhost:8000
- API prefix: /api/v1

## 1. Health

Endpoint:
- GET /api/v1/health

Description:
- Kiem tra trang thai API va ket noi den Databricks + LLM.

Success response (200):

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

Degraded response (200):

```json
{
	"status": "degraded",
	"services": {
		"api": "healthy",
		"databricks": "unhealthy",
		"llm": "healthy"
	},
	"errors": {
		"databricks": "<error detail>",
		"llm": null
	}
}
```

## 2. Schema

Endpoint:
- GET /api/v1/schema

Description:
- Tra ve metadata schema hien tai tu Databricks (catalog, schema, tables, columns).

Success response (200):

```json
{
	"catalog": "ai_analyst",
	"schema": "ecommerce",
	"tables": [
		{
			"name": "orders",
			"columns": [
				{
					"name": "order_id",
					"type": "STRING",
					"comment": "Order identifier"
				}
			],
			"ddl": "CREATE TABLE ..."
		}
	],
	"raw_info": "...",
	"cached_at": 1770000000.0
}
```

Error response (500):

```json
{
	"detail": "<error detail>"
}
```

## 3. Chat Query

Endpoint:
- POST /api/v1/chat/query

Description:
- Nhan cau hoi ngon ngu tu nhien, sinh SQL, kiem tra an toan, thuc thi va tra ket qua.

Request body:

```json
{
	"question": "Top 5 san pham co doanh thu cao nhat"
}
```

Success response (200):

```json
{
	"question": "Top 5 san pham co doanh thu cao nhat",
	"generated_sql": "SELECT ... LIMIT 1000",
	"data": [
		{
			"col_0": "electronics",
			"col_1": 12345.67
		}
	],
	"row_count": 1,
	"visualization_recommendation": {
		"chart_type": "bar",
		"x": "col_0",
		"y": "col_1",
		"reason": "Comparison detected"
	},
	"error": null
}
```

Failure response (200 with error field):

```json
{
	"question": "...",
	"generated_sql": null,
	"data": [],
	"row_count": 0,
	"visualization_recommendation": {
		"chart_type": "table"
	},
	"error": "That bai sau 3 lan thu: <error detail>"
}
```

Server error response (500):

```json
{
	"detail": "<error detail>"
}
```

## 4. Root Endpoint

Endpoint:
- GET /

Description:
- Kiem tra API service da chay hay chua.

Response (200):

```json
{
	"message": "AI Agent - Smart Data Analyst API is running!"
}
```

## 5. Notes for Phase 1

- SQL validation duoc thuc thi truoc khi query xuong Databricks.
- API hien tai uu tien luong read-only (SELECT/CTE).
- CORS dang mo (`allow_origins=["*"]`) de thu nghiem local; can gioi han trong production.
