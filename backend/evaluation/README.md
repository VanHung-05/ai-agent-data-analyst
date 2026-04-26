# Workstream A — SQL Accuracy Evaluation

Bộ benchmark đánh giá chất lượng SQL sinh ra từ Agent theo kế hoạch Phase 2.

---

## 0. Cài đặt môi trường (chạy lần đầu)

> Thực hiện từ thư mục **`backend/`**.

**Bước 1 — Tạo virtual environment:**

```bash
python3 -m venv .venv
```

**Bước 2 — Kích hoạt venv:**

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Sau khi kích hoạt, terminal sẽ hiện `(.venv)` ở đầu dòng.

**Bước 3 — Cài dependencies:**

```bash
pip install -r requirements.txt
```

**Bước 4 — Tạo file `.env`** (copy từ mẫu rồi điền thông tin Databricks + API key):

```bash
cp .env.example .env   # nếu có file mẫu
# hoặc tạo mới và điền các biến cần thiết
```

Các biến bắt buộc trong `.env`:
```env
DATABRICKS_HOST=...
DATABRICKS_HTTP_PATH=...
DATABRICKS_TOKEN=...
GOOGLE_API_KEY=...
```

**Lần sau:** chỉ cần kích hoạt lại venv (Bước 2) trước khi chạy.

---

## 1. Chuẩn bị

File dataset: `evaluation/eval_dataset.json`  
- 100 test cases, 16 category, phân loại easy / medium / hard.
- Mỗi case gồm: `id`, `question`, `gold_sql`, `category`, `difficulty`.
- Runner đọc khóa `"cases"` (định dạng mới) hoặc `"samples"` (tương thích ngược).

Chạy từ thư mục **`backend/`** (không phải `backend/evaluation/`).

---

## 2. Chạy benchmark — mode `sql_only` (khuyên dùng)

Mode này gọi thẳng LLM để sinh SQL, bỏ qua router/visualize → tiết kiệm quota.

```bash
python -m evaluation.sql_eval_runner \
  --dataset evaluation/eval_dataset.json \
  --output-dir evaluation/reports \
  --generator sql_only \
  --min-request-interval-sec 4.2 \
  --generation-max-attempts 5 \
  --estimated-llm-calls-per-sample 1
```

Chạy **tối đa 20 mẫu** để test nhanh:

```bash
python -m evaluation.sql_eval_runner \
  --dataset evaluation/eval_dataset.json \
  --output-dir evaluation/reports \
  --generator sql_only \
  --max-samples 20 \
  --min-request-interval-sec 4.2 \
  --generation-max-attempts 5 \
  --estimated-llm-calls-per-sample 1
```

---

## 3. Chạy benchmark — mode `api`

Gọi qua endpoint `/api/v1/chat/query` (tốn nhiều quota hơn, cần backend đang chạy).

```bash
python -m evaluation.sql_eval_runner \
  --dataset evaluation/eval_dataset.json \
  --output-dir evaluation/reports \
  --generator api \
  --api-url http://localhost:8000/api/v1/chat/query \
  --min-request-interval-sec 4.2 \
  --generation-max-attempts 5 \
  --estimated-llm-calls-per-sample 4
```

> Với quota Gemini 15 req/phút:
> - `sql_only` → `--estimated-llm-calls-per-sample 1` (≈ 4.2s/câu)
> - `api` → `--estimated-llm-calls-per-sample 4` (≈ 16.8s/câu)

---

## 4. Chạy 1 lần duy nhất qua shell script

```bash
chmod +x evaluation/run_eval_once.sh

./evaluation/run_eval_once.sh \
  --dataset evaluation/eval_dataset.json \
  --max-samples 100
```

Script mặc định dùng: `--generator sql_only`, `--generation-max-attempts 3`, `--estimated-llm-calls-per-sample 1`.  
Output sẽ ở: `evaluation/reports/<timestamp>/`

---

## 5. Output

Runner sinh ra 2 file trong thư mục `--output-dir`:

| File | Nội dung |
|------|----------|
| `eval_report.json` | Dữ liệu thô đầy đủ (máy đọc) |
| `eval_report.md`  | Báo cáo Markdown dễ đọc |

---

## 6. Metrics & ý nghĩa

### 6.1 Metrics tổng hợp (Summary)

| Metric | Ý nghĩa | Target |
|--------|----------|--------|
| `ExecutionSuccessRate` | Tỷ lệ câu SQL chạy đúng kết quả hoàn toàn | ≥ 90% |
| `SafetyPassRate` | Tỷ lệ câu SQL không chứa DML nguy hiểm | = 100% |
| `SemanticMatchRate` | Tỷ lệ câu có SemanticScore ≥ 0.8 | ≥ 80% |
| `OverallWeightedScore` | Điểm tổng hợp (xem công thức bên dưới) | ≥ 85% |

**Công thức OverallWeightedScore:**
```
0.35 × ExecutionSuccessRate
+ 0.25 × SafetyPassRate
+ 0.20 × PerformancePassRate
+ 0.20 × AvgSemanticScore
```

### 6.2 Benchmark metrics (Spider / BIRD style)

| Metric | Mô tả | Ghi chú |
|--------|--------|---------|
| **EM** (Exact Match) | Khớp 100% chuỗi SQL sau normalize | Rất khắt khe — khác 1 token = 0 |
| **CM** (Component Match) | So khớp từng mệnh đề SQL (SELECT/WHERE/GROUP BY...) bằng Jaccard similarity, weighted average | Không yêu cầu thứ tự clause |
| **EX** (Execution Accuracy) | 1.0 nếu result set khớp hoàn toàn với gold | Column-order-insensitive + float epsilon |
| **EX_partial** | F1-score dựa trên số dòng khớp (partial credit) | Ví dụ: đúng 8/10 dòng → 0.8 |
| **VES** (Valid Efficiency Score) | `sqrt(T_gold / T_gen)`, cap = 1.0 | Chỉ tính khi EX = 1.0; chuẩn BIRD |

> **VES = 1.0** nghĩa là SQL sinh ra nhanh bằng hoặc nhanh hơn gold SQL → tối ưu.

### 6.3 Metrics per-case (từng test case)

| Field | Ý nghĩa |
|-------|---------|
| `SyntaxPass` | SQL có cú pháp cơ bản hợp lệ (bắt đầu SELECT/WITH, dấu ngoặc cân bằng) |
| `SafetyPass` | Không chứa DROP/DELETE/UPDATE/INSERT/ALTER/TRUNCATE |
| `PerformancePass` | Có LIMIT và giá trị ≤ giới hạn cho phép |
| `SemanticScore` | Điểm ngữ nghĩa tổng hợp: `0.4 × lexical + 0.6 × EX_partial` |
| `EX Diff Analysis` | Báo cáo chi tiết "tại sao EX thất bại": thiếu cột, thừa cột, số dòng sai, sample 3 dòng gold không khớp |

---

## 7. Tất cả tham số CLI

| Tham số | Mặc định | Ý nghĩa |
|---------|----------|---------|
| `--dataset` | `evaluation/eval_dataset.json` | Đường dẫn tới file dataset |
| `--output-dir` | `evaluation/reports` | Thư mục lưu kết quả |
| `--generator` | `sql_only` | Mode sinh SQL: `sql_only` \| `api` \| `process_question` |
| `--api-url` | `http://localhost:8000/api/v1/chat/query` | Endpoint khi dùng mode `api` |
| `--timeout-sec` | `60.0` | HTTP timeout (giây) cho mode `api` |
| `--min-request-interval-sec` | `4.2` | Khoảng cách tối thiểu giữa 2 lần gọi LLM |
| `--generation-max-attempts` | `5` | Số lần retry khi gặp lỗi 429/503 |
| `--estimated-llm-calls-per-sample` | `1` | Ước tính số lần gọi LLM mỗi câu hỏi (dùng để tính rate-limit pacing) |
| `--max-samples` | `0` (= tất cả) | Giới hạn số câu chạy (0 = chạy hết) |
