# Prompts as they were for pipeline v2 (the published public-split numbers), taken from commit `b8f4af6` via `git show` (proof entry `advanced-v2-1787952546`)

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
Reply ONLY JSON: {{"probes": [{{"id": "p-<claim_id>", "claim_id": "...", "image": "python:3.11-slim", "network": "none|install-only", "setup": [..], "commands": [..], "timeout_s": 120}}]}}
```

```text
You adjudicate ONE repository claim from EXECUTION EVIDENCE only.
{FEWSHOT}
Claim ({claim['id']}): {claim['text']}
Probe transcript (cmd, exit codes, output head/tail): {json.dumps(probe_log)[:8000]}
Rules: verdict from evidence in the transcript alone; quote the exit code you rely on; if evidence is missing or ambiguous -> unverifiable + low confidence. Reply ONLY JSON:
{{"id": "{claim['id']}", "verdict": "verified|refuted|unverifiable", "confidence": "high|low",
 "evidence": [{{"kind": "command", "ref": "<exact cmd string or probe id>", "excerpt": "<quoted output line + exit code>"}}]}}
Claim: {claim['text']}
```

```text
You adjudicate repository claims from EXECUTION EVIDENCE only.
{FEWSHOT}
Claims: {claims}
Probe transcripts (probe p-cN corresponds to claim cN): {json.dumps(slim)[:60000]}
Rules: verdict from the transcript alone; quote the exit code you rely on; missing/ambiguous evidence -> unverifiable + low. Reply ONLY JSON:
{{"claims": [{{"id": "cN", "verdict": "verified|refuted|unverifiable", "confidence": "high|low", "evidence": [{{"kind": "command", "ref": "p-cN", "excerpt": "<quoted output line + exit_code N>"}}]}}]}}
Claims again: {claims}
```

```text
These probe SETUP steps failed in a fresh container (environment problem, before the claim was tested). Repair each probe's setup/commands ONCE so the claim itself gets tested; keep the claim's own install method; each retry must CHANGE the command. Failures: {json.dumps(errs)[:6000]}
Original probes: {json.dumps([p for p in probes if p['id'] in errs])[:6000]}
Reply ONLY JSON: {{"probes": [...same schema...]}}
```

Few-shot examples:
```text
Examples of good verdicts:
- Claim "pip install X works": exit_code 0 and import succeeded -> verified/high, evidence command ref.
- Claim "supports Python 3.12": probe on python:3.12-slim exited 1 with ModuleNotFoundError: imp -> refuted/high.
- Claim "2x faster than Y": no benchmark was run -> unverifiable/low, escalate; NEVER guess from reputation.
```
