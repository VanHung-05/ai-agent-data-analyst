-- TV1 Step 5 - Backend Connector Smoke Test (Databricks SQL)
-- Purpose: Provide deterministic checks for TV3/TV5 after backend wiring.

-- 1) Connectivity baseline
SELECT 1 AS connectivity_ok;

-- 2) Row counts (expected from seed)
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.users
UNION ALL
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.products
UNION ALL
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.orders;

-- 3) Join sanity check
SELECT
  o.order_id,
  u.full_name,
  p.product_name,
  o.quantity,
  o.unit_price,
  o.order_status,
  o.order_date
FROM ai_analyst.ecommerce.orders o
JOIN ai_analyst.ecommerce.users u ON o.user_id = u.user_id
JOIN ai_analyst.ecommerce.products p ON o.product_id = p.product_id
ORDER BY o.order_date DESC
LIMIT 10;

-- 4) Core analytics query used by agent demo
SELECT date_trunc('month', order_date) AS month,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM ai_analyst.ecommerce.orders
WHERE order_status IN ('shipped', 'delivered')
GROUP BY 1
ORDER BY 1;

-- 5) Read-only posture check (must fail when executed with backend principal)
-- INSERT INTO ai_analyst.ecommerce.orders VALUES ('Z999','U001','P001',1,1.00,DATE '2026-04-02','pending');
