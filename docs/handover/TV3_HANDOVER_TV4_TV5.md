# TV3 Handover Package cho TV4/TV5

Ngày cập nhật: 07/04/2026
Người bàn giao: TV3 - Kim Đức Trí

## 1) Scope bàn giao

Tài liệu này bàn giao Backend API Layer cho TV4 (Frontend) và TV5 (DevOps/QA), bao gồm:

- Thông tin kết nối Backend API endpoints
- API specification chi tiết (Request/Response schemas)
- OpenAPI documentation tự động
- Error handling và status codes
- Integration examples và best practices
- Testing checklist cho QA

## 2) Thông tin kết nối Backend API

**Development Environment:**

- Base URL: `http://localhost:8000`
- API Prefix: `/api/v1`
- OpenAPI Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

**Production Environment (Phase 2):**

- Base URL: `https://api.yourdomain.com`
- API Prefix: `/api/v1`

## 3) Danh sách Endpoints sử dụng

### Core Endpoints (Phase 1 - ĐÃ HOÀN THÀNH)

**1. Health Check**

```
GET /api/v1/health
```

- Mục đích: Kiểm tra trạng thái hệ thống và dependencies
- Response: JSON với status của API, Databricks, LLM
- Use case: Monitoring, debugging, load balancer health checks

**2. Schema Metadata**

```
GET /api/v1/schema
```

- Mục đích: Lấy metadata database (tables, columns, types, comments)
- Response: JSON với catalog, schema, tables array
- Cache: 5 phút TTL
- Use case: Schema explorer UI, AI context

**3. Query Processing**

```
POST /api/v1/chat/query
```

- Mục đích: Xử lý câu hỏi ngôn ngữ tự nhiên
- Request: `{"question": "string"}`
- Response: JSON với SQL, data, visualization recommendation
- Timeout: 30 giây
- Use case: Main chat interface

### Advanced Endpoints (Phase 2 - CHƯA TRIỂN KHAI)

- `GET /api/v1/chat/sessions` - Lịch sử phiên chat
- `GET /api/v1/chat/sessions/{id}/history` - Chi tiết phiên
- `POST /api/v1/export` - Export CSV/Excel

## 4) API Specification Chi Tiết

### 4.1 Health Check API

**Request:**

```bash
curl http://localhost:8000/api/v1/health
```

**Response (Success):**

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

**Response (Degraded):**

```json
{
  "status": "degraded",
  "services": {
    "api": "healthy",
    "databricks": "unhealthy",
    "llm": "healthy"
  },
  "errors": {
    "databricks": "Connection timeout after 10s",
    "llm": null
  }
}
```

### 4.2 Schema Metadata API

**Request:**

```bash
curl http://localhost:8000/api/v1/schema
```

**Response:**

```json
{
  "catalog": "ai_analyst",
  "schema": "ecommerce",
  "tables": [
    {
      "name": "olist_orders",
      "columns": [
        {
          "name": "order_id",
          "type": "STRING",
          "comment": "Khóa chính của đơn hàng"
        },
        {
          "name": "customer_id",
          "type": "STRING",
          "comment": "FK → olist_customers.customer_id"
        }
      ],
      "ddl": "CREATE TABLE ai_analyst.ecommerce.olist_orders ..."
    }
  ],
  "raw_info": "Full DDL text...",
  "cached_at": 1712345678.9
}
```

### 4.3 Query Processing API

**Request:**

```bash
curl -X POST http://localhost:8000/api/v1/chat/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Top 5 sản phẩm bán chạy nhất?"}'
```

**Response (Success):**

```json
{
  "question": "Top 5 sản phẩm bán chạy nhất?",
  "generated_sql": "SELECT p.product_category_name_english, COUNT(*) as total_sold FROM olist_order_items oi JOIN olist_products p ON oi.product_id = p.product_id GROUP BY p.product_category_name_english ORDER BY total_sold DESC LIMIT 5",
  "data": [
    {"product_category_name_english": "bed_bath_table", "total_sold": 3029},
    {"product_category_name_english": "health_beauty", "total_sold": 2444},
    {"product_category_name_english": "sports_leisure", "total_sold": 2096}
  ],
  "row_count": 5,
  "visualization_recommendation": {
    "chart_type": "bar",
    "x": "product_category_name_english",
    "y": "total_sold",
    "reason": "Comparison detected"
  },
  "error": null
}
```

**Response (Error - SQL Blocked):**

```json
{
  "question": "DROP TABLE orders",
  "generated_sql": null,
  "data": [],
  "row_count": 0,
  "visualization_recommendation": {"chart_type": "table"},
  "error": "Câu lệnh DML bị chặn: Phát hiện lệnh nguy hiểm: DROP"
}
```

**Response (Error - LLM Failed):**

```json
{
  "question": "Câu hỏi không rõ ràng...",
  "generated_sql": null,
  "data": [],
  "row_count": 0,
  "visualization_recommendation": {"chart_type": "table"},
  "error": "Thất bại sau 3 lần thử: LLM quota exceeded"
}
```

## 5) Visualization Recommendation Logic

Backend tự động gợi ý loại biểu đồ dựa trên:

- Cấu trúc dữ liệu (số cột, số dòng)
- Từ khóa trong câu hỏi
- Pattern trong SQL (GROUP BY, date functions)

**Chart Types:**

- `metric`: Single value (1 row, 1 column) - Hiển thị số to
- `bar`: Comparison data (GROUP BY) - Biểu đồ cột
- `line`: Time series (date/month columns) - Biểu đồ đường
- `pie`: Proportions (tỷ lệ, phần trăm) - Biểu đồ tròn
- `table`: Default fallback - Bảng dữ liệu

## 6) Integration Examples

### 6.1 JavaScript/React Example

```javascript
// Query API
async function askQuestion(question) {
  try {
    const response = await fetch('http://localhost:8000/api/v1/chat/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
  
    const data = await response.json();
  
    if (data.error) {
      console.error('Error:', data.error);
      return null;
    }
  
    return {
      sql: data.generated_sql,
      data: data.data,
      chartType: data.visualization_recommendation.chart_type
    };
  } catch (error) {
    console.error('Network error:', error);
    return null;
  }
}

// Usage
const result = await askQuestion('Top 5 sản phẩm?');
if (result) {
  console.log('SQL:', result.sql);
  console.log('Data:', result.data);
  console.log('Chart:', result.chartType);
}
```

### 6.2 Python/Streamlit Example

```python
import requests
import streamlit as st

def ask_question(question: str):
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/chat/query',
            json={'question': question},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return None

# Usage in Streamlit
question = st.text_input("Nhập câu hỏi:")
if st.button("Hỏi"):
    with st.spinner("Đang xử lý..."):
        result = ask_question(question)
      
    if result and not result['error']:
        st.code(result['generated_sql'], language='sql')
        st.dataframe(result['data'])
      
        # Render chart based on recommendation
        chart_type = result['visualization_recommendation']['chart_type']
        if chart_type == 'bar':
            st.bar_chart(result['data'])
        elif chart_type == 'line':
            st.line_chart(result['data'])
    elif result:
        st.error(result['error'])
```

## 7) Error Handling Best Practices

### HTTP Status Codes

- `200 OK`: Request thành công (kể cả khi có error trong response body)
- `422 Unprocessable Entity`: Request body không hợp lệ (Pydantic validation)
- `500 Internal Server Error`: Lỗi server (exception trong xử lý)

### Error Response Format

Tất cả errors đều có format:

```json
{
  "question": "...",
  "generated_sql": null,
  "data": [],
  "row_count": 0,
  "visualization_recommendation": {"chart_type": "table"},
  "error": "Error message here"
}
```

### Common Errors và Xử lý

**1. "Câu lệnh DML bị chặn"**

- Nguyên nhân: LLM sinh SQL có DML keywords
- Xử lý: Hiển thị error, đề xuất user hỏi lại

**2. "Thất bại sau 3 lần thử"**

- Nguyên nhân: LLM quota exceeded hoặc Databricks timeout
- Xử lý: Hiển thị error, retry sau vài giây

**3. "Connection timeout"**

- Nguyên nhân: Databricks hoặc LLM không phản hồi
- Xử lý: Check health endpoint, thông báo user

## 8) Checklist cho TV4 (Frontend)

### Phase 1 MVP

- [ ] Đã test kết nối tới Backend API (health endpoint)
- [ ] Đã hiển thị được schema metadata từ `/schema`
- [ ] Đã gửi được câu hỏi qua `/chat/query`
- [ ] Đã hiển thị được SQL generated
- [ ] Đã hiển thị được data dạng bảng
- [ ] Đã xử lý error gracefully (hiển thị error message)
- [ ] Đã thêm loading state khi chờ response (3-8 giây)
- [ ] Đã test với các câu hỏi mẫu (xem section 10)

### Phase 2 Advanced

- [ ] Đã render biểu đồ theo visualization_recommendation
- [ ] Đã implement lịch sử chat (khi API sessions có)
- [ ] Đã implement export CSV/Excel (khi API có)
- [ ] Đã optimize UX (debounce, cancel requests)

## 9) Checklist cho TV5 (DevOps/QA)

### Testing

- [ ] Đã chạy unit tests: `pytest backend/tests/ -v`
- [ ] Đã verify 14/14 tests passed
- [ ] Đã test health endpoint trả đúng status
- [ ] Đã test query endpoint với câu hỏi hợp lệ
- [ ] Đã test query endpoint với câu hỏi nguy hiểm (DROP, DELETE)
- [ ] Đã test schema endpoint trả đúng metadata
- [ ] Đã test CORS từ Frontend origin
- [ ] Đã test timeout handling (câu hỏi phức tạp)

### Deployment

- [ ] Đã verify Backend chạy được: `uvicorn main:app --reload`
- [ ] Đã verify OpenAPI docs accessible tại `/docs`
- [ ] Đã verify environment variables đầy đủ (.env)
- [ ] Đã verify không commit secrets vào git
- [ ] Đã chuẩn bị Dockerfile cho Backend (Phase 2)
- [ ] Đã chuẩn bị docker-compose.yml (Phase 2)

### Security

- [ ] Đã verify SQL Validator chặn DML
- [ ] Đã verify LIMIT tối đa 1000 rows
- [ ] Đã verify không lộ sensitive info trong error messages
- [ ] Đã verify CORS config (restrict origins trong production)

## 10) Câu hỏi mẫu để test

### Câu hỏi đơn giản (nên thành công)

1. "Có bao nhiêu đơn hàng?"
2. "Có bao nhiêu khách hàng?"
3. "Liệt kê 10 sản phẩm đầu tiên"

### Câu hỏi trung bình (nên thành công)

1. "Top 5 sản phẩm bán chạy nhất?"
2. "Doanh thu theo tháng năm 2017?"
3. "Điểm đánh giá trung bình theo bang?"

### Câu hỏi phức tạp (có thể cần retry)

1. "Tỷ lệ giao hàng trễ theo bang?"
2. "Top 10 người bán có doanh thu cao nhất?"
3. "Phương thức thanh toán nào phổ biến nhất?"

### Câu hỏi nguy hiểm (phải bị chặn)

1. "DROP TABLE orders"
2. "DELETE FROM users WHERE id = 1"
3. "UPDATE orders SET status = 'done'"

## 11) Performance Expectations

**Response Times:**

- Health check: < 1 giây
- Schema metadata (cached): < 100ms
- Schema metadata (uncached): 1-2 giây
- Query processing: 3-8 giây (phụ thuộc LLM)

**Timeouts:**

- Query processing: 30 giây
- Health checks: 10 giây

**Cache:**

- Schema metadata: TTL 5 phút
- Giảm 95% số lần gọi Databricks API

## 12) Troubleshooting Guide

### Issue: "CORS error from Frontend"

**Symptom:** Browser console shows CORS policy error**Solution:**

- Verify Frontend origin
- Check CORS middleware config trong `backend/main.py`
- Hiện tại allow all origins (`*`) cho MVP

### Issue: "Health check returns degraded"

**Symptom:** `/health` shows databricks or llm unhealthy**Solution:**

- Check Backend logs
- Verify Databricks credentials (.env)
- Verify LLM API key (.env)
- Check network connectivity

### Issue: "Query timeout"

**Symptom:** Request takes > 30 seconds**Solution:**

- Câu hỏi quá phức tạp
- LLM response chậm
- Databricks query chậm
- Đề xuất user đơn giản hóa câu hỏi

### Issue: "SQL validation failed"

**Symptom:** Error "Câu lệnh DML bị chặn"**Solution:**

- LLM sinh SQL không an toàn
- Đây là expected behavior (security feature)
- User cần hỏi lại câu hỏi khác

## 13) OpenAPI Documentation

**Access:** `http://localhost:8000/docs`

**Features:**

- Interactive API testing (Try it out)
- Request/Response schemas
- Example values
- Authentication info (Phase 2)

**Khuyến nghị:** TV4 nên dùng Swagger UI để:

- Hiểu rõ API contract
- Test endpoints trước khi integrate
- Debug issues nhanh hơn

## 14) Mẫu .env cho TV4/TV5 (Development)

```env
# Backend API
BACKEND_API_URL=http://localhost:8000

# Databricks (từ TV1)
DATABRICKS_HOST=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/xxxxx
DATABRICKS_CLIENT_ID=your-service-principal-id
DATABRICKS_CLIENT_SECRET=your-service-principal-secret
DATABRICKS_CATALOG=ai_analyst
DATABRICKS_SCHEMA=ecommerce

# LLM (từ TV2)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash

# App Config
APP_ENV=development
APP_PORT=8000
LOG_LEVEL=INFO
SQL_MAX_LIMIT=1000
SQL_QUERY_TIMEOUT=30
```

## 15) Quy tắc bảo mật

- **KHÔNG commit** API keys, secrets vào git
- **KHÔNG log** sensitive data (SQL với PII, credentials)
- **KHÔNG expose** full error stack traces cho user
- **SỬ DỤNG** HTTPS trong production
- **RESTRICT** CORS origins trong production
- **ROTATE** secrets sau demo/presentation

## 16) Next Steps (Phase 2)

**Backend API Enhancements:**

- [ ] Session management API
- [ ] Export API (CSV/Excel)
- [ ] Rate limiting middleware
- [ ] JWT authentication
- [ ] Redis cache thay in-memory

**Frontend Integration:**

- [ ] Implement chart rendering
- [ ] Add conversation history
- [ ] Optimize UX (debounce, cancel)
- [ ] Add error recovery flows

**DevOps:**

- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring & alerting
- [ ] Load testing

## 17) Liên hệ và Support

**TV3 - Kim Đức Trí**

- Role: Backend Developer
- Responsible: API Gateway, Schema Provider, Integration
