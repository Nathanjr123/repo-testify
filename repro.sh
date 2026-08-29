#!/usr/bin/env bash
# Level-1 reproduction: verifies the case contract, the scorer, and regenerates every number from proof/.
# Needs only Python 3.10+ (no make, no docker, no credentials).
set -euo pipefail; cd "$(dirname "$0")"
python3 -m eval.selftest
python3 tests/test_scorer.py
python3 eval/validate_cases.py
python3 -m eval.runner --arm baseline --cases eval/cases/public --sanity
python3 -m eval.report > RESULTS.md
python3 eval/render_readme.py
ID=$(python3 -c "import json;print([e['id'] for e in json.load(open('proof/build_proof.json')) if e['label']=='advanced-v2-rescored'][-1])")
python3 -m eval.replay --run "$ID"
git diff --quiet -- README.md RESULTS.md && echo "REPRO OK: README/RESULTS regenerate byte-identically from proof" || { echo "REPRO DRIFT: generated tables differ from committed ones"; git --no-pager diff --stat -- README.md RESULTS.md; exit 1; }
