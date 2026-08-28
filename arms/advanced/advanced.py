"""Advanced arm — code-orchestrated pipeline (see DESIGN.md).
Stages: map -> plan -> execute (GH Actions, deterministic) -> adjudicate (k=3 vote) -> report.
Flags via ADVANCED_DISABLE (comma-separated): execution | k3 | notes | retry
Usage: advanced.py <case.json>   -> report JSON on stdout
Artifacts land in arms-runs/<case_id>/ ; report carries _run_dir for evidence checks."""
import base64, json, os, pathlib, re, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
DISABLE = set(filter(None, os.environ.get("ADVANCED_DISABLE", "").split(",")))
GHREPO = "Nathanjr123/repo-testify"

def llm(prompt, retries=3):
    """claude -p with usage-limit backoff (limits are infra faults, never verdicts)."""
    delay = 60
    for i in range(retries + 1):
        r = subprocess.run(["claude", "-p", prompt, "--model", "claude-fable-5"],
                           capture_output=True, text=True, timeout=600)
        out = r.stdout.strip()
        low = (out + r.stderr).lower()
        if r.returncode == 0 and out:
            return out
        if any(k in low for k in ("rate limit", "usage limit", "429", "overloaded")):
            time.sleep(delay); delay = min(delay * 5, 900); continue
        raise RuntimeError(f"llm failed: {r.stderr[:500]}")
    raise RuntimeError("llm blocked on limits after retries")

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
For EACH claim below, emit ONE probe: a bash command sequence that would settle it in a fresh python container. Rules: probe must terminate <=120s; prefer the claim's own words (install its way, run its snippet verbatim from the README); for python-version claims pick image accordingly (python:3.X-slim); no GPU; pip installs go in "setup", checks go in "commands"; expected-output checks compare with grep/python asserts.
Claims: {claims}
README (for verbatim snippets): {repo_map['readme'][:15000]}
Reply ONLY JSON: {{"probes": [{{"id": "p-<claim_id>", "claim_id": "...", "image": "python:3.11-slim", "network": "none|install-only", "setup": [..], "commands": [..], "timeout_s": 120}}]}}"""
    return jparse(llm(prompt))["probes"]

def stage_execute(case, probes, run_dir):
    spec = {"case_id": case["id"], "repo": case["repo"], "commit": case["commit"], "probes": probes}
    pf = ROOT / "eval" / "probes" / f"{case['id']}.json"
    pf.write_text(json.dumps(spec, indent=1))
    subprocess.run(["git", "-C", str(ROOT), "add", str(pf)], check=True)
    subprocess.run(["git", "-C", str(ROOT), "-c", "user.email=p.szczepanik94@gmail.com",
                    "-c", "user.name=Nathanjr123", "commit", "-qm", f"probes: {case['id']}"], check=False)
    subprocess.run(["git", "-C", str(ROOT), "push", "-q"], check=True)
    r = gh(["workflow", "run", "probe.yml", "--ref", "master", "-f",
            f"probes_path=eval/probes/{case['id']}.json", "--repo", GHREPO])
    if r.returncode != 0:
        raise RuntimeError("dispatch failed: " + r.stderr[:300])
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
    k = 1 if "k3" in DISABLE else 3
    clog_text = (run_dir / "commands.log").read_text() if probe_log else ""
    verdicts = [adjudicate_claim(case, c, [p for p in probe_log if c["id"] in p.get("probe", "")] or probe_log, k)
                for c in case["claims"]]
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
    main()
