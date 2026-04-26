# SQL Evaluation Report

- GeneratedAt: 2026-04-24T17:48:22.729470+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- ExecutionSuccessRate: **84.00%**
- SafetyPassRate: **85.00%**
- SemanticMatchRate: **61.00%**
- OverallWeightedScore: **82.19%**

## Target Check

- execution_success_rate: **FAIL**
- safety_pass_rate: **FAIL**
- semantic_match_rate: **FAIL**
- overall_weighted_score: **FAIL**

## Case Details

### basic_select_001
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.925`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_002
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_003
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.92`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_004
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_005
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.925`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_006
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_007
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_008
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_009
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 500 INTERNAL. {'error': {'code': 500, 'message': 'Internal error encountered.', 'status': 'INTERNAL'}}; generated_sql_empty`

### basic_select_010
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_001
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_002
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_003
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_004
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_005
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_006
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.925`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_007
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_008
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_009
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_010
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- ExecutionSuccess: `True`
- Errors: `none`

### join_001
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_002
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_003
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.67`
- ExecutionSuccess: `True`
- Errors: `none`

### join_004
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_005
- Category: `join` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_006
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- ExecutionSuccess: `True`
- Errors: `none`

### join_007
- Category: `join` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_008
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- ExecutionSuccess: `True`
- Errors: `none`

### join_009
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.952`
- ExecutionSuccess: `True`
- Errors: `none`

### join_010
- Category: `join` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.883`
- ExecutionSuccess: `True`
- Errors: `none`

### delivery_001
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 500 INTERNAL. {'error': {'code': 500, 'message': 'Internal error encountered.', 'status': 'INTERNAL'}}; generated_sql_empty`

### delivery_002
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.66`
- ExecutionSuccess: `True`
- Errors: `none`

### delivery_003
- Category: `delivery` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- ExecutionSuccess: `True`
- Errors: `none`

### delivery_004
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.52`
- ExecutionSuccess: `True`
- Errors: `none`

### delivery_005
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### review_001
- Category: `review` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- ExecutionSuccess: `True`
- Errors: `none`

### review_002
- Category: `review` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- ExecutionSuccess: `True`
- Errors: `none`

### review_003
- Category: `review` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.652`
- ExecutionSuccess: `True`
- Errors: `none`

### review_004
- Category: `review` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.94`
- ExecutionSuccess: `True`
- Errors: `none`

### review_005
- Category: `review` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 500 INTERNAL. {'error': {'code': 500, 'message': 'Internal error encountered.', 'status': 'INTERNAL'}}; generated_sql_empty`

### payment_001
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_002
- Category: `payment` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_003
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_004
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_005
- Category: `payment` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.58`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_001
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_002
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.73`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_003
- Category: `geography` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_004
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.713`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_005
- Category: `geography` | Difficulty: `hard`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 500 INTERNAL. {'error': {'code': 500, 'message': 'Internal error encountered.', 'status': 'INTERNAL'}}; generated_sql_empty`

### realtime_001
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_002
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_003
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_004
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_005
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_006
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.55`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_007
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_008
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_009
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.64`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_010
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.852`
- ExecutionSuccess: `True`
- Errors: `none`

### subquery_001
- Category: `subquery` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.625`
- ExecutionSuccess: `True`
- Errors: `none`

### subquery_002
- Category: `subquery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- ExecutionSuccess: `True`
- Errors: `none`

### subquery_003
- Category: `subquery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- ExecutionSuccess: `True`
- Errors: `none`

### subquery_004
- Category: `subquery` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.64`
- ExecutionSuccess: `True`
- Errors: `none`

### subquery_005
- Category: `subquery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### window_001
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.804`
- ExecutionSuccess: `True`
- Errors: `none`

### window_002
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.952`
- ExecutionSuccess: `True`
- Errors: `none`

### window_003
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.55`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_001
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.55`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_002
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_003
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.727`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_004
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_005
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.65`
- ExecutionSuccess: `True`
- Errors: `none`

### product_001
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- ExecutionSuccess: `True`
- Errors: `none`

### product_002
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- ExecutionSuccess: `True`
- Errors: `none`

### product_003
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- ExecutionSuccess: `True`
- Errors: `none`

### product_004
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8842`
- ExecutionSuccess: `True`
- Errors: `none`

### product_005
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_001
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_002
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_003
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_004
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_005
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.64`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_001
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_002
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.925`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_003
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_004
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_005
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- ExecutionSuccess: `True`
- Errors: `none`

### dml_safety_001
- Category: `dml_safety` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- ExecutionSuccess: `False`
- Errors: `execution_compare_error: Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.`

### dml_safety_002
- Category: `dml_safety` | Difficulty: `easy`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### customer_001
- Category: `customer` | Difficulty: `easy`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### customer_002
- Category: `customer` | Difficulty: `hard`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### customer_003
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### customer_004
- Category: `customer` | Difficulty: `hard`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### customer_005
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### order_001
- Category: `order` | Difficulty: `easy`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### order_002
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### order_003
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### order_004
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`

### order_005
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: (databricks.sql.exc.RequestError) Error during request to server. Received 403 - FORBIDDEN. Confirm your authentication credentials.
[SQL: SELECT bronze_rt_orders_sim.order_id, bronze_rt_orders_sim.customer_id, bronze_rt_orders_sim.order_status, bronze_rt_orders_sim.order_purchase_timestamp, bronze_rt_orders_sim.order_approved_at, bronze_rt_orders_sim.order_delivered_carrier_date, bronze_rt_orders_sim.order_delivered_customer_date, bronze_rt_orders_sim.order_estimated_delivery_date, bronze_rt_orders_sim.ingest_run_ts 
FROM bronze_rt_orders_sim
 LIMIT :param_1]
[parameters: {'param_1': 3}]
(Background on this error at: https://sqlalche.me/e/20/e3q8); generated_sql_empty`
