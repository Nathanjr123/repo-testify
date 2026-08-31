"""Single-shot execution baseline: a FAIRER baseline than the reading arm.
One agent, given the README + file tree, writes ONE bash script that attempts to check every claim,
runs it once in the same sandbox the pipeline uses, then makes ONE adjudication over the whole output.
This isolates the pipeline's structure (one probe per claim + VERDICT_LINE contract + per-claim voting)
from raw 'an agent that can execute'. Same case file, same scorer, same schema as the other arms.
Usage: single_shot.py <case.json>  -> report JSON on stdout"""
import json, os, pathlib, subprocess, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import llm, exit_if_limited
ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
GHREPO = os.environ.get("GHREPO", "Nathanjr123/repo-testify")
sys.path.insert(0, str(ROOT))
from arms.advanced.advanced import stage_map, stage_execute, jparse  # reuse map + CI execute


def main():
    case = json.loads(pathlib.Path(sys.argv[1]).read_text())
    run_dir = ROOT / "arms-runs" / f"ss-{case['id']}-{int(time.time())}"; run_dir.mkdir(parents=True)
    rmap = stage_map(case)
    claims = json.dumps([{"id": c["id"], "text": c["text"]} for c in case["claims"]])
    plan = llm(f"""You are auditing a repository by executing ONE bash script in a fresh python container.
Write a single script that checks ALL of these claims and, for each, prints a line `CLAIM <id>: PASS|FAIL <one-line reason>`.
You get one script, not one-per-claim. Install the repo the README's way; run the README's own snippets; no here-documents (use python3 -c or printf a file).
Claims: {claims}
README: {rmap['readme'][:12000]}
Reply ONLY JSON: {{"image":"python:3.11-slim","network":"none","setup":[...],"commands":[...],"timeout_s":300}}""")
    spec = jparse(plan)
    probe = {"id": "ss", "claim_id": "all", "image": spec.get("image", "python:3.11-slim"),
             "network": spec.get("network", "none"), "setup": spec.get("setup", []),
             "commands": spec.get("commands", []), "timeout_s": min(spec.get("timeout_s", 300), 400)}
    probe_log, rid = stage_execute(case, [probe], run_dir)
    txt = "\n".join(f'{p["probe"]} {p["cmd.txt"][:300]}\nSTDOUT {p["stdout.log"][:6000]}\nSTDERR {p["stderr.log"][-1500:]}\nEXIT {p["exit_code"].strip()}' for p in probe_log)
    verdict = llm(f"""From this single script's recorded output, give a verdict for EVERY claim: verified | refuted | unverifiable, confidence high|low, and an evidence excerpt (a line from the output).
Claims: {claims}
Script output:\n{txt[:14000]}
Reply ONLY JSON: {{"claims":[{{"id":"cN","verdict":"...","confidence":"...","evidence":[{{"kind":"command","ref":"ss","excerpt":"..."}}]}}]}}""")
    vs = {v["id"]: v for v in jparse(verdict)["claims"]}
    idx_text = txt
    out_claims = []
    for c in case["claims"]:
        v = vs.get(c["id"]) or {"id": c["id"], "verdict": "unverifiable", "confidence": "low", "evidence": []}
        out_claims.append(v)
    nver = sum(v["verdict"] == "verified" for v in out_claims); nref = sum(v["verdict"] == "refuted" for v in out_claims)
    esc = [v["id"] for v in out_claims if v["verdict"] == "unverifiable"]
    score = round(100 * (nver + 0.5 * (len(out_claims) - nver - nref)) / max(1, len(out_claims)))
    (run_dir / "commands.log").write_text(json.dumps(probe_log, indent=1))
    report = {"repo": case["repo"], "overall_score": score, "claims": out_claims, "escalations": esc,
              "run_id": rid, "_run_dir": str(run_dir),
              "_evidence_index": {"probes": ["ss"], "text": idx_text},
              "llm_calls": 2, "usage": {}, "memo_md": f"single-shot: {nver} verified, {nref} refuted, {len(esc)} escalated"}
    print(json.dumps(report))


exit_if_limited(main)
