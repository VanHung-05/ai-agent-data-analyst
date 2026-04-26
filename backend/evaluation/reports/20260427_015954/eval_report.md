# SQL Evaluation Report

- GeneratedAt: 2026-04-26T19:28:58.325452+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **100** / InputSamples: **100**
- ExecutionSuccessRate: **47.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **61.00%**
- OverallWeightedScore: **77.48%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.08**
- Component Match (CM) mean: **0.7561**
- Execution Accuracy (EX) mean: **0.47**
- Partial Execution / F1 (EX_partial) mean: **0.6689**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.4653**

- EM_gte_0.8: **FAIL**
- CM_gte_0.8: **FAIL**
- EX_gte_0.9: **FAIL**
- VES_gte_1.0: **FAIL**

## EX Failure Dashboard

- EX failed total: **53**
- Alias-only mismatch: **0** (rate: 0.00%)
- LIMIT/TOP-N mismatch: **10** (rate: 18.87%)
  - Sample IDs: `basic_select_010, aggregate_009, join_010, review_004, geography_002, realtime_006, window_003, seller_004, seller_005, seller_006`
- Semantic mismatch: **43** (rate: 81.13%)
  - Sample IDs: `basic_select_004, basic_select_006, aggregate_007, aggregate_008, join_003, join_006, join_008, join_009, delivery_002, delivery_004`
- Top missing columns:
  - `product_category_name`: `4`
  - `total_orders`: `4`
  - `total_value`: `3`
  - `customer_city`: `2`
  - `customer_state`: `2`
  - `total_reviews`: `2`
  - `product_count`: `2`
  - `review_id`: `1`
  - `total_freight`: `1`
  - `avg_delivery_days`: `1`

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
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9548`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_002
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8571`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9686`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_003
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.4444`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9812`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_004
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.8519`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_006
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.7846`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['review_id']`
  - Số dòng: generated=`5` | gold=`5` | matched=`0` | missing=`5` | extra=`5`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'review_score': '1', 'order_id': 'b18dcdf73be66366873cd26c5724d1dc', 'review_comment_message': 'None', 'review_creation_date': '2018-04-13 00:00:00+00:00'}`
    - `{'review_score': '1', 'order_id': '583174fbe37d3d5f0d6661be3aad1786', 'review_comment_message': 'Péssimo', 'review_creation_date': '2018-08-15 00:00:00+00:00'}`
    - `{'review_score': '1', 'order_id': '0ce9a24111d850192a933fcaab6fbad3', 'review_comment_message': 'Não gostei ! Comprei gato por lebre', 'review_creation_date': '2017-12-13 00:00:00+00:00'}`

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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

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
- VES: `0.969`
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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_010
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9917`
- EM: `0.0`
- CM: `0.1556`
- EX (strict): `0.0`
- EX_partial (F1): `0.9861`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`73` | gold=`71` | matched=`71` | missing=`0` | extra=`2`

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
- CM: `0.8611`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.997`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_003
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.776`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9989`
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
- VES: `0.9885`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_005
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

### aggregate_006
- Category: `aggregate` | Difficulty: `medium`
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

### aggregate_007
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.5926`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_freight']`
  - ➕ Thừa cột: `['total_freight_value']`
  - Số dòng: generated=`27` | gold=`27` | matched=`27` | missing=`0` | extra=`0`

### aggregate_008
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.775`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`0` | missing=`1` | extra=`1`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'avg_items_per_order': '1.14'}`

### aggregate_009
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- EM: `0.0`
- CM: `0.8333`
- EX (strict): `0.0`
- EX_partial (F1): `0.8333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`5` | gold=`7` | matched=`5` | missing=`2` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'review_score': '4', 'total_reviews': '19142'}`
    - `{'review_score': '5', 'total_reviews': '57328'}`

### aggregate_010
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7963`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9845`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### join_001
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8765`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9721`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### join_002
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9286`
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
- SemanticScore: `0.88`
- EM: `0.0`
- CM: `0.9316`
- EX (strict): `0.0`
- EX_partial (F1): `0.8`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### join_004
- Category: `join` | Difficulty: `medium`
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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### join_006
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.55`
- EM: `0.0`
- CM: `0.4444`
- EX (strict): `0.0`
- EX_partial (F1): `0.25`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name']`
  - Số dòng: generated=`1` | gold=`5` | matched=`1` | missing=`4` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'product_id': '69c590f7ffc7bf8db97190b6cb6ed62e', 'category_english': 'computers', 'max_item_price_brl': '6729.00'}`
    - `{'product_id': '1bdf5e6731585cf01aa8169c7028d6ad', 'category_english': 'art', 'max_item_price_brl': '6499.00'}`
    - `{'product_id': 'a6492cc69376c469ab6f61d8f44de961', 'category_english': 'small_appliances', 'max_item_price_brl': '4799.00'}`

### join_007
- Category: `join` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.881`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9744`
- ExecutionSuccess: `True`
- Errors: `none`

### join_008
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.7747`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders']`
  - Số dòng: generated=`22` | gold=`22` | matched=`22` | missing=`0` | extra=`0`

### join_009
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.67`
- EM: `0.0`
- CM: `0.5879`
- EX (strict): `0.0`
- EX_partial (F1): `0.45`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['customer_city', 'customer_state']`
  - Số dòng: generated=`10` | gold=`10` | matched=`9` | missing=`1` | extra=`1`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_unique_id': 'c8460e4251689ba205045f3ea17884a1', 'total_spent': '4655.88'}`

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
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### delivery_002
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.6558`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['avg_delivery_days']`
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### delivery_003
- Category: `delivery` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8148`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9802`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### delivery_004
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4436`
- EM: `0.0`
- CM: `0.6227`
- EX (strict): `0.0`
- EX_partial (F1): `0.0727`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['thoi_gian_mua_vn', 'ngay_du_kien_vn', 'ngay_giao_thuc_te_vn']`
  - ➕ Thừa cột: `['order_delivered_customer_date', 'order_estimated_delivery_date']`
  - Số dòng: generated=`100` | gold=`10` | matched=`10` | missing=`0` | extra=`90`

### delivery_005
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9097`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### review_001
- Category: `review` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.6667`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_reviews']`
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### review_002
- Category: `review` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9328`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### review_003
- Category: `review` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4988`
- EM: `0.0`
- CM: `0.7443`
- EX (strict): `0.0`
- EX_partial (F1): `0.1646`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_reviews']`
  - Số dòng: generated=`71` | gold=`10` | matched=`10` | missing=`0` | extra=`61`

### review_004
- Category: `review` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.4854`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### review_005
- Category: `review` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6625`
- EM: `0.0`
- CM: `0.6`
- EX (strict): `0.0`
- EX_partial (F1): `0.4375`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['negative_reviews']`
  - ➕ Thừa cột: `['negative_review_count']`
  - Số dòng: generated=`24` | gold=`24` | matched=`21` | missing=`3` | extra=`3`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'month': 'None'}`
    - `{'month': '2016-11'}`
    - `{'month': '2016-12'}`

### payment_001
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9545`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### payment_002
- Category: `payment` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.6722`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_transactions']`
  - Số dòng: generated=`5` | gold=`5` | matched=`5` | missing=`0` | extra=`0`

### payment_003
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.7361`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_value']`
  - Số dòng: generated=`24` | gold=`24` | matched=`24` | missing=`0` | extra=`0`

### payment_004
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.719`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['yr', 'total_value']`
  - ➕ Thừa cột: `['order_year', 'total_payment_value']`
  - Số dòng: generated=`13` | gold=`13` | matched=`13` | missing=`0` | extra=`0`

### payment_005
- Category: `payment` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4545`
- EM: `0.0`
- CM: `0.2407`
- EX (strict): `0.0`
- EX_partial (F1): `0.0909`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['order_id']`
  - Số dòng: generated=`1` | gold=`10` | matched=`1` | missing=`9` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'total_paid': '7274.88'}`
    - `{'total_paid': '6929.31'}`
    - `{'total_paid': '6922.21'}`

### geography_001
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.9524`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`10` | matched=`0` | missing=`10` | extra=`10`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_city': 'sao paulo', 'customer_state': 'SP', 'total_customers': '14984'}`
    - `{'customer_city': 'rio de janeiro', 'customer_state': 'RJ', 'total_customers': '6620'}`
    - `{'customer_city': 'belo horizonte', 'customer_state': 'MG', 'total_customers': '2672'}`

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
- CM: `0.9444`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9892`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_004
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8611`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9945`
- ExecutionSuccess: `True`
- Errors: `none`

### geography_005
- Category: `geography` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.6769`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`0` | missing=`1` | extra=`1`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'cross_state_orders': '63313'}`

### realtime_001
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9091`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9966`
- ExecutionSuccess: `True`
- Errors: `none`

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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_003
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9375`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9451`
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
- VES: `0.9955`
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
- VES: `0.9794`
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
- VES: `1.0`
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
  - ⚠️ Cột không khớp — generated: `['latest_order_time_vn']` vs gold: `['latest_order_date_vn', 'tong_don_hom_nay']`
  - ❌ Thiếu cột: `['latest_order_date_vn', 'tong_don_hom_nay']`
  - ➕ Thừa cột: `['latest_order_time_vn']`

### realtime_010
- Category: `realtime` | Difficulty: `medium`
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

### subquery_001
- Category: `subquery` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.4188`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['customer_city', 'customer_state', 'order_count']`
  - ➕ Thừa cột: `['total_orders']`
  - Số dòng: generated=`3` | gold=`0` | matched=`0` | missing=`0` | extra=`3`

### subquery_002
- Category: `subquery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6389`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['product_category_name']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

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
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.9231`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`100` | gold=`20` | matched=`0` | missing=`20` | extra=`100`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_id': '5996cddab893a4652a15592fb58ab8db', 'seller_city': 'presidente prudente', 'seller_state': 'SP'}`
    - `{'seller_id': '392353362d22cc2c236e1ee81ff19890', 'seller_city': 'blumenau', 'seller_state': 'SC'}`
    - `{'seller_id': 'a3b0df0065e264a91b7bbf5f844af5cd', 'seller_city': 'sao bernardo do capo', 'seller_state': 'SP'}`

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
- VES: `0.9907`
- ExecutionSuccess: `True`
- Errors: `none`

### window_001
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.784`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['revenue_rank']`
  - Số dòng: generated=`27` | gold=`27` | matched=`27` | missing=`0` | extra=`0`

### window_002
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.997`
- ExecutionSuccess: `True`
- Errors: `none`

### window_003
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6769`
- EM: `0.0`
- CM: `0.8761`
- EX (strict): `0.0`
- EX_partial (F1): `0.4615`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`100` | gold=`30` | matched=`30` | missing=`0` | extra=`70`

### complex_001
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.6296`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['last_purchase_date_vn', 'monetary']`
  - ➕ Thừa cột: `['last_purchase_date', 'monetary_value']`
  - Số dòng: generated=`100` | gold=`20` | matched=`0` | missing=`20` | extra=`100`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'frequency': '1', 'customer_unique_id': '0a0a92112bd4c708ca5fde585afaa872'}`
    - `{'frequency': '2', 'customer_unique_id': 'da122df9eeddfedc1dc1f5349a1a690c'}`
    - `{'frequency': '1', 'customer_unique_id': '763c8b1c9c68a0229c42c9fc6f662b93'}`

### complex_002
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7833`
- EM: `0.0`
- CM: `0.5812`
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
- SemanticScore: `0.49`
- EM: `0.0`
- CM: `0.6412`
- EX (strict): `0.0`
- EX_partial (F1): `0.15`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_delivered', 'late_count', 'late_pct']`
  - ➕ Thừa cột: `['late_delivery_percentage']`
  - Số dòng: generated=`5` | gold=`5` | matched=`3` | missing=`2` | extra=`2`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'category': 'books_technical'}`
    - `{'category': 'home_confort'}`

### complex_004
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.55`
- EM: `0.0`
- CM: `0.7892`
- EX (strict): `0.0`
- EX_partial (F1): `0.25`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders']`
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### complex_005
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5666`
- EM: `0.0`
- CM: `0.7604`
- EX (strict): `0.0`
- EX_partial (F1): `0.2777`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['cancel_rate']`
  - ➕ Thừa cột: `['cancellation_rate']`
  - Số dòng: generated=`20` | gold=`10` | matched=`5` | missing=`5` | extra=`15`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_state': 'SP', 'seller_id': '4c8b8048e33af2bf94f2eb547746a916', 'seller_city': 'ibitinga', 'total_orders': '23', 'canceled_orders': '4'}`
    - `{'seller_state': 'SP', 'seller_id': 'bc47d5d1490df2b36add65d733eafaba', 'seller_city': 'santo andre', 'total_orders': '24', 'canceled_orders': '2'}`
    - `{'seller_state': 'SP', 'seller_id': '23d7c96d4a1160db1c726b248601b25a', 'seller_city': 'capivari', 'total_orders': '53', 'canceled_orders': '3'}`

### product_001
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.729`
- EX (strict): `0.0`
- EX_partial (F1): `0.75`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### product_002
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4099`
- EM: `0.0`
- CM: `0.6212`
- EX (strict): `0.0`
- EX_partial (F1): `0.0165`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_count']`
  - Số dòng: generated=`71` | gold=`10` | matched=`1` | missing=`9` | extra=`70`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'category': 'office_furniture', 'avg_weight_g': '12740.9'}`
    - `{'category': 'kitchen_dining_laundry_garden_furniture', 'avg_weight_g': '11598.6'}`
    - `{'category': 'furniture_bedroom', 'avg_weight_g': '9997.2'}`

### product_003
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6728`
- EM: `0.0`
- CM: `0.7411`
- EX (strict): `0.0`
- EX_partial (F1): `0.4546`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['category']`
  - ➕ Thừa cột: `['product_category_name', 'product_category_name_english']`
  - Số dòng: generated=`6` | gold=`5` | matched=`5` | missing=`0` | extra=`1`

### product_004
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5474`
- EM: `0.0`
- CM: `0.5684`
- EX (strict): `0.0`
- EX_partial (F1): `0.2456`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_count']`
  - Số dòng: generated=`19` | gold=`19` | matched=`7` | missing=`12` | extra=`12`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'product_photos_qty': '1', 'avg_price': '113.72'}`
    - `{'product_photos_qty': '2', 'avg_price': '111.52'}`
    - `{'product_photos_qty': '3', 'avg_price': '135.83'}`

### product_005
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.7778`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['avg_freight']`
  - ➕ Thừa cột: `['avg_freight_value']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

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
- VES: `0.9551`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_002
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.5238`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['seller_state']`
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### seller_003
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8391`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9889`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### seller_004
- Category: `seller` | Difficulty: `medium`
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
  - Số dòng: generated=`100` | gold=`10` | matched=`10` | missing=`0` | extra=`90`

### seller_005
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.2222`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`100` | gold=`20` | matched=`20` | missing=`0` | extra=`80`

### trend_001
- Category: `trend` | Difficulty: `medium`
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

### trend_002
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7621`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.979`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### trend_003
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.6071`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['avg_score']`
  - ➕ Thừa cột: `['avg_review_score']`
  - Số dòng: generated=`10` | gold=`9` | matched=`0` | missing=`9` | extra=`10`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'yr': 'None', 'qtr': 'None', 'total_reviews': '8832'}`
    - `{'yr': '2016', 'qtr': '4', 'total_reviews': '296'}`
    - `{'yr': '2017', 'qtr': '1', 'total_reviews': '3959'}`

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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_005
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8125`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9915`
- ExecutionSuccess: `True`
- Errors: `none`

### join_011
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.463`
- EX (strict): `0.0`
- EX_partial (F1): `0.75`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### seller_006
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.8548`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### customer_001
- Category: `customer` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.7738`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`27` | gold=`27` | matched=`0` | missing=`27` | extra=`27`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'SP', 'total_customers': '40302'}`
    - `{'customer_state': 'RJ', 'total_customers': '12384'}`
    - `{'customer_state': 'MG', 'total_customers': '11259'}`

### customer_002
- Category: `customer` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.253`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.969`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### customer_003
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7937`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### customer_004
- Category: `customer` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.3222`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['new_customers']`
  - ➕ Thừa cột: `['total_new_customers']`
  - Số dòng: generated=`12` | gold=`12` | matched=`12` | missing=`0` | extra=`0`

### customer_005
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5621`
- EM: `0.0`
- CM: `0.671`
- EX (strict): `0.0`
- EX_partial (F1): `0.2702`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['avg_wait_days']`
  - ➕ Thừa cột: `['avg_delivery_days']`
  - Số dòng: generated=`27` | gold=`10` | matched=`10` | missing=`0` | extra=`17`

### order_001
- Category: `order` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8958`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9926`
- ExecutionSuccess: `True`
- Errors: `none`

### order_002
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8333`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9919`
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
- CM: `0.8909`
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
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.7179`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['thoi_gian_dat_vn', 'thoi_gian_giao_vn']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### order_005
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.6299`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`0` | missing=`1` | extra=`1`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'avg_orders_per_day': '124.9'}`
