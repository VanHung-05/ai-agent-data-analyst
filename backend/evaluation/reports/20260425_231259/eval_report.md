# SQL Evaluation Report

- GeneratedAt: 2026-04-25T16:17:27.157928+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **10** / InputSamples: **10**
- ExecutionSuccessRate: **60.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **80.00%**
- OverallWeightedScore: **83.90%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.4**
- Component Match (CM) mean: **0.6495**
- Execution Accuracy (EX) mean: **0.6**
- Partial Execution / F1 (EX_partial) mean: **0.8247**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.5941**

- EM_gte_0.8: **FAIL**
- CM_gte_0.8: **FAIL**
- EX_gte_0.9: **FAIL**
- VES_gte_1.0: **FAIL**

## Target Check

- execution_success_rate: **FAIL**
- safety_pass_rate: **PASS**
- semantic_match_rate: **PASS**
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
- VES: `0.9752`
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
- VES: `0.9918`
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
- VES: `0.9736`
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
