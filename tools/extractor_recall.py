"""Measure the README claim-extractor's recall against the hand-authored claim lists on the public+extension repos.
For each repo: run the extractor, ask a model to match each hand-authored claim to an extracted one (semantic),
report recall = matched / hand-authored. Puts a number on the 'audit any repo' story."""
import json, os, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from arms.common import llm
ROOT = pathlib.Path(__file__).resolve().parent.parent
pub = sorted((ROOT / "eval/cases/public").glob("r*.json"))
res = []
for cp in pub:
    case = json.loads(cp.read_text())
    ext = subprocess.run([sys.executable, str(ROOT / "tools/extract_claims.py"), case["repo"], "--commit", case["commit"]],
                         capture_output=True, text=True, timeout=600)
    try:
        extracted = json.loads(ext.stdout[ext.stdout.find("{"):ext.stdout.rfind("}")+1])["claims"]
    except Exception as e:
        res.append({"id": case["id"], "error": str(e)[:100]}); continue
    hand = [c["text"] for c in case["claims"]]
    exl = [c["text"] for c in extracted]
    m = llm(f"""Hand-authored claims (H) and extractor-produced claims (E) for the same repo. For each H, does some E express the SAME checkable claim (yes/no)? Reply ONLY JSON {{"matched": <int>, "total": {len(hand)}}}.
H: {json.dumps(hand)}
E: {json.dumps(exl)}""")
    try:
        mm = json.loads(m[m.find("{"):m.rfind("}")+1])
        res.append({"id": case["id"], "matched": mm["matched"], "total": len(hand), "extracted": len(exl)})
    except Exception as e:
        res.append({"id": case["id"], "error": "match-parse " + str(e)[:80]})
tot_m = sum(r.get("matched", 0) for r in res if "matched" in r); tot_h = sum(r.get("total", 0) for r in res if "matched" in r)
out = {"per_repo": res, "recall": round(tot_m / tot_h, 3) if tot_h else None, "matched": tot_m, "hand_total": tot_h}
(ROOT / "proof" / "extractor_recall.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
