# <project name>
<!-- E2E Quality bar: a person would sign their name to this. No AI-draft smell. -->
## Intended user
TODO — who has this problem (a real, specific person/team).
## The bottleneck
TODO — what makes it worth solving; what the manual process costs today.
## Why solving it is valuable
TODO.
## The solution (and the baseline)
Baseline = TODO (one of: direct prompt / general agent with basic tools / simple script / the manual process). Final = TODO. Same cases, same resources; differences declared here.
## Measured improvement
<!-- generated: make report — do not hand-edit numbers -->
See RESULTS.md (primary outcome, human time per task, cost per task; public + held-out; per-case table incl. the hard case and what it revealed).
## Improvement Changelog
See CHANGELOG.md (stage | what we tried and why | evidence | decision/learning — removed experiments included).
## Main failure mode
TODO — the taxonomy entry with a repro.
## Hot take
TODO — falsifiable, tied to a table above.
## Reproduction guide
From a clean environment: `docker build -t hack . && docker run hack make baseline advanced eval report`. Data required: eval/cases/. Expected output: RESULTS.md. Versions/runtime/cost: TODO. Tree hash of the final proof run: TODO.
## Agents, tools, and provenance
Tools used: Claude Code (model: claude-fable-5) — trajectories in traces/, one per session, failures included, human checkpoints marked. Pre-existing before kickoff: this problem-agnostic harness (Makefile, eval/ skeleton, trace exporter). Added during the competition: everything else.
