#!/usr/bin/env bash
# Noise floor: 3 identical baseline runs over public cases (law: no delta is real below this spread)
set -uo pipefail
cd "$(dirname "$0")"
for i in 1 2 3; do
  python3 -m eval.runner --arm baseline --cases eval/cases/public --label baseline-n$i \
    >> proof/baseline_noise.log 2>&1
  echo "run $i done: $(date -u +%H:%M)" >> proof/baseline_noise.log
done
python3 -m eval.report > RESULTS.md
echo ALL_DONE >> proof/baseline_noise.log
