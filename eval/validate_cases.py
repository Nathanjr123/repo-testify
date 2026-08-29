"""Validate every case file against the contract. Run via `make test`."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent
TYPES = {"install", "environment", "quickstart", "interface", "test_ci", "quantitative"}
errs = []
cases = sorted(p for p in (ROOT / "cases").glob("*/r*.json") if p.parent.name != "self")  # self-run case is not part of the evaluation set
for f in cases:
    j = json.loads(f.read_text())
    for k in ("id", "repo", "commit", "bucket", "buyer_question", "claims"):
        if k not in j: errs.append(f"{f.name}: missing {k}")
    if len(j.get("commit", "")) < 7: errs.append(f"{f.name}: unpinned commit")
    if not (8 <= len(j.get("claims", [])) <= 15): errs.append(f"{f.name}: {len(j.get('claims', []))} claims outside 8-15")
    ids = [c.get("id") for c in j.get("claims", [])]
    if len(ids) != len(set(ids)): errs.append(f"{f.name}: duplicate claim ids")
    for c in j.get("claims", []):
        if c.get("type") not in TYPES: errs.append(f"{f.name}:{c.get('id')}: bad type {c.get('type')}")
        for k in ("text", "source_quote", "probe_hint"):
            if not c.get(k): errs.append(f"{f.name}:{c.get('id')}: empty {k}")
    if not any(c["type"] == "install" for c in j.get("claims", [])): errs.append(f"{f.name}: no install claim")
print(f"{len(cases)} case files checked")
if errs:
    print("\n".join(errs)); sys.exit(1)
print("all valid")
