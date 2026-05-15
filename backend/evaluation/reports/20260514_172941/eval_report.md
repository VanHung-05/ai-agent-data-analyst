# SQL Evaluation Report

- GeneratedAt: 2026-05-14T11:09:17.920556+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **100** / InputSamples: **100**
- ExecutionSuccessRate: **66.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **83.00%**
- OverallWeightedScore: **86.05%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.28**
- Component Match (CM) mean: **0.8533**
- Execution Accuracy (EX) mean: **0.66**
- Partial Execution / F1 (EX_partial) mean: **0.8294**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.6535**

- EM_gte_0.8: **FAIL**
- CM_gte_0.8: **PASS**
- EX_gte_0.9: **FAIL**
- VES_gte_1.0: **FAIL**

## EX Failure Dashboard

- EX failed total: **34**
- Alias-only mismatch: **0** (rate: 0.00%)
- LIMIT/TOP-N mismatch: **6** (rate: 17.65%)
  - Sample IDs: `aggregate_009, join_010, geography_004, realtime_006, subquery_004, seller_004`
- Semantic mismatch: **28** (rate: 82.35%)
  - Sample IDs: `basic_select_005, basic_select_006, aggregate_005, aggregate_006, join_003, join_006, join_008, join_009, delivery_005, review_001`
- Top missing columns:
  - `total_orders`: `5`
  - `product_category_name`: `5`
  - `total_value`: `3`
  - `total_spent`: `2`
  - `seller_zip_code_prefix`: `1`
  - `late_orders`: `1`
  - `total_reviews`: `1`
  - `total_transactions`: `1`
  - `order_id`: `1`
  - `tong_don_hom_nay`: `1`

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
- VES: `0.9851`
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
- VES: `0.9898`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_003
- Category: `basic_select` | Difficulty: `easy`
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
- VES: `0.988`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_005
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.9091`
- EX (strict): `0.0`
- EX_partial (F1): `0.75`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['seller_zip_code_prefix']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### basic_select_006
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.8462`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`5` | gold=`5` | matched=`0` | missing=`5` | extra=`5`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'review_id': '15197aa66ff4d0650b5434f1b46cda19', 'order_id': 'b18dcdf73be66366873cd26c5724d1dc', 'review_score': '1', 'review_comment_message': 'None', 'review_creation_date': '2018-04-13 00:00:00+00:00'}`
    - `{'review_id': '373cbeecea8286a2b66c97b1b157ec46', 'order_id': '583174fbe37d3d5f0d6661be3aad1786', 'review_score': '1', 'review_comment_message': 'Péssimo', 'review_creation_date': '2018-08-15 00:00:00+00:00'}`
    - `{'review_id': '2c5e27fc178bde7ac173c9c62c31b070', 'order_id': '0ce9a24111d850192a933fcaab6fbad3', 'review_score': '1', 'review_comment_message': 'Não gostei ! Comprei gato por lebre', 'review_creation_date': '2017-12-13 00:00:00+00:00'}`

### basic_select_007
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9091`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9725`
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
- VES: `0.9946`
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
- VES: `0.9893`
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
- CM: `0.6625`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9815`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_004
- Category: `aggregate` | Difficulty: `medium`
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
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.9407`
- EX (strict): `0.0`
- EX_partial (F1): `0.75`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders']`
  - Số dòng: generated=`9` | gold=`9` | matched=`9` | missing=`0` | extra=`0`

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
- VES: `0.9888`
- ExecutionSuccess: `True`
- Errors: `none`

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
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9728`
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
- VES: `0.9902`
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
- CM: `0.8815`
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
- VES: `0.9014`
- ExecutionSuccess: `True`
- Errors: `none`

### join_006
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.55`
- EM: `0.0`
- CM: `0.2654`
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
- CM: `0.8`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9558`
- ExecutionSuccess: `True`
- Errors: `none`

### join_008
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.7259`
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
- SemanticScore: `0.805`
- EM: `0.0`
- CM: `0.659`
- EX (strict): `0.0`
- EX_partial (F1): `0.675`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_spent']`
  - ➕ Thừa cột: `['monetary']`
  - Số dòng: generated=`10` | gold=`10` | matched=`9` | missing=`1` | extra=`1`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_unique_id': 'c8460e4251689ba205045f3ea17884a1', 'customer_city': 'porto alegre', 'customer_state': 'RS'}`

### join_010
- Category: `join` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.9286`
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
- CM: `0.836`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9966`
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
- VES: `0.9963`
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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### delivery_005
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6933`
- EM: `0.0`
- CM: `0.7045`
- EX (strict): `0.0`
- EX_partial (F1): `0.4889`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['late_orders']`
  - ➕ Thừa cột: `['late_deliveries', 'total_delivered', 'late_pct']`
  - Số dòng: generated=`23` | gold=`22` | matched=`22` | missing=`0` | extra=`1`

### review_001
- Category: `review` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.7143`
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
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
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
- CM: `0.6583`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9432`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### review_005
- Category: `review` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8875`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### payment_002
- Category: `payment` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.8426`
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
- CM: `0.7625`
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
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8766`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9985`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

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
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9524`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9848`
- ExecutionSuccess: `True`
- Errors: `none`

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
- VES: `0.9728`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### geography_004
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7637`
- EM: `0.0`
- CM: `0.8611`
- EX (strict): `0.0`
- EX_partial (F1): `0.6061`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`23` | matched=`10` | missing=`13` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_state': 'CE', 'total_sellers': '13'}`
    - `{'seller_state': 'PE', 'total_sellers': '9'}`
    - `{'seller_state': 'PB', 'total_sellers': '6'}`

### geography_005
- Category: `geography` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.8615`
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
- CM: `0.7636`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9932`
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
- CM: `0.875`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
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
- VES: `1.0`
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
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.681`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`5` | matched=`5` | missing=`0` | extra=`5`

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
- VES: `0.9932`
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
- VES: `0.9917`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_009
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.4364`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['tong_don_hom_nay']`
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### realtime_010
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8791`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

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
- VES: `0.9919`
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
- CM: `0.7143`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9798`
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
- VES: `1.0`
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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### complex_001
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9876`
- ExecutionSuccess: `True`
- Errors: `none`

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
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.9467`
- EX (strict): `0.0`
- EX_partial (F1): `0.75`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

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
- VES: `0.9881`
- ExecutionSuccess: `True`
- Errors: `none`

### product_001
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.535`
- EM: `0.0`
- CM: `0.7222`
- EX (strict): `0.0`
- EX_partial (F1): `0.225`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name', 'category_english', 'total_sold']`
  - ➕ Thừa cột: `['category', 'total_orders']`
  - Số dòng: generated=`10` | gold=`10` | matched=`9` | missing=`1` | extra=`1`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'product_id': '3dd2a17168ec895c781a9191c1e95ad7'}`

### product_002
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.4497`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name', 'avg_weight']`
  - ➕ Thừa cột: `['avg_weight_g', 'product_count']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### product_003
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5818`
- EM: `0.0`
- CM: `0.7098`
- EX (strict): `0.0`
- EX_partial (F1): `0.303`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name', 'product_category_name_english']`
  - ➕ Thừa cột: `['category']`
  - Số dòng: generated=`5` | gold=`6` | matched=`5` | missing=`1` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'product_count': '3'}`

### product_004
- Category: `product` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.61`
- EM: `0.0`
- CM: `0.5111`
- EX (strict): `0.0`
- EX_partial (F1): `0.35`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['product_count']`
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
- VES: `0.9965`
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
- VES: `0.9969`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_002
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.88`
- EM: `0.0`
- CM: `0.8929`
- EX (strict): `0.0`
- EX_partial (F1): `0.8`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['seller_state']`
  - Số dòng: generated=`10` | gold=`10` | matched=`8` | missing=`2` | extra=`2`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'category_count': '14', 'seller_id': '44073f8b7e41514de3b7815dd0237f4f', 'seller_city': 'brasilia'}`
    - `{'category_count': '14', 'seller_id': '7178f9f4dd81dcef02f62acdf8151e01', 'seller_city': 'videira'}`

### seller_003
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.9214`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`10` | matched=`0` | missing=`10` | extra=`10`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_id': '54965bbe3e4f07ae045b90b0b8541f52', 'seller_city': 'foz do iguacu', 'seller_state': 'PR', 'total_orders': '81', 'late_orders': '26', 'late_rate': '32.10'}`
    - `{'seller_id': '2a1348e9addc1af5aaa619b1a3679d6b', 'seller_city': 'belo horizonte', 'seller_state': 'MG', 'total_orders': '51', 'late_orders': '15', 'late_rate': '29.41'}`
    - `{'seller_id': '6039e27294dc75811c0d8a39069f52c0', 'seller_city': 'osasco', 'seller_state': 'SP', 'total_orders': '74', 'late_orders': '19', 'late_rate': '25.68'}`

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
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9856`
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
- VES: `0.9833`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_002
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8732`
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
- VES: `0.9623`
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
- VES: `0.9848`
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
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.8704`
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
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### customer_002
- Category: `customer` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8222`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9186`
- ExecutionSuccess: `True`
- Errors: `none`

### customer_003
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.6593`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_spent']`
  - ➕ Thừa cột: `['total_revenue']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

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
- VES: `1.0`
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
- CM: `0.8958`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
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
- VES: `0.9994`
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
- CM: `0.8788`
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
- CM: `0.7436`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
- **EX Diff Analysis:**

### order_005
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8788`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`
