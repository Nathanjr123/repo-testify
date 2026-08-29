# Agent trajectories
One coding agent was used: **Claude Code (claude-fable-5)**, driven by Nathan Obiekwe. The pipeline's own model calls (`claude -p`) are recorded per run in `proof/build_proof.json` (`per_case.*.output`, with per-claim votes) and are not agent trajectories in the PDF's sense; the trajectories below are the authoring sessions.

Format: `Step NN — Model Thinking / Tool Call: <tool> / Tool Result`, exported by `tools/export_traces.py` from the session log. Failures and dead ends are kept; nothing is cut.

## Pipeline agent — one trajectory per repository
`traces/pipeline/<case>.md` (rendered from persisted data by `tools/render_pipeline_traces.py`): the instructions (`arms/PROMPTS.md`), the probes the PLAN stage wrote, the GitHub Actions run that executed them, the transcript index, the three adjudication votes per claim, and the final verdict with its cited artifact. Retries appear as `-r1` probe files; escalations are listed in the report.

## Authoring agent — sessions
| file | purpose | steps | outcome |
|---|---|---|---|
| `ddf39f00-….md` | main build session: harness → cases → arms → measurements → README (curated, redacted export published with the final submission) | — | shipped everything in this repo |

## Human checkpoints worth reading (search the file for the strings)
1. **`exit=127`** — the first sandbox run showed green on CI; the human-directed rule "inspect the artifact, not the badge" caught that the probe never ran (no `git` in the slim image). The agent's initial reading trusted the job status.
2. **`arm_error`** — three baseline runs scored exactly 0.000 in 8 seconds; recognised as an infrastructure fault (CLI not on PATH), discarded, never a datum.
3. **`'17 minutes'`** — the arm refuted a README doctest the draft truth had marked verified; the human decision was to correct truth from recorded execution and log it, not to override the arm.
4. **`0.842`** — a rescore silently dropped a crashed case and inflated the composite; caught and reverted before any number was published (`crash-as-zero`).
5. **`post-hoc`** — the scorer had a design defect visible only after the first real data; the decision to change it was disclosed with both arms' before/after rather than quietly applied.

Retries/feedback loops are visible inline as consecutive Tool Call → Tool Result pairs.
