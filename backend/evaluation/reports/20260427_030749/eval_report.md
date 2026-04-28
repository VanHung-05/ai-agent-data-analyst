# SQL Evaluation Report

- GeneratedAt: 2026-04-26T20:14:47.859596+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **20** / InputSamples: **20**
- ExecutionSuccessRate: **85.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **95.00%**
- OverallWeightedScore: **94.05%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.45**
- Component Match (CM) mean: **0.8718**
- Execution Accuracy (EX) mean: **0.85**
- Partial Execution / F1 (EX_partial) mean: **0.9417**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.8412**

- EM_gte_0.8: **FAIL**
- CM_gte_0.8: **PASS**
- EX_gte_0.9: **FAIL**
- VES_gte_1.0: **FAIL**

## EX Failure Dashboard

- EX failed total: **3**
- Alias-only mismatch: **0** (rate: 0.00%)
- LIMIT/TOP-N mismatch: **1** (rate: 33.33%)
  - Sample IDs: `aggregate_009`
- Semantic mismatch: **2** (rate: 66.67%)
  - Sample IDs: `basic_select_006, aggregate_010`

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
- VES: `0.9558`
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
- CM: `0.6667`
- EX (strict): `1.0`
- EX_partial (F1): `1.0`
- VES: `0.9955`
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
- VES: `0.9989`
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
- VES: `0.9867`
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
- EM: `0.0`
- CM: `0.8364`
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
- VES: `0.9593`
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
- VES: `0.9888`
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
- VES: `1.0`
- ExecutionSuccess: `True`
- Errors: `none`

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
- VES: `0.9795`
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
- VES: `0.996`
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
- VES: `0.9634`
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
- CM: `0.8852`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ➕ Thừa cột: `['total_orders']`
  - Số dòng: generated=`3` | gold=`3` | matched=`3` | missing=`0` | extra=`0`
