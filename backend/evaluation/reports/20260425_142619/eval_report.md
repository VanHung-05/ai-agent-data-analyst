# SQL Evaluation Report

- GeneratedAt: 2026-04-25T07:55:07.351311+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- ExecutionSuccessRate: **35.00%**
- SafetyPassRate: **65.00%**
- SemanticMatchRate: **65.00%**
- OverallWeightedScore: **53.99%**

## Benchmark metrics (Spider / BIRD style)

- Exact Match (EM) mean: **0.0**
- Component Match (CM) mean: **0.4113**
- Execution Accuracy (EX) mean: **0.5385**
- Valid Efficiency Score (VES) mean: **0.5384**

- EM_gte_0.8: **FAIL**
- CM_gte_0.8: **FAIL**
- EX_gte_0.9: **FAIL**
- VES_gte_1.0: **FAIL**

## Target Check

- execution_success_rate: **FAIL**
- safety_pass_rate: **FAIL**
- semantic_match_rate: **FAIL**
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
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`

### basic_select_003
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.4444`
- EX: `1.0`
- VES: `0.984`
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
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9091`
- EX: `1.0`
- VES: `1.0058`
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
- EX: `1.0`
- VES: `1.0139`
- ExecutionSuccess: `True`
- Errors: `none`

### basic_select_009
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.925`
- EM: `0.0`
- CM: `0.5481`
- EX: `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`

### basic_select_010
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.9915`
- EM: `0.0`
- CM: `0.16`
- EX: `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`

### aggregate_001
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.9231`
- EX: `1.0`
- VES: `0.9882`
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
- EX: `1.0`
- VES: `1.0107`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_003
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6042`
- EX: `1.0`
- VES: `0.9884`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_004
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`

### aggregate_005
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.675`
- EX: `1.0`
- VES: `1.0085`
- ExecutionSuccess: `True`
- Errors: `none`

### aggregate_006
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.925`
- EM: `0.0`
- CM: `0.8049`
- EX: `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`

### aggregate_007
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.5164`
- EX: `0.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`

### aggregate_008
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`

### aggregate_009
- Category: `aggregate` | Difficulty: `easy`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`

### aggregate_010
- Category: `aggregate` | Difficulty: `medium`
- SyntaxPass: `False`
- SafetyPass: `False`
- PerformancePass: `False`
- SemanticScore: `0.0`
- EM: `0.0`
- CM: `0.0`
- ExecutionSuccess: `False`
- Errors: `generate_sql_error: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}; generated_sql_empty`
