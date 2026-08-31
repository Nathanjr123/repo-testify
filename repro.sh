#!/usr/bin/env bash
# Level-1 reproduction: verifies the case contract, the scorer, and regenerates every number from proof/.
# Needs only Python 3.10+ (no make, no docker, no credentials, no git — runs from a plain source archive).
set -euo pipefail; cd "$(dirname "$0")"
python3 -m eval.selftest
python3 tests/test_scorer.py
python3 eval/validate_cases.py
python3 -m eval.runner --arm baseline --cases eval/cases/public --sanity
# snapshot the shipped tables BEFORE regenerating, so we can compare without depending on git
before_readme=$(sha256sum README.md | cut -d' ' -f1)
before_results=$(sha256sum RESULTS.md 2>/dev/null | cut -d' ' -f1 || echo missing)
python3 -m eval.report > RESULTS.md
python3 eval/render_readme.py
ID=$(python3 -c "import json;print([e['id'] for e in json.load(open('proof/build_proof.json')) if e['label']=='advanced-v2-rescored'][-1])")
python3 -m eval.replay --run "$ID"
after_readme=$(sha256sum README.md | cut -d' ' -f1)
after_results=$(sha256sum RESULTS.md | cut -d' ' -f1)
if [ "$before_readme" = "$after_readme" ] && [ "$before_results" = "$after_results" ]; then
  echo "REPRO OK: README/RESULTS regenerate byte-identically from proof"
else
  echo "REPRO DRIFT: generated tables differ from the shipped ones"
  [ "$before_readme" != "$after_readme" ] && echo "  README.md changed"
  [ "$before_results" != "$after_results" ] && echo "  RESULTS.md changed"
  exit 1
fi
