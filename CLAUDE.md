# micro1 Agentic Workflows Hackathon — working rules (read every session)
Deadline: Sun 2026-08-30 23:59 UTC. Rubric /100: Engineering 30, E2E Quality 20 ("would sign their name to it", must NOT read AI-generated), Problem & User Value 15, Measured Improvement 15, Reproducibility 15, Hot Take 5.

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

## Voice
micro1 register: judgment, failure taxonomy, verifiers, golden reference, verifiable intermediate steps, tradeoffs, thresholds, truth-vs-taste. Never: annotation, vibe coding, "AI did it", uncalibrated LLM-judge, credentials. Understated; the work is the résumé. Every philosophical claim points at a table.
