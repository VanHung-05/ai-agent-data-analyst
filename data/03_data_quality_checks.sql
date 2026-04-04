-- TV1 Step 2 - Data Quality Checks (Databricks SQL)
-- Purpose: Verify row counts, key integrity, and business-domain consistency.

-- 1) Row counts
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.users
UNION ALL
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.products
UNION ALL
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.orders;

-- 2) Duplicate key checks
SELECT user_id, COUNT(*) AS cnt
FROM ai_analyst.ecommerce.users
GROUP BY user_id
HAVING COUNT(*) > 1;

SELECT product_id, COUNT(*) AS cnt
FROM ai_analyst.ecommerce.products
GROUP BY product_id
HAVING COUNT(*) > 1;

SELECT order_id, COUNT(*) AS cnt
FROM ai_analyst.ecommerce.orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 3) Orphan key checks
SELECT COUNT(*) AS orphan_user
FROM ai_analyst.ecommerce.orders o
LEFT JOIN ai_analyst.ecommerce.users u ON o.user_id = u.user_id
WHERE u.user_id IS NULL;

SELECT COUNT(*) AS orphan_product
FROM ai_analyst.ecommerce.orders o
LEFT JOIN ai_analyst.ecommerce.products p ON o.product_id = p.product_id
WHERE p.product_id IS NULL;

-- 4) Null checks on important analytical columns
SELECT
  SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) AS null_user_id,
  SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) AS null_product_id,
  SUM(CASE WHEN quantity IS NULL THEN 1 ELSE 0 END) AS null_quantity,
  SUM(CASE WHEN unit_price IS NULL THEN 1 ELSE 0 END) AS null_unit_price,
  SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) AS null_order_date,
  SUM(CASE WHEN order_status IS NULL THEN 1 ELSE 0 END) AS null_order_status
FROM ai_analyst.ecommerce.orders;

-- 5) Domain checks
SELECT order_status, COUNT(*) AS cnt
FROM ai_analyst.ecommerce.orders
GROUP BY order_status
ORDER BY cnt DESC;

-- 6) KPI smoke tests for demo stability
SELECT date_trunc('month', order_date) AS month,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM ai_analyst.ecommerce.orders
WHERE order_status IN ('shipped', 'delivered')
GROUP BY 1
ORDER BY 1;
