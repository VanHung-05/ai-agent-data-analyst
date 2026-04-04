# TV1 Handover Package cho TV3/TV5

Ngay cap nhat: 02/04/2026
Nguoi ban giao: TV1 - Nguyen Tuan Anh

## 1) Scope ban giao

Tai lieu nay ban giao Data Layer Databricks cho TV3 (Backend) va TV5 (DevOps/QA), bao gom:
- Thong tin ket noi Databricks SQL Warehouse
- Schema da san sang cho text-to-SQL
- Metadata comment da du
- Chinh sach quyen read-only theo least privilege
- Bo query smoke test cho connector/backend

## 2) Thong tin ket noi can cho Backend

- Server hostname: <DATABRICKS_HOST_REDACTED>
- HTTP Path: <DATABRICKS_HTTP_PATH_REDACTED>
- Catalog: ai_analyst
- Schema: ecommerce
- Warehouse ID: c4b9846edf9d97af

## 3) Danh sach bang su dung

- ai_analyst.ecommerce.users
- ai_analyst.ecommerce.products
- ai_analyst.ecommerce.orders

## 4) Cau hinh danh tinh va quyen

- Group read-only: backend_readonly
- Service principal backend: sp-backend-api
- Muc tieu quyen:
  - Duoc: USE CATALOG, USE SCHEMA, SELECT
  - Khong duoc: MODIFY, WRITE, MANAGE, ALL PRIVILEGES

## 5) Thu tu script can tham chieu

1. sql/01_create_data_layer.sql
2. sql/02_seed_sample_data.sql
3. sql/03_data_quality_checks.sql
4. sql/04_add_business_comments.sql
5. sql/05_verify_metadata_comments.sql
6. sql/06_grant_readonly_backend.sql
7. sql/07_verify_backend_privileges.sql
8. sql/08_backend_connector_smoke_test.sql

## 6) Checklist cho TV3 (Backend)

- [ ] Da nhan du thong tin hostname + http path + catalog/schema
- [ ] Da cau hinh env cho backend connector
- [ ] API schema tra metadata bang/cot
- [ ] API query chay thanh cong query dem so dong
- [ ] API query chay thanh cong query join 3 bang
- [ ] API query chay thanh cong query doanh thu theo thang
- [ ] Khi test bang principal backend, lenh ghi bi tu choi

## 7) Checklist cho TV5 (DevOps/QA)

- [ ] Co script smoke test trong pipeline test tai moi truong demo
- [ ] Co test negative (khong duoc INSERT/UPDATE/DELETE)
- [ ] Co luu evidence output khi chay smoke test
- [ ] Khong de lo secret trong repo, logs, screenshot

## 8) Mau env cho TV3 (khong chua secret that)

DATABRICKS_SERVER_HOSTNAME=<DATABRICKS_HOST_REDACTED>
DATABRICKS_HTTP_PATH=<DATABRICKS_HTTP_PATH_REDACTED>
DATABRICKS_CATALOG=ai_analyst
DATABRICKS_SCHEMA=ecommerce
DATABRICKS_CLIENT_ID=<service-principal-client-id>
DATABRICKS_CLIENT_SECRET=<service-principal-client-secret>


$env:DATABRICKS_CLIENT_ID="<DATABRICKS_CLIENT_ID_REDACTED>"
$env:DATABRICKS_CLIENT_SECRET="<ĐÃ_CHE_GIẤU_BẢO_MẬT>"
& "python" "sp_negative_test.py"


## 9) Quy tac bao mat

- Khong commit client secret/token vao git
- Neu secret da lo, revoke ngay va tao secret moi
- Uu tien rotate secret sau demo
- Khuyen nghi su dung service principal thay vi user email
