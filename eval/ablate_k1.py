# PROVENANCE — read before modifying.
# Written during the competition (2026-08-28/31) by Claude Code (claude-fable-5) under Nathan Obiekwe's
# direction; every design decision it encodes is recorded in DESIGN.md / DECISIONS.md / CHANGELOG.md, and the
# session trajectory that produced it is in traces/. Pre-existing before kickoff: only the problem-agnostic
# skeleton (Makefile targets, eval/ layout, trace exporter). Human review: Nathan audits truth files and results.
"""FREE ablation: k=1 adjudication = take the first of the persisted k=3 votes per claim, re-score.
Isolates the value of self-consistency voting without spending LLM calls (votes were persisted by the arm)."""
import json, pathlib, sys, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from eval.scorer import score, WEIGHTS
from eval.aggregate import aggregate
ROOT = pathlib.Path(__file__).resolve().parent.parent
label = sys.argv[1] if len(sys.argv) > 1 else "advanced-v2"
proof = json.loads((ROOT / "proof" / "build_proof.json").read_text())
e = [x for x in proof if x["label"] == label][-1]
per, res = [], {}
for cname, r in e["per_case"].items():
    if r["status"] != "ok":
        per.append({"rows": {k: 0.0 for k in WEIGHTS}, "gates": {"valid_report": False, "no_fabricated_evidence": True}, "settled_fraction": 0.0}); res[cname] = r; continue
    out = json.loads(json.dumps(r["output"]))
    for c in out["claims"]:
        v0 = (c.get("votes") or [{}])[0]
        if v0.get("verdict"):
            c["verdict"], c["confidence"] = v0["verdict"], v0.get("confidence") or c["confidence"]
    case = json.loads(next(ROOT.glob(f"eval/cases/*/{cname}")).read_text())
    s = score(case, out); s.update({"status": "ok", "output": out, "wall_s": r["wall_s"]}); per.append(s); res[cname] = s
new = dict(e); new["id"] = f"ablate-k1-{int(time.time())}"; new["label"] = "ablate-k1"; new["disable"] = "k3(replayed from votes[0])"
new["agg"] = aggregate(per); new["per_case"] = res; new["rescored_from"] = e["id"]; new["cmd"] = "python3 eval/ablate_k1.py " + label
proof.append(new); (ROOT / "proof" / "build_proof.json").write_text(json.dumps(proof, indent=1))
print("ablate-k1 raw", new["agg"]["raw"], new["agg"]["rows"])
