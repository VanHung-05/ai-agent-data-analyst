# SQL Evaluation Report

- GeneratedAt: 2026-04-25T15:28:53.623636+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **20** / InputSamples: **20**
- ExecutionSuccessRate: **50.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **50.00%**
- OverallWeightedScore: **76.95%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.1**
- Component Match (CM) mean: **0.6496**
- Execution Accuracy (EX) mean: **0.5**
- Partial Execution / F1 (EX_partial) mean: **0.5373**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.4964**

- EM_gte_0.8: **FAIL**
- CM_gte_0.8: **FAIL**
- EX_gte_0.9: **FAIL**
- VES_gte_1.0: **FAIL**

## Target Check

- execution_success_rate: **FAIL**
- safety_pass_rate: **PASS**
- semantic_match_rate: **FAIL**
- overall_weighted_score: **FAIL**

## Case Details

### basic_select_001
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.4926`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp']` vs gold: `['order_id', 'customer_id', 'order_status', 'thoi_gian_vn']`
  - ❌ Thiếu cột: `['thoi_gian_vn']`
  - ➕ Thừa cột: `['order_purchase_timestamp']`

### basic_select_002
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.6667`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['total_unique_customers']` vs gold: `['total_customers']`
  - ❌ Thiếu cột: `['total_customers']`
  - ➕ Thừa cột: `['total_unique_customers']`

### basic_select_003
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.4074`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_004
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `0.7037`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9788`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_005
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.5766`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`10` | matched=`5` | missing=`5` | extra=`5`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_id': '3442f8959a84dea7ee197c632cb2df15', 'seller_city': 'campinas', 'seller_state': 'SP', 'seller_zip_code_prefix': '13023'}`
    - `{'seller_id': 'd1b65fc7debc3361ea86b5f14c68d2e2', 'seller_city': 'mogi guacu', 'seller_state': 'SP', 'seller_zip_code_prefix': '13844'}`
    - `{'seller_id': '51a04a8a6bdcb23deccc82b0b80742cf', 'seller_city': 'braganca paulista', 'seller_state': 'SP', 'seller_zip_code_prefix': '12914'}`

### basic_select_006
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.7692`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['review_id', 'order_id', 'review_score', 'review_comment_message', 'review_creation_date']` vs gold: `['review_id', 'order_id', 'review_score', 'review_comment_title', 'review_comment_message', 'review_creation_date_vn']`
  - ❌ Thiếu cột: `['review_comment_title', 'review_creation_date_vn']`
  - ➕ Thừa cột: `['review_creation_date']`

### basic_select_007
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.7273`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['total_canceled_orders']` vs gold: `['canceled_orders']`
  - ❌ Thiếu cột: `['canceled_orders']`
  - ➕ Thừa cột: `['total_canceled_orders']`

### basic_select_008
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.5185`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_009
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.5481`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp']` vs gold: `['order_id', 'customer_id', 'order_status', 'thoi_gian_vn']`
  - ❌ Thiếu cột: `['thoi_gian_vn']`
  - ➕ Thừa cột: `['order_purchase_timestamp']`

### basic_select_010
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5481`
- EM: `0.0`
- CM: `0.16`
- EX (strict): `0.0`
- EX_partial (F1): `0.2469`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`71` | matched=`10` | missing=`61` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'product_category_name': 'agro_industria_e_comercio', 'product_category_name_english': 'agro_industry_and_commerce'}`
    - `{'product_category_name': 'artes', 'product_category_name_english': 'art'}`
    - `{'product_category_name': 'artes_e_artesanato', 'product_category_name_english': 'arts_and_craftmanship'}`

### aggregate_001
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9231`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_002
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6131`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9963`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_003
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6136`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9908`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_004
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9375`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_005
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `0.7583`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9696`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_006
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.8551`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['yr', 'qtr', 'quarterly_revenue']` vs gold: `['yr', 'qtr', 'quarterly_revenue', 'total_orders']`
  - ❌ Thiếu cột: `['total_orders']`

### aggregate_007
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.6037`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['customer_state', 'total_freight_value']` vs gold: `['customer_state', 'total_freight']`
  - ❌ Thiếu cột: `['total_freight']`
  - ➕ Thừa cột: `['total_freight_value']`

### aggregate_008
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.775`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9916`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_009
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.5417`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_010
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.8016`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['order_year', 'total_revenue', 'total_freight']` vs gold: `['yr', 'total_revenue', 'total_freight']`
  - ❌ Thiếu cột: `['yr']`
  - ➕ Thừa cột: `['order_year']`
