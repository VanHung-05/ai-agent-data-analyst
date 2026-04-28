#!/usr/bin/env bash
set -euo pipefail

# One-shot evaluation (no baseline/candidate split)
# Default: SQL-only generation, 100 samples, with retry enabled.
#
# Usage:
# ./evaluation/run_eval_once.sh \
#   --dataset evaluation/eval_dataset.json \
#   --max-samples 100

DATASET="evaluation/eval_dataset.json"
MAX_SAMPLES="100"
OUTPUT_ROOT="evaluation/reports"
GENERATOR="sql_only"
MIN_REQUEST_INTERVAL_SEC="4.2"
ESTIMATED_LLM_CALLS_PER_SAMPLE="1"
GENERATION_MAX_ATTEMPTS="3"
API_URL="http://localhost:8000/api/v1/chat/query"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dataset) DATASET="$2"; shift 2 ;;
    --max-samples) MAX_SAMPLES="$2"; shift 2 ;;
    --output-root) OUTPUT_ROOT="$2"; shift 2 ;;
    --generator) GENERATOR="$2"; shift 2 ;;
    --min-request-interval-sec) MIN_REQUEST_INTERVAL_SEC="$2"; shift 2 ;;
    --estimated-llm-calls-per-sample) ESTIMATED_LLM_CALLS_PER_SAMPLE="$2"; shift 2 ;;
    --generation-max-attempts) GENERATION_MAX_ATTEMPTS="$2"; shift 2 ;;
    --api-url) API_URL="$2"; shift 2 ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"
OUTPUT_DIR="${OUTPUT_ROOT}/${TIMESTAMP}"
mkdir -p "${OUTPUT_DIR}"

echo "[INFO] Run one-shot evaluation..."
python3 -m evaluation.sql_eval_runner \
  --dataset "${DATASET}" \
  --output-dir "${OUTPUT_DIR}" \
  --generator "${GENERATOR}" \
  --api-url "${API_URL}" \
  --min-request-interval-sec "${MIN_REQUEST_INTERVAL_SEC}" \
  --estimated-llm-calls-per-sample "${ESTIMATED_LLM_CALLS_PER_SAMPLE}" \
  --generation-max-attempts "${GENERATION_MAX_ATTEMPTS}" \
  --max-samples "${MAX_SAMPLES}"

echo "[DONE] Report dir: ${OUTPUT_DIR}"
