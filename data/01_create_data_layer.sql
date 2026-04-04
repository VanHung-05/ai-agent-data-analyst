-- TV1 Step 2 - Create Data Layer (Databricks SQL)
-- Purpose: Create catalog, schema, and Delta tables for MVP analytics.

CREATE CATALOG IF NOT EXISTS ai_analyst;
CREATE SCHEMA IF NOT EXISTS ai_analyst.ecommerce;

-- Users dimension
CREATE TABLE IF NOT EXISTS ai_analyst.ecommerce.users (
  user_id STRING NOT NULL,
  full_name STRING,
  email STRING,
  city STRING,
  created_at DATE
)
USING DELTA
TBLPROPERTIES (
  delta.autoOptimize.optimizeWrite = true,
  delta.autoOptimize.autoCompact = true
);

-- Products dimension
CREATE TABLE IF NOT EXISTS ai_analyst.ecommerce.products (
  product_id STRING NOT NULL,
  product_name STRING,
  category STRING,
  price DECIMAL(12,2),
  is_active BOOLEAN
)
USING DELTA
TBLPROPERTIES (
  delta.autoOptimize.optimizeWrite = true,
  delta.autoOptimize.autoCompact = true
);

-- Orders fact
CREATE TABLE IF NOT EXISTS ai_analyst.ecommerce.orders (
  order_id STRING NOT NULL,
  user_id STRING,
  product_id STRING,
  quantity INT,
  unit_price DECIMAL(12,2),
  order_date DATE,
  order_status STRING
)
USING DELTA
PARTITIONED BY (order_date)
TBLPROPERTIES (
  delta.autoOptimize.optimizeWrite = true,
  delta.autoOptimize.autoCompact = true
);

-- Business constraints (defensive data quality)
ALTER TABLE ai_analyst.ecommerce.products
  DROP CONSTRAINT IF EXISTS chk_products_price_non_negative;

ALTER TABLE ai_analyst.ecommerce.products
  ADD CONSTRAINT chk_products_price_non_negative CHECK (price >= 0);

ALTER TABLE ai_analyst.ecommerce.orders
  DROP CONSTRAINT IF EXISTS chk_orders_quantity_positive;

ALTER TABLE ai_analyst.ecommerce.orders
  ADD CONSTRAINT chk_orders_quantity_positive CHECK (quantity > 0);

ALTER TABLE ai_analyst.ecommerce.orders
  DROP CONSTRAINT IF EXISTS chk_orders_unit_price_non_negative;

ALTER TABLE ai_analyst.ecommerce.orders
  ADD CONSTRAINT chk_orders_unit_price_non_negative CHECK (unit_price >= 0);

ALTER TABLE ai_analyst.ecommerce.orders
  DROP CONSTRAINT IF EXISTS chk_orders_status_domain;

ALTER TABLE ai_analyst.ecommerce.orders
  ADD CONSTRAINT chk_orders_status_domain CHECK (
    order_status IN ('pending', 'shipped', 'delivered', 'cancelled')
  );
