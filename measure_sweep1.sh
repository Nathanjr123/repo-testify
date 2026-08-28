#!/usr/bin/env bash
# Budgeted sweep 1 (Max 5x economy): baseline x2 (noise floor, outputs persisted) then advanced x1 on public.
# Runner halts on usage limit (exit 75) and flags the partial entry; rerun resumes cleanly.
set -uo pipefail
cd "$(dirname "$0")"
L=proof/sweep1.log; : > $L
for i in 1 2; do
  python3 -m eval.runner --arm baseline --cases eval/cases/public --label baseline-v2-n$i >> $L 2>&1
  grep -q "USAGE LIMIT" $L && { echo "HALTED_ON_LIMIT after baseline n$i" >> $L; exit 75; }
done
python3 -m eval.runner --arm advanced --cases eval/cases/public --label advanced-v1 >> $L 2>&1
grep -q "USAGE LIMIT" $L && { echo "HALTED_ON_LIMIT during advanced" >> $L; exit 75; }
python3 -m eval.report > RESULTS.md
echo SWEEP1_DONE >> $L
