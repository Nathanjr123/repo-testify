#!/usr/bin/env bash
# One tiny call. exit 0 = usage available, 75 = still limited. Poller uses this every 15 min when blocked.
CL=$(ls -t ~/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude 2>/dev/null | head -1)
OUT=$(timeout 90 "$CL" -p "Reply with exactly: OK" --model claude-haiku-4-5-20251001 2>&1)
case "$OUT" in *OK*) echo "usage available"; exit 0;; *) echo "LIMITED: ${OUT:0:120}"; exit 75;; esac
