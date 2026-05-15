# SQL Evaluation Report

- GeneratedAt: 2026-05-14T17:25:31.947789+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **100** / InputSamples: **100**
- ExecutionSuccessRate: **83.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **87.00%**
- OverallWeightedScore: **92.71%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.48**
- Component Match (CM) mean: **0.902**
- Execution Accuracy (EX) mean: **0.83**
- Partial Execution / F1 (EX_partial) mean: **0.8887**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.8228**

- EM_gte_0.8: **FAIL**
- CM_gte_0.8: **PASS**
- EX_gte_0.9: **FAIL**
- VES_gte_1.0: **FAIL**

## EX Failure Dashboard

- EX failed total: **17**
- Alias-only mismatch: **0** (rate: 0.00%)
- LIMIT/TOP-N mismatch: **5** (rate: 29.41%)
  - Sample IDs: `join_010, geography_002, realtime_006, subquery_004, customer_003`
- Semantic mismatch: **12** (rate: 70.59%)
  - Sample IDs: `aggregate_005, join_006, review_003, review_005, realtime_009, realtime_010, subquery_001, subquery_003, complex_002, product_002`
- Top missing columns:
  - `total_value`: `2`
  - `product_category_name`: `1`
  - `latest_order_date_vn`: `1`
  - `tong_don_hom_nay`: `1`
  - `thoi_gian_vn`: `1`
  - `order_count`: `1`
  - `total_orders`: `1`

## Target Check

- execution_success_rate: **FAIL**
- safety_pass_rate: **PASS**
- semantic_match_rate: **PASS**
- overall_weighted_score: **PASS**

## Case Details

### basic_select_001
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9663`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_002
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_003
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.5714`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9858`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_004
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9825`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_005
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9957`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_006
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9953`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_007
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8364`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9946`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_008
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

### basic_select_009
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9874`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_010
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9971`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_001
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9971`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_002
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9444`
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
- CM: `0.6`
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
- EM: `1.0`
- CM: `1.0`
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
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.8148`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_value']`
  - Số dòng: generated=`5` | gold=`5` | matched=`5` | missing=`0` | extra=`0`

### aggregate_006
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_007
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_008
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.3778`
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
- EM: `1.0`
- CM: `1.0`
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
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9708`
- ExecutionSuccess: `True`
- Errors: `none`

### join_001
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_002
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_003
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9877`
- ExecutionSuccess: `True`
- Errors: `none`

### join_004
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9955`
- ExecutionSuccess: `True`
- Errors: `none`

### join_005
- Category: `join` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.988`
- ExecutionSuccess: `True`
- Errors: `none`

### join_006
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.55`
- EM: `0.0`
- CM: `0.713`
- EX (strict): `0.0`
- EX_partial (F1): `0.25`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name']`
  - Số dòng: generated=`1` | gold=`5` | matched=`1` | missing=`4` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'product_id': '69c590f7ffc7bf8db97190b6cb6ed62e', 'category': 'computers', 'max_item_price_brl': '6729.00'}`
    - `{'product_id': '1bdf5e6731585cf01aa8169c7028d6ad', 'category': 'art', 'max_item_price_brl': '6499.00'}`
    - `{'product_id': 'a6492cc69376c469ab6f61d8f44de961', 'category': 'small_appliances', 'max_item_price_brl': '4799.00'}`

### join_007
- Category: `join` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9524`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9986`
- ExecutionSuccess: `True`
- Errors: `none`

### join_008
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7815`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9977`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### join_009
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_010
- Category: `join` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.7937`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`100` | gold=`50` | matched=`50` | missing=`0` | extra=`50`

### delivery_001
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9572`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9857`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### delivery_002
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### delivery_003
- Category: `delivery` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9753`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### delivery_004
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7821`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9755`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### delivery_005
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9963`
- ExecutionSuccess: `True`
- Errors: `none`

### review_001
- Category: `review` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### review_002
- Category: `review` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9854`
- ExecutionSuccess: `True`
- Errors: `none`

### review_003
- Category: `review` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.82`
- EM: `0.0`
- CM: `0.875`
- EX (strict): `0.0`
- EX_partial (F1): `0.7`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`10` | matched=`7` | missing=`3` | extra=`3`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'category': 'fashion_shoes', 'avg_score': '4.23', 'total_reviews': '261'}`
    - `{'category': 'food', 'avg_score': '4.22', 'total_reviews': '495'}`
    - `{'category': 'cine_photo', 'avg_score': '4.21', 'total_reviews': '73'}`

### review_004
- Category: `review` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7583`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### review_005
- Category: `review` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.675`
- EM: `0.0`
- CM: `0.9318`
- EX (strict): `0.0`
- EX_partial (F1): `0.4583`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`24` | gold=`24` | matched=`11` | missing=`13` | extra=`13`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'month': 'None', 'negative_reviews': '1283'}`
    - `{'month': '2017-03', 'negative_reviews': '352'}`
    - `{'month': '2017-05', 'negative_reviews': '479'}`

### payment_001
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9763`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_002
- Category: `payment` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8333`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9811`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_003
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9932`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_004
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_005
- Category: `payment` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9934`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_001
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_002
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7243`
- EM: `0.0`
- CM: `0.7286`
- EX (strict): `0.0`
- EX_partial (F1): `0.5405`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`27` | gold=`10` | matched=`10` | missing=`0` | extra=`17`

### geography_003
- Category: `geography` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8704`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### geography_004
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9838`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_005
- Category: `geography` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9756`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_001
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7636`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9942`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### realtime_002
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9831`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_003
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.875`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9702`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_004
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9375`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9612`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_005
- Category: `realtime` | Difficulty: `medium`
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

### realtime_006
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5875`
- EM: `0.0`
- CM: `0.681`
- EX (strict): `0.0`
- EX_partial (F1): `0.3125`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`27` | gold=`5` | matched=`5` | missing=`0` | extra=`22`

### realtime_007
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8571`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9999`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_008
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9429`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_009
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.3802`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['thoi_diem_don_moi_nhat_vn']` vs gold: `['latest_order_date_vn', 'tong_don_hom_nay']`
  - ❌ Thiếu cột: `['latest_order_date_vn', 'tong_don_hom_nay']`
  - ➕ Thừa cột: `['thoi_diem_don_moi_nhat_vn']`

### realtime_010
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.8791`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['thoi_gian_vn']`
  - ➕ Thừa cột: `['thoi_gian_dat_vn']`
  - Số dòng: generated=`0` | gold=`0` | matched=`0` | missing=`0` | extra=`0`

### subquery_001
- Category: `subquery` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.2812`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['order_count']`
  - ➕ Thừa cột: `['total_orders']`
  - Số dòng: generated=`3` | gold=`0` | matched=`0` | missing=`0` | extra=`3`

### subquery_002
- Category: `subquery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9643`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### subquery_003
- Category: `subquery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.6768`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_value']`
  - Số dòng: generated=`5` | gold=`5` | matched=`5` | missing=`0` | extra=`0`

### subquery_004
- Category: `subquery` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.9231`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`100` | gold=`20` | matched=`20` | missing=`0` | extra=`80`

### subquery_005
- Category: `subquery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7857`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9836`
- ExecutionSuccess: `True`
- Errors: `none`

### window_001
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9556`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9932`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### window_002
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8333`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### window_003
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9995`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_001
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9012`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### complex_002
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7833`
- EM: `0.0`
- CM: `0.6667`
- EX (strict): `0.0`
- EX_partial (F1): `0.6389`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders']`
  - ➕ Thừa cột: `['total_reviews']`
  - Số dòng: generated=`24` | gold=`24` | matched=`23` | missing=`1` | extra=`1`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'payment_installments': '1', 'avg_review_score': '4.15'}`

### complex_003
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_004
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9612`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_005
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.98`
- ExecutionSuccess: `True`
- Errors: `none`

### product_001
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9979`
- ExecutionSuccess: `True`
- Errors: `none`

### product_002
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.46`
- EM: `0.0`
- CM: `0.963`
- EX (strict): `0.0`
- EX_partial (F1): `0.1`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`10` | matched=`1` | missing=`9` | extra=`9`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'category': 'office_furniture', 'avg_weight_g': '12740.87', 'product_count': '309'}`
    - `{'category': 'kitchen_dining_laundry_garden_furniture', 'avg_weight_g': '11598.56', 'product_count': '94'}`
    - `{'category': 'furniture_bedroom', 'avg_weight_g': '9997.22', 'product_count': '45'}`

### product_003
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9063`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9959`
- ExecutionSuccess: `True`
- Errors: `none`

### product_004
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.61`
- EM: `0.0`
- CM: `0.5778`
- EX (strict): `0.0`
- EX_partial (F1): `0.35`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`20` | gold=`20` | matched=`7` | missing=`13` | extra=`13`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'product_photos_qty': 'None', 'avg_price': '112.00'}`
    - `{'product_photos_qty': '1', 'avg_price': '113.72'}`
    - `{'product_photos_qty': '2', 'avg_price': '111.52'}`

### product_005
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_001
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9707`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_002
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9849`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_003
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_004
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.8`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`10` | matched=`0` | missing=`10` | extra=`10`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_id': 'e3b4998c7a498169dc7bce44e6bb6277', 'seller_city': 'sao paulo', 'seller_state': 'SP', 'avg_revenue_per_order': '6735.00'}`
    - `{'seller_id': '80ceebb4ee9b31afb6c6a916a574a1e2', 'seller_city': 'londrina', 'seller_state': 'PR', 'avg_revenue_per_order': '6729.00'}`
    - `{'seller_id': 'ee27a8f15b1dded4d213a468ba4eb391', 'seller_city': 'goiania', 'seller_state': 'GO', 'avg_revenue_per_order': '6499.00'}`

### seller_005
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9652`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_001
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9167`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_002
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8864`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### trend_003
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_004
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9444`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9902`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_005
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_011
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9896`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_006
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9879`
- ExecutionSuccess: `True`
- Errors: `none`

### customer_001
- Category: `customer` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9809`
- ExecutionSuccess: `True`
- Errors: `none`

### customer_002
- Category: `customer` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### customer_003
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5091`
- EM: `0.0`
- CM: `0.9444`
- EX (strict): `0.0`
- EX_partial (F1): `0.1818`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`10` | matched=`1` | missing=`9` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_city': 'rio de janeiro', 'customer_state': 'RJ', 'total_spent': '955573.97'}`
    - `{'customer_city': 'belo horizonte', 'customer_state': 'MG', 'total_spent': '346039.04'}`
    - `{'customer_city': 'brasilia', 'customer_state': 'DF', 'total_spent': '295814.72'}`

### customer_004
- Category: `customer` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9657`
- ExecutionSuccess: `True`
- Errors: `none`

### customer_005
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### order_001
- Category: `order` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7708`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9644`
- ExecutionSuccess: `True`
- Errors: `none`

### order_002
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.85`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9924`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### order_003
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7879`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### order_004
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8462`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9916`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### order_005
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9879`
- ExecutionSuccess: `True`
- Errors: `none`
