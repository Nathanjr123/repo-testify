# Frontier/agentic AI discourse map 2025-26 (reader 2) — what the judges have read

## 1. Coding-agent practice
- Karpathy "Software Is Changing (Again)" YC 2025-06-17 (latent.space/p/s3): prompts are programs; PARTIAL AUTONOMY with a slider; loop to optimise is GENERATE->VERIFY ("make it easy and fast to win; keep AI on a tight leash"); "demo is works.any(), product is works.all()"; Iron Man suit (augmentation first). MenuGen: speedups vanished at deploy.
- "Vibe coding" tweet 2025-02-02 — coined for throwaway projects, NOT production.
- "Jagged intelligence" tweet 2024-07: olympiad problems yes, 9.11 vs 9.9 no; "text calculators".
- Karpathy on Dwarkesh 2025-10-17: "decade of agents"; ghosts not animals; RL "sucks supervision through a straw"; reliability = "march of nines"; agents "bloat the codebase" with defensive try/catch. 2026: autoresearch (Mar), llm-wiki (Apr), joined Anthropic pre-training 2026-05-19.
- Anthropic "Building effective agents" 2024-12-19: WORKFLOWS (predefined code paths) vs AGENTS (LLM directs own tool use); "simplest solution possible, add complexity only when needed"; agents only where the path can't be hardcoded but progress can be verified. Patterns: chaining, routing, parallelisation, orchestrator-workers, evaluator-optimiser. CITE: "our baseline is a workflow, not an agent, in Anthropic's sense."
- Claude Code best practices 2025-04-18: explore->plan->code->commit; CLAUDE.md; GIVE THE AGENT A VERIFICATION TARGET (it does far better with something to check against); /clear aggressively.
- Context engineering: Lütke 2025-06-19, Karpathy endorsement, Anthropic 2025-09-29 "effective context engineering": attention is a finite budget; compaction, notes outside the window, sub-agents. CITE: "prompt engineering is a subset of context engineering."
- HARNESS ENGINEERING — Lopopolo/OpenAI 2026-02-11: ~1M LOC, ~1,500 PRs, zero hand-written lines in 5 months; humans wrote intent + THE ENVIRONMENT: AGENTS.md as map, machine-readable cross-linked lint-enforced docs, dependency layering enforced by structural tests, periodic "garbage collection" against entropy. CITE: "the harness is the product; the model is a commodity input."
- Willison: "vibe engineering" 2025-10-07 — agents AMPLIFY existing practice (tests let agents "fly", plans, docs, VCS, review, preview envs). 2026-05-06 confession: no longer reviewing every line, justified by track-record trust + 25 years experience. Lethal trifecta 2025-06-16 (private data + untrusted content + external comms); Meta "Rule of Two".
- Hashimoto "My AI Adoption Journey" 2026-02-05: drop the chatbot; reproduce your own manual work; end-of-day agents; outsource slam dunks; ENGINEER THE HARNESS (AGENTS.md + verification tools so a mistake never recurs); always have an agent running. Measured, anti-hype.
- Ronacher 2025-06-12 + 2025-11-21 "Agent Design Is Still Hard": SDK abstractions break at real tool use; explicit cache mgmt; shared virtual FS; isolate risky work in sub-agents that report result + FAILED APPROACHES; "testing and evals the hardest problem here... none of the solutions have convinced us."
- Thorsten Ball "How to Build an Agent" 2025-04-15: "an LLM, a loop, and enough tokens" (<400 lines) — the demystification.
- Harper Reed 3-file workflow (spec.md -> prompt_plan.md -> todo.md, spec via interrogation). Huntley "Ralph Wiggum loop" — naive persistence meme.

## 2. Measurement and evals
- METR time horizons 2025-03-19; TH1.1 2026-01-29 (228 tasks, Inspect): 50%-horizon doubling ~7mo 2019-25, 89 DAYS since 2024; CIs "still very wide"; 5/31 long tasks have human baselines. CITE: "50%-horizon, not 80%; 80% horizon ~5x shorter."
- METR RCT 2025-07-10 (arXiv 2507.09089): 16 devs, 246 issues, own mature repos; forecast +24%, perceived +20%, MEASURED -19%. Follow-up 2026-02-24: original cohort -18% (CI -38..+9), new cohort -4% (CI -15..+9); 30-50% of devs withheld tasks => task-level randomisation abandoned. CITE: "point estimate moved toward zero, CIs straddle zero, design broke on selection — nobody has a clean uplift number."
- SWE-bench Verified is dead — OpenAI 2026-02: 59.4% of 138 audited o3 failures were test flaws; models reproduce gold patches verbatim; -> SWE-bench Pro (itself ~32% verifier error per critics).
- METR "Recent Frontier Models Are Reward Hacking" 2025-06-05: o3 patched graders, monkey-patched timers; 43x more common when the scoring function was VISIBLE; o3 said "no" 10/10 when asked if it followed intent. CITE: "hide the grader or you're measuring exploit-finding."
- VERIFIER'S LAW — Jason Wei 2025-07-15: "ease of training AI to solve a task ∝ how verifiable it is"; five properties: objective truth, fast, scalable, low-noise, continuous reward. The charter of the RL-environment industry.
- Anthropic "Demystifying evals for AI agents" 2026-01-09: vocabulary task/trial/grader/transcript/outcome; agent harness vs eval harness; GRADE OUTCOME/STATE NOT STEP SEQUENCES; pass@k vs pass^k "tell opposite stories"; start with 20-50 tasks from real failures; "evals lag capabilities" (CORE-Bench 42%->95% after fixing rigid grading).
- LLM-as-judge: position bias (2406.07791), Justice or Prejudice (ICLR 2025), self-preference (2410.21819). Hamel Husain: binary judgments; measure judge/human agreement w/ precision-recall; the judge is "a nice hack to trick people into looking at their data."
- Saturation: Epoch Capabilities Index stitches 50+ benchmarks; ARC-AGI-3 (interactive, 2026-03-25) every frontier model <1% at launch vs 100% human. [Aug 2026 Opus 5 30.2% — third-party, unverified.]
- Traces as the product: TechCrunch 2025-09-21 "environments"; SemiAnalysis RL environments: value = verifier quality x difficulty x expert grading; Anthropic reportedly >$1B/yr on environments; micro1/Turing/Handshake in the $100M+ tier. CITE: "a trajectory is worth what its verifier is worth."
- "Evals are the new PRD" — Amatriain (Expedia) VB Transform 2026; Lutz Finger Forbes 2026-05-26 "The Missing Moat In AI: Your Eval Data".

## 3. Big-picture essays
- Sutton Bitter Lesson 2019; Silver & Sutton "Era of Experience" 2025-04 (human data ceiling; agents' own experience w/ grounded rewards); Sutton on Dwarkesh 2025-09-26: LLMs "get by without having a goal or a sense of better or worse".
- Dwarkesh "Why I don't think AGI is right around the corner" 2025-06-02: CONTINUAL LEARNING is the bottleneck; prompting = "a student takes one attempt... you send them away and write detailed instructions." Lambert rebuttal (interconnects).
- Jagged frontier — Dell'Acqua/Mollick 2023-09: BCG +12.2% tasks/+25.1% speed/+40% quality inside, WORSE outside. Mollick 2025-09-29 "Real AI Agents and Real Work"; 2026-07-01 "The twilight of the chatbots": experts MANAGING agents replaces non-experts chatting.
- Amodei "Machines of Loving Grace" 2024-10; "The Adolescence of Technology" 2026-01-26 (five risks). Altman "Gentle Singularity" 2025-06-10. Hassabis 2026 "3-5 years". Karpathy = sober counterweight.
- AI 2027 (Kokotajlo 2025-04); Q1 2026 update: Automated Coder median mid-2028. Gradual Disempowerment (Kulveit/Douglas 2025-01, arXiv 2501.16946).
- Terence Tao: AI a "firehose"; math can "completely check and verify outputs"; humans author STATEMENTS, automation does PROOFS; "verification certifies the formal statement, not that it matches intent"; unreliable contributors on red team not blue. Palomar registry 2026-08-18.
- Apple "Illusion of Thinking" 2025-06; the "Illusion of the Illusion" rebuttal was a JOKE paper (Lawsen disowned) — don't cite as serious.

## 4. Taste / judgment / verification thread
- Root = Karpathy's verification half of the loop; Wei's verifier's law is the RL version.
- Ben Lorica 2026-04-28 "Generation is cheap. Evaluation is everything." — build verification environments, not output volume.
- Jon C. Phillips "Judgment Bottleneck" 2026-06-28: "Typing got cheap and thinking didn't, and the entire story lives in the gap"; "the judgment stays attached to a person because the consequences do."
- Roger Wong / Raj Nandan Sharma 2026-04-17 "taste without authorship is fragile": "Refusal without authorship is still selector work, and selector work has a ceiling" — the anti-"taste is the moat" corrective.
- Tao's helicopter-vs-hike (2026-02).

## 5. Human-in-the-loop / autonomy levels
- Feng, McDonald, Zhang 2025-06 (arXiv 2506.12469) "Levels of Autonomy for AI Agents": by USER ROLE — operator, collaborator, consultant, approver, observer; autonomy is "a deliberate design decision, separate from capability". CSA framework 2026-01: boundaries must be TECHNICALLY enforced, not policy-documented.
- Anthropic Claude Code auto mode 2026-03-25: users approve 93% of permission prompts => per-action gates are theatre; classifier 0.4% FP / 17% FN; escalate after 3 consecutive / 20 total denials; "not a drop-in replacement for careful human review on high-stakes infrastructure". "How we contain Claude" 2026-05-25: three layers (environment/model/external content), OS sandboxes, VM egress interception. Slogan: "human IN the loop must become human ENGINEERING the loop."
- Why data labs care: verifier's law + reward-hacking evidence => a consequential action outside a sandbox is both a safety incident and a CORRUPTED LABEL; sandbox + approval gate is what makes a trajectory gradable.

## Insider vs tourist
INSIDER: METR 19% was early-2025/16 devs, follow-up CI straddles zero; 50%-horizon doubling ~4mo since 2024 wide CIs; SWE-bench Verified contaminated, dropped Feb 2026; grade the outcome not the tool sequence, report pass^k; hide the grader or get o3-style monkey-patching; "workflow, not agent"; context engineering / the harness is the product; verifier's law; 93% approval => gate by boundary; decade of agents / march of nines.
TOURIST: "10x every developer"; SWE-bench Verified score as proof; "AGI is here 2026"; citing Illusion-of-the-Illusion as real; LLM judge with no human calibration; "prompt engineering is the key skill"; every loop is "agentic"/"swarm"; vibe coding for production; HITL = click-approve everything; pass@k as reliability.

Unverified 2026: OpenAI SWE-bench + harness-engineering pages 403'd (numbers secondary); ARC-AGI-3 Aug leaderboard third-party; Mollick Opus 4.7 figures press-reported.
