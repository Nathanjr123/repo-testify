# Submission notes

**Status:** ready. Commit `0605ad3`, tree `ae28bd7e0e04`. Reproduction verified from a clean clone; CI green; archive attached to the release below. Only the video link is outstanding.

Revisions before Monday 18:00 UTC appear as later commits; the Releases page names the exact submitted commit.

**Project:** repo-testify: make the repository testify
**Repository (public):** https://github.com/Nathanjr123/repo-testify
**Video:** _paste the recording link here before you submit (script in VIDEO-SCRIPT.md, under 5 minutes)_

**One paragraph.** An engineer doing due diligence on a repository they did not write has to check a README's promises by hand, and two reviewers reading the same signals reach different conclusions. repo-testify takes the README's own claims (install command, quickstart snippet, supported Python versions, features, benchmarks), executes each one in a clean container on GitHub Actions, and returns a verdict per claim with the recorded evidence attached; anything the sandbox cannot settle is escalated to a human instead of guessed. Against a fair baseline (one model call over the README and file tree, same claims, same schema) per-claim accuracy went from 0.15 to 0.87 across 13 public repositories (143 claims, 95% intervals 0.10 to 0.22 versus 0.81 to 0.92), with every number regenerated from a proof file by `./repro.sh` and checked by CI inside the shipped Docker image on every push. A held-out split of 7 repositories was run once and is reported on both its untouched draft truth and its evidence-corrected truth. Along the way the tool refuted stale examples in "honest" repositories (humanize, tabulate, docopt) and one of our own README claims, which we kept in the write-up.

**Where the required pieces are**
- Complete code and Improvement Changelog: the repository; `CHANGELOG.md` (one row per experiment with proof ids; removed experiments included)
- Reproduction guide: `README.md`, section "Reproduction guide"; `repro.sh`; `Dockerfile`
- Solution video: link above (script in `VIDEO-SCRIPT.md`)
- Agent trajectories: `traces/README.md` (guide), `traces/authoring-session-1.md` (the coding agent's session from kickoff, redacted only for private paths and identifiers), `traces/pipeline/*.md` (one reconstructed trajectory per repository: instructions, probes, CI run, votes, verdict)
- Instructions that shape each agent: `arms/PROMPTS.md` (current) and `arms/PROMPTS-v2.md` (the prompts behind the published public-split numbers)
- Ground truth and cases: `eval/cases/`, `eval/truth/` (audited by the author; `provisional` flags are honest about what has and has not been re-audited)
- Tools disclosed: Claude Code (claude-fable-5) for authoring; the pipeline's own model calls use the same model through the CLI

**What existed before the competition:** a problem-agnostic evaluation skeleton (Makefile targets, the `eval/` layout, a trajectory exporter). Everything else was built during the event.

**Deadline on the official page:** Monday 31 August 2026, 18:00 UTC.
