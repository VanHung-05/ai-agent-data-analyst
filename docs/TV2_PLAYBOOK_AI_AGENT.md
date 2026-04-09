# TV2 PLAYBOOK - AI/ML ENGINEER

Tài liệu vận hành dành cho TV2: cách phát triển, kiểm thử, debug và bàn giao module AI Agent trong dự án.

---

## 1) Phạm vi trách nhiệm TV2

TV2 làm việc chủ yếu trên:

- `backend/services/agent_service.py`
- `backend/services/llm_service.py`
- `backend/services/router_agent.py`
- `backend/services/conversation_agent.py`
- `backend/services/visualize_agent.py`
- `backend/services/nlg_agent.py`
- `backend/services/query_result_parser.py`
- `backend/prompts/system_prompt.txt`
- `backend/utils/sql_validator.py`

Không chỉnh router API (`backend/routers/*`) trừ khi cần thêm endpoint cho luồng AI và đã thống nhất với TV3.

---

## 2) Luồng nghiệp vụ chuẩn

### 2.1 Request/Response

Input:
```json
{ "question": "..." }
```

Output chính:
- `current_agent`
- `routing_info`
- `answer`
- `generated_sql`
- `data`
- `row_count`
- `visualization_recommendation`
- `error`

### 2.2 Processing pipeline

1. Khởi tạo LLM (singleton).
2. Router chọn intent.
3. Conversation short-circuit hoặc vào SQL path.
4. SQL generation -> validate -> execute Databricks.
5. Parse result -> rename columns.
6. Recommend visualization.
7. NLG final answer.

---

## 3) Quy tắc kỹ thuật bắt buộc

### 3.1 SQL Safety

- Chỉ cho phép truy vấn read-only.
- Bắt buộc đi qua SQL validator/sanitizer.
- Không cho phép DML/DDL nguy hiểm.

### 3.2 Prompting

- System prompt phải bám schema thật.
- Không mô tả cột không tồn tại.
- Ưu tiên cột mô tả người dùng hiểu được (không chỉ id).

### 3.3 Error handling

- Retry self-correction tối đa 3 lần cho SQL path.
- Có fallback về Conversation khi thất bại hoàn toàn.

---

## 4) Hướng dẫn phát triển hằng ngày

## 4.1 Chạy backend local

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

## 4.2 Kiểm tra nhanh

- Health nhẹ: `GET /api/v1/health`
- Health sâu: `GET /api/v1/health?deep=true`
- Query chuẩn: `POST /api/v1/chat/query`
- Query stream realtime: `POST /api/v1/chat/query/stream`

## 4.3 Test câu hỏi mẫu

1. SQL thường: "Tổng doanh thu là bao nhiêu?"
2. Visualize line: "Vẽ biểu đồ doanh thu theo tháng năm 2017"
3. Visualize pie: "Vẽ biểu đồ tỷ lệ phương thức thanh toán"
4. Conversation: "Xin chào"
5. Fallback lỗi: câu hỏi cố tình sai ngữ cảnh

---

## 5) Quy tắc Visualize Agent thực chiến

Không vẽ chart nếu dữ liệu không đủ ngữ nghĩa:

- 1 cột duy nhất -> table
- 1 dòng aggregate KPI -> table (không pie 100%)
- Pie chỉ khi >=2 nhóm
- Line/bar/scatter/area cần >=2 điểm

---

## 6) Quy tắc NLG Agent

- Trả lời dựa đúng dữ liệu.
- Không bịa số liệu.
- Súc tích, lịch sự, dễ hiểu.
- Ưu tiên ngôn ngữ theo câu hỏi user.

---

## 7) Checklist trước khi bàn giao PR

- [ ] Code chạy được local
- [ ] Không còn lỗi syntax
- [ ] API response không phá contract
- [ ] SQL safety pass
- [ ] Visualize không vẽ sai case thực tế
- [ ] NLG có fallback
- [ ] Log đủ để debug
- [ ] Docs cập nhật nếu có endpoint/hành vi mới

---

## 8) Anti-pattern cần tránh

1. Gọi LLM không cần thiết trong `/health`.
2. Khởi tạo LLM/DB lặp lại mỗi request.
3. Ép chart type chỉ theo keyword mà không validate data.
4. Parse raw result mà bỏ qua `Decimal(...)`.
5. Đưa logic business vào frontend thay vì backend agent.

---

## 9) Hướng mở rộng sau MVP

- Tool-calling có kiểm soát cho từng agent.
- Telemetry/metrics theo step (latency router/sql/nlg).
- Persistent memory cho chat history.
- Evaluation benchmark cho SQL correctness.
- Guardrails nâng cao cho prompt injection.
