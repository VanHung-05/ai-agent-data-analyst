# BAO CAO TV1 - DATA LAYER & CLOUD (MVP PHASE 1)

## 1. Thong tin chung

- Mon hoc: Kien truc huong dich vu va Dien toan dam may
- De tai: AI Agent - Smart Data Analyst on Databricks
- Vai tro bao cao: TV1 (Data Engineer & Cloud)
- Nguoi thuc hien: Nguyen Tuan Anh
- Thoi gian thuc hien: 30/03/2026 - 02/04/2026
- Tai lieu doi chieu chinh:
  - PROJECT_PLAN_NHIEM_VU.md
  - TV1_PLAYBOOK_DATBRICKS.md

## 2. Muc tieu TV1 trong kien truc du an

TV1 phu trach xay dung tang du lieu tren Databricks de bao dam:

1. He thong co Data Layer on dinh de backend query.
2. Schema va metadata du ro de Agent/LLM sinh SQL dung.
3. Quyen truy cap theo least privilege (backend chi doc du lieu).
4. Co bo evidence kiem thu de nghiem thu MVP va handover cho TV3/TV5.

Lien ket voi kien truc tong the:

- Frontend -> Backend API -> Databricks SQL Warehouse
- TV1 cung cap:
  - Catalog/schema/tables
  - Metadata comment
  - Security grants
  - Smoke tests cho connector

## 3. Pham vi va phuong phap thuc hien

### 3.1 Pham vi

- Databricks workspace + SQL Warehouse
- Unity Catalog schema ai_analyst.ecommerce
- 3 bang Delta:
  - users
  - products
  - orders
- Sample data de demo analytics
- Metadata comment table/cot
- Quyen read-only theo group backend_readonly
- Connector runtime test bang service principal

### 3.2 Phuong phap ky thuat

- Cac script SQL duoc to chuc theo pipeline idempotent:
  1. Create layer
  2. Seed data
  3. Data quality checks
  4. Add business comments
  5. Verify metadata comments
  6. Grant read-only
  7. Verify privileges
  8. Backend connector smoke test
- Kiem soat chat luong theo quality gates:
  - Data integrity (duplicate/orphan/null)
  - Business domain validity
  - Security least privilege
  - Runtime proof qua service principal

## 4. Cong nghe va tai nguyen da su dung

- Nen tang: Databricks (SQL Warehouse)
- Storage format: Delta Lake
- Query engine: Databricks SQL
- Security model: Group-based access control
- Nhom quyen backend: backend_readonly
- Service principal backend: sp-backend-api
- Connector test: databricks-sql-connector + OAuth token flow

## 5. Trien khai thuc te theo tung buoc

### 5.1 Buoc 1 - Chuan bi moi truong

Ket qua:

- Da xac nhan workspace host va warehouse hoat dong.
- Da xac nhan ket noi SQL co ban bang SELECT 1.
- Da chot naming convention:
  - Catalog: ai_analyst
  - Schema: ecommerce
  - Tables: users, products, orders

### 5.2 Buoc 2 - Tao Data Layer + Seed + Quality gate

Script:

- sql/01_create_data_layer.sql
- sql/02_seed_sample_data.sql
- sql/03_data_quality_checks.sql

Ket qua nghiem thu:

- Catalog/schema/tables tao thanh cong.
- Data quality checks dat:
  - Duplicate: PASS
  - Orphan: PASS
  - Null checks: PASS
  - Domain status: PASS
- KPI doanh thu theo thang:
  - 2026-01: 199.00
  - 2026-02: 338.00
  - 2026-03: 216.00

### 5.3 Buoc 3 - Metadata business comments

Script:

- sql/04_add_business_comments.sql
- sql/05_verify_metadata_comments.sql

Ket qua nghiem thu:

- Table comments da ap dung cho 3 bang.
- Column comments da ap dung day du 17/17 cot.
- Metadata dictionary doc duoc qua information_schema.

Y nghia hoc thuat:

- Tang semantic clarity cho schema.
- Giam hallucination khi AI sinh SQL.
- Tang kha nang prompt grounding cho TV2/TV3.

### 5.4 Buoc 4 - Security theo least privilege

Script:

- sql/06_grant_readonly_backend.sql
- sql/07_verify_backend_privileges.sql

Ket qua nghiem thu:

- Group backend_readonly duoc tao.
- Service principal sp-backend-api da duoc add vao group.
- Grants xac nhan:
  - Co SELECT tren users/products/orders
  - Khong co MODIFY/ALL PRIVILEGES/MANAGE

### 5.5 Buoc 5 - Backend connector + handover

Script/tai lieu:

- sql/08_backend_connector_smoke_test.sql
- handover/TV1_HANDOVER_TV3_TV5.md
- sp_negative_test.py

Ket qua nghiem thu runtime:

- current_user() tra ve application id cua service principal.
- SELECT query thanh cong (connector activity PASS).
- INSERT/UPDATE/DELETE bi tu choi voi PERMISSION_DENIED MODIFY.
- Security posture dat muc read-only dung muc tieu.

Ghi chu du lieu:

- row_count orders hien tai = 13 do co ban ghi test lich su.
- Neu can reset ve baseline 12, can xoa ban ghi test theo order_id.
- Kiem tra KPI sau cleanup (script 09):
  - 2026-01: 199.00
  - 2026-02: 338.00
  - 2026-03: 216.00

## 6. Doi chieu voi PROJECT PLAN

### 6.1 Doi chieu theo module TV1

Yeu cau trong plan (Khoi 1 - Data Layer):

1. Setup dataset va bang du lieu: DA DAT
2. Them comment nghiep vu table/cot: DA DAT
3. Unity Catalog quyen backend chi SELECT: DA DAT
4. Quan tri warehouse va toi uu van hanh MVP: DA DAT

### 6.2 Doi chieu theo MVP checkpoints

- Checkpoint 02/04 (Databricks OK): DAT
- Milestone MVP data side (07/04): SAN SANG cho backend/frontend tich hop

### 6.3 Doi chieu Definition of Done lien quan TV1

Trang thai hien tai:

- Data Warehouse co >= 3 bang va data mau: DAT
- Schema metadata san sang cho API /schema: DAT
- Security read-only cho backend principal: DAT
- Handover package cho TV3/TV5: DAT

## 7. Danh sach artefacts ban giao

### 7.1 SQL scripts

1. sql/01_create_data_layer.sql
2. sql/02_seed_sample_data.sql
3. sql/03_data_quality_checks.sql
4. sql/04_add_business_comments.sql
5. sql/05_verify_metadata_comments.sql
6. sql/06_grant_readonly_backend.sql
7. sql/07_verify_backend_privileges.sql
8. sql/08_backend_connector_smoke_test.sql
9. sql/09_restore_baseline_after_security_test.sql

### 7.2 Tai lieu

1. TV1_PLAYBOOK_DATBRICKS.md
2. handover/TV1_HANDOVER_TV3_TV5.md
3. handover/TV1_FASTTRACK_E2E_EXECUTION.md
4. BAO_CAO_TV1_DATA_LAYER_MVP.md (tai lieu nay)

## 8. Danh gia rui ro va huong xu ly

1. Rui ro lo secret:
   - Da xay ra trong qua trinh test.
   - Xu ly: revoke secret cu, tao secret moi, khong commit secret.

2. Rui ro sai identity khi test quyen:
   - Da gap truong hop chay bang user ca nhan thay vi service principal.
   - Xu ly: bat buoc ghi nhan current_user() trong evidence runtime.

3. Rui ro lech data baseline do test ghi:
   - Da xuat hien row_count orders = 13 thay vi 12.
   - Xu ly: bo sung script dọn data test neu can truoc demo.

## 9. Bai hoc rut ra

1. Khong chi grant dung quyen, ma phai runtime-proof bang dung principal.
2. Quality gate can duoc xac minh bang so lieu cu the, khong chi "query chay duoc".
3. Metadata chat luong cao la thanh phan cot loi cho text-to-SQL.
4. Handover som giup TV3/TV5 giam thoi gian debug va tang toc do E2E.

## 10. Moc thuc hien TV1 va dan chung hoc thuat

Bang duoi day tong hop cac moc TV1 da thuc hien, doi chieu voi timeline plan va giai thich y nghia ky thuat trong kien truc SOA + Cloud.

| Moc | Noi dung TV1 | Dan chung hoan thanh | Y nghia kien truc | Giai thich dat chuan hoc thuat |
|---|---|---|---|---|
| 30/03 | Khoi tao Databricks workspace va SQL Warehouse | Co host, warehouse id, HTTP path; test `SELECT 1` PASS | Tao endpoint truy van trung tam cho backend | Chung minh he tinh toan san sang truoc khi tao schema |
| 31/03 - 01/04 | Tao Data Layer (catalog/schema/3 bang Delta) + seed data | Script 01, 02; row counts users/products/orders dat muc tieu | Dat nen du lieu cho query phan tich va join | Trien khai theo pipeline idempotent, co quality gate |
| 01/04 | Data quality validation | Script 03; duplicate/orphan/null/domain deu PASS | Dam bao do tin cay du lieu truoc khi LLM sinh SQL | Kiem soat chat luong bang chi so dinh luong, khong danh gia cam tinh |
| 01/04 | Metadata semantics cho AI | Script 04, 05; 17/17 cot co COMMENT | Giup Schema Provider va Prompt Engine hieu nghiep vu | Giam hallucination va tang kha nang grounding cho text-to-SQL |
| 01/04 - 02/04 | Security least privilege cho backend | Script 06, 07; group backend_readonly + SP sp-backend-api; chi co SELECT | Bao ve Data Layer truoc truy cap ghi trai phep | Ap dung nguyen ly least privilege, co verify bang grant metadata |
| 02/04 | Runtime proof bang service principal | `current_user()` la application id SP; INSERT/UPDATE/DELETE bi PERMISSION_DENIED | Xac minh quyen thuc te trong runtime, khong chi tren ly thuyet GRANT | Day la bang chung nghiem thu bao mat co gia tri cao nhat |
| 02/04 | Handover va fast-track E2E cho lien nhom | Tai lieu handover + script smoke test + restore baseline | Dam bao TV3/TV5 tich hop nhanh, giam rui ro tre milestone MVP | Co tai lieu tac nghiep va evidence-run de tai lap tren moi truong demo |

Nhan xet tong hop theo moc:

1. TV1 da di dung thu tu dependency (ha tang -> du lieu -> chat luong -> metadata -> security -> handover).
2. Moi moc deu co artefact ky thuat va evidence nghiem thu, phu hop yeu cau mon hoc.
3. Trang thai tai moc 02/04 cho thay TV1 san sang ho tro E2E milestone 07/04.

## 11. Ket luan

TV1 da hoan thanh day du cac muc tieu ky thuat trong scope Data Layer cho MVP:

- Data layer on dinh, schema ro rang, metadata day du
- Security least privilege da duoc xac minh bang runtime service principal
- Tai lieu handover va smoke tests da san sang cho tich hop lien service

Trang thai de nghi nghiem thu TV1 (Phase 1): HOAN THANH.
