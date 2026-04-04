-- TV1 Step 4 - Least Privilege Grants for Backend (Databricks SQL)
-- Purpose: Grant minimum required permissions so backend can read data only.
-- Recommended model: Grant permissions to a group, then add service principal into that group.

-- Default group for this project: backend_readonly

-- 0) Target grantee (group)
-- If your real group name is different, replace backend_readonly below.

-- 1) Recommended hardening: explicitly remove write-level privileges on schema.
REVOKE CREATE ON SCHEMA ai_analyst.ecommerce FROM `backend_readonly`;

-- 2) Minimum privileges for read access.
GRANT USE CATALOG ON CATALOG ai_analyst TO `backend_readonly`;
GRANT USE SCHEMA ON SCHEMA ai_analyst.ecommerce TO `backend_readonly`;

-- 3) Read-only on required tables.
GRANT SELECT ON TABLE ai_analyst.ecommerce.users TO `backend_readonly`;
GRANT SELECT ON TABLE ai_analyst.ecommerce.products TO `backend_readonly`;
GRANT SELECT ON TABLE ai_analyst.ecommerce.orders TO `backend_readonly`;

-- 4) Databricks SQL does not support "ON FUTURE TABLES" syntax.
-- Operational rule: when a new table is created, run an explicit GRANT SELECT for that table.
-- Example:
-- GRANT SELECT ON TABLE ai_analyst.ecommerce.<new_table_name> TO `backend_readonly`;

-- 5) Defensive revokes on current tables (no-op if privilege was never granted).
REVOKE MODIFY ON TABLE ai_analyst.ecommerce.users FROM `backend_readonly`;
REVOKE MODIFY ON TABLE ai_analyst.ecommerce.products FROM `backend_readonly`;
REVOKE MODIFY ON TABLE ai_analyst.ecommerce.orders FROM `backend_readonly`;

-- 6) Post-setup reminder:
-- Run sql/07_verify_backend_privileges.sql immediately after this script.
