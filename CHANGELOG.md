# Improvement Changelog
| Stage | What we tried and why | Evidence (proof id) | Decision / learning |
|---|---|---|---|
| Baseline | | | Established the starting point |
| Iteration 1 | Smoke-tested the execution rig end to end before building on it | run 33191764896: probe exit 127 — `git` absent from python:3.11-slim; job green, artifact inspection caught it | Fixed: host-side clone + read-only mount into container. Learning: job status is not evidence; the artifact is |
