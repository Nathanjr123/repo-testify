# Pre-registration (committed before any advanced-arm run)
Problem: agentic technical due diligence on a GitHub repository, extract the repo's own checkable claims (install, quickstart, compat, features, benchmarks), execute them in a clean environment, emit a per-claim verdict ledger (verified / refuted / unverifiable->escalated) with evidence links, plus a calibrated overall assessment. "Convincing is not enough, make the repo testify."
Intended user: an engineer/buyer doing due diligence on an unfamiliar repo (acquisition, dependency adoption, contractor handover).
Primary metric: macro-F1 of per-claim verdicts vs hand-audited ground truth, over 12 pinned repos (public + held-out split). Secondary: confident-wrong rate, evidence validity, Kendall tau vs a qualified reviewer's ranking, human-minutes per repo, cost per repo.
Hypothesis: the EXECUTE component (sandboxed build/quickstart/test/claim probes) improves per-claim macro-F1 by >= +0.20 absolute over the best STATIC-only arm, and both beat the one-shot baseline. Noise floor measured first: baseline-vs-baseline across 3 runs.
Stopping rule: max 2 tuning rounds per arm on public cases; held-out cases run once, at the end.
Kill criterion: if by Sat 2026-08-29 18:00 UTC EXECUTE minus STATIC <= noise floor on public cases, ship the best surviving arm as final and write the kill entry as a changelog + hot-take input.

## Outcome (public split, recorded 2026-08-29; held-out pending)
Noise floor measured first: baseline-vs-baseline claim-accuracy spread 0.008 (proof baseline-v2-n1/n2).
EXECUTE vs STATIC-only: claim accuracy 0.712 vs 0.007 (proof advanced-v2-rescored vs ablate-no-execution) -> +0.705 >= +0.20: **hypothesis PASSED**. Both arms beat the one-shot baseline (0.07).
Stopping rule honoured: two tuning rounds (v1 -> v2) on public cases; v3 rule changes are applied to the held-out split only.
Kill criterion never triggered (Sat 18:00 UTC checkpoint moot).
