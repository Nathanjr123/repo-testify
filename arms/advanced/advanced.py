"""Advanced arm — code-orchestrated pipeline (see DESIGN.md).
Stages: map -> plan -> execute (GH Actions, deterministic) -> adjudicate (k=3 vote) -> report.
Flags via ADVANCED_DISABLE (comma-separated): execution | k3 | notes | retry
Usage: advanced.py <case.json>   -> report JSON on stdout
Artifacts land in arms-runs/<case_id>/ ; report carries _run_dir for evidence checks."""
import base64, json, os, pathlib, re, subprocess, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import llm, exit_if_limited

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DISABLE = set(filter(None, os.environ.get("ADVANCED_DISABLE", "").split(",")))
GHREPO = "Nathanjr123/repo-testify"


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
INTERFACE CONTRACT: the LAST line every probe prints must be exactly `VERDICT_LINE: PASS <short reason>` or `VERDICT_LINE: FAIL <short reason>` (use `|| echo "VERDICT_LINE: FAIL ..."`), so the adjudicator reads one line, not a dump. Print the key observed value on the line before it.
NETWORK: default "none". For claims about badges/URLs/CI status/remote resources set "network": "on" and check with python urllib (no curl in slim images): status code + a distinctive substring; a dead badge host or 404 is evidence.
Do NOT add dependencies the README does not mention to make a claim pass; if the claim only works with an extra package, the probe should FAIL as written and print what was missing.
Claims: {claims}
README (for verbatim snippets): {repo_map['readme'][:15000]}
Reply ONLY JSON: {{"probes": [{{"id": "p-<claim_id>", "claim_id": "...", "image": "python:3.11-slim", "network": "none|install-only", "setup": [..], "commands": [..], "timeout_s": 120}}]}}"""
    return jparse(llm(prompt))["probes"]

def stage_execute(case, probes, run_dir):
    spec = {"case_id": case["id"], "repo": case["repo"], "commit": case["commit"], "probes": probes}
    n = len(list((ROOT / "eval" / "probes").glob(f"{case['id']}*.json")))
    pf = ROOT / "eval" / "probes" / (f"{case['id']}.json" if n == 0 else f"{case['id']}-r{n}.json")
    pf.write_text(json.dumps(spec, indent=1))
    subprocess.run(["git", "-C", str(ROOT), "add", str(pf)], check=True)
    subprocess.run(["git", "-C", str(ROOT), "-c", "user.email=p.szczepanik94@gmail.com",
                    "-c", "user.name=Nathanjr123", "commit", "-qm", f"probes: {case['id']}"], check=False)
    subprocess.run(["git", "-C", str(ROOT), "push", "-q"], check=True)
    for attempt in range(4):  # GitHub returned 504 on dispatch once (r05, sweep1); transient, retry
        r = gh(["workflow", "run", "probe.yml", "--ref", "master", "-f",
                f"probes_path={pf.relative_to(ROOT)}", "--repo", GHREPO])
        if r.returncode == 0:
            break
        time.sleep(30 * (attempt + 1))
    else:
        raise RuntimeError("dispatch failed after retries: " + r.stderr[:300])
    time.sleep(20)
    rid = gh(["run", "list", "--repo", GHREPO, "--workflow", "probe", "--limit", "1",
              "--json", "databaseId,status", "--jq", ".[0].databaseId"]).stdout.strip()
    for _ in range(60):  # up to 30 min
        st = gh(["run", "view", rid, "--repo", GHREPO, "--json", "status,conclusion",
                 "--jq", ".status"]).stdout.strip()
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

def adjudicate_claim(case, claim, probe_log, k):
    votes = []
    prompt = f"""You adjudicate ONE repository claim from EXECUTION EVIDENCE only.
{FEWSHOT}
Claim ({claim['id']}): {claim['text']}
Probe transcript (cmd, exit codes, output head/tail): {json.dumps(probe_log)[:8000]}
Rules: verdict from evidence in the transcript alone; quote the exit code you rely on; if evidence is missing or ambiguous -> unverifiable + low confidence. Reply ONLY JSON:
{{"id": "{claim['id']}", "verdict": "verified|refuted|unverifiable", "confidence": "high|low",
 "evidence": [{{"kind": "command", "ref": "<exact cmd string or probe id>", "excerpt": "<quoted output line + exit code>"}}]}}
Claim: {claim['text']}"""
    for _ in range(k):
        try:
            votes.append(jparse(llm(prompt)))
        except Exception:
            pass
    if not votes:
        return {"id": claim["id"], "verdict": "unverifiable", "confidence": "low", "evidence": []}
    tally = {}
    for v in votes:
        tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1
    win = max(tally, key=tally.get)
    best = next(v for v in votes if v["verdict"] == win)
    if tally[win] < len(votes):  # disagreement -> demote confidence (ToE-style)
        best["confidence"] = "low"
    return best

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
 (a) A probe's own `VERDICT_LINE: PASS/FAIL` is its conclusion — follow it unless you quote contrary evidence from the same transcript.
 (b) The claim is judged AS WRITTEN in the README. If a documented prerequisite (install line, pinned dependency, required tool) fails as written, every claim that depends on it is REFUTED (high), not unverifiable — "could be made to work" is not the question.
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

def crosscheck(verdicts, commands_log_text):
    """Code-checked evidence: a quoted exit code must appear in the recorded log (DESIGN stage 5)."""
    for v in verdicts:
        for e in v.get("evidence", []):
            m = re.search(r"exit[_ ]?code[:= ]+(\d+)", e.get("excerpt", ""), re.I)
            if m and f'"exit_code": "{m.group(1)}"' not in commands_log_text and f"exit={m.group(1)}" not in commands_log_text:
                v["verdict"], v["confidence"] = "unverifiable", "low"
                e["excerpt"] += " [CROSSCHECK FAILED: quoted exit code not in recorded log]"
    return verdicts

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
            broken = [p for p in probe_log if p["cmd.txt"].startswith("PHASE_A_FAILED")]
            if broken:  # ONE repair round (DESIGN: self-repair plateaus after 2; budget allows 1): environment failed, not the claim
                errs = {b["probe"]: b["phase_a.log"][-500:] for b in broken}
                fix_prompt = f"""These probe SETUP steps failed in a fresh container (environment problem, before the claim was tested). Repair each probe's setup/commands ONCE so the claim itself gets tested; keep the claim's own install method; each retry must CHANGE the command. Failures: {json.dumps(errs)[:6000]}
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
    clog_text = (run_dir / "commands.log").read_text() if probe_log else ""
    verdicts = adjudicate_batch(case, probe_log, k)
    verdicts = crosscheck(verdicts, clog_text)
    esc = [v["id"] for v in verdicts if v["verdict"] == "unverifiable"]
    n_ver = sum(v["verdict"] == "verified" for v in verdicts)
    n_ref = sum(v["verdict"] == "refuted" for v in verdicts)
    score = round(100 * (n_ver + 0.5 * (len(verdicts) - n_ver - n_ref)) / max(1, len(verdicts)))
    report = {"repo": case["repo"], "overall_score": score, "claims": verdicts,
              "escalations": esc, "run_id": rid, "_run_dir": str(run_dir),
              "memo_md": f"{n_ver} verified, {n_ref} refuted, {len(esc)} escalated of {len(verdicts)} claims."}
    (run_dir / "report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report))

if __name__ == "__main__":
    exit_if_limited(main)
