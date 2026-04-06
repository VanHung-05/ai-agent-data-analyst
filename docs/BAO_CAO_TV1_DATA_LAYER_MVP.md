# BÁO CÁO TV1 - DATA LAYER & CLOUD (MVP PHASE 1)

## 1. Thông tin chung

- **Môn học:** Kiến trúc hướng dịch vụ và Điện toán đám mây
- **Đề tài:** AI Agent - Smart Data Analyst on Databricks
- **Vai trò báo cáo:** TV1 (Data Engineer & Cloud)
- **Người thực hiện:** Nguyễn Tuấn Anh
- **Thời gian thực hiện:** 30/03/2026 - 02/04/2026
- **Tài liệu đối chiếu chính:**
  - `PROJECT_PLAN_NHIEM_VU.md`
  - `TV1_PLAYBOOK_DATABRICKS.md`

## 2. Mục tiêu TV1 trong kiến trúc dự án

TV1 phụ trách xây dựng tầng dữ liệu trên Databricks để bảo đảm:

1. Hệ thống có **Data Layer** ổn định để Backend truy vấn.
2. **Schema và metadata** đủ rõ ràng để Agent/LLM sinh SQL đúng.
3. Quyền truy cập theo nguyên lý **Least Privilege** (Backend chỉ có quyền đọc dữ liệu).
4. Có bộ bằng chứng (**Evidence**) kiểm thử để nghiệm thu MVP và bàn giao cho TV3/TV5.

**Liên kết với kiến trúc tổng thể:**
- Frontend -> Backend API -> Databricks SQL Warehouse
- **TV1 cung cấp:**
  - Catalog / Schema / Tables
  - Metadata comments (mô tả nghiệp vụ)
  - Security grants (phân quyền)
  - Smoke tests cho Connector

## 3. Phạm vi và phương pháp thực hiện

### 3.1 Phạm vi
- Cấu hình Databricks Workspace + SQL Warehouse.
- Unity Catalog schema: `ai_analyst.ecommerce`.
- 3 bảng Delta cốt lõi: `users`, `products`, `orders`.
- Dữ liệu mẫu (Sample data) để demo phân tích.
- Metadata comment cho từng bảng và cột.
- Phân quyền Read-only thông qua nhóm `backend_readonly`.
- Kiểm tra Runtime Connector bằng Service Principal.

### 3.2 Phương pháp kỹ thuật
- Các script SQL được tổ chức theo quy trình **Idempotent** (có thể chạy lại nhiều lần không lỗi):
  1. Khởi tạo Layer (Catalog/Schema).
  2. Nạp dữ liệu mẫu (Seed Data).
  3. Kiểm tra chất lượng dữ liệu (Data Quality Checks).
  4. Thêm mô tả nghiệp vụ (Business Comments).
  5. Xác minh Metadata Comments.
  6. Cấp quyền Read-only.
  7. Xác minh quyền hạn (Privileges).
  8. Kiểm tra kết nối Backend (Smoke Test).
- Kiểm soát chất lượng theo các tiêu chí (**Quality Gates**):
  - Tính toàn vẹn dữ liệu (Trùng lặp / Mồ côi / Giá trị Null).
  - Tính hợp lệ của miền nghiệp vụ.
  - Bảo mật tối thiểu (Least Privilege).
  - Minh chứng chạy thực tế qua Service Principal.

## 4. Công nghệ và tài nguyên đã sử dụng

- **Nền tảng:** Databricks (SQL Warehouse)
- **Định dạng lưu trữ:** Delta Lake
- **Engine truy vấn:** Databricks SQL
- **Mô hình bảo mật:** Group-based access control (RBAC)
- **Nhóm quyền Backend:** `backend_readonly`
- **Service Principal Backend:** `sp-backend-api`
- **Connector Test:** `databricks-sql-connector` + OAuth Token Flow

## 5. Triển khai thực tế theo từng bước

### 5.1 Bước 1 - Chuẩn bị môi trường
- Đã xác nhận Host của Workspace và Warehouse ID đang hoạt động.
- Xác nhận kết nối SQL cơ bản bằng câu lệnh `SELECT 1`.
- Chốt danh sách đặt tên (Naming Convention):
  - Catalog: `ai_analyst`
  - Schema: `ecommerce`
  - Tables: `users`, `products`, `orders`

### 5.2 Bước 2 - Tạo Data Layer + Seed Data + Quality Gate
- **Scripts:** `sql/01_create_data_layer.sql`, `02_seed_sample_data.sql`, `03_data_quality_checks.sql`.
- **Kết quả nghiệm thu:**
  - Catalog/Schema/Tables tạo thành công.
  - Data Quality Checks đạt: Trùng lặp (PASS), Mồ côi (PASS), Null checks (PASS), Trạng thái miền (PASS).
  - KPI doanh thu theo tháng đạt các mốc: 199.00 (Tháng 1), 338.00 (Tháng 2), 216.00 (Tháng 3).

### 5.3 Bước 3 - Thêm Metadata Business Comments
- **Scripts:** `04_add_business_comments.sql`, `05_verify_metadata_comments.sql`.
- **Kết quả nghiệm thu:**
  - Table comments áp dụng cho 3 bảng.
  - Column comments áp dụng đầy đủ cho 17/17 cột.
  - Thư viện Metadata đọc được qua `information_schema`.
- **Ý nghĩa học thuật:** Tăng cường độ rõ ràng về ngữ nghĩa (Semantic Clarity), giúp giảm thiểu hiện tượng ảo giác (Hallucination) khi AI sinh mã SQL.

### 5.4 Bước 4 - Bảo mật theo nguyên lý Least Privilege
- **Scripts:** `06_grant_readonly_backend.sql`, `07_verify_backend_privileges.sql`.
- **Kết quả nghiệm thu:**
  - Nhóm `backend_readonly` được tạo.
  - Service Principal `sp-backend-api` đã được thêm vào nhóm.
  - Xác nhận quyền: Có quyền `SELECT` trên các bảng; Không có quyền MODIFY/ALL PRIVILEGES.

### 5.5 Bước 5 - Backend Connector + Bàn giao
- **Kết quả nghiệm thu thực tế:**
  - `current_user()` trả về đúng Application ID của Service Principal.
  - Truy vấn `SELECT` thành công.
  - Các lệnh INSERT/UPDATE/DELETE bị từ chối với lỗi `PERMISSION_DENIED`.
  - Row count của bảng `orders` hiện tại là 13 (do có 1 bản ghi test). Đã chuẩn bị script (09) để reset về 12 dòng chuẩn trước khi demo.

## 6. Đối chiếu với PROJECT PLAN

### 6.1 Đối chiếu theo module TV1
- Thiết lập Dataset và bảng dữ liệu: **ĐÃ ĐẠT**.
- Thêm comment nghiệp vụ bảng/cột: **ĐÃ ĐẠT**.
- Unity Catalog phân quyền Backend chỉ SELECT: **ĐÃ ĐẠT**.
- Quản trị Warehouse và tối ưu vận hành: **ĐĐÃ ĐẠT**.

### 6.2 Đối chiếu theo Milestone MVP
- Checkpoint 02/04 (Databricks OK): **ĐẠT**.
- Trạng thái ngày 07/04: **SẴN SÀNG** cho việc tích hợp Backend/Frontend.

## 7. Danh sách Artefacts bàn giao

- **SQL Scripts:** Từ `01` đến `09` (Create, Seed, Quality, Comments, Security, Restore).
- **Tài liệu:** `TV1_PLAYBOOK_DATABRICKS.md`, `TV1_HANDOVER_TV3_TV5.md`, và báo cáo này.

## 8. Đánh giá rủi ro và hướng xử lý

1. **Lộ Secret:** Đã xử lý bằng cách thu hồi Secret cũ, tạo mới và không commit tệp chứa Secret vào Git.
2. **Sai thực thể khi test (Identity):** Đã bổ sung việc kiểm tra `current_user()` trong minh chứng để xác nhận đúng Service Principal.
3. **Lệch dữ liệu gốc (Baseline):** Đã bổ sung script 09 để dọn dẹp dữ liệu test trước khi demo chính thức.

## 9. Bài học rút ra

1. Cần thực chứng bảo mật qua Runtime thực tế thay vì chỉ tin vào câu lệnh Grant trên lý thuyết.
2. Metadata chất lượng cao (Comments) là thành phần cốt lõi giúp AI hiểu đúng dữ liệu.
3. Bàn giao sớm cùng các Smoke Tests giúp giảm đáng kể thời gian tích hợp liên nhóm.

## 10. Kết luận

TV1 đã hoàn thành đầy đủ các mục tiêu kỹ thuật trong phạm vi **Data Layer** cho giai đoạn MVP:
- Tầng dữ liệu ổn định, Schema rõ ràng, Metadata đầy đủ.
- Bảo mật Read-only được xác minh qua Service Principal.
- Tài liệu bàn giao sẵn sàng cho giai đoạn tích hợp hệ thống.

**Trạng thái đề nghị nghiệm thu TV1 (Giai đoạn 1): HOÀN THÀNH.**
