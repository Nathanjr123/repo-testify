"""Run an arm over a case set; score; append a proof entry. Arms are arms/<name>/run.sh:
  run.sh <case.json>  -> writes output JSON to stdout (may include {"usage": {"cost_usd":..,"tokens":..}})
Ablations: ADVANCED_DISABLE=<flag> env reaches the arm's code."""
import argparse, json, os, pathlib, subprocess, sys, time
from .scorer import score, SANITY_CASE
from .aggregate import aggregate

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROOF = ROOT / "proof" / "build_proof.json"

def git_hash():
    try:
        return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "nogit"

def run_case(arm, case_path):
    t0 = time.monotonic()
    p = subprocess.run(["bash", str(ROOT / "arms" / arm / "run.sh"), str(case_path)],
                       capture_output=True, text=True, timeout=1800)
    wall = round(time.monotonic() - t0, 2)
    if p.returncode != 0:
        return {"status": "arm_error", "stderr": p.stderr[-2000:], "wall_s": wall}
    try:
        out = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"status": "invalid_output", "raw_stdout": p.stdout[-2000:], "wall_s": wall}
    case = json.loads(pathlib.Path(case_path).read_text())
    s = score(case, out)
    return {"status": "ok", "wall_s": wall, "usage": out.get("usage", {}), **s}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--label", default=None)
    ap.add_argument("--sanity", action="store_true")
    a = ap.parse_args()
    if a.sanity:
        if SANITY_CASE is None:
            sys.exit("law 2: define SANITY_CASE in eval/scorer.py before measuring anything")
        case, out, expected = SANITY_CASE
        got = aggregate([score(case, out)])["raw"]
        assert abs(got - expected) < 1e-9, f"sanity cell FAILED: {got} != {expected}"
        print(f"sanity cell ok: {got}")
        return
    cases = sorted(pathlib.Path(a.cases).glob("*.json"))
    if not cases:
        sys.exit(f"no cases in {a.cases}")
    per_case, results = [], {}
    for c in cases:
        r = run_case(a.arm, c)
        results[c.name] = r
        if r["status"] == "ok":
            per_case.append(r)
        print(f"{c.name}: {r['status']} wall={r['wall_s']}s", file=sys.stderr)
    agg = aggregate(per_case)
    entry = {"id": f"{a.label or a.arm}-{int(time.time())}", "arm": a.arm,
             "label": a.label or a.arm, "disable": os.environ.get("ADVANCED_DISABLE"),
             "cases_dir": a.cases, "git": git_hash(),
             "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "cmd": " ".join(sys.argv),
             "agg": agg,
             "human_time_s": None,  # fill from measurement, per PDF metric table
             "cost_usd": round(sum(r.get("usage", {}).get("cost_usd", 0) for r in per_case), 4),
             "wall_total_s": round(sum(r["wall_s"] for r in results.values()), 1),
             "per_case": results}
    PROOF.parent.mkdir(exist_ok=True)
    proof = json.loads(PROOF.read_text()) if PROOF.exists() else []
    proof.append(entry)
    PROOF.write_text(json.dumps(proof, indent=1))
    print(json.dumps({"id": entry["id"], "agg": agg}, indent=1))

if __name__ == "__main__":
    main()
