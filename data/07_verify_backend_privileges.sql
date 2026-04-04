-- TV1 Step 4 - Verify Backend Read-Only Privileges (Databricks SQL)
-- Purpose: Confirm principal has read-only access and no write privileges.
-- Default grantee for this project: backend_readonly (group).

-- A) Human-readable grants per object
SHOW GRANTS ON CATALOG ai_analyst;
SHOW GRANTS ON SCHEMA ai_analyst.ecommerce;
SHOW GRANTS ON TABLE ai_analyst.ecommerce.users;
SHOW GRANTS ON TABLE ai_analyst.ecommerce.products;
SHOW GRANTS ON TABLE ai_analyst.ecommerce.orders;

-- B) Structured check via information_schema
SELECT grantee, privilege_type, table_catalog, table_schema, table_name
FROM system.information_schema.table_privileges
WHERE table_catalog = 'ai_analyst'
  AND table_schema = 'ecommerce'
  AND grantee = 'backend_readonly'
ORDER BY table_name, privilege_type;

-- C) Negative check: backend principal must not have write/admin privileges
SELECT grantee, privilege_type, table_catalog, table_schema, table_name
FROM system.information_schema.table_privileges
WHERE table_catalog = 'ai_analyst'
  AND table_schema = 'ecommerce'
  AND grantee = 'backend_readonly'
  AND privilege_type IN (
    'MODIFY', 'ALL PRIVILEGES', 'OWN', 'WRITE_METADATA', 'MANAGE'
  )
ORDER BY table_name, privilege_type;

-- D) Optional runtime proof (run this section ONLY when connected as backend principal)
-- Expected: SELECT succeeds, INSERT fails with permission denied.
-- SELECT COUNT(*) FROM ai_analyst.ecommerce.orders;
-- INSERT INTO ai_analyst.ecommerce.orders VALUES ('T999','U001','P001',1,1.00,DATE '2026-04-01','pending');
