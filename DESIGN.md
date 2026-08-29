# Harness design — every component earns its place
The advanced arm is a code-orchestrated pipeline, not a free-running agent. Due diligence has a known shape (extract -> plan -> execute -> adjudicate), and the evidence says fixed structure beats free loops on known-shape tasks: Agentless (arXiv:2407.01489) outperformed agent frameworks on SWE-bench with a three-stage pipeline; constrained action spaces beat free loops by wide margins in SWE-Gym (arXiv:2412.21139); light task adaptation beat a generalist agent on CORE-Bench (arXiv:2409.11363); staged flows took CodeContests pass@5 from 19% to 44% (AlphaCodium, arXiv:2401.08500).

## Stages
1. **Map** (no LLM): file tree + manifests (setup.py/pyproject) + README -> repo_map.json.
2. **Claims** — on the scored path the claim list is *provided* by the case file (DECISIONS #2: deterministic scoring); one claim = one executable probe (granularity matched to the verifier, arXiv:2503.15354). A README extractor exists for real-world use but is not evaluated here (README, "What we did not attempt").
3. **Plan** (per claim): claim + map + notes.json -> a probe spec drawn from a FIXED vocabulary: run_install, import_check, run_snippet, run_tests, check_cli. Few purpose-built tools with compact structured output — the interface, not the model, drove a 3.3x gain in SWE-agent (arXiv:2405.15793).
4. **Execute** (no LLM decisions in the loop): Docker on GitHub Actions, pinned image digest; phase A network-on install, phase B network-off probes; per-probe artifact dir (cmd, stdout head+tail, exit code). At most **2 repair rounds** per failed probe — self-repair plateaus after 2 iterations (arXiv:2604.10508) — and each retry must change the command. Probes run in parallel across claims; the orchestrator is a script, because multi-agent handoffs add failure modes without gains on tasks like this (MAST, arXiv:2503.13657).
5. **Adjudicate** (per claim: k=3 votes, low temperature, few-shot verdict examples): claim + truncated probe transcript -> verdict + evidence pointer. Execution feedback is the load-bearing component: models cannot self-correct without external signal (Huang et al., arXiv:2310.01798) — which is also why the one-shot baseline is structurally limited. Code cross-checks every cited exit code/string against the recorded logs; a verdict may only change when NEW execution evidence arrives.
6. **Report**: verdict ledger + escalations + memo. Stages 5-6 replay deterministically from cached artifacts.

Context is assembled per stage by code (smallest high-signal set; notes.json scratchpad carried forward) rather than dumping the repo into one window — long-context degradation is positional (arXiv:2307.03172) and cumulative ("context rot", Anthropic context-engineering guidance).

## Ablation map (make ablate)
--no-execution (= the baseline; isolates external-feedback value) · --retries {0,1,2} · --k {1,3} · --full-context (one-window adjudication) · --no-notes · --freeloop (same tools, single free-running agent; time permitting).

## What we deliberately did NOT build
Conversing multi-agent roles (MAST: minimal gains, new failure modes); a free-loop autonomous core (Agentless/Moatless/CORE-Bench); ungrounded self-critique passes (Huang et al.); embedding/PageRank retrieval (tree + manifests sufficed for SOTA in Agentless).
