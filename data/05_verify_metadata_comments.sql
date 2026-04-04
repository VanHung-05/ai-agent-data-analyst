-- TV1 Step 3 - Verify Metadata Comments (Databricks SQL)
-- Purpose: Validate that table/column comments were applied successfully.

-- 1) Table comments coverage (expected = 3)
SELECT COUNT(*) AS table_comment_count
FROM system.information_schema.tables
WHERE table_catalog = 'ai_analyst'
  AND table_schema = 'ecommerce'
  AND table_name IN ('users', 'products', 'orders')
  AND comment IS NOT NULL;

-- 2) Column comments coverage (expected = 17)
SELECT COUNT(*) AS column_comment_count
FROM system.information_schema.columns
WHERE table_catalog = 'ai_analyst'
  AND table_schema = 'ecommerce'
  AND table_name IN ('users', 'products', 'orders')
  AND comment IS NOT NULL;

-- 3) List columns still missing comments (expected = 0 rows)
SELECT table_name, column_name
FROM system.information_schema.columns
WHERE table_catalog = 'ai_analyst'
  AND table_schema = 'ecommerce'
  AND table_name IN ('users', 'products', 'orders')
  AND comment IS NULL
ORDER BY table_name, ordinal_position;

-- 4) Review full metadata dictionary
SELECT table_name, column_name, data_type, comment
FROM system.information_schema.columns
WHERE table_catalog = 'ai_analyst'
  AND table_schema = 'ecommerce'
  AND table_name IN ('users', 'products', 'orders')
ORDER BY table_name, ordinal_position;
