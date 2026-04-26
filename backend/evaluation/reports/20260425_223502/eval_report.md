# SQL Evaluation Report

- GeneratedAt: 2026-04-25T15:41:38.125643+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **20** / InputSamples: **20**
- ExecutionSuccessRate: **65.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **65.00%**
- OverallWeightedScore: **84.00%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.1**
- Component Match (CM) mean: **0.6496**
- Execution Accuracy (EX) mean: **0.65**
- Partial Execution / F1 (EX_partial) mean: **0.6873**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.647**

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
  - ❌ Thiếu cột: `['thoi_gian_vn']`
  - ➕ Thừa cột: `['order_purchase_timestamp']`
  - Số dòng: generated=`10` | gold=`10` | matched=`0` | missing=`10` | extra=`10`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'order_id': '2e7a8482f6fb09756ca50c10d7bfc047', 'customer_id': '08c5351a6aca1c1589a38f244edeee9d', 'order_status': 'shipped', 'thoi_gian_vn': '2016-09-05 04:15:19+00:00'}`
    - `{'order_id': 'e5fa5a7210941f7d56d0208e4e071d35', 'customer_id': '683c54fc24d40ee9f8a6fc179fd9856c', 'order_status': 'canceled', 'thoi_gian_vn': '2016-09-05 07:15:34+00:00'}`
    - `{'order_id': '809a282bbd5dbcabb6f2f724fca862ec', 'customer_id': '622e13439d6b5a0b486c435618b2679e', 'order_status': 'canceled', 'thoi_gian_vn': '2016-09-13 22:24:19+00:00'}`

### basic_select_002
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6667`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**
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
- VES: `0.9773`
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
- VES: `1.0`
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
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7273`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9734`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**
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
  - ❌ Thiếu cột: `['thoi_gian_vn']`
  - ➕ Thừa cột: `['order_purchase_timestamp']`
  - Số dòng: generated=`10` | gold=`10` | matched=`0` | missing=`10` | extra=`10`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'order_id': '10a045cdf6a5650c21e9cfeb60384c16', 'customer_id': 'a4b417188addbc05b26b72d5e44837a1', 'order_status': 'canceled', 'thoi_gian_vn': '2018-10-18 00:30:18+00:00'}`
    - `{'order_id': 'b059ee4de278302d550a3035c4cdb740', 'customer_id': '856336203359aa6a61bf3826f7d84c49', 'order_status': 'canceled', 'thoi_gian_vn': '2018-10-17 03:16:02+00:00'}`
    - `{'order_id': 'a2ac6dad85cf8af5b0afb510a240fe8c', 'customer_id': '4c2ec60c29d10c34bd49cb88aa85cfc4', 'order_status': 'canceled', 'thoi_gian_vn': '2018-10-04 01:55:29+00:00'}`

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
- VES: `1.0`
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
- VES: `1.0`
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
- VES: `0.9976`
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
- VES: `1.0`
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
  - ❌ Thiếu cột: `['total_freight']`
  - ➕ Thừa cột: `['total_freight_value']`
  - Số dòng: generated=`27` | gold=`27` | matched=`0` | missing=`27` | extra=`27`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'SP', 'total_freight': '718723.07'}`
    - `{'customer_state': 'RJ', 'total_freight': '305589.31'}`
    - `{'customer_state': 'MG', 'total_freight': '270853.46'}`

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
- VES: `1.0`
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
- VES: `0.9924`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_010
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8016`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['yr']`
  - ➕ Thừa cột: `['order_year']`
