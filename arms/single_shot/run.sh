#!/usr/bin/env bash
set -euo pipefail
python3 "$(dirname "$0")/single_shot.py" "$1"
