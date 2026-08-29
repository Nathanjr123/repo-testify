"""THE PROPOSED RUBRIC — "make the repo testify".
Agent report schema (arms must emit this JSON):
{ "repo": str, "overall_score": 0-100,
  "claims": [ {"id": str, "verdict": "verified|refuted|unverifiable",
               "confidence": "high|low",
               "evidence": [{"kind": "command|file|url", "ref": str, "excerpt": str}] } ],
  "escalations": [claim ids sent to a human], "memo_md": str }
Case schema (eval/cases/*.json):
{ "id": str, "repo": str, "commit": str, "buyer_question": str,
  "claims": [{"id": str, "text": str, "type": "install|quickstart|compat|feature|benchmark"}] }
Ground truth (PRIVATE, eval/truth/<case_id>.json — heldout half never seen during tuning):
{ "verdicts": {claim_id: "verified|refuted|unverifiable"}, "reviewer_score": 0-100 }
Rows ADD (weights below), gates MULTIPLY (award nothing, only remove).
Bands to be set AFTER measuring row distributions on the first baseline run (law 5).
"""
import json, pathlib, re

WEIGHTS = {  # v2 (2026-08-28, after first row-distribution measurement — see CHANGELOG iteration 6)
    "verdict_acc":     0.45,  # per-claim accuracy vs ground truth; unaddressed claims count as wrong (coverage folded in: it was 1.00 on every case = saturated row)
    "confident_wrong": 0.20,  # 1 - (high-confidence wrong verdicts / claims); abstention is the honest exit
    "evidence_valid":  0.20,  # fraction of verdicts whose evidence refs exist in run artifacts
    "score_error":     0.15,  # 1 - |overall_score - reviewer_score|/100
}
SETTLED_MIN, SETTLED_CAP = 0.50, 0.35  # objective = settle claims. If < half are settled (verified/refuted), raw <= 0.35:
                                       # an arm that abstains on everything must not out-score one that tries (incomplete-objective cap)
BANDS = {}  # set after first distribution measurement — no dead/saturated/crushed rows

TRUTH_DIR = pathlib.Path(__file__).resolve().parent / "truth"

def _macro_f1(pred: dict, truth: dict) -> float:
    classes = ("verified", "refuted", "unverifiable")
    f1s = []
    for c in classes:
        tp = sum(1 for k, v in truth.items() if v == c and pred.get(k) == c)
        fp = sum(1 for k in pred if pred[k] == c and truth.get(k) != c)
        fn = sum(1 for k, v in truth.items() if v == c and pred.get(k) != c)
        if tp == fp == fn == 0:
            continue  # class absent in this case; skip rather than award free 0/1
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        f1s.append(2 * p * r / (p + r) if p + r else 0.0)
    return sum(f1s) / len(f1s) if f1s else 0.0

def score(case: dict, output: dict) -> dict:
    truth_path = TRUTH_DIR / f"{case['id']}.json"
    truth = json.loads(truth_path.read_text())
    claims = {c["id"] for c in case["claims"]}
    rep_claims = {c["id"]: c for c in output.get("claims", []) if c.get("id") in claims}
    pred = {cid: c.get("verdict") for cid, c in rep_claims.items()}

    ev_total = ev_ok = 0
    run_dir = pathlib.Path(output.get("_run_dir", "."))  # local artifacts, if still present
    idx = output.get("_evidence_index")  # portable: {"probes": [...], "text": "<cmds+filenames>"} — makes replay self-contained
    for c in rep_claims.values():
        for e in c.get("evidence", []):
            ev_total += 1
            ref = str(e.get("ref", ""))
            if e.get("kind") in ("file", "command"):
                clog = (run_dir / "commands.log")
                text = idx["text"] if idx else (clog.read_text(errors="replace") if clog.exists() else "")
                probe_hit = re.search(r"\bp-c\d+\b", ref) and re.search(r"\bp-c\d+\b", ref).group(0) in text
                ev_ok += bool(probe_hit or ref in text or (run_dir / ref).exists()
                              or any(run_dir.rglob(pathlib.Path(ref).name)) if ref else False)
            else:
                ev_ok += bool(ref.startswith("http"))
    # Fabrication = evidence asserted but NONE of it resolves to a recorded artifact.
    # Imprecise pointers are penalised through the evidence_valid row, not zeroed by the gate.
    fabricated = ev_total > 0 and ev_ok == 0

    hi_wrong = sum(1 for cid, c in rep_claims.items()
                   if c.get("confidence") == "high" and pred.get(cid) != truth["verdicts"].get(cid))
    rows = {
        "verdict_acc": sum(1 for cid in claims if pred.get(cid) == truth["verdicts"].get(cid)) / max(1, len(claims)),
        "confident_wrong": 1.0 - hi_wrong / max(1, len(claims)),
        "evidence_valid": (ev_ok / ev_total) if ev_total else 0.0,
        "score_error": max(0.0, 1.0 - abs(float(output.get("overall_score", 0)) - truth["reviewer_score"]) / 100.0),
    }
    rows = {k: (v if v == v and v is not None else 0.0) for k, v in rows.items()}  # non-finite -> 0
    gates = {
        "valid_report": bool(rep_claims),
        "no_fabricated_evidence": not fabricated,
    }
    settled = sum(1 for v in pred.values() if v in ("verified", "refuted")) / max(1, len(claims))
    return {"rows": {k: round(min(1.0, max(0.0, v)), 3) for k, v in rows.items()}, "gates": gates,
            "settled_fraction": round(settled, 3)}

SANITY_CASE = (
    {"id": "_sanity", "repo": "x", "commit": "0", "buyer_question": "q",
     "claims": [{"id": "c1", "text": "t", "type": "feature"}, {"id": "c2", "text": "t", "type": "install"}]},
    {"repo": "x", "overall_score": 80,
     "claims": [{"id": "c1", "verdict": "verified", "confidence": "high", "evidence": [{"kind": "url", "ref": "http://x", "excerpt": ""}]},
                {"id": "c2", "verdict": "refuted", "confidence": "low", "evidence": [{"kind": "url", "ref": "http://y", "excerpt": ""}]}],
     "escalations": [], "memo_md": "m"},
    1.0,
)
