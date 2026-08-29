#!/usr/bin/env bash
# Held-out run: arms run ONCE. Scoring uses whatever truth is in eval/truth (provisional until the human audit);
# after the audit, `python3 -m eval.replay --run <id> --rescore` re-scores the persisted outputs for free.
set -uo pipefail; cd "$(dirname "$0")"
for c in eval/cases/heldout/r*.json; do id=$(basename $c .json); test -f eval/truth/$id.json || { echo "MISSING TRUTH $id"; exit 2; }; done
L=proof/heldout.log; : > $L
python3 -m eval.runner --arm baseline --cases eval/cases/heldout --label baseline-heldout >> $L 2>&1
grep -q "USAGE LIMIT" $L && { echo HALTED_ON_LIMIT >> $L; exit 75; }
python3 -m eval.runner --arm advanced --cases eval/cases/heldout --label advanced-v3-heldout >> $L 2>&1
grep -q "USAGE LIMIT" $L && { echo HALTED_ON_LIMIT >> $L; exit 75; }
find arms-runs -type d -name artifacts -prune -exec rm -rf {} + 2>/dev/null
echo HELDOUT_DONE >> $L
