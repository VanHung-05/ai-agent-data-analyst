-- TV1 Ops - Restore Baseline After Security Tests
-- Purpose: Bring demo dataset back to baseline row counts after write-test attempts.

-- 1) Remove known security test records if they exist.
DELETE FROM ai_analyst.ecommerce.orders WHERE order_id IN ('Z998', 'Z999');

-- 2) Show current row counts (expected baseline: users=5, products=8, orders=12).
SELECT 'users' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.users
UNION ALL
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.products
UNION ALL
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM ai_analyst.ecommerce.orders;

-- 3) Re-check KPI baseline after cleanup.
SELECT date_trunc('month', order_date) AS month,
       ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM ai_analyst.ecommerce.orders
WHERE order_status IN ('shipped', 'delivered')
GROUP BY 1
ORDER BY 1;
