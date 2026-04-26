# SQL Evaluation Report

- GeneratedAt: 2026-04-25T09:31:59.041217+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **6** / InputSamples: **10**
- SkippedSamples: **4** (cases with errors)
- ExecutionSuccessRate: **50.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **100.00%**
- OverallWeightedScore: **81.58%**

## Benchmark metrics (Spider / BIRD style)

- Exact Match (EM) mean: **0.0**
- Component Match (CM) mean: **0.6062**
- Execution Accuracy (EX) mean: **0.5**
- Valid Efficiency Score (VES) mean: **0.4949**

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
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`

### basic_select_002
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.8571`
- EX: `1.0`
- VES: `0.9944`
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
- EX: `1.0`
- VES: `0.9881`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_004
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- EM: `0.0`
- CM: `0.5926`
- EX: `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`

### basic_select_005
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`

### basic_select_006
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9`
- EM: `0.0`
- CM: `0.7692`
- EX: `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`

### basic_select_007
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`

### basic_select_008
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`

### basic_select_009
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.925`
- EM: `0.0`
- CM: `0.4926`
- EX: `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`

### basic_select_010
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.4815`
- EX: `1.0`
- VES: `0.987`
- ExecutionSuccess: `True`
- Errors: `none`
