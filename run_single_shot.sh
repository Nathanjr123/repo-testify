#!/usr/bin/env bash
set -uo pipefail; cd "$(dirname "$0")"; export PROBE_DISPATCH=approve
L=proof/single_shot.log; : > $L
for c in eval/cases/public/r01-humanize.json eval/cases/public/r05-records.json eval/cases/public/r07-newspaper3k.json; do
  id=$(basename $c .json)
  python3 arms/single_shot/single_shot.py $c > /tmp/ss-$id.json 2>> $L && python3 -m eval.runner --arm single_shot --cases <(echo) --label ss-$id 2>>$L || true
  echo "$id done" >> $L
done
echo SS_DONE >> $L
