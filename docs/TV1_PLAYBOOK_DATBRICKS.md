# TV1 Playbook Chi Tiet - Data Engineer & Cloud

> Vai tro: TV1 - Data Engineer & Cloud
> Muc tieu: Xay duoc Data Layer tren Databricks de toan bo he thong AI Agent co the sinh SQL dung, chay an toan, va demo on dinh den ngay deadline.

---

## Tien do thuc thi (Tracking)

Cap nhat lan cuoi: 02/04/2026

| Buoc | Noi dung | Trang thai | Bat dau | Hoan thanh | Ghi chu |
|---|---|---|---|---|---|
| 1 | Chuan bi tai khoan va moi truong Databricks | Done | 01/04/2026 | 01/04/2026 | Da co tai khoan, phan vai, dataset, naming convention va tai lieu tham chieu |
| 2 | Tao catalog/schema/table va nap data | Done | 01/04/2026 | 01/04/2026 | Da hoan thanh tao layer, seed data va vuot quality gate (duplicate/orphan/null/domain) |
| 3 | Them metadata COMMENT cho bang/cot | Done | 01/04/2026 | 01/04/2026 | Da ap dung metadata va xac minh information schema day du 17/17 cot co COMMENT |
| 4 | Setup quyen read-only cho backend | Done | 01/04/2026 | 02/04/2026 | Da cap quyen least privilege qua group va verify SELECT/khong co write privilege |
| 5 | Kiem thu ket noi voi backend + handover | Done | 02/04/2026 | 02/04/2026 | Da co runtime proof bang service principal, write bi tu choi, handover package san sang |

### Nhat ky cap nhat

- 01/04/2026: Kick-off Buoc 1. Muc tieu trong buoc nay la chot duoc ten workspace, catalog/schema theo convention, ten SQL Warehouse, va nguoi so huu tai nguyen.
- 01/04/2026: Da nhan thong tin tai khoan Databricks, phan chia nhiem vu TV1-TV5, va danh sach 2 dataset de lua chon. Chot dataset uu tien cho MVP la Olist Brazilian E-commerce.
- 01/04/2026: Da xac nhan SQL Warehouse thuc te la Serverless Starter Warehouse. Da test truy van `SELECT 1` thanh cong tren SQL Editor.
- 01/04/2026: Bat dau Buoc 2 theo huong production-ready. Da tao 3 script SQL: create data layer, seed sample data, va quality checks de chay theo thu tu.
- 01/04/2026: Hardening script Buoc 2 theo huong idempotent (drop-if-exists truoc khi add constraint) de dam bao chay lai an toan trong moi truong demo.
- 01/04/2026: Bo sung SOP thuc thi Buoc 2 theo chuan hoc thuat (pre-check, execution protocol, validation gate, evidence log).
- 01/04/2026: Execution evidence (user-run) - Pha 1 `01_create_data_layer.sql`: OK. Pha 2 `02_seed_sample_data.sql`: num_affected_rows=12, num_inserted_rows=12 (batch orders insert). Pha 3 KPI output: 2026-01=199.00, 2026-02=338.00, 2026-03=216.00.
- 01/04/2026: Domain check `order_status` PASS voi phan bo: delivered=6, shipped=3, pending=2, cancelled=1.
- 01/04/2026: Null checks PASS - null_user_id=0, null_product_id=0, null_quantity=0, null_unit_price=0, null_order_date=0, null_order_status=0.
- 01/04/2026: Duplicate checks PASS - khong co ban ghi trung lap cho user_id, product_id, order_id (No rows returned).
- 01/04/2026: Orphan checks PASS - truy van chi tiet orphan user/product tra ve `No rows returned`, xac nhan du lieu join key hop le.
- 01/04/2026: Chot Buoc 2 = DONE theo quality gate hoc thuat (duplicate=PASS, orphan=PASS, null=PASS, domain=PASS, KPI smoke test=PASS).
- 01/04/2026: Bat dau Buoc 3. Da tao script `sql/04_add_business_comments.sql` de them COMMENT cho tat ca table/cot theo semantic nghiep vu phuc vu AI text-to-SQL.
- 01/04/2026: Execution evidence (user-run) - `sql/04_add_business_comments.sql` ra OK.
- 01/04/2026: Metadata verification PASS qua information schema dictionary: 17/17 cot cua users/products/orders co COMMENT nghiep vu.
- 01/04/2026: Chot Buoc 3 = DONE.
- 01/04/2026: Bat dau Buoc 4 theo principle of least privilege. Da tao script cap quyen read-only va script verify quyen backend.
- 01/04/2026: Da tao group `backend_readonly` va add service principal `sp-backend-api` vao group.
- 01/04/2026: Da chay `sql/07_verify_backend_privileges.sql`; negative check tra ve `No rows returned` (khong phat hien write/admin privilege).
- 02/04/2026: Structured check PASS - `backend_readonly` co `SELECT` tren 3 bang `users`, `products`, `orders` trong `ai_analyst.ecommerce`.
- 02/04/2026: Chot Buoc 4 = DONE theo cloud security gate.
- 02/04/2026: Bat dau Buoc 5. Da tao script `sql/08_backend_connector_smoke_test.sql` va tai lieu handover `handover/TV1_HANDOVER_TV3_TV5.md`.
- 02/04/2026: Buoc 5 (smoke test analytics) co ket qua doanh thu theo thang: 2026-01=199.00, 2026-02=338.00, 2026-03=216.00.
- 02/04/2026: Buoc 5 connectivity PASS - `connectivity_ok = 1`.
- 02/04/2026: Buoc 5 row counts PASS - users=5, products=8, orders=12.
- 02/04/2026: Buoc 5 join sanity PASS - query join 3 bang tra du 10 dong ket qua hop le.
- 02/04/2026: Negative security test hien tai FAIL - lenh INSERT tra ve `num_inserted_rows = 1`. Can xac minh lai identity thuc thi va quyen hieu luc cua principal backend.
- 02/04/2026: Xac minh identity thuc thi: current_user = nguyentuananhck2005@gmail.com (user ca nhan).
- 02/04/2026: Xac minh grant tren orders: principal `backend_readonly` chi co `SELECT`.
- 02/04/2026: Ket luan tam thoi Buoc 5: can runtime proof bang principal backend (khong phai user ca nhan) de xac nhan INSERT/UPDATE/DELETE bi tu choi.
- 02/04/2026: Runtime proof bang service principal PASS - current_user = application id `<REDACTED>`.
- 02/04/2026: Runtime read test PASS - `SELECT COUNT(*)` tren orders thanh cong (count=13).
- 02/04/2026: Runtime security test PASS - `INSERT`, `UPDATE`, `DELETE` deu bi tu choi voi loi `PERMISSION_DENIED: User does not have MODIFY on Table ai_analyst.ecommerce.orders`.
- 02/04/2026: Ghi chu du lieu: row_count orders = 13 do ton tai ban ghi test lich su; co the don dep bang delete theo `order_id` neu can tra lai baseline 12.
- 02/04/2026: Chot Buoc 5 = DONE.
- 02/04/2026: Tang toc E2E - da bo sung script `sql/09_restore_baseline_after_security_test.sql` de reset baseline sau security tests.
- 02/04/2026: Tang toc E2E - da bo sung huong dan van hanh nhanh `handover/TV1_FASTTRACK_E2E_EXECUTION.md` cho TV3/TV5.
- 02/04/2026: Baseline KPI sau cleanup duoc xac nhan on dinh: 2026-01=199.00, 2026-02=338.00, 2026-03=216.00.

### Checklist Buoc 1 (Day 0)

- [x] Co tai khoan Databricks va xac nhan dang nhap duoc workspace
- [x] Co danh sach thanh vien + vai tro can phan quyen
- [x] Co bo dataset mau (CSV hoac script insert)
- [x] Chot naming convention chung cho project
- [x] Luu thong tin vao tai lieu noi bo de TV3/TV5 cung tham chieu

### Thong tin da cung cap (01/04/2026)

1. Tai khoan Databricks
   - Email: nguyentuananhck2005@gmail.com
   - Mat khau/tokens: <DAP_TOKEN_REDACTED>

2. Phan chia nhiem vu
   - TV1: Nguyen Tuan Anh
   - TV2: Nguyen Van Hung
   - TV3: Kim Duc Tri
   - TV4: Tran Nhut Hao
   - TV5: Nguyen Anh Huy

3. Dataset de xuat
   - Candidate 1: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
   - Candidate 2: https://www.kaggle.com/datasets/vijayuv/onlineretail
   - Lua chon uu tien cho MVP: Olist Brazilian E-commerce (phu hop hon voi mo hinh users/products/orders va de mapping voi schema TV1)

4. Naming convention da chot
   - Catalog: ai_analyst
   - Schema: ecommerce
   - Table: users, products, orders
   - SQL Warehouse (target name): ai_analyst_wh_small
   - SQL Warehouse (thuc te hien tai): Serverless Starter Warehouse

94. Thong tin ket noi Databricks (xac nhan)
   - Workspace Hostname: <DATABRICKS_HOST_REDACTED>
   - Warehouse URL: <DATABRICKS_WH_URL_REDACTED>
   - Connection Details URL: <DATABRICKS_CONN_URL_REDACTED>
   - Warehouse ID: c4b9846edf9d97af
   - Workspace/Org ID: <DATABRICKS_ORG_ID_REDACTED>
   - Smoke test: `SELECT 1` => PASS (tra ve 1 dong)
   - HTTP Path: /sql/1.0/warehouses/c4b9846edf9d97af

5. Tai lieu noi bo de tham chieu
   - Tai lieu tracking chinh: TV1_PLAYBOOK_DATBRICKS.md
   - Script Buoc 2: sql/01_create_data_layer.sql
   - Script seed data: sql/02_seed_sample_data.sql
   - Script quality checks: sql/03_data_quality_checks.sql
   - Script metadata COMMENT: sql/04_add_business_comments.sql
   - Script verify metadata COMMENT: sql/05_verify_metadata_comments.sql
   - Script GRANT read-only backend: sql/06_grant_readonly_backend.sql
   - Script verify backend privileges: sql/07_verify_backend_privileges.sql
   - Script restore baseline sau security test: sql/09_restore_baseline_after_security_test.sql
   - Huong dan fast-track E2E: handover/TV1_FASTTRACK_E2E_EXECUTION.md

### Runbook Buoc 2 (Professional Execution)

Muc tieu hoc thuat va cloud: trien khai Data Layer theo nguyen ly reproducible, idempotent, quality-gated.

1. Chay script tao Data Layer
   - File: sql/01_create_data_layer.sql
   - Ket qua mong doi:
     - Co catalog `ai_analyst`
     - Co schema `ai_analyst.ecommerce`
     - Co 3 Delta tables: `users`, `products`, `orders`
     - Co business constraints cho gia/so luong/order_status

2. Chay script nap sample data
   - File: sql/02_seed_sample_data.sql
   - Ket qua mong doi:
     - Data seed duoc nap thanh cong, khong loi constraint
     - Co du du lieu theo nhieu thang de phuc vu KPI query

3. Chay script quality checks
   - File: sql/03_data_quality_checks.sql
   - Ket qua mong doi:
     - Duplicate key checks tra ve 0 dong
     - Orphan checks = 0
     - Null checks cot nghiep vu trong `orders` = 0
     - Revenue smoke test tra ve ket qua hop ly

4. Ghi lai evidence vao tracking
   - Row counts moi bang
   - Screenshot ket qua quality checks
   - Neu co loi, note root cause + cach khac phuc

### Checklist Buoc 2 (Execution Gate)

- [x] Co bo script SQL theo thu tu thuc thi
- [x] Chay xong `sql/01_create_data_layer.sql` tren Databricks SQL Editor
- [x] Chay xong `sql/02_seed_sample_data.sql` tren Databricks SQL Editor
- [x] Chay xong `sql/03_data_quality_checks.sql` va dat tat ca dieu kien pass
- [x] Cap nhat row counts + evidence vao Nhat ky cap nhat

### Runbook Buoc 3 (Business Metadata for AI)

Muc tieu: chuan hoa metadata de AI hieu ro y nghia cot, join key, va logic KPI khi sinh SQL.

1. Chay script metadata
   - File: sql/04_add_business_comments.sql
   - Ket qua mong doi:
     - Ca 3 bang (`users`, `products`, `orders`) co TABLE COMMENT.
     - Tat ca cot nghiep vu co COLUMN COMMENT.

2. Kiem tra metadata da ap dung
   - Co the dung `DESCRIBE EXTENDED ai_analyst.ecommerce.orders;`
   - Hoac query information schema de doc comment bang/cot.

3. Quy tac chat luong metadata
   - Mo ta ro nghia nghiep vu, khong mo ho.
   - Neu cot co don vi tinh, bat buoc neu don vi.
   - Neu cot tham gia KPI, note dieu kien tinh (vi du trang thai don hop le).

### Checklist Buoc 3 (Execution Gate)

- [x] Tao script COMMENT day du cho 3 bang va toan bo cot
- [x] Chay xong `sql/04_add_business_comments.sql` tren Databricks SQL Editor
- [x] Kiem tra metadata table/cot doc duoc qua DESCRIBE hoac information schema
- [x] Cap nhat evidence vao Nhat ky cap nhat

### Runbook Buoc 4 (Least Privilege Security)

Muc tieu: backend chi co quyen doc du lieu (SELECT), khong duoc tao/sua/xoa doi tuong du lieu.

1. Chon principal cho backend
   - Service principal/group/user danh rieng cho backend query.
   - Tuyet doi khong dung owner account de ket noi API.

2. Chay script cap quyen toi thieu
   - File: sql/06_grant_readonly_backend.sql
   - Bat buoc thay `backend_service_principal` bang principal thuc te truoc khi run.

3. Chay script verify quyen
   - File: sql/07_verify_backend_privileges.sql
   - Kiem tra:
     - Co `USE CATALOG`, `USE SCHEMA`, `SELECT`.
     - Khong co `MODIFY`/`ALL PRIVILEGES`/`MANAGE`.

4. Runtime proof (neu co thong tin dang nhap principal backend)
   - `SELECT` phai thanh cong.
   - Thu `INSERT` phai bi tu choi (permission denied).

### Checklist Buoc 4 (Cloud Security Gate)

- [x] Tao script GRANT theo least privilege
- [x] Tao script verify permission
- [x] Chot principal backend thuc te (service principal/group)
- [x] Chay `sql/06_grant_readonly_backend.sql` thanh cong
- [x] Chay `sql/07_verify_backend_privileges.sql` va xac nhan khong co write privilege
- [x] Luu evidence grant/verify vao Nhat ky cap nhat

### Runbook Buoc 5 (Backend Connector + Handover)

Muc tieu: xac nhan TV3 ket noi duoc Databricks SQL connector bang principal read-only va TV5 co bo kiem thu/evidence de van hanh.

1. Ban giao goi tai lieu cho TV3/TV5
   - File handover: handover/TV1_HANDOVER_TV3_TV5.md
   - File smoke test: sql/08_backend_connector_smoke_test.sql

2. Kiem thu voi TV3
   - Chay baseline query `SELECT 1` qua backend connector.
   - Chay row counts + query join + query doanh thu theo thang.
   - Xac nhan API schema/query tra du lieu that.

3. Kiem thu bao mat voi TV5
   - Thu INSERT/UPDATE/DELETE bang principal backend phai fail.
   - Luu evidence grant/verify/smoke test.

### Checklist Buoc 5 (Execution Gate)

- [x] Tao handover package cho TV3/TV5
- [x] Tao script smoke test ket noi backend
- [x] TV3 test connector thanh cong (schema + query)
- [x] TV5 xac nhan negative security test (write bi tu choi)
- [x] Luu evidence E2E vao Nhat ky cap nhat

### SOP Buoc 2 (Chuan hoc thuat + Cloud)

#### A. Tien dieu kien (Pre-Run Control)

1. Xac nhan SQL Warehouse dang Running va dang chon dung warehouse.
2. Xac nhan context SQL Editor dang o workspace dung (`workspace.default` hoac catalog/schema ban chi dinh).
3. Xac nhan thu tu thuc thi script: 01 -> 02 -> 03 (khong dao thu tu).
4. Xac nhan khong chay song song nhieu query ghi du lieu vao cung bang trong cung thoi diem.

#### B. Quy trinh thuc thi chuan (Execution Protocol)

1. Pha 1 - Provision Data Layer
    - Mo va chay file `sql/01_create_data_layer.sql`.
    - Ky vong he thong:
       - Tao du catalog/schema.
       - Tao du 3 Delta tables.
       - Tao du business constraints.
    - Neu loi:
       - Ghi lai exact error message.
       - Dung quy trinh, khong nhay sang Pha 2.

2. Pha 2 - Data Seeding Co Kiem Soat
    - Mo va chay file `sql/02_seed_sample_data.sql`.
    - Ky vong he thong:
       - Xoa du lieu cu theo thu tu an toan.
       - Nap moi sample data thanh cong.
    - Kiem tra nhanh sau pha 2:
       - `users` co du lieu.
       - `products` co du lieu.
       - `orders` co du lieu.

3. Pha 3 - Validation va Quality Gate
    - Mo va chay file `sql/03_data_quality_checks.sql`.
    - Dieu kien PASS bat buoc:
       - Duplicate key checks tra ve 0 ban ghi.
       - `orphan_user = 0` va `orphan_product = 0`.
       - Null check cot nghiep vu trong `orders` bang 0.
       - Revenue query theo thang tra ket qua hop ly.

#### C. Tieu chi danh gia (Academic Evaluation Criteria)

1. Tinh tai lap (Reproducibility): chay lai toan bo script khong gay loi nghiem trong.
2. Tinh toan ven du lieu (Data Integrity): khong duplicate key, khong orphan key.
3. Tinh dung nghiep vu (Business Validity): domain `order_status` dung tap gia tri quy dinh.
4. Tinh san sang demo (Demo Readiness): KPI query cho ket qua co y nghia phan tich.

#### D. Mau bien ban chay (Execution Evidence Template)

Sao chep mau nay vao Nhat ky cap nhat sau moi lan run:

```
Ngay gio run:
Nguoi thuc hien:
Warehouse su dung:

Pha 1 - Create Layer:
- Trang thai: PASS/FAIL
- Loi (neu co):

Pha 2 - Seed Data:
- Trang thai: PASS/FAIL
- Row counts: users=?, products=?, orders=?

Pha 3 - Quality Checks:
- Duplicate keys: PASS/FAIL
- Orphan keys: PASS/FAIL
- Null checks: PASS/FAIL
- KPI smoke test: PASS/FAIL

Ket luan run:
Hanh dong tiep theo:
```

#### E. Nguyen tac van hanh an toan (Cloud Ops Discipline)

1. Khong commit secret/token vao file SQL hoac markdown.
2. Giu auto stop warehouse de toi uu chi phi.
3. Moi thay doi schema phai co log va thoi diem cap nhat.
4. Moi lan loi phai ghi root cause + corrective action de tai su dung tri thuc cho team.

---

## 1. Ban dang giai quyet bai toan gi?

### 1.1 Muc tieu cua TV1 trong du an
TV1 khong chi "tao bang du lieu". TV1 dang xay phan nen de:
1. AI co du lieu de hoi dap.
2. Backend co schema ro rang de dua vao prompt.
3. He thong chay an toan, tiet kiem chi phi cloud.

Neu TV1 lam dung, ket qua la:
1. TV2 sinh SQL de hon (do schema ro rang, cot co mo ta).
2. TV3 lay metadata nhanh (Schema Provider dung duoc ngay).
3. TV4 demo du lieu len UI muot (khong bi loi schema/data).

### 1.2 Dau ra cuoi cung TV1 phai ban giao
1. Workspace Databricks hoat dong.
2. SQL Warehouse + Cluster duoc cau hinh on.
3. It nhat 3 Delta tables co du lieu mau: users, products, orders.
4. Metadata day du (COMMENT cho bang/cot).
5. Quyen truy cap an toan (credential backend chi SELECT).
6. Tai lieu huong dan ket noi cho TV3/TV5.

---

## 2. Tong quan luong cong viec TV1

1. Chuan bi tai khoan va moi truong Databricks.
2. Tao catalog/schema bang theo convention thong nhat.
3. Nap sample data co logic nghiep vu.
4. Them metadata (COMMENT) cho AI va Schema Provider.
5. Cau hinh Unity Catalog + phan quyen read-only cho backend.
6. Cau hinh SQL Warehouse de toi uu chi phi/doi on dinh.
7. Kiem thu truy van dau-cuoi va ban giao.

Y nghia: Day la chuoi buoc theo dung dependency. Lam sai thu tu se gay loi day chuyen (vi du chua co table ma da test connector, chua co quyen ma da cho backend query).

---

## 3. Chuan bi truoc khi bat dau (Day 0)

## 3.1 Input can co
1. Tai khoan Databricks (Community, AWS, Azure tuy team).
2. Danh sach thanh vien va vai tro can phan quyen.
3. Bo dataset mau (CSV hoac tao bang tay).
4. Quy uoc dat ten du an: catalog, schema, table.

## 3.2 Vi sao buoc nay bat buoc?
Neu bo qua, team se gap:
1. Dat ten loai xon => TV3 map schema kho.
2. Quyen cap nham => backend query fail do permission.
3. Data mau khong co logic => AI sinh SQL khong dung.

## 3.3 Cach lam
1. Tao 1 file note noi bo (Google Doc hoac docs/report) luu:
   - Ten workspace
   - Ten catalog/schema
   - Ten warehouse
   - Nguoi so huu tai nguyen
2. Chot naming convention (vi du):
   - Catalog: `ai_analyst`
   - Schema: `ecommerce`
   - Table: `users`, `products`, `orders`

## 3.4 Dau ra mong doi
1. Team thong nhat mot bo ten duy nhat.
2. Co tai lieu de tat ca thanh vien tham chieu.

---

## 4. Setup Databricks Workspace va SQL Warehouse (Day 1)

## 4.1 Muc dich
Tao moi truong tinh toan va truy van de luu/chay du lieu cho du an.

## 4.2 Nguyen nhan phai lam
Khong co workspace/warehouse thi:
1. Khong tao duoc Delta table.
2. Backend khong co endpoint SQL de ket noi.

## 4.3 Cach lam chi tiet
1. Dang nhap Databricks workspace.
2. Tao SQL Warehouse:
   - Type: Serverless neu co, neu khong dung Pro/classic.
   - Auto stop: 10-15 phut.
   - Kich thuoc: nho nhat du cho demo (Small).
3. Tao Cluster (neu can ETL bang notebook/Spark):
   - Auto terminate 10-20 phut.
   - Runtime phu hop Delta/Spark SQL.
4. Test 1 truy van SQL co ban: `SELECT 1;`

## 4.4 Y nghia tung cau hinh
1. Auto stop/auto terminate:
   - Y nghia: tranh dot tien cloud khi quen tat.
   - Tac dong project: giu budget on den ngay demo.
2. Chon size nho:
   - Y nghia: du cho MVP, tranh overkill.
   - Tac dong project: khoi dong nhanh, de test lien tuc.

## 4.5 Dau ra
1. Warehouse o trang thai Running khi can.
2. Truy van SQL co ban chay thanh cong.

---

## 5. Thiet ke schema du lieu cho AI Agent (Day 1-2)

## 5.1 Muc dich
Tao mo hinh du lieu toi thieu nhung du nghia de AI co the sinh SQL phan tich.

## 5.2 Nguyen nhan
AI sinh SQL dua tren ten bang/cot + metadata. Neu schema mo ho:
1. AI nham join key.
2. AI nham y nghia metric (doanh thu, so don, so user).

## 5.3 De xuat mo hinh 3 bang
1. `users`:
   - user_id, full_name, email, city, created_at
2. `products`:
   - product_id, product_name, category, price, is_active
3. `orders`:
   - order_id, user_id, product_id, quantity, unit_price, order_date, order_status

## 5.4 Y nghia mo hinh
1. `orders` la fact table (su kien mua hang).
2. `users`, `products` la dimension table (thong tin mo ta).
3. Co khoa noi ro rang de AI join:
   - orders.user_id -> users.user_id
   - orders.product_id -> products.product_id

## 5.5 Dau ra
Schema du de hoi dap cac cau:
1. Doanh thu theo thang
2. Top san pham ban chay
3. So don theo thanh pho

---

## 6. Tao catalog/schema/table Delta (Day 2)

## 6.1 Cach lam mau (SQL)
```sql
CREATE CATALOG IF NOT EXISTS ai_analyst;
CREATE SCHEMA IF NOT EXISTS ai_analyst.ecommerce;

CREATE TABLE IF NOT EXISTS ai_analyst.ecommerce.users (
  user_id STRING,
  full_name STRING,
  email STRING,
  city STRING,
  created_at DATE
) USING DELTA;

CREATE TABLE IF NOT EXISTS ai_analyst.ecommerce.products (
  product_id STRING,
  product_name STRING,
  category STRING,
  price DECIMAL(12,2),
  is_active BOOLEAN
) USING DELTA;

CREATE TABLE IF NOT EXISTS ai_analyst.ecommerce.orders (
  order_id STRING,
  user_id STRING,
  product_id STRING,
  quantity INT,
  unit_price DECIMAL(12,2),
  order_date DATE,
  order_status STRING
) USING DELTA;
```

## 6.2 Vi sao dung Delta?
1. Ho tro ACID va schema reliability.
2. Hop voi kien truc Databricks va SQL Warehouse.
3. De bao tri/extend sau nay (time travel, optimize).

## 6.3 Dau ra
1. 3 bang tao thanh cong.
2. Co the `SELECT * FROM ... LIMIT 10` khong loi.

---

## 7. Nap sample data chat luong (Day 2)

## 7.1 Nguyen tac data mau
1. Data phai du da dang de query co y nghia.
2. Co tinh huong thuc te: nhieu city, nhieu category, nhieu ngay.
3. Co du so luong de GROUP BY ra bieu do co nghia.

## 7.2 Nguyen nhan
Neu data xau, AI co sinh SQL dung cung khong tao duoc ket qua dep.

## 7.3 Cach lam
1. Nap tu CSV hoac INSERT tay.
2. Kiem tra sau khi nap:
   - So dong moi bang
   - Null bat thuong
   - Khoa join co match khong

## 7.4 SQL check nhanh
```sql
SELECT COUNT(*) AS users_cnt FROM ai_analyst.ecommerce.users;
SELECT COUNT(*) AS products_cnt FROM ai_analyst.ecommerce.products;
SELECT COUNT(*) AS orders_cnt FROM ai_analyst.ecommerce.orders;

SELECT COUNT(*) AS orphan_user
FROM ai_analyst.ecommerce.orders o
LEFT JOIN ai_analyst.ecommerce.users u ON o.user_id = u.user_id
WHERE u.user_id IS NULL;
```

## 7.5 Dau ra
1. Khong co orphan key nghiem trong.
2. Du lieu du de demo truy van tong hop.

---

## 8. Them metadata COMMENT cho bang va cot (Day 3)

## 8.1 Day la buoc rat quan trong voi AI
AI khong "hieu nghiep vu" nhu con nguoi. COMMENT chinh la cach ban day AI biet nghia cot.

## 8.2 Cach lam
```sql
COMMENT ON TABLE ai_analyst.ecommerce.orders IS
'Bang don hang, luu thong tin giao dich mua san pham cua nguoi dung';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.unit_price IS
'Gia ban 1 don vi san pham tai thoi diem dat hang';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.order_status IS
'Trang thai don hang: pending, shipped, delivered, cancelled';
```

## 8.3 Y nghia
1. TV3 goi schema API se lay duoc mo ta cot.
2. TV2 dua schema vao prompt se giam hallucination.
3. SQL sinh ra sat nghiep vu hon.

## 8.4 Dau ra
1. Tat ca bang/cot quan trong deu co COMMENT.
2. Metadata doc duoc tu information schema hoac catalog API.

---

## 9. Unity Catalog va phan quyen read-only cho Backend (Day 3-4)

## 9.1 Muc dich
Dam bao bao mat: backend chi doc du lieu, khong sua/xoa.

## 9.2 Nguyen nhan
Neu cap quyen rong, neu co bug hoac injection co the gay mat du lieu.

## 9.3 Cach lam tham khao
1. Tao principal/service user cho backend (neu ha tang cho phep).
2. Cap quyen toi thieu:
   - USE CATALOG
   - USE SCHEMA
   - SELECT tren bang can doc
3. Khong cap:
   - INSERT, UPDATE, DELETE, DROP, ALTER

## 9.4 SQL mau cap quyen
```sql
GRANT USE CATALOG ON CATALOG ai_analyst TO `backend_service_principal`;
GRANT USE SCHEMA ON SCHEMA ai_analyst.ecommerce TO `backend_service_principal`;
GRANT SELECT ON TABLE ai_analyst.ecommerce.users TO `backend_service_principal`;
GRANT SELECT ON TABLE ai_analyst.ecommerce.products TO `backend_service_principal`;
GRANT SELECT ON TABLE ai_analyst.ecommerce.orders TO `backend_service_principal`;
```

## 9.5 Dau ra
Credential backend query duoc SELECT, nhung khong the ghi du lieu.

---

## 10. Kiem thu ket noi voi Backend (Day 4)

## 10.1 Muc dich
Xac minh TV3 co the dung databricks-sql-connector truy van that.

## 10.2 Cach lam
1. Ban giao cho TV3:
   - Hostname
   - HTTP path cua warehouse
   - Token/service credential
   - Catalog/schema/table names
2. Cung TV3 test query:
   - `SELECT COUNT(*) FROM ...`
   - 1 query join users-orders-products

## 10.3 Y nghia
Day la diem noi giua Data Layer va Backend. Neu fail o day, E2E se dung.

## 10.4 Dau ra
1. API `/schema` doc duoc metadata.
2. API `/query` lay duoc data that tu Databricks.

---

## 11. Toi uu va on dinh truoc MVP demo (Day 4-7)

## 11.1 Viec can lam
1. Rasoat kieu du lieu cot (date/decimal/int).
2. Chuan hoa gia tri enum (`order_status`).
3. Bo sung them data cho cac ngay/thang khac nhau.
4. Kiem tra hieu nang query tong hop co ban.

## 11.2 Nguyen nhan
MVP can chay muot trong demo, tranh:
1. Query tra rong.
2. Chart xau do data lech.
3. LLM sinh SQL dung nhung output vo nghia.

## 11.3 Dau ra
1. Bo data "demo-friendly".
2. Query thuong gap tra ket qua dung va de nhin.

---

## 12. Checklist DoD rieng cho TV1

## 12.1 DoD ky thuat
- [ ] Co 1 catalog + 1 schema thong nhat cho du an
- [ ] Co it nhat 3 Delta tables (users/products/orders)
- [ ] Data da nap va qua check quality co ban
- [ ] Tat ca cot nghiep vu quan trong da co COMMENT
- [ ] Backend credential chi co quyen SELECT
- [ ] SQL Warehouse co auto stop
- [ ] TV3 query duoc thanh cong qua connector

## 12.2 DoD ve phoi hop
- [ ] Gui tai lieu ket noi cho TV3/TV5
- [ ] Co 5-10 cau SQL mau phuc vu demo
- [ ] Co note "known issues" va cach workaround

---

## 13. Mau bo truy van de tu test truoc khi ban giao

```sql
-- 1) Tong doanh thu theo thang
SELECT date_trunc('month', order_date) AS month,
       SUM(quantity * unit_price) AS revenue
FROM ai_analyst.ecommerce.orders
WHERE order_status IN ('shipped', 'delivered')
GROUP BY 1
ORDER BY 1;

-- 2) Top 5 san pham ban chay
SELECT p.product_name,
       SUM(o.quantity) AS total_qty
FROM ai_analyst.ecommerce.orders o
JOIN ai_analyst.ecommerce.products p ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_qty DESC
LIMIT 5;

-- 3) So don theo thanh pho
SELECT u.city,
       COUNT(*) AS total_orders
FROM ai_analyst.ecommerce.orders o
JOIN ai_analyst.ecommerce.users u ON o.user_id = u.user_id
GROUP BY u.city
ORDER BY total_orders DESC;
```

Y nghia: Neu 3 query nay ra ket qua hop ly, du lieu cua ban da san sang cho MVP.

---

## 14. Rui ro thuong gap va cach xu ly

1. Loi permission denied:
   - Nguyen nhan: thieu USE CATALOG/SCHEMA hoac SELECT.
   - Xu ly: check lai grant theo thu tu catalog -> schema -> table.
2. Query cham:
   - Nguyen nhan: warehouse tat/bat lien tuc, size qua nho.
   - Xu ly: giu warehouse warm truoc buoi demo, tang size toi thieu neu can.
3. LLM hoi ra ket qua vo nghia:
   - Nguyen nhan: ten cot mo ho, thieu COMMENT.
   - Xu ly: viet lai comment ro nghia nghiep vu va don vi tinh.
4. Join ra rong:
   - Nguyen nhan: data key sai format hoac co orphan key.
   - Xu ly: chuan hoa key va bo sung/lam sach records.

---

## 15. Ke hoach theo ngay de bam sat timeline

1. 30/03: Khoi tao workspace, warehouse, cluster, test `SELECT 1`.
2. 31/03: Tao Delta tables + nap data mau + check row counts.
3. 01/04: Setup Unity Catalog + grant read-only + test SQL Warehouse.
4. 02/04: Phoi hop TV3 test connector va API schema/query.
5. 03/04: Bo sung COMMENT day du cho bang/cot + toi uu schema.
6. 04/04: Rasoat output query, fix data issue.
7. 05/04: Buffer ho tro team.
8. 06/04: Debug cloud/connectivity cung ca nhom.
9. 07/04: Chay MVP demo E2E.

---

## 16. Ban giao cho nhom (handover package)

TV1 nen ban giao 1 goi nho gom:
1. File SQL tao bang + grant quyen.
2. File SQL test nhanh (cac query tong hop).
3. Bang mo ta schema (table, column, y nghia, don vi).
4. Huong dan ket noi backend (host, http path, token scope).

Y nghia: Ban giao tot giup team khong phu thuoc vao mot nguoi, giam rui ro tre deadline.

---

## 17. Tu duy "vua lam vua hieu"

Moi buoc ban tu hoi 3 cau:
1. Buoc nay phuc vu thanh phan nao trong kien truc (AI, Backend, Frontend)?
2. Neu bo qua buoc nay thi loi gi xay ra?
3. Dau ra cua buoc nay co do duoc bang test/query nao khong?

Neu tra loi duoc 3 cau nay, ban dang khong chi lam cho xong, ma dang hieu dung ban chat du an SOA + Cloud.

---

## 18. Tieu chuan san sang truoc ngay 15/04

Ban TV1 dat muc "san sang nop" khi:
1. He thong E2E chay duoc qua docker-compose cung team.
2. Data va schema du ro de AI tra loi nhat quan.
3. Quyen truy cap an toan (read-only cho backend).
4. Co tai lieu de nguoi khac tiep quan va demo duoc ngay.

Khi dat du 4 dieu tren, TV1 da hoan thanh dung vai tro Data Engineer & Cloud cua project nay.
