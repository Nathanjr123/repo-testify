# Decisions
| # | Assumption / question | Alternatives considered | Tradeoff chosen & why | Truth or taste? |
|---|---|---|---|---|
| 1 | Where does execution truth run? | Local docker (no disk) / box venvs (Windows-skewed verdicts) / GH Actions | GH Actions ubuntu runners: Linux+docker, free, and the workflow log IS judge-facing reproduction evidence | Truth |
| 2 | Case claim lists: agent-discovered or case-provided? | Free discovery (realistic, unscoreable) vs provided claim list (deterministic scoring; agent may add extras uncredited) | Provided in case file; we audit exactly those. Deterministic scorer > realism here | Truth |
| 3 | Overall repo score: pure model output or rubric-aggregated? | Holistic LLM score vs weighted rubric rows | Rubric rows, weights published, mirrors how a real reviewer justifies a score | Taste (declared) |
| 4 | Windows box for repo execution? | venv-per-repo on box | Rejected: Windows-specific failures would put false "refuted" verdicts in ground truth | Truth |
| 5 | Verdict classes: 3 or 5? | {verified, refuted, unverifiable} vs adding partially-verified, unverifiable-by-sandbox | 3 classes + separate escalations list: hand-audit stays unambiguous, macro-F1 clean; "partially" folds into refuted-with-evidence-note. Granularity matched to what the verifier can settle (arXiv 2503.15354) | Truth |
| 6 | Abstention framing | Formal ToE guarantee vs "ToE-style" | n=12 makes the binomial bound vacuous, we implement the mechanism (ensemble confidence -> threshold -> escalate) and disclaim the guarantee explicitly | Truth |
| 7 | Arms could read eval/truth/ from the repo FS | Trust arms / isolate | Arms receive only the case path; no arm code references the truth files (verifiable: `grep -rn "eval/truth\|truth/" arms/` returns nothing). Not sandbox-enforced, a deliberate scope cut, disclosed | Truth |
| 8 | Ground-truth auditor = the builder (bias) | Only-me audit vs evidence-first audit | Every verdict must cite third-party evidence (issue link, CI run, executed command output), preference for breakage documented by OTHERS; Nate re-audits all 14 before heldout runs; provisional-until-audited flag in truth files | Truth |
