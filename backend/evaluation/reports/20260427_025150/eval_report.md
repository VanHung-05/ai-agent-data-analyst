# SQL Evaluation Report

- GeneratedAt: 2026-04-26T19:58:20.015045+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **20** / InputSamples: **20**
- ExecutionSuccessRate: **70.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **90.00%**
- OverallWeightedScore: **87.95%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.25**
- Component Match (CM) mean: **0.8221**
- Execution Accuracy (EX) mean: **0.7**
- Partial Execution / F1 (EX_partial) mean: **0.8708**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.6974**

- EM_gte_0.8: **FAIL**
- CM_gte_0.8: **PASS**
- EX_gte_0.9: **FAIL**
- VES_gte_1.0: **FAIL**

## EX Failure Dashboard

- EX failed total: **6**
- Alias-only mismatch: **0** (rate: 0.00%)
- LIMIT/TOP-N mismatch: **1** (rate: 16.67%)
  - Sample IDs: `aggregate_009`
- Semantic mismatch: **5** (rate: 83.33%)
  - Sample IDs: `basic_select_004, basic_select_010, aggregate_005, aggregate_006, aggregate_007`
- Top missing columns:
  - `product_category_name`: `1`
  - `product_category_name_english`: `1`
  - `total_value`: `1`
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
- CM: `0.8571`
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
- CM: `0.4444`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9811`
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
- SemanticScore: `1.0`
- EM: `1.0`
- CM: `1.0`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9941`
- ExecutionSuccess: `True`
- Errors: `none`

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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_010
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.7`
- EM: `0.0`
- CM: `0.5556`
- EX (strict): `0.0`
- EX_partial (F1): `0.5`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['product_category_name_english']`
  - ➕ Thừa cột: `['category_english']`
  - Số dòng: generated=`71` | gold=`71` | matched=`71` | missing=`0` | extra=`0`

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
- CM: `0.9444`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9948`
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
- SemanticScore: `0.4`
- EM: `0.0`
- CM: `0.7778`
- EX (strict): `0.0`
- EX_partial (F1): `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
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
- CM: `0.3778`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9876`
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
- EM: `0.0`
- CM: `0.9444`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9912`
- ExecutionSuccess: `True`
- Errors: `none`
