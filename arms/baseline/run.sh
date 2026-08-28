#!/usr/bin/env bash
# BASELINE: one-shot LLM with README + file tree only. No execution, no iteration.
# Usage: run.sh <case.json>  -> report JSON on stdout
set -euo pipefail
CASE="$1"
python3 "$(dirname "$0")/baseline.py" "$CASE"
