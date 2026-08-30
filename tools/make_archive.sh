#!/usr/bin/env bash
# Build the submission archive from the current HEAD (tracked files only, so nothing private can leak),
# record its hash, and attach it to a GitHub release tagged with the tree hash. Run at finalisation.
set -euo pipefail; cd "$(dirname "$0")/.."
SHA=$(git rev-parse --short HEAD); TREE=$(git rev-parse HEAD^{tree} | cut -c1-12)
OUT="/tmp/repo-testify-${SHA}.zip"
git archive --format=zip --prefix="repo-testify-${SHA}/" -o "$OUT" HEAD
echo "archive: $OUT ($(du -k "$OUT" | cut -f1) KB) sha256 $(sha256sum "$OUT" | cut -c1-16) tree $TREE"
gh release create "submission-${SHA}" "$OUT" --repo Nathanjr123/repo-testify --title "Submission archive ${SHA}" \
  --notes "Zip of the repository at commit ${SHA} (tree ${TREE}), tracked files only. sha256 $(sha256sum "$OUT" | cut -d' ' -f1)" >/dev/null && echo "release: https://github.com/Nathanjr123/repo-testify/releases/tag/submission-${SHA}"
