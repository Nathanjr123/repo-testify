# PROVENANCE — read before modifying.
# Written during the competition (2026-08-28/31) by Claude Code (claude-fable-5) under Nathan Obiekwe's
# direction; every design decision it encodes is recorded in DESIGN.md / DECISIONS.md / CHANGELOG.md, and the
# session trajectory that produced it is in traces/. Pre-existing before kickoff: only the problem-agnostic
# skeleton (Makefile targets, eval/ layout, trace exporter). Human review: Nathan audits truth files and results.
"""Re-score a stored run's persisted outputs through the CURRENT scorer+aggregate.
--check: assert it reproduces the stored raw (grader-drift detector). --rescore: write a new proof entry
labelled <label>-rescored (scorer changes replay without LLM cost)."""
import argparse, json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from eval.scorer import score
from eval.aggregate import aggregate
ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(); ap.add_argument("--run", required=True); ap.add_argument("--rescore", action="store_true")
a = ap.parse_args()
proof = json.loads((ROOT / "proof" / "build_proof.json").read_text())
e = next(x for x in proof if x["id"] == a.run)
per = []
for cname, r in e["per_case"].items():
    if r["status"] in ("arm_error", "invalid_output"):  # crash-as-zero, same as the runner — never hidden
        from eval.scorer import WEIGHTS
        per.append((cname, {"rows": {k: 0.0 for k in WEIGHTS}, "gates": {"valid_report": False, "no_fabricated_evidence": True}, "status": r["status"], "settled_fraction": 0.0}))
        continue
    if r["status"] != "ok" or "output" not in r: continue
    cp = next(ROOT.glob(f"eval/cases/*/{cname}"))
    s = score(json.loads(cp.read_text()), r["output"]); s["output"] = r["output"]; s["status"] = "ok"; s["wall_s"] = r["wall_s"]
    per.append((cname, s))
agg = aggregate([s for _, s in per])
if a.rescore:
    new = dict(e); new["id"] = f"{e['label']}-rescored-{int(time.time())}"; new["label"] = e["label"] + "-rescored"
    new["agg"] = agg; new["per_case"] = {c: s for c, s in per}; new["rescored_from"] = e["id"]; new.pop("discarded", None)
    proof.append(new); (ROOT / "proof" / "build_proof.json").write_text(json.dumps(proof, indent=1))
    print("rescored ->", new["id"], "raw", agg["raw"])
else:
    assert agg["raw"] == e["agg"]["raw"], f"REPLAY MISMATCH {agg['raw']} != {e['agg']['raw']} (grader drift)"
    print("replay ok:", a.run, "raw", agg["raw"])
