-- TV1 Step 2 - Seed Data (Databricks SQL)
-- Purpose: Load stable and demo-friendly sample data.

-- Idempotent approach for demo reruns.
DELETE FROM ai_analyst.ecommerce.orders;
DELETE FROM ai_analyst.ecommerce.products;
DELETE FROM ai_analyst.ecommerce.users;

INSERT INTO ai_analyst.ecommerce.users (user_id, full_name, email, city, created_at)
VALUES
  ('U001', 'Nguyen Van An', 'an.nguyen@example.com', 'Ho Chi Minh', DATE '2025-10-03'),
  ('U002', 'Tran Thi Bich', 'bich.tran@example.com', 'Ha Noi', DATE '2025-11-15'),
  ('U003', 'Le Minh Khoa', 'khoa.le@example.com', 'Da Nang', DATE '2025-12-01'),
  ('U004', 'Pham Thu Ha', 'ha.pham@example.com', 'Can Tho', DATE '2026-01-08'),
  ('U005', 'Vo Quang Huy', 'huy.vo@example.com', 'Hai Phong', DATE '2026-01-20');

INSERT INTO ai_analyst.ecommerce.products (product_id, product_name, category, price, is_active)
VALUES
  ('P001', 'Wireless Mouse M1', 'Accessories', 12.50, true),
  ('P002', 'Mechanical Keyboard K87', 'Accessories', 59.90, true),
  ('P003', 'USB-C Hub 7 in 1', 'Accessories', 34.90, true),
  ('P004', 'Laptop Stand L2', 'Office', 26.40, true),
  ('P005', 'Bluetooth Earbuds E5', 'Audio', 45.00, true),
  ('P006', 'Portable SSD 1TB', 'Storage', 89.00, true),
  ('P007', '4K Monitor 27inch', 'Display', 249.00, true),
  ('P008', 'Webcam W1080', 'Video', 38.50, false);

INSERT INTO ai_analyst.ecommerce.orders (
  order_id, user_id, product_id, quantity, unit_price, order_date, order_status
)
VALUES
  ('O001', 'U001', 'P001', 2, 12.50, DATE '2026-01-05', 'delivered'),
  ('O002', 'U002', 'P002', 1, 59.90, DATE '2026-01-09', 'shipped'),
  ('O003', 'U003', 'P003', 1, 34.90, DATE '2026-01-12', 'delivered'),
  ('O004', 'U004', 'P004', 3, 26.40, DATE '2026-01-20', 'delivered'),
  ('O005', 'U005', 'P005', 1, 45.00, DATE '2026-02-02', 'pending'),
  ('O006', 'U001', 'P006', 1, 89.00, DATE '2026-02-10', 'shipped'),
  ('O007', 'U002', 'P001', 1, 12.50, DATE '2026-02-14', 'cancelled'),
  ('O008', 'U003', 'P007', 1, 249.00, DATE '2026-02-19', 'delivered'),
  ('O009', 'U004', 'P002', 2, 59.90, DATE '2026-03-01', 'delivered'),
  ('O010', 'U005', 'P003', 2, 34.90, DATE '2026-03-07', 'shipped'),
  ('O011', 'U001', 'P004', 1, 26.40, DATE '2026-03-09', 'delivered'),
  ('O012', 'U002', 'P006', 1, 89.00, DATE '2026-03-12', 'pending');
