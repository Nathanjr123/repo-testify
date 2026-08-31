#!/usr/bin/env bash
# One command to run the tool. Three ways:
#   ./run.sh https://github.com/owner/repo      extract claims, execute them, open the report
#   ./run.sh path/to/case.json                  run a case you already wrote
#   ./run.sh --demo                             render the report from bundled results (no run, no cost)
# Executing a repository's code on CI is a consequential action; this script is your approval for it.
set -euo pipefail
cd "$(dirname "$0")"
export PROBE_DISPATCH=approve
open_report() { python3 eval/render_html.py > /dev/null && echo && echo "Report: file://$(pwd)/report.html" && { command -v xdg-open >/dev/null && xdg-open report.html 2>/dev/null || true; }; }

if [ "${1:-}" = "--demo" ] || [ -z "${1:-}" ]; then
  echo "Rendering the report from the results already in proof/build_proof.json (no run)."
  open_report; exit 0
fi

if [[ "$1" == http*github.com* ]]; then
  echo "1/3  Extracting checkable claims from $1 ..."
  CASE=$(mktemp --suffix=.json); python3 tools/extract_claims.py "$1" > "$CASE"
  echo "     $(python3 -c "import json;print(len(json.load(open('$CASE'))['claims']))") claims extracted."
else
  CASE="$1"; echo "Using case file $CASE"
fi
echo "2/3  Running the pipeline (probes execute on GitHub Actions; watch: gh run watch, or the Actions tab) ..."
OUT=$(mktemp --suffix=.json); python3 arms/advanced/advanced.py "$CASE" | tee "$OUT"
echo "3/3  Result:"; python3 -c "import json;r=json.load(open('$OUT'));print('  score',r['overall_score'],'/100 |',sum(c['verdict']=='verified' for c in r['claims']),'verified,',sum(c['verdict']=='refuted' for c in r['claims']),'refuted,',len(r['escalations']),'escalated')"
python3 eval/render_html.py --report "$OUT" > /dev/null && echo && echo "Report: file://$(pwd)/report.html"
