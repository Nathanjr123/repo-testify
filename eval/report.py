"""proof/build_proof.json -> RESULTS.md tables. Numbers are NEVER hand-typed (law 9)."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
proof = json.loads((ROOT / "proof" / "build_proof.json").read_text())
latest = {}
for e in proof:
    if e.get("discarded") or e.get("limit_blocked") or e.get("partial"):
        continue
    latest[(e["label"], e["cases_dir"])] = e  # newest wins
print("# Results\n")
print("| run | cases | raw | rows | gates | cost $ | wall s | git | ts |")
print("|---|---|---|---|---|---|---|---|---|")
for (label, cd), e in sorted(latest.items()):
    a = e["agg"]
    rows = " ".join(f"{k}={v}" for k, v in a["rows"].items())
    gates = " ".join(f"{k}={v:.2f}" for k, v in a["gates"].items())
    print(f"| {label} | {cd.split('/')[-1]} | **{a['raw']}** | {rows} | {gates} "
          f"| {e['cost_usd']} | {e['wall_total_s']} | {e['git']} | {e['ts']} |")
print("\nPer-case detail lives in proof/build_proof.json (find the run id above).")
