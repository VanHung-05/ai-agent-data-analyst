# TV2 Playbook Chi Tiết - AI / ML Engineer

> **Vai trò:** TV2 - Kỹ sư AI & LangChain
> **Mục tiêu:** Xây dựng Engine trí tuệ nhân tạo (AI Agent) có khả năng xử lý ngôn ngữ tự nhiên thành luồng truy vấn SQL chính xác, tự động tương tác an toàn với Databricks và cung cấp dữ liệu cho tầng Backend API.

---

## 1. Tiến độ thực thi (Tracking)

Cập nhật lần cuối: 04/04/2026

| Bước | Nội dung công việc | Trạng thái | Bắt đầu | Hoàn thành | Ghi chú Evidence |
|---|---|---|---|---|---|
| 1 | Khởi tạo kiến trúc Backend & Cài đặt môi trường | Done | 04/04/2026 | 04/04/2026 | Đã thiết lập venv, kiến trúc Microservices, cài đặt databricks-sql-connector, langchain, fastapi. |
| 2 | Setup System Prompt & Rule An toàn cốt lõi | Done | 04/04/2026 | 04/04/2026 | Đã áp dụng quy tắc vào `.cursorrules`, chặn hàm DML, tự động thêm hằng số `LIMIT 1000`. |
| 3 | Tích hợp xác thực tĩnh (Databricks OAuth M2M) | Done | 04/04/2026 | 04/04/2026 | Cập nhật `config.py` đọc Service Principal do TV1 bàn giao. |
| 4 | Trích xuất Schema Metadata vào LLM | Done | 04/04/2026 | 04/04/2026 | Đã cập nhật `system_prompt.txt` với schema Olist chi tiết (8 bảng, quan hệ PK-FK, business logic). |
| 5 | Tích hợp LLM & Xử lý lỗi kết nối | Done | 04/04/2026 | 04/04/2026 | Chuyển đổi sang Gemini 2.5 Flash SDK mới, sửa lỗi 404 (model deprecated) và 429 (quota). |
| 6 | Test Run: Chạy thử phiên Interactive Mode | Done | 04/04/2026 | 04/04/2026 | Đã nghiệm thu E2E: User nhập câu hỏi -> Gemini gen SQL -> Databricks trả kết quả JSON. |
| 7 | Handover: Chuyển giao AI Service cho TV3 | In-Progress | 04/04/2026 |  | Đang hoàn thiện các hàm wrapper để TV3 gọi API `/query`. |

### Nhật ký làm việc (Log)
- **04/04/2026:** Hoàn thiện tổ chức cấu trúc thư mục quy chuẩn, loại trừ tham chiếu chéo không cần thiết. Thiết lập `.gitignore` loại trừ file cấu hình `.env` nội bộ và đẩy `.env.example` làm tiêu chuẩn môi trường cho nhóm.
- **04/04/2026:** Tiếp nhận gói bàn giao System API Keys từ TV1. Triển khai thuật toán xác thực M2M OAuth tĩnh trực tiếp vào `config.py` & `sql_executor.py` để tự động hóa quy trình xin cấp Token trên Databricks.
- **04/04/2026:** Nâng cấp bộ não AI: Tích hợp **Google Gemini 2.0 Flash** thông qua SDK chính chủ (`google-genai`), khắc phục hoàn toàn lỗi 404 của thư viện LangChain cũ. Xây dựng class wrapper để giữ tính tương thích với LangChain chains.
- **04/04/2026:** Thiết kế hệ thống Prompt chi tiết dựa trên bộ dữ liệu **Olist Brazilian E-Commerce (Kaggle)**. Hệ thống hiện đã nhận diện được 8 bảng chính, hiểu sâu về logic doanh thu (Revenue), trạng thái đơn hàng và hỗ trợ đa ngôn ngữ (Việt, Anh, Bồ Đào Nha).
- **04/04/2026:** Hoàn thiện bộ lọc đầu ra (Post-processing): Tự động cắt bỏ các prefix dư thừa (`SQLQuery:`, `SQLResult:`, `Answer:`) và làm sạch SQL comment để vượt qua vòng kiểm duyệt bảo mật (Validation Gate) mà không làm mất tính đúng đắn của câu lệnh.
- **04/04/2026:** Triển khai **Interactive Mode** cho phép test Agent trực tiếp qua giao diện dòng lệnh (CLI), sẵn sàng cho việc đóng gói thành API endpoint cho TV3/TV4.

---

## 2. Quy trình Xử lý nghiệp vụ của AI (SOP - Core Logic)
... (Giữ nguyên phần cũ) ...

---

## 3. Kiến trúc Kỹ thuật (Technical Highlights)

### 3.1 Cấu hình Model & Môi trường
- **Mô hình chính:** `gemini-2.0-flash` (Ưu điểm: Tốc độ cực nhanh, hỗ trợ context window lớn, hiểu schema phức tạp tốt).
- **Thư viện lõi:** `google-genai` (SDK mới nhất), `langchain` (0.3.0), `databricks-sql-connector`.

### 3.2 Cơ chế Self-Correction (Tự sửa lỗi)
Hệ thống tích hợp logic `_retry_with_correction`: Nếu Databricks báo lỗi cú pháp SQL (Syntax Error), Agent sẽ tự động gửi thông báo lỗi ngược lại cho Gemini kèm theo câu hỏi ban đầu để AI tự chẩn đoán và sửa lỗi ngay lập tức (Tối đa 1 lần retry để đảm bảo Performance).

### 3.3 Cơ chế Bảo mật & Kiểm soát (Safety Guards)
- **Read-only Policy:** Chặn mọi từ khóa biến đổi dữ liệu (DML).
- **Comment Strip:** Tự động xóa SQL comments (`--`) trước khi thực thi để tránh các lỗi logic tiềm ẩn và bypass giả (False Positives) trong bộ lọc injection.
- **Limit Enforcement:** Ép `LIMIT 100` trực tiếp vào SQL chain để bảo vệ tài nguyên tính toán của Databricks Warehouse.

---

## 4. Hướng dẫn Vận hành & Kiểm thử (How-to-run)

Dành cho TV2 hoặc Hội đồng chấm đồ án khi muốn chạy độc lập AI Agent:

### Bước 1: Chuẩn bị môi trường
1. Truy cập vào thư mục backend:
   ```bash
   cd backend
   ```
2. Kích hoạt môi trường ảo:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Cài đặt các thư viện mới nhất (đã fix version):
   ```bash
   pip install -r requirements.txt
   ```

### Bước 2: Cấu hình biến môi trường (`.env`)
Đảm bảo file `.env` đã được điền đầy đủ các thông tin sau:
- `GEMINI_API_KEY`: Key lấy từ Google AI Studio.
- `GEMINI_MODEL`:  `gemini-2.5-flash`.
- `DATABRICKS_*`: Các thông tin kết nối Auth M2M do TV1 cung cấp.

### Bước 3: Chạy thử chế độ Tương tác (Interactive Mode)
Chạy file dịch vụ agent để bắt đầu hỏi đáp trực tiếp với AI:
```bash
python services/agent_service.py
```

**Các câu lệnh gợi ý để kiểm thử (Test Cases):**
1. **Dễ:** "Có bao nhiêu khách hàng ở thành phố Sao Paulo?"
2. **Trung bình:** "Top 10 sản phẩm có doanh thu cao nhất năm 2017?"
3. **Khó:** "Tỷ lệ đơn hàng bị hủy theo từng phương thức thanh toán?"
4. **An toàn:** "DROP TABLE olist_orders" (Agent phải báo lỗi và chặn lại).
### Bước 4: Chạy Unit Test & Integration Test (Tự động)
Để chứng minh với Hội đồng rằng mã nguồn AI xử lý lỗi và bảo mật tốt, bạn có thể chạy toàn bộ kịch bản test chúng ta đã viết sẵn:
```bash
pytest
```
*Kết quả sẽ hiển thị 100% Passed (Màu xanh), bao gồm các lỗi injection bị chặn và logic Databricks hoạt động trơn tru.*

---

## 5. Kết luận & Hướng phát triển (Phase 2)
- Tích hợp **Semantic Layer** để giảm thiểu việc LLM tự sinh SQL (tránh sai tên cột).
- Triển khai **Vector Database (ChromaDB)** để xử lý RAG cho Schema nếu số lượng bảng tăng lên >100.
- Xây dựng hệ thống **Evaluation (Ragas/LangSmith)** để chấm điểm độ chính xác của các câu lệnh SQL tự sinh.

### 2.1 Luồng thực thi Text-to-SQL (The AI Flow)
1. **Tiếp nhận Request:** Cổng kết nối từ TV3 (FastAPI) tiếp nhận và chuyển giao Input của người dùng vào module `agent_service.py`.
2. **Tiêm ngữ cảnh (Context / Metadata Injection):** LangChain Agent trích xuất metadata (Tên cột, kiểu dữ liệu, table comment) từ Databricks Unity Catalog thông qua file `schema_service.py` để xây dựng prompt hoàn chỉnh.
3. **Sinh truy vấn SQL (Text-to-SQL):** Công cụ LLM (GPT-4o/DBRX) biên dịch yêu cầu tự nhiên thành SQL thuần (Spark SQL). Runtime tự động đính kèm thêm từ khóa `LIMIT 1000` nhằm giảm thiểu rủi ro quá tải bộ nhớ và tối ưu chi phí (Resource Optimization).
4. **Kiểm duyệt Bảo mật (Validation Gate):** Chặn đứng các câu lệnh vi phạm nguyên lý Read-only qua Regex validator (`sql_validator.py`), hệ thống bóc tách và chối bỏ mọi luồng lệnh mang rủi ro như `DROP`, `DELETE`, `UPDATE`, `INSERT`.
5. **Thực thi và Phản hồi (Query Execution):** Modun gửi luồng truy vấn SQL hợp lệ lên Databricks Cloud SQL Warehouse, thu nhận dữ liệu thô (JSON format) và điều phối về Backend Rest API cho frontend sử dụng.

### 2.2 Các rủi ro hệ thống liên quan và Biện pháp phòng tránh
- **Rủi ro Ảo giác của LLM (Hallucination):** Nguy cơ LLM tạo ra Field / Column không tồn tại trong cấu trúc dữ liệu vật lý.
  - *Biện pháp:* Kỹ thuật Prompt Grounding nghiêm ngặt bằng Data Dictionary đã được chuẩn hóa bởi TV1. Bổ sung kỹ thuật Few-shot prompt bằng các câu truy vấn lý tưởng mẫu (Gold Queries).
- **Rủi ro Tối đa hóa chi phí Token (Token Limit Exceeded):** Gửi lượng data (raw data) quá lớn ngược lại lên LLM hòng phân tích.
  - *Biện pháp:* Khẳng định kiến trúc Agent chỉ giao tiếp định dạng cấu trúc (Schema metadata) lên LLM Endpoint API. Dữ liệu dòng (Data rows) được tải về cục bộ và không phát tán qua bên thứ ba (OpenAI), đảm bảo tuân thủ nghiêm ngặt chuẩn bảo mật Data Privacy và tối ưu chi phí Cloud.

*(Sẽ tiếp tục cập nhật Evidence Log quá trình nghiệm thu các tính năng trong Phase 2...)*
