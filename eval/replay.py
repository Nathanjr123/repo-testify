"""Re-score a stored run through the SAME scorer+aggregate; must reproduce its raw exactly."""
import argparse, json, pathlib
from .aggregate import aggregate
ROOT = pathlib.Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(); ap.add_argument("--run", required=True)
rid = ap.parse_args().run
proof = json.loads((ROOT / "proof" / "build_proof.json").read_text())
e = next(x for x in proof if x["id"] == rid)
ok = [r for r in e["per_case"].values() if r["status"] == "ok"]
got = aggregate(ok)["raw"]
assert got == e["agg"]["raw"], f"REPLAY MISMATCH {got} != {e['agg']['raw']} — grader drift (law: replay calls the grader path)"
print(f"replay ok: {rid} raw={got}")
