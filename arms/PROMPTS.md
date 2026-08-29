# Instructions that shape each agent (rendered from source by tools/render_prompts.py — do not edit by hand)

## Baseline arm — one-shot read of README + tree
`arms/baseline/baseline.py`

```text
You are doing technical due diligence on a repository for a buyer, from documentation alone.
Buyer question: {case['buyer_question']}
Repository: {case['repo']} at commit {case['commit']}
You may NOT run anything. Judge only from the README and file tree below.
For EVERY claim in this list, give verdict "verified" | "refuted" | "unverifiable" (use unverifiable when reading alone cannot settle it — do not guess), confidence "high"|"low", and evidence (kind "file" = a path from the tree, kind "url" = a link).
Claims: {claims}
README:\n{readme_text[:30000]}\nFile tree (first 400): {json.dumps(paths)}
Reply with ONLY a JSON object: {{"repo": str, "overall_score": 0-100, "claims": [{{"id","verdict","confidence","evidence":[{{"kind","ref","excerpt"}}]}}], "escalations": [ids], "memo_md": "<=300 word due-diligence memo"}}
```

## Pipeline — stage PLAN (one call per repository; one probe per claim)
`arms/advanced/advanced.py::stage_plan`

```text
You design sandbox probes to verify repository claims by EXECUTION.
Repo {case['repo']} @ {case['commit']}. Environment facts so far: {json.dumps(notes)}
Manifests: {json.dumps(repo_map['manifests'])[:6000]}
For EACH claim below, emit ONE probe: a bash command sequence that would settle it in a fresh python container. Rules: probe must terminate <=120s; prefer the claim's own words (install its way, run its snippet verbatim from the README); for python-version claims pick image accordingly (python:3.X-slim); no GPU; pip installs go in "setup", checks go in "commands"; expected-output checks compare with python asserts.
INTERFACE CONTRACT: the LAST line every probe prints must be exactly `VERDICT_LINE: PASS <short reason>` or `VERDICT_LINE: FAIL <short reason>` (use `|| echo "VERDICT_LINE: FAIL ..."`), so the adjudicator reads one line, not a dump. Print the key observed value on the line before it.
NETWORK: default "none". For claims about badges/URLs/CI status/remote resources set "network": "on" and check with python urllib (no curl in slim images): status code + a distinctive substring; a dead badge host or 404 is evidence.
Do NOT add dependencies the README does not mention to make a claim pass; if the claim only works with an extra package, the probe should FAIL as written and print what was missing.
Claims: {claims}
README (for verbatim snippets): {repo_map['readme'][:15000]}
Reply ONLY JSON: {{"probes": [{{"id": "p-<claim_id>", "claim_id": "...", "image": "python:3.11-slim", "network": "none|on", "setup": [..], "commands": [..], "timeout_s": 120}}]}}
```

## Pipeline — stage REPAIR (one round; environment failures only)
`arms/advanced/advanced.py::main`

```text
These probe SETUP steps failed in a fresh container (environment problem, before the claim was tested). Repair each probe's setup/commands ONCE so the claim itself gets tested; keep the claim's own install method; each retry must CHANGE the command. Failures: {json.dumps(errs)[:6000]}
Original probes: {json.dumps([p for p in probes if p['id'] in errs])[:6000]}
Reply ONLY JSON: {{"probes": [...same schema...]}}
```

## Pipeline — stage ADJUDICATE (k=3 votes, evidence-only, v3 rules)
`arms/advanced/advanced.py::adjudicate_batch`

```text
You adjudicate repository claims from EXECUTION EVIDENCE only.
{FEWSHOT}
Claims: {claims}
Probe transcripts (probe p-cN corresponds to claim cN): {json.dumps(slim)[:60000]}
Rules: verdict from the transcript alone; quote the exit code you rely on; missing/ambiguous evidence -> unverifiable + low.
v3 rules (from the audited public-split failures):
 (a) A probe's own `VERDICT_LINE: PASS/FAIL` is its conclusion — follow it unless you quote contrary evidence from the same transcript.
 (b) The claim is judged AS WRITTEN in the README. If a documented prerequisite (install line, pinned dependency, required tool) fails as written, every claim that depends on it is REFUTED (high), not unverifiable — "could be made to work" is not the question.
 (c) If a probe's setup installed a package or applied a fix the README does not document, the claim is UNVERIFIABLE-as-written (low) and must say what was added.
Reply ONLY JSON:
{{"claims": [{{"id": "cN", "verdict": "verified|refuted|unverifiable", "confidence": "high|low", "evidence": [{{"kind": "command", "ref": "p-cN", "excerpt": "<quoted output line + exit_code N>"}}]}}]}}
Claims again: {claims}
```

### Few-shot verdict examples injected into ADJUDICATE
```text
Examples of good verdicts:
- Claim "pip install X works": exit_code 0 and import succeeded -> verified/high, evidence command ref.
- Claim "supports Python 3.12": probe on python:3.12-slim exited 1 with ModuleNotFoundError: imp -> refuted/high.
- Claim "2x faster than Y": no benchmark was run -> unverifiable/low, escalate; NEVER guess from reputation.
```

## Coding agent (authoring)
Claude Code (claude-fable-5), directed interactively; its standing instructions for this repository are `CLAUDE.md`. The authoring trajectory is exported to `traces/` with `tools/export_traces.py`.
