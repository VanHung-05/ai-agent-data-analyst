# SQL Evaluation Report

- GeneratedAt: 2026-04-25T15:55:43.046410+00:00
- Dataset: `/Users/macbook/Documents/HK2_Nam3(2526)/Theory/Cloud/ai-agent-data-analyst/backend/evaluation/eval_dataset.json`
- GeneratorMode: `sql_only`

## Summary Metrics

- EvaluatedSamples: **10** / InputSamples: **10**
- ExecutionSuccessRate: **30.00%**
- SafetyPassRate: **100.00%**
- SemanticMatchRate: **70.00%**
- OverallWeightedScore: **72.20%**

## Benchmark metrics (Spider / BIRD style)

> **Giải thích metrics:**
> - **EM**: Khớp chính xác chuỗi SQL sau normalize (rất khắt khe).
> - **CM**: So khớp từng mệnh đề (SELECT/WHERE/GROUP BY...) độc lập, Jaccard similarity.
> - **EX**: Kết quả thực thi khớp hoàn toàn với gold (column-order-insensitive, float-epsilon).
> - **EX_partial**: F1-score dựa trên số dòng khớp (partial credit khi EX < 1.0).
> - **VES**: Hiệu năng SQL so với gold — `sqrt(T_gold/T_gen)`, cap = 1.0 (chuẩn BIRD).

- Exact Match (EM) mean: **0.1**
- Component Match (CM) mean: **0.557**
- Execution Accuracy (EX) mean: **0.3**
- Partial Execution / F1 (EX_partial) mean: **0.7247**
- Valid Efficiency Score (VES) mean [cap=1.0]: **0.3**

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
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.4926`
- EX (strict): `0.0`
- EX_partial (F1): `0.75`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['thoi_gian_vn']`
  - ➕ Thừa cột: `['order_purchase_timestamp']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

### basic_select_002
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.6667`
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
  - ❌ Thiếu cột: `['review_comment_title', 'review_creation_date_vn']`
  - ➕ Thừa cột: `['review_creation_date']`
  - Số dòng: generated=`5` | gold=`5` | matched=`0` | missing=`5` | extra=`5`
  - Sample dòng gold không khớp (tối đa 3):
    - `{'review_score': '1', 'review_id': 'f238b2f2738a38e3058911efccd46f9c', 'order_id': 'd4dcec44106e7301b362ee4b771b7ff3', 'review_comment_message': 'O pedido se tratava de 5 frascos de oleo de linhaça, veio 1oleo de coco. Se não tinha os 5, não deveria vender.Estou a 2 dias tentando contato com por e_mail e ninguem responde. Por telefone e imposs'}`
    - `{'review_score': '1', 'review_id': '2c573bdf789cae8761dc8357cc6d2663', 'order_id': '919baca007d9525b6668c18f79a33197', 'review_comment_message': 'Não recebi meu produto e ainda não respondem meus contatos. Horrível essa loja '}`
    - `{'review_score': '1', 'review_id': 'b321ab5a94150664805153075900edf6', 'order_id': '9cb197309d8105d9d407533fce50ae34', 'review_comment_message': 'None'}`

### basic_select_007
- Category: `basic_select` | Difficulty: `easy`
- SyntaxPass: `True`
- SafetyPass: `True`
- PerformancePass: `True`
- SemanticScore: `1.0`
- EM: `0.0`
- CM: `0.7273`
- EX (strict): `0.0`
- EX_partial (F1): `1.0`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - Số dòng: generated=`1` | gold=`1` | matched=`1` | missing=`0` | extra=`0`

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
- SemanticScore: `0.85`
- EM: `0.0`
- CM: `0.5481`
- EX (strict): `0.0`
- EX_partial (F1): `0.75`
- VES: `0.0`
- ExecutionSuccess: `False`
- Errors: `none`
- **EX Diff Analysis:**
  - ❌ Thiếu cột: `['thoi_gian_vn']`
  - ➕ Thừa cột: `['order_purchase_timestamp']`
  - Số dòng: generated=`10` | gold=`10` | matched=`10` | missing=`0` | extra=`0`

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
