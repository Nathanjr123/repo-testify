# micro1 Agentic Workflows Hackathon — working rules (read every session)
Deadline: **Mon 2026-08-31 18:00 UTC** (verified on the official HackerEarth page 2026-08-28 late evening: "Aug 28 – Aug 31, 3:00 PM – 6:00 PM UTC"; was Sun 23:59). Internal target: submission-complete Sun night; Monday = buffer for polish and the final proof run, never new scope. Rubric /100: Engineering 30, E2E Quality 20 ("would sign their name to it", must NOT read AI-generated), Problem & User Value 15, Measured Improvement 15, Reproducibility 15, Hot Take 5.

## The 12 laws
1. Scorer + cases + replay BEFORE any solution code. Freeze, commit the hash.
2. Sanity cell first in every measurement (known case -> known score). If cell 0 fails, the table is junk.
3. Baseline = strongest obvious weak strategy, SAME cases + budget as advanced, tuned. Record its number before advanced exists.
4. Public/held-out split. Anything that wins on public and loses on held-out is REJECTED, in writing.
5. Measure each row's distribution before banding. No dead/saturated/crushed rows.
6. Gates multiply, rows add, nothing is both.
7. Ablate every advanced component (ADVANCED_DISABLE flag), re-tuned, in a table. The flat one = "experiment you removed".
8. Bit-identical results after a change = the change did not land. Stop and find out why.
9. Every number -> proof entry (cmd, cases, git hash, timestamp, wall, cost). README tables GENERATED from proof (make report). Never hand-type a number.
10. Full proof re-run is the FINAL act. No edits after. Tree hash in README.
11. Keep every trace incl. failures; mark human checkpoints; provenance header on agent-written files ("what existed before / what the agent wrote / what I changed").
12. HYPOTHESIS.md committed BEFORE the advanced run (predicted effect, stopping rule, kill criterion, Sat 18:00 UTC checkpoint).

## Ground rules from the PDF (binding)
Declare pre-existing vs added; licenses respected; consequential actions sandboxed + human approval BEFORE the action; qualified human reviewer in any people-affecting loop; public/synthetic/approved data only; no credentials in the repo; every claim tied to submitted evidence; judges must be able to run everything.

## Metrics contract (from the PDF)
>=10 eval cases incl. one hard case (explain what it revealed). Same cases for baseline and final. Report: primary outcome + human time per task + cost per task, baseline vs agent vs change. We run the eval ourselves and PROPOSE OUR RUBRIC to the judges (eval/scorer.py is that rubric — keep it legible).

## Writing standards
Evidence first; every claim in the README points at a table generated from proof/. Name ambiguities and the interpretation chosen. State what was not attempted. Failures and removed experiments are recorded, not hidden. Plain language; no hype.

## THE PROBLEM (locked Fri 2026-08-28): "Make the repo testify"
Agentic due diligence on GitHub repos. Pipeline components (each behind ADVANCED_DISABLE flag):
CLAIMS (extract atomic checkable claims from README/docs/badges) -> STATIC (7-axis structured code review) -> EXECUTE (clean-env build/install/quickstart/tests/claim probes) -> EVIDENCE (claim->verdict->artifact ledger; every verdict cites a real artifact) -> CALIBRATE+ABSTAIN (overall score; unverifiable claims escalate to a human, never guessed).
Baseline arm: one-shot LLM with README + file tree -> same report schema.
Case = {repo, pinned commit, buyer question, claim list}. 12 repos across buckets: solid-honest / solid-overclaiming / abandoned / green-badge-mirage / research-paper code. Hard case = all visible tests pass, a central README claim is false.
Ground truth: per-claim hand audit (objective) + Nate's reviewer ranking under a published rubric (subjective — truth-vs-taste DECLARED in DECISIONS.md).

## Compute plan
- Local machine: orchestration, arms (`claude -p`), scoring, docs. Repository execution truth runs on GitHub Actions ubuntu runners in Docker — Linux verdicts only (DECISIONS #1, #4).

## Epistemic standards (why the eval looks the way it does)
Metrics are stated operationalizations of a construct; optimization pressure finds any gap between them (hence held-out truth, read-only claim lists, evidence-existence gates). No improvement is claimed below the baseline-vs-baseline noise floor. Ambiguities are named and our interpretation justified, not silently assumed. Adverse results go in the main table. Truth-vs-taste is declared per decision in DECISIONS.md. What we did NOT attempt is listed in the README.
