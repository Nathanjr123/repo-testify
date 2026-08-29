"""Advanced arm, code-orchestrated pipeline (see DESIGN.md).
Stages: map -> plan -> execute (GH Actions, deterministic) -> adjudicate (k=3 vote) -> report.
Flags via ADVANCED_DISABLE (comma-separated): execution | k3 | notes | retry
Usage: advanced.py <case.json>   -> report JSON on stdout
Artifacts land in arms-runs/<case_id>/ ; report carries _run_dir for evidence checks."""
import base64, json, os, pathlib, re, subprocess, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import llm, exit_if_limited, CALLS

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DISABLE = set(filter(None, os.environ.get("ADVANCED_DISABLE", "").split(",")))
GHREPO = os.environ.get("GHREPO", "Nathanjr123/repo-testify")  # set to your fork to run Level 3 yourself


def jparse(text):
    s, e = text.find("{"), text.rfind("}")
    return json.loads(text[s:e + 1])

def gh(args, **kw):
    return subprocess.run(["gh", *args], capture_output=True, text=True, timeout=300, **kw)

def stage_map(case):
    owner_repo = case["repo"].split("github.com/")[-1].strip("/")
    tree = gh(["api", f"repos/{owner_repo}/git/trees/{case['commit']}?recursive=1"])
    paths = [e["path"] for e in json.loads(tree.stdout).get("tree", [])] if tree.returncode == 0 else []
    manifests = {}
    for m in ("setup.py", "pyproject.toml", "setup.cfg", "requirements.txt"):
        if m in paths:
            r = gh(["api", f"repos/{owner_repo}/contents/{m}?ref={case['commit']}", "--jq", ".content"])
            if r.returncode == 0:
                manifests[m] = base64.b64decode(r.stdout)[:4000].decode(errors="replace")
    rd = gh(["api", f"repos/{owner_repo}/readme?ref={case['commit']}", "--jq", ".content"])
    readme = base64.b64decode(rd.stdout).decode(errors="replace") if rd.returncode == 0 else ""
    return {"paths": paths[:400], "manifests": manifests, "readme": readme[:25000]}

def stage_plan(case, repo_map, notes):
    claims = json.dumps(case["claims"], indent=1)
    prompt = f"""You design sandbox probes to verify repository claims by EXECUTION.
Repo {case['repo']} @ {case['commit']}. Environment facts so far: {json.dumps(notes)}
Manifests: {json.dumps(repo_map['manifests'])[:6000]}
For EACH claim below, emit ONE probe: a bash command sequence that would settle it in a fresh python container. Rules: probe must terminate <=120s; prefer the claim's own words (install its way, run its snippet verbatim from the README); for python-version claims pick image accordingly (python:3.X-slim); no GPU; pip installs go in "setup", checks go in "commands"; expected-output checks compare with python asserts.
SHELL RULES: every command runs through `bash -lc` joined with ' && '; NEVER use here-documents (<<EOF) or multi-line python; put Python in `python3 -c '...'` with single quotes (double quotes inside), or write a script with printf '%s' > /tmp/p.py && python3 /tmp/p.py. A probe that cannot run is worthless.
INTERFACE CONTRACT: the LAST line every probe prints must be exactly `VERDICT_LINE: PASS <short reason>` or `VERDICT_LINE: FAIL <short reason>` (use `|| echo "VERDICT_LINE: FAIL ..."`), so the adjudicator reads one line, not a dump. Print the key observed value on the line before it.
NETWORK: default "none". For claims about badges/URLs/CI status/remote resources set "network": "on" and check with python urllib (no curl in slim images): status code + a distinctive substring; a dead badge host or 404 is evidence.
Do NOT add dependencies the README does not mention to make a claim pass; if the claim only works with an extra package, the probe should FAIL as written and print what was missing.
Claims: {claims}
README (for verbatim snippets): {repo_map['readme'][:15000]}
Reply ONLY JSON: {{"probes": [{{"id": "p-<claim_id>", "claim_id": "...", "image": "python:3.11-slim", "network": "none|on", "setup": [..], "commands": [..], "timeout_s": 120}}]}}"""
    return jparse(llm(prompt))["probes"]

def stage_execute(case, probes, run_dir):
    """Commit the probe spec to a probes/<case> branch through the GitHub API (no local git, nothing touches master),
    dispatch the deterministic probe workflow on that branch, wait, download the artifacts."""
    spec = {"case_id": case["id"], "repo": case["repo"], "commit": case["commit"], "probes": probes}
    local = ROOT / "eval" / "probes"; local.mkdir(exist_ok=True)
    n = len(list(local.glob(f"{case['id']}*.json")))
    name = f"{case['id']}.json" if n == 0 else f"{case['id']}-r{n}.json"
    (local / name).write_text(json.dumps(spec, indent=1))  # local copy for the trajectory renderer; committed by a human, never by the arm
    path = f"eval/probes/{name}"; branch = f"probes/{case['id']}"
    master = gh(["api", f"repos/{GHREPO}/git/ref/heads/master", "--jq", ".object.sha"]).stdout.strip()
    gh(["api", "-X", "POST", f"repos/{GHREPO}/git/refs", "-f", f"ref=refs/heads/{branch}", "-f", f"sha={master}"])  # 422 if it exists: fine
    existing = gh(["api", f"repos/{GHREPO}/contents/{path}?ref={branch}", "--jq", ".sha"])
    args = ["api", "-X", "PUT", f"repos/{GHREPO}/contents/{path}", "-f", f"message=probes: {case['id']} ({name})",
            "-f", f"content={base64.b64encode(json.dumps(spec, indent=1).encode()).decode()}", "-f", f"branch={branch}"]
    if existing.returncode == 0 and existing.stdout.strip():
        args += ["-f", f"sha={existing.stdout.strip()}"]
    put = gh(args)
    if put.returncode != 0:
        raise RuntimeError("probe spec upload failed: " + put.stderr[:300])
    for attempt in range(4):  # GitHub returned 504 on dispatch once; transient, retry
        r = gh(["workflow", "run", "probe.yml", "--ref", branch, "-f", f"probes_path={path}", "--repo", GHREPO])
        if r.returncode == 0:
            break
        time.sleep(30 * (attempt + 1))
    else:
        raise RuntimeError("dispatch failed after retries: " + r.stderr[:300])
    time.sleep(20)
    rid = gh(["run", "list", "--repo", GHREPO, "--workflow", "probe", "--branch", branch, "--limit", "1",
              "--json", "databaseId", "--jq", ".[0].databaseId"]).stdout.strip()
    for _ in range(60):  # up to 30 min
        st = gh(["run", "view", rid, "--repo", GHREPO, "--json", "status", "--jq", ".status"]).stdout.strip()
        if st == "completed":
            break
        time.sleep(30)
    dl = run_dir / "artifacts"
    gh(["run", "download", rid, "--repo", GHREPO, "-D", str(dl)])
    outs = list(dl.glob(f"*/{case['id']}"))
    if not outs:
        raise RuntimeError(f"no artifacts for {case['id']} in run {rid}")
    # build commands.log for evidence checking
    log = []
    for pd in sorted(outs[0].iterdir()):
        if pd.is_dir():
            entry = {"probe": pd.name}
            for f in ("cmd.txt", "exit_code", "stdout.log", "stderr.log", "phase_a.log"):
                fp = pd / f
                entry[f] = fp.read_text(errors="replace")[:3000] if fp.exists() else ""
            log.append(entry)
    (run_dir / "commands.log").write_text(json.dumps(log, indent=1))
    return log, rid

FEWSHOT = """Examples of good verdicts:
- Claim "pip install X works": exit_code 0 and import succeeded -> verified/high, evidence command ref.
- Claim "supports Python 3.12": probe on python:3.12-slim exited 1 with ModuleNotFoundError: imp -> refuted/high.
- Claim "2x faster than Y": no benchmark was run -> unverifiable/low, escalate; NEVER guess from reputation."""

def adjudicate_batch(case, probe_log, k):
    """One LLM call per vote covering ALL claims (usage economy: 11x fewer calls than per-claim)."""
    claims = json.dumps([{"id": c["id"], "text": c["text"]} for c in case["claims"]])
    def tail_with_verdict(s, n):
        lines = s.strip().splitlines()
        vl = [l for l in lines if "VERDICT_LINE:" in l]
        return (s[-n:] + ("\n" + vl[-1] if vl and vl[-1] not in s[-n:] else ""))
    slim = [{"probe": p["probe"], "cmd": p["cmd.txt"][:700], "exit_code": p["exit_code"].strip(),
             "stdout": tail_with_verdict(p["stdout.log"], 1400), "stderr": p["stderr.log"][-600:], "phase_a_tail": p["phase_a.log"][-400:]}
            for p in probe_log]
    prompt = f"""You adjudicate repository claims from EXECUTION EVIDENCE only.
{FEWSHOT}
Claims: {claims}
Probe transcripts (probe p-cN corresponds to claim cN): {json.dumps(slim)[:60000]}
Rules: verdict from the transcript alone; quote the exit code you rely on; missing/ambiguous evidence -> unverifiable + low.
v3 rules (from the audited public-split failures):
 (a) A probe's own `VERDICT_LINE: PASS/FAIL` is its conclusion, follow it unless you quote contrary evidence from the same transcript.
 (b) The claim is judged AS WRITTEN in the README. If a documented prerequisite (install line, pinned dependency, required tool) fails as written, every claim that depends on it is REFUTED (high), not unverifiable, "could be made to work" is not the question.
 (c) If a probe's setup installed a package or applied a fix the README does not document, the claim is UNVERIFIABLE-as-written (low) and must say what was added.
Reply ONLY JSON:
{{"claims": [{{"id": "cN", "verdict": "verified|refuted|unverifiable", "confidence": "high|low", "evidence": [{{"kind": "command", "ref": "p-cN", "excerpt": "<quoted output line + exit_code N>"}}]}}]}}
Claims again: {claims}"""
    votes = []
    for _ in range(k):
        try:
            votes.append({v["id"]: v for v in jparse(llm(prompt))["claims"]})
        except Exception:
            pass
    out = []
    for c in case["claims"]:
        vs = [v[c["id"]] for v in votes if c["id"] in v]
        if not vs:
            out.append({"id": c["id"], "verdict": "unverifiable", "confidence": "low", "evidence": []}); continue
        tally = {}
        for v in vs: tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1
        win = max(tally, key=tally.get)
        best = dict(next(v for v in vs if v["verdict"] == win))
        if tally[win] < len(vs): best["confidence"] = "low"
        best["votes"] = [{"verdict": v["verdict"], "confidence": v.get("confidence")} for v in vs]  # k=1 ablation replays from vote 0
        out.append(best)
    return out

def crosscheck(verdicts, probe_log):
    """Code-checked evidence: a quoted exit code must match the RECORDED exit code of the probe the verdict cites."""
    by_probe = {p["probe"]: p for p in probe_log}
    for v in verdicts:
        for e in v.get("evidence", []):
            m = re.search(r"exit[_ ]?code[:= ]+(\d+)", str(e.get("excerpt", "")), re.I)
            ref = str(e.get("ref", "")); pm = re.search(r"\bp-c\d+\b", ref)
            if m and pm and pm.group(0) in by_probe:
                if by_probe[pm.group(0)]["exit_code"].strip() != m.group(1):
                    v["verdict"], v["confidence"] = "unverifiable", "low"
                    e["excerpt"] = str(e.get("excerpt", "")) + f" [CROSSCHECK FAILED: probe {pm.group(0)} recorded exit {by_probe[pm.group(0)]['exit_code'].strip()}]"
    return verdicts

def write_memo(case, verdicts, esc, score):
    """A memo the buyer can forward: refuted claims first with their evidence, then escalations, then what held."""
    txt = {c["id"]: c["text"] for c in case["claims"]}
    def line(v):
        ev = (v.get("evidence") or [{}])[0]
        return f"- **{v['id']}** {txt.get(v['id'], '')}\n  Evidence: `{str(ev.get('ref',''))[:40]}` {str(ev.get('excerpt',''))[:220]}"
    ref = [v for v in verdicts if v["verdict"] == "refuted"]; ver = [v for v in verdicts if v["verdict"] == "verified"]; unv = [v for v in verdicts if v["verdict"] == "unverifiable"]
    parts = [f"# Due-diligence memo: {case['repo']} @ {case['commit'][:12]}", f"Question: {case['buyer_question']}", "",
             f"**Bottom line.** {len(ver)} of {len(verdicts)} README claims held under execution, {len(ref)} were refuted, {len(unv)} could not be settled in the sandbox and need a human. Rubric score {score}/100.", ""]
    if ref: parts += ["## Refuted (negotiate on these)"] + [line(v) for v in ref] + [""]
    if unv: parts += ["## Escalated to a human reviewer (not settled by execution)"] + [line(v) for v in unv] + [""]
    if ver: parts += ["## Verified as written"] + [f"- **{v['id']}** {txt.get(v['id'], '')[:140]}" for v in ver] + [""]
    parts += ["Every verdict above cites a recorded probe (command, exit code, output) from the CI run named in the report."]
    return "\n".join(parts)

def main():
    case = json.loads(pathlib.Path(sys.argv[1]).read_text())
    run_dir = ROOT / "arms-runs" / f"{case['id']}-{int(time.time())}"
    run_dir.mkdir(parents=True)
    notes = {}
    repo_map = stage_map(case)
    if "notes" not in DISABLE:
        notes["manifest_files"] = list(repo_map["manifests"])
    if "execution" in DISABLE:
        probe_log, rid = [], "none"
    else:
        probes = stage_plan(case, repo_map, notes)
        probe_log, rid = stage_execute(case, probes, run_dir)
        if "retry" not in DISABLE:
            def malformed(p):
                err = p.get("stderr.log", ""); out = p.get("stdout.log", "")
                return ("here-document" in err or "syntax error" in err.lower() or "unexpected EOF" in err) and "VERDICT_LINE" not in out
            broken = [p for p in probe_log if p["cmd.txt"].startswith("PHASE_A_FAILED") or malformed(p)]
            if broken:  # ONE repair round (DESIGN: self-repair plateaus after 2; budget allows 1): environment failed, not the claim
                errs = {b["probe"]: b["phase_a.log"][-500:] for b in broken}
                errs = {b["probe"]: (b["phase_a.log"][-500:] if b["cmd.txt"].startswith("PHASE_A_FAILED") else "PROBE DID NOT EXECUTE (shell error): " + b["stderr.log"][-400:]) for b in broken}
                fix_prompt = f"""These probes failed before the claim was tested: either the SETUP failed in a fresh container, or the probe command itself did not execute (shell syntax, e.g. a here-document inside an && chain). Repair each probe ONCE so the claim itself gets tested; keep the claim's own install method; NEVER use here-documents, use python3 -c '...' or printf a script file; each retry must CHANGE the command. Failures: {json.dumps(errs)[:6000]}
Original probes: {json.dumps([p for p in probes if p['id'] in errs])[:6000]}
Reply ONLY JSON: {{"probes": [...same schema...]}}"""
                try:
                    repaired = jparse(llm(fix_prompt))["probes"]
                    notes["repair_round"] = list(errs)
                    log2, rid2 = stage_execute(case, repaired, run_dir)
                    fixed = {p["probe"]: p for p in log2}
                    probe_log = [fixed.get(p["probe"], p) for p in probe_log]
                    rid = f"{rid}+{rid2}"
                except Exception as e:
                    notes["repair_round_error"] = str(e)[:200]
    k = 1 if "k3" in DISABLE else 3
    verdicts = adjudicate_batch(case, probe_log, k)
    verdicts = crosscheck(verdicts, probe_log)
    esc = [v["id"] for v in verdicts if v["verdict"] == "unverifiable"]
    n_ver = sum(v["verdict"] == "verified" for v in verdicts)
    n_ref = sum(v["verdict"] == "refuted" for v in verdicts)
    score = round(100 * (n_ver + 0.5 * (len(verdicts) - n_ver - n_ref)) / max(1, len(verdicts)))
    idx_text = "\n".join(f'{p["probe"]} {p["cmd.txt"][:600]}\nSTDOUT {p["stdout.log"][:3000]}\nSTDERR {p["stderr.log"][-1500:]}\nPHASE_A {p["phase_a.log"][-800:]}\nEXIT {p["exit_code"].strip()}' for p in probe_log)
    report = {"repo": case["repo"], "overall_score": score, "claims": verdicts,
              "escalations": esc, "run_id": rid, "_run_dir": str(run_dir),
              "_evidence_index": {"probes": [p["probe"] for p in probe_log], "text": idx_text},
              "llm_calls": CALLS["n"], "usage": {"cost_usd": CALLS["cost_usd"], "input_tokens": CALLS["input_tokens"], "output_tokens": CALLS["output_tokens"]},
              "memo_md": write_memo(case, verdicts, esc, score)}
    (run_dir / "report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report))

if __name__ == "__main__":
    exit_if_limited(main)
