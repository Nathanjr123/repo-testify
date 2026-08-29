#!/usr/bin/env bash
# FINAL held-out run, ONCE, after Nate's audit is copied into eval/truth/ (all 7 heldout truth files present, provisional=false).
set -uo pipefail; cd "$(dirname "$0")"
for c in eval/cases/heldout/r*.json; do id=$(basename $c .json); test -f eval/truth/$id.json || { echo "MISSING TRUTH $id, audit first"; exit 2; }; done
grep -l '"provisional": true' eval/truth/r03-* eval/truth/r06-* eval/truth/r08-* eval/truth/r10-* eval/truth/r12-* eval/truth/r13-* eval/truth/r14-* 2>/dev/null && { echo "heldout truth still provisional, audit first"; exit 2; }
L=proof/heldout.log; : > $L
python3 -m eval.runner --arm baseline --cases eval/cases/heldout --label baseline-heldout >> $L 2>&1
grep -q "USAGE LIMIT" $L && { echo HALTED_ON_LIMIT >> $L; exit 75; }
python3 -m eval.runner --arm advanced --cases eval/cases/heldout --label advanced-v3-heldout >> $L 2>&1
grep -q "USAGE LIMIT" $L && { echo HALTED_ON_LIMIT >> $L; exit 75; }
find arms-runs -type d -name artifacts -prune -exec rm -rf {} + 2>/dev/null
python3 -m eval.report > RESULTS.md && python3 eval/render_readme.py && echo HELDOUT_DONE >> $L
