# TV4 Playbook Chi Tiết - Frontend Developer

> **Vai trò:** TV4 - Kỹ sư Frontend & UI/UX
> **Mục tiêu:** Xây dựng giao diện người dùng thân thiện cho AI Agent, cho phép người dùng dễ dàng tương tác với hệ thống phân tích dữ liệu qua ngôn ngữ tự nhiên.

---

## 1. Tiến độ thực thi (Tracking)

Cập nhật lần cuối: 07/04/2026

| Bước | Nội dung công việc | Trạng thái | Bắt đầu | Hoàn thành | Ghi chú Evidence |
|------|------------------|-----------|---------|-----------|-----------------|
| 1 | Khởi tạo Streamlit project structure | Done | 07/04/2026 | 07/04/2026 | frontend/app.py + components/ |
| 2 | Xây dựng Chat UI component | Done | 07/04/2026 | 07/04/2026 | components/chat.py hoàn thành |
| 3 | Xây dựng Result Table component | Done | 07/04/2026 | 07/04/2026 | components/result_table.py hoàn thành |
| 4 | Xây dựng Chart Visualization component | Done | 07/04/2026 | 07/04/2026 | components/charts.py với Plotly |
| 5 | Setup API integration with Backend | In Progress | 07/04/2026 | 07/04/2026 | requests library, error handling |
| 6 | Test end-to-end Frontend ↔ Backend | Not Started | 08/04/2026 | 08/04/2026 | |
| 7 | Styling & UX Polish (Phase 2) | Not Started | 09/04/2026 | 11/04/2026 | |
| 8 | Performance optimization | Not Started | 12/04/2026 | 13/04/2026 | |

### Nhật ký làm việc (Log)

- **07/04/2026:** Tạo Streamlit project với structure hoàn chỉnh - main app.py, components folder với chat, result_table, charts. Cài đặt dependencies (streamlit, plotly, pandas, requests).
- **07/04/2026:** Hoàn thành Chat UI component - hiển thị chat history, text input form, cơ chế clear/save session trong sidebar.
- **07/04/2026:** Hoàn thành Result Table component - convert dữ liệu từ API thành Pandas DataFrame, hiển thị interactive table, thêm download CSV button.
- **07/04/2026:** Hoàn thành Chart Visualization component - auto-detect dữ liệu, sinh biểu đồ phù hợp (bar, line, pie, scatter, metric) bằng Plotly.
- **07/04/2026:** Setup API integration - gọi Backend /chat/query, xử lý lỗi, loading state, error messages thân thiện.

---

## 2. Kiến trúc Frontend (Architecture Overview)

### 2.1 Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND (TV4 - Streamlit)              │
│                     app.py (Main)                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │            Streamlit Session State                │   │
│  │  ┌──────────────────────────────────────────┐   │   │
│  │  │ - chat_history: [messages]               │   │   │
│  │  │ - api_base_url: string                   │   │   │
│  │  │ - last_response: dict                    │   │   │
│  │  │ - health_status: dict                    │   │   │
│  │  └──────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
│                          │                               │
│  ┌───────────────────────┴──────────────────────────┐   │
│  │          Sidebar Components                       │   │
│  │  - Settings (API config)                         │   │
│  │  - Health Check                                  │   │
│  │  - Chat Management (save, clear)                 │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                               │
│  ┌───────────────────────┴──────────────────────────┐   │
│  │        Main Components                            │   │
│  │  ┌──────────────┐  ┌───────────────────────────┐ │   │
│  │  │ chat.py      │  │ result_table.py           │ │   │
│  │  │ Chat input + │  │ - Pandas DataFrame        │ │   │
│  │  │ History      │  │ - Download CSV            │ │   │
│  │  └──────────────┘  │ - Display SQL             │ │   │
│  │                    └───────────────────────────┘ │   │
│  │                                                    │   │
│  │  ┌───────────────────────────────────────────┐   │   │
│  │  │ charts.py                                 │   │   │
│  │  │ - Auto-detect chart type (Plotly)        │   │   │
│  │  │ - Bar, Line, Pie, Scatter, Metric        │   │   │
│  │  └───────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────────┬─────────────────────────────────┘
                         │ HTTP REST API (JSON)
                         ↓
            ┌────────────────────────┐
            │   BACKEND API (TV3)     │
            │   FastAPI              │
            │   Port 8000            │
            │ - /health              │
            │ - /schema              │
            │ - /chat/query          │
            └────────────────────────┘
```

### 2.2 Phân tách trách nhiệm (Separation of Concerns)

**TV4 (Frontend Developer) chịu trách nhiệm:**

- `app.py`: Main Streamlit application, page setup, session state, main logic
- `components/chat.py`: Chat UI component - nhập câu hỏi, hiển thị lịch sử
- `components/result_table.py`: Result display - bảng dữ liệu, tải CSV, SQL code
- `components/charts.py`: Chart visualization - tự động sinh biểu đồ phù hợp
- `requirements.txt`: Frontend dependencies

**Nguyên tắc phối hợp:**

- Frontend gọi Backend API qua `requests` library
- Không chỉnh sửa Backend code
- Xử lý error gracefully trên Frontend

---

## 3. Component Specification Chi Tiết

### 3.1 Chat Component (components/chat.py)

**Chức năng:**
- Hiển thị chat history (messages từ user và AI)
- Input box cho user nhập câu hỏi
- Submit button
- Sidebar controls (save, clear)

**Key Functions:**

```python
def render_chat_interface() -> str | None:
    """
    Render chat UI, return user question nếu user submit
    Returns: question string hoặc None
    """

def add_message_to_history(role: str, content: str):
    """role: 'user' hoặc 'assistant'"""

def get_chat_history() -> list:
    """Trả về danh sách messages"""

def clear_chat_history():
    """Xóa toàn bộ chat history"""
```

**Features:**
- ✅ Hiển thị chat history dạng bubbles
- ✅ Clear trên submit (auto-clear text input)
- ✅ Save session to .txt file
- ✅ Message counter trong sidebar

---

### 3.2 Result Table Component (components/result_table.py)

**Chức năng:**
- Convert list of dicts → Pandas DataFrame
- Hiển thị interactive table
- Cho phép tải kết quả dưới dạng CSV
- Hiển thị SQL query được sinh

**Key Functions:**

```python
def render_result_table(data: list, row_count: int) -> pd.DataFrame | None:
    """
    Render kết quả từ API
    - Auto-paginate nếu > 100 rows
    - Download CSV button
    - Summary stats (rows, columns)
    """

def render_sql_query(sql: str):
    """Hiển thị SQL code block với syntax highlighting"""
```

**Features:**
- ✅ Interactive dataframe (Streamlit's st.dataframe)
- ✅ CSV export
- ✅ Pagination warning nếu quá nhiều data
- ✅ Column count + row count display

---

### 3.3 Chart Visualization Component (components/charts.py)

**Chức năng:**
- Nhận dữ liệu + chart type từ Backend
- Tự động sinh biểu đồ phù hợp bằng Plotly
- Fallback to table nếu không thể vẽ

**Key Functions:**

```python
def recommend_and_render_chart(data: list, chart_type: str, reason: str = ""):
    """
    Main function - dispatch to specific chart renderer
    chart_type: 'bar' | 'line' | 'pie' | 'scatter' | 'metric' | 'table'
    reason: explanation why this chart type (from AI)
    """

def render_bar_chart(df: pd.DataFrame):
    """Biểu đồ cột - so sánh categorical values"""

def render_line_chart(df: pd.DataFrame):
    """Biểu đồ đường - xu hướng theo thời gian"""

def render_pie_chart(df: pd.DataFrame):
    """Biểu đồ tròn - phân bổ tỷ lệ"""

def render_scatter_chart(df: pd.DataFrame):
    """Biểu đồ scatter - tương quan 2 biến"""

def render_metric(df: pd.DataFrame, data: list):
    """Hiển thị metric (số to) - 1 giá trị hoặc nhiều metrics"""
```

**Features:**
- ✅ Auto-detect x, y columns từ dữ liệu
- ✅ Responsive design (use_container_width)
- ✅ Light theme (plotly_light)
- ✅ Error handling + fallback to table

---

### 3.4 Main App (app.py)

**Chức năng:**
- Page setup & config
- Session state management
- Sidebar rendering (settings, health check)
- Main content rendering (chat + results)
- API integration logic

**Key Functions:**

```python
def main():
    """Main entry point"""

def render_sidebar():
    """Sidebar with settings, API config, health status"""

def test_health():
    """GET /health from Backend"""

def render_main_content():
    """Main chat interface + process user input"""

def render_response_section(response):
    """Render API response in tabs (Data, SQL, Chart, Info)"""
```

**Luồng xử lý:**

```
1. User nhập question
2. Add to chat history
3. POST /chat/query to Backend
4. Show loading spinner
5. Receive response
6. Add AI message to history
7. Render response in tabs
```

---

## 4. API Integration

### 4.1 Backend API Endpoints (được gọi từ Frontend)

| Endpoint | Method | Purpose | Response |
|----------|--------|---------|----------|
| `/health` | GET | Test connection | Status của API, Databricks, LLM |
| `/schema` | GET | Lấy database schema | Metadata (tables, columns, types) |
| `/chat/query` | POST | Gửi câu hỏi, nhận kết quả | SQL + data + chart recommendation |

### 4.2 Request/Response Examples

**Query Request:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/chat/query",
    json={"question": "Top 5 sản phẩm?"},
    timeout=30
)
data = response.json()
```

**Query Response:**
```json
{
  "question": "Top 5 sản phẩm?",
  "generated_sql": "SELECT product_id, COUNT(*) as count FROM orders GROUP BY product_id ORDER BY count DESC LIMIT 5",
  "data": [
    {"product_id": "P001", "count": 150},
    {"product_id": "P002", "count": 120}
  ],
  "row_count": 5,
  "visualization_recommendation": {
    "chart_type": "bar",
    "reason": "Comparison of product sales counts"
  },
  "error": null
}
```

**Error Response:**
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

### 4.3 Error Handling

**Handle các loại lỗi:**

1. **Connection Error**: Backend không chạy
   ```python
   except requests.exceptions.ConnectionError:
       st.error("🔌 Cannot connect to backend")
   ```

2. **Timeout**: Query quá lâu (> 30s)
   ```python
   except requests.exceptions.Timeout:
       st.error("⏱️ Request timeout")
   ```

3. **API Error**: Response không phải 200
   ```python
   if response.status_code != 200:
       st.error(f"API Error: {response.status_code}")
   ```

4. **Data Error**: Không thể parse response
   ```python
   try:
       data = response.json()
   except json.JSONDecodeError:
       st.error("Invalid response format")
   ```

---

## 5. Streamlit Features & Best Practices

### 5.1 Session State (st.session_state)

Dùng để lưu trữ dữ liệu giữa reruns:

```python
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sử dụng
st.session_state.chat_history.append(msg)
```

### 5.2 Forms (st.form)

Dùng để group input + submit button:

```python
with st.form(key="chat_form", clear_on_submit=True):
    question = st.text_input("Question:")
    submit = st.form_submit_button("Submit")
    if submit and question:
        # Process question
```

**Benefit:** Auto-clear input sau khi submit

### 5.3 Columns & Containers

Layout đa-cột:

```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rows", 1000)
with col2:
    st.metric("Columns", 10)
```

### 5.4 Tabs

Nhóm content:

```python
tab1, tab2, tab3 = st.tabs(["Data", "SQL", "Chart"])
with tab1:
    st.dataframe(df)
with tab2:
    st.code(sql, language="sql")
```

### 5.5 Spinner & Progress

Loading indicators:

```python
with st.spinner("Processing..."):
    response = requests.post(...)
    
st.progress(0.5)
```

---

## 6. Hướng dẫn Vận hành

### 6.1 Cài đặt môi trường

**Bước 1: Clone repository**

```bash
git clone <repo-url>
cd frontend
```

**Bước 2: Tạo virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# hoặc
.venv\Scripts\activate  # Windows
```

**Bước 3: Cài đặt dependencies**

```bash
pip install -r requirements.txt
```

### 6.2 Chạy Frontend Server

```bash
streamlit run app.py
```

**Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 6.3 Chạy Both Backend + Frontend

**Terminal 1 (Backend):**
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
source .venv/bin/activate
streamlit run app.py
```

Truy cập:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000/api/v1
- Backend Docs: http://localhost:8000/docs

---

## 7. Testing Strategy

### 7.1 Manual Testing Scenarios

**Scenario 1: Basic Query**
- Input: "Có bao nhiêu đơn hàng?"
- Expected: Table với 1 row, 1 column (count)
- Chart: Metric card hiển thị số

**Scenario 2: Top N Query**
- Input: "Top 10 sản phẩm?"
- Expected: Table với 10 rows
- Chart: Bar chart tự động

**Scenario 3: Error Handling**
- Input: "DROP TABLE orders"
- Expected: Error message từ Backend
- Display: Error trong tab Data

**Scenario 4: Large Result**
- Input: Câu hỏi trả > 100 rows
- Expected: Warning "Quá nhiều dữ liệu"
- Behavior: Chỉ hiển thị 100 dòng đầu

### 7.2 Edge Cases

- [ ] Empty response (row_count = 0)
- [ ] Network timeout
- [ ] API not running
- [ ] Invalid JSON response
- [ ] Very large datasets (>1000 rows)
- [ ] Special characters in data

---

## 8. UI/UX Considerations

### 8.1 Current MVP (Phase 1)

- ✅ Functional chat interface
- ✅ Data table display
- ✅ Auto-generated charts
- ✅ SQL display
- ✅ Loading indicators
- ✅ Error messages
- ✅ Sidebar controls

### 8.2 Phase 2 Improvements

- [ ] Responsive design mobile
- [ ] Dark theme option
- [ ] Better loading animations
- [ ] Keyboard shortcuts
- [ ] Copy-to-clipboard for SQL
- [ ] Pinned favorite queries
- [ ] Theme customization

### 8.3 Accessibility

- [ ] ARIA labels
- [ ] Keyboard navigation
- [ ] Color contrast
- [ ] Mobile responsiveness

---

## 9. Troubleshooting

### Issue 1: "Connection refused"
**Cause:** Backend không chạy
**Solution:** 
```bash
# Terminal khác
cd backend
uvicorn main:app --reload
```

### Issue 2: "ModuleNotFoundError: No module named 'components'"
**Cause:** Chạy từ folder sai
**Solution:** 
```bash
cd frontend
streamlit run app.py  # NOT: streamlit run frontend/app.py
```

### Issue 3: "Matplotlib figures cannot be pickled"
**Cause:** Plotly chart rendering issue
**Solution:** Use `use_container_width=True` và `height` parameter

### Issue 4: Port 8501 already in use
**Solution:** 
```bash
streamlit run app.py --server.port 8502
```

---

## 10. Phase 2 Roadmap

### Features Planned

- [ ] Advanced filtering UI
- [ ] Saved queries history
- [ ] Query templates
- [ ] Export to multiple formats (PDF, PNG, etc.)
- [ ] Realtime collaboration (multiple users)
- [ ] Dark mode
- [ ] Mobile app (React Native)
- [ ] Voice input for queries

### Performance Optimizations

- [ ] Cache chart rendering
- [ ] Lazy load large dataframes
- [ ] Reduce API calls
- [ ] Client-side filtering

---

## 11. Kết luận

Frontend (TV4) đã hoàn thành MVP với:

✅ **Streamlit Application** - Clean, modern interface
✅ **Chat Interface** - User-friendly message history
✅ **Data Display** - Interactive tables with export
✅ **Visualizations** - Auto-generated charts (Plotly)
✅ **Error Handling** - Graceful error messages
✅ **API Integration** - Seamless Backend connection
✅ **Session Management** - Save/clear chat history

**Frontend sẵn sàng cho Phase 2 & Production!**

---

## 📞 Support & Questions

Nếu cần hỗ trợ:
1. Check SETUP_GUIDE.md trong frontend/
2. Xem logs: Streamlit console output
3. Debug Backend connection: Check health status in Settings
4. Ask TV3 (Backend) hoặc TV2 (AI) nếu vấn đề nằm ở backend
