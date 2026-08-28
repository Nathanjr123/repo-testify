# Decisions
| # | Assumption / question | Alternatives considered | Tradeoff chosen & why | Truth or taste? |
|---|---|---|---|---|
| 1 | Where does execution truth run? | Local docker (no disk) / box venvs (Windows-skewed verdicts) / GH Actions | GH Actions ubuntu runners: Linux+docker, free, and the workflow log IS judge-facing reproduction evidence | Truth |
| 2 | Case claim lists: agent-discovered or case-provided? | Free discovery (realistic, unscoreable) vs provided claim list (deterministic scoring; agent may add extras uncredited) | Provided in case file; we audit exactly those. Deterministic scorer > realism here | Truth |
| 3 | Overall repo score: pure model output or rubric-aggregated? | Holistic LLM score vs weighted rubric rows | Rubric rows, weights published — mirrors how a real reviewer justifies a score | Taste (declared) |
| 4 | Windows box for repo execution? | venv-per-repo on box | Rejected: Windows-specific failures would put false "refuted" verdicts in ground truth | Truth |
