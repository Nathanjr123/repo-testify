#!/usr/bin/env bash
set -uo pipefail; cd "$(dirname "$0")"; L=proof/ext.log; : > $L
C=/tmp/claude-1000/-home-nate-lbx-rl-tasks-template/ddf39f00-2ebe-4b74-9147-5303458caa78/scratchpad/ext-cases
python3 -m eval.runner --arm baseline --cases $C --label baseline-ext >> $L 2>&1; grep -q "USAGE LIMIT" $L && { echo HALTED_ON_LIMIT >> $L; exit 75; }
python3 -m eval.runner --arm advanced --cases $C --label advanced-v3-ext >> $L 2>&1; grep -q "USAGE LIMIT" $L && { echo HALTED_ON_LIMIT >> $L; exit 75; }
find arms-runs -type d -name artifacts -prune -exec rm -rf {} + 2>/dev/null; echo EXT_DONE >> $L
