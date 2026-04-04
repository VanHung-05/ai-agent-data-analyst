-- TV1 Step 3 - Business Metadata Comments (Databricks SQL)
-- Purpose: Improve AI SQL generation quality by providing explicit business semantics.

-- =========================
-- TABLE: users
-- =========================
COMMENT ON TABLE ai_analyst.ecommerce.users IS
'Nguoi dung trong he thong ecommerce. Bang dimension mo ta thong tin ho so va khu vuc cua khach hang.';

COMMENT ON COLUMN ai_analyst.ecommerce.users.user_id IS
'Khoa dinh danh duy nhat cua nguoi dung. Duoc dung de join voi orders.user_id.';

COMMENT ON COLUMN ai_analyst.ecommerce.users.full_name IS
'Ho va ten day du cua nguoi dung, phuc vu hien thi va phan tich co ban.';

COMMENT ON COLUMN ai_analyst.ecommerce.users.email IS
'Dia chi email nguoi dung, dinh danh lien he. Khong dung de tinh KPI tai chinh.';

COMMENT ON COLUMN ai_analyst.ecommerce.users.city IS
'Thanh pho cua nguoi dung tai thoi diem tao tai khoan. Dung cho phan tich theo khu vuc dia ly.';

COMMENT ON COLUMN ai_analyst.ecommerce.users.created_at IS
'Ngay tao tai khoan nguoi dung. Co the dung de phan tich user growth theo thoi gian.';

-- =========================
-- TABLE: products
-- =========================
COMMENT ON TABLE ai_analyst.ecommerce.products IS
'Danh muc san pham duoc ban tren he thong ecommerce. Bang dimension mo ta thuoc tinh san pham.';

COMMENT ON COLUMN ai_analyst.ecommerce.products.product_id IS
'Khoa dinh danh duy nhat cua san pham. Duoc dung de join voi orders.product_id.';

COMMENT ON COLUMN ai_analyst.ecommerce.products.product_name IS
'Ten thuong mai cua san pham de hien thi tren bao cao va dashboard.';

COMMENT ON COLUMN ai_analyst.ecommerce.products.category IS
'Nhom danh muc san pham, dung cho phan tich co cau doanh thu theo nganh hang.';

COMMENT ON COLUMN ai_analyst.ecommerce.products.price IS
'Gia niem yet hien tai cua san pham, don vi tien te la USD. Khong phai luc nao cung bang gia ban trong don hang.';

COMMENT ON COLUMN ai_analyst.ecommerce.products.is_active IS
'Trang thai kinh doanh cua san pham: true la dang kinh doanh, false la tam ngung/khong con ban.';

-- =========================
-- TABLE: orders
-- =========================
COMMENT ON TABLE ai_analyst.ecommerce.orders IS
'Don hang giao dich. Bang fact luu su kien mua hang cua nguoi dung theo ngay va trang thai don.';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.order_id IS
'Khoa dinh danh duy nhat cua don hang.';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.user_id IS
'Khoa ngoai tham chieu den users.user_id, xac dinh khach hang dat don.';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.product_id IS
'Khoa ngoai tham chieu den products.product_id, xac dinh san pham duoc dat mua.';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.quantity IS
'So luong don vi san pham trong dong don hang. Gia tri phai lon hon 0.';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.unit_price IS
'Gia ban thuc te moi don vi tai thoi diem dat hang, don vi tien te la USD.';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.order_date IS
'Ngay phat sinh don hang. Dung de phan tich xu huong theo ngay/thang/quy.';

COMMENT ON COLUMN ai_analyst.ecommerce.orders.order_status IS
'Trang thai don hang: pending, shipped, delivered, cancelled. Khi tinh doanh thu thuc thu, uu tien shipped va delivered.';
