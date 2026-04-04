# TV1 Fast-Track E2E Execution (for TV3/TV5)

Ngay cap nhat: 02/04/2026
Muc tieu: Chay nhanh luong E2E dung chuan hoc thuat trong 15-30 phut.

## 1) Inputs bat buoc

- Hostname: dbc-8e02bd60-745e.cloud.databricks.com
- HTTP Path: /sql/1.0/warehouses/c4b9846edf9d97af
- Catalog/Schema: ai_analyst.ecommerce
- SP backend: sp-backend-api
- Group read-only: backend_readonly

## 2) Fast sequence (khong bo qua)

1. TV3 test connector baseline
   - Chay query `SELECT 1`
   - Chay `sql/08_backend_connector_smoke_test.sql` (muc 1-4)
2. TV5 test security
   - Chay `sp_negative_test.py` bang SP backend
   - Xac nhan INSERT/UPDATE/DELETE bi PERMISSION_DENIED
3. TV1 restore baseline
   - Chay `sql/09_restore_baseline_after_security_test.sql`
4. Team re-run smoke
   - Chay lai row counts + revenue de xac nhan baseline

## 3) Dieu kien PASS

- Connector pass: SELECT/join/revenue tra ket qua hop le
- Security pass: SP backend khong ghi du lieu
- Baseline pass: row counts = users 5, products 8, orders 12

## 4) Evidence can luu

- 01 anh output connector success
- 01 anh output permission denied (INSERT/UPDATE/DELETE)
- 01 anh output row counts baseline sau cleanup

## 5) Luu y bao mat

- Khong chua client secret trong file markdown/python commit
- Neu lo secret: revoke ngay, tao secret moi
- Chi chia se secret qua kenh rieng cua nhom
