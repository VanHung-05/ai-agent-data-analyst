# SQL Evaluation Report

- GeneratedAt: 2026-04-26T18:36:58.252679+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **100** / InputSamples: **100**
- ExecutionSuccessRate: **31.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **52.00%**
- OverallWeightedScore: **70.99%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.1**
- Component Match (CM) mean: **0.7055**
- Execution Accuracy (EX) mean: **0.31**
- Partial Execution / F1 (EX_partial) mean: **0.5949**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.3081**

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
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `0.7259`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_002
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8095`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

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
- VES: `0.9938`
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
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7844`
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
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_008
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.2778`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['total_transactions']`
  - Số dòng: generated=`5` | gold=`5` | matched=`5` | missing=`0` | extra=`0`

### basic_select_009
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `0.7259`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9949`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_010
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5481`
- EM: `0.0`
- CM: `0.2143`
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
- CM: `0.6964`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9889`
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
- VES: `0.9933`
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
- VES: `0.9939`
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
- CM: `0.6037`
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
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.675`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.949`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_009
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.625`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9967`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_010
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.8016`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['yr']`
  - ➕ Thừa cột: `['order_year']`
  - Số dòng: generated=`3` | gold=`3` | matched=`3` | missing=`0` | extra=`0`

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
- SemanticScore: `0.7243`
- EM: `0.0`
- CM: `0.7894`
- EX (strict): `0.0`
- EX_partial (F1): `0.5405`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`27` | matched=`10` | missing=`17` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'SC', 'avg_score': '4.07', 'total_reviews': '3623'}`
    - `{'customer_state': 'DF', 'avg_score': '4.06', 'total_reviews': '2148'}`
    - `{'customer_state': 'RO', 'avg_score': '4.05', 'total_reviews': '252'}`

### join_003
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.88`
- EM: `0.0`
- CM: `0.9407`
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
- SemanticScore: `0.7243`
- EM: `0.0`
- CM: `0.7831`
- EX (strict): `0.0`
- EX_partial (F1): `0.5405`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`27` | matched=`10` | missing=`17` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'RR', 'avg_delivery_days': '29.3'}`
    - `{'customer_state': 'AP', 'avg_delivery_days': '27.2'}`
    - `{'customer_state': 'AM', 'avg_delivery_days': '26.4'}`

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
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.6151`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['product_category_name_english', 'total_revenue']` vs gold: `['product_id', 'product_category_name', 'category_english', 'max_item_price_brl']`
  - ❌ Thiếu cột: `['product_id', 'product_category_name', 'category_english', 'max_item_price_brl']`
  - ➕ Thừa cột: `['product_category_name_english', 'total_revenue']`

### join_007
- Category: `join` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7243`
- EM: `0.0`
- CM: `0.8929`
- EX (strict): `0.0`
- EX_partial (F1): `0.5405`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`27` | matched=`10` | missing=`17` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'PE', 'total_orders': '1652'}`
    - `{'customer_state': 'CE', 'total_orders': '1336'}`
    - `{'customer_state': 'PA', 'total_orders': '975'}`

### join_008
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.65`
- EM: `0.0`
- CM: `0.7817`
- EX (strict): `0.0`
- EX_partial (F1): `0.4167`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders']`
  - Số dòng: generated=`10` | gold=`22` | matched=`10` | missing=`12` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_state': 'ES', 'total_revenue': '46941.64'}`
    - `{'seller_state': 'MA', 'total_revenue': '36097.98'}`
    - `{'seller_state': 'CE', 'total_revenue': '19517.84'}`

### join_009
- Category: `join` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.6796`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['customer_city', 'customer_state']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### join_010
- Category: `join` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.44`
- EM: `0.0`
- CM: `0.7623`
- EX (strict): `0.0`
- EX_partial (F1): `0.0667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_payment']`
  - ➕ Thừa cột: `['total_payment_value']`
  - Số dòng: generated=`10` | gold=`50` | matched=`3` | missing=`47` | extra=`7`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'AC', 'payment_type': 'credit_card'}`
    - `{'customer_state': 'AC', 'payment_type': 'boleto'}`
    - `{'customer_state': 'AC', 'payment_type': 'voucher'}`

### delivery_001
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9091`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9884`
- ExecutionSuccess: `True`
- Errors: `none`

### delivery_002
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.6329`
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
- CM: `0.7326`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`27` | gold=`27` | matched=`27` | missing=`0` | extra=`0`

### delivery_004
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.48`
- EM: `0.0`
- CM: `0.65`
- EX (strict): `0.0`
- EX_partial (F1): `0.1333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['thoi_gian_mua_vn', 'ngay_du_kien_vn', 'ngay_giao_thuc_te_vn']`
  - ➕ Thừa cột: `['customer_state']`
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### delivery_005
- Category: `delivery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8068`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`22` | gold=`22` | matched=`22` | missing=`0` | extra=`0`

### review_001
- Category: `review` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.4026`
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
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.7619`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['positive_reviews']`
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### review_003
- Category: `review` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.8125`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### review_004
- Category: `review` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.6829`
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
- CM: `0.5714`
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
- CM: `0.8663`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### payment_002
- Category: `payment` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.5896`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`5` | gold=`5` | matched=`5` | missing=`0` | extra=`0`

### payment_003
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5818`
- EM: `0.0`
- CM: `0.3911`
- EX (strict): `0.0`
- EX_partial (F1): `0.303`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders', 'total_value']`
  - ➕ Thừa cột: `['total_transactions']`
  - Số dòng: generated=`20` | gold=`24` | matched=`20` | missing=`4` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'payment_installments': '0'}`
    - `{'payment_installments': '21'}`
    - `{'payment_installments': '22'}`

### payment_004
- Category: `payment` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.7327`
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
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.3056`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### geography_001
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.6019`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`5` | gold=`10` | matched=`0` | missing=`10` | extra=`5`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_city': 'sao paulo', 'customer_state': 'SP', 'total_customers': '14984'}`
    - `{'customer_city': 'rio de janeiro', 'customer_state': 'RJ', 'total_customers': '6620'}`
    - `{'customer_city': 'belo horizonte', 'customer_state': 'MG', 'total_customers': '2672'}`

### geography_002
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.7806`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`5` | gold=`10` | matched=`5` | missing=`5` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'SC', 'total_orders': '3637'}`
    - `{'customer_state': 'BA', 'total_orders': '3380'}`
    - `{'customer_state': 'DF', 'total_orders': '2140'}`

### geography_003
- Category: `geography` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5875`
- EM: `0.0`
- CM: `0.9444`
- EX (strict): `0.0`
- EX_partial (F1): `0.3125`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`5` | gold=`27` | matched=`5` | missing=`22` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'SC', 'total_revenue': '507012.13'}`
    - `{'customer_state': 'BA', 'total_revenue': '493584.14'}`
    - `{'customer_state': 'DF', 'total_revenue': '296498.41'}`

### geography_004
- Category: `geography` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6143`
- EM: `0.0`
- CM: `0.6131`
- EX (strict): `0.0`
- EX_partial (F1): `0.3571`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`5` | gold=`23` | matched=`5` | missing=`18` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_state': 'RS', 'total_sellers': '129'}`
    - `{'seller_state': 'GO', 'total_sellers': '40'}`
    - `{'seller_state': 'DF', 'total_sellers': '30'}`

### geography_005
- Category: `geography` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.7912`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['total_cross_state_orders']` vs gold: `['cross_state_orders']`
  - ❌ Thiếu cột: `['cross_state_orders']`
  - ➕ Thừa cột: `['total_cross_state_orders']`

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
- VES: `1.0`
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
- VES: `0.996`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_003
- Category: `realtime` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.7039`
- EX (strict): `1.0`
- EX_partial (F1): `0.0`
- VES: `0.9724`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_004
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `0.0`
- VES: `0.994`
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
- VES: `0.9931`
- ExecutionSuccess: `True`
- Errors: `none`

### realtime_006
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.5608`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_rt_orders']`
  - ➕ Thừa cột: `['total_orders']`
  - Số dòng: generated=`0` | gold=`5` | matched=`0` | missing=`5` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'SP'}`
    - `{'customer_state': 'RJ'}`
    - `{'customer_state': 'MG'}`

### realtime_007
- Category: `realtime` | Difficulty: `medium`
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

### realtime_008
- Category: `realtime` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9592`
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
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.9231`
- EX (strict): `1.0`
- EX_partial (F1): `0.0`
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
- CM: `0.2562`
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
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.6119`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['product_category_name']`
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### subquery_003
- Category: `subquery` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.4583`
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
- CM: `0.6154`
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
- CM: `0.4524`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### window_001
- Category: `window_function` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.7929`
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
- CM: `0.8135`
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
- SemanticScore: `0.6077`
- EM: `0.0`
- CM: `0.7472`
- EX (strict): `0.0`
- EX_partial (F1): `0.3461`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['rank_in_state']`
  - Số dòng: generated=`100` | gold=`30` | matched=`30` | missing=`0` | extra=`70`

### complex_001
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5125`
- EM: `0.0`
- CM: `0.6821`
- EX (strict): `0.0`
- EX_partial (F1): `0.1875`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['last_purchase_date_vn']`
  - ➕ Thừa cột: `['last_purchase_date']`
  - Số dòng: generated=`100` | gold=`20` | matched=`15` | missing=`5` | extra=`85`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_unique_id': '0a0a92112bd4c708ca5fde585afaa872', 'frequency': '1', 'monetary': '13440.00'}`
    - `{'customer_unique_id': '763c8b1c9c68a0229c42c9fc6f662b93', 'frequency': '1', 'monetary': '7160.00'}`
    - `{'customer_unique_id': '4007669dec559734d6f53e029e360987', 'frequency': '1', 'monetary': '5934.60'}`

### complex_002
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7833`
- EM: `0.0`
- CM: `0.5648`
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
- SemanticScore: `0.58`
- EM: `0.0`
- CM: `0.7932`
- EX (strict): `0.0`
- EX_partial (F1): `0.3`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['late_count', 'late_pct']`
  - ➕ Thừa cột: `['late_deliveries', 'late_percentage']`
  - Số dòng: generated=`5` | gold=`5` | matched=`3` | missing=`2` | extra=`2`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'category': 'books_technical', 'total_delivered': '263'}`
    - `{'category': 'home_confort', 'total_delivered': '429'}`

### complex_004
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.55`
- EM: `0.0`
- CM: `0.7964`
- EX (strict): `0.0`
- EX_partial (F1): `0.25`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['total_orders']`
  - ➕ Thừa cột: `['total_reviews']`
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### complex_005
- Category: `complex` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4833`
- EM: `0.0`
- CM: `0.7736`
- EX (strict): `0.0`
- EX_partial (F1): `0.1389`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['cancel_rate']`
  - ➕ Thừa cột: `['cancellation_rate']`
  - Số dòng: generated=`50` | gold=`10` | matched=`5` | missing=`5` | extra=`45`
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
- CM: `0.8071`
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
- SemanticScore: `0.4267`
- EM: `0.0`
- CM: `0.6429`
- EX (strict): `0.0`
- EX_partial (F1): `0.0445`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_count']`
  - Số dòng: generated=`20` | gold=`10` | matched=`1` | missing=`9` | extra=`19`
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
- CM: `0.7674`
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
- CM: `0.5458`
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
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.7814`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`20` | gold=`10` | matched=`10` | missing=`0` | extra=`10`

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
- VES: `0.9788`
- ExecutionSuccess: `True`
- Errors: `none`

### seller_002
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.8`
- EM: `0.0`
- CM: `0.6524`
- EX (strict): `0.0`
- EX_partial (F1): `0.6667`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['seller_state']`
  - Số dòng: generated=`20` | gold=`10` | matched=`10` | missing=`0` | extra=`10`

### seller_003
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- EM: `0.0`
- CM: `0.8372`
- EX (strict): `0.0`
- EX_partial (F1): `0.8333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['late_orders']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### seller_004
- Category: `seller` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.6`
- EM: `0.0`
- CM: `0.9444`
- EX (strict): `0.0`
- EX_partial (F1): `0.3333`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### seller_005
- Category: `seller` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4172`
- EM: `0.0`
- CM: `0.1958`
- EX (strict): `0.0`
- EX_partial (F1): `0.0286`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['total_revenue', 'total_orders']`
  - Số dòng: generated=`50` | gold=`20` | matched=`1` | missing=`19` | extra=`49`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'seller_state': 'SP', 'seller_id': '5996cddab893a4652a15592fb58ab8db', 'seller_city': 'presidente prudente'}`
    - `{'seller_state': 'SP', 'seller_id': 'ffc470761de7d0232558ba5e786e57b7', 'seller_city': 'guarulhos'}`
    - `{'seller_state': 'SP', 'seller_id': '1690cada046eb7e92c12f98b1f8a8167', 'seller_city': 'sao paulo'}`

### trend_001
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6875`
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
- CM: `0.875`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`25` | gold=`25` | matched=`25` | missing=`0` | extra=`0`

### trend_003
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.4383`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['avg_score']`
  - ➕ Thừa cột: `['avg_review_score']`
  - Số dòng: generated=`9` | gold=`9` | matched=`0` | missing=`9` | extra=`9`
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
- CM: `0.7963`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9895`
- ExecutionSuccess: `True`
- Errors: `none`

### trend_005
- Category: `trend` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7049`
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
- CM: `0.8185`
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
- SemanticScore: `0.56`
- EM: `0.0`
- CM: `0.8333`
- EX (strict): `0.0`
- EX_partial (F1): `0.2666`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['avg_freight']`
  - ➕ Thừa cột: `['avg_freight_value']`
  - Số dòng: generated=`50` | gold=`10` | matched=`10` | missing=`0` | extra=`40`

### customer_001
- Category: `customer` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.4177`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['total_orders']`
  - Số dòng: generated=`3` | gold=`27` | matched=`0` | missing=`27` | extra=`3`
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
- CM: `0.4583`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### customer_003
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.659`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`3` | gold=`10` | matched=`0` | missing=`10` | extra=`3`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_city': 'sao paulo', 'customer_state': 'SP', 'total_spent': '2107960.17'}`
    - `{'customer_city': 'rio de janeiro', 'customer_state': 'RJ', 'total_spent': '1111732.21'}`
    - `{'customer_city': 'belo horizonte', 'customer_state': 'MG', 'total_spent': '405950.51'}`

### customer_004
- Category: `customer` | Difficulty: `hard`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.2167`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`3` | gold=`12` | matched=`0` | missing=`12` | extra=`3`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'month': '2017-01', 'new_customers': '764'}`
    - `{'month': '2017-02', 'new_customers': '1752'}`
    - `{'month': '2017-03', 'new_customers': '2636'}`

### customer_005
- Category: `customer` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.5385`
- EM: `0.0`
- CM: `0.802`
- EX (strict): `0.0`
- EX_partial (F1): `0.2308`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['avg_wait_days']`
  - ➕ Thừa cột: `['avg_delivery_days']`
  - Số dòng: generated=`3` | gold=`10` | matched=`3` | missing=`7` | extra=`0`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'customer_state': 'AL'}`
    - `{'customer_state': 'PA'}`
    - `{'customer_state': 'SE'}`

### order_001
- Category: `order` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6473`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.986`
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
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### order_003
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6242`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

### order_004
- Category: `order` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.7318`
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
- CM: `0.5361`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ⚠️ Cột không khớp — generated: `['avg_orders_per_day_2017']` vs gold: `['avg_orders_per_day']`
  - ❌ Thiếu cột: `['avg_orders_per_day']`
  - ➕ Thừa cột: `['avg_orders_per_day_2017']`
