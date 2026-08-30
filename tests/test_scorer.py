"""Scorer contract tests. Run: python3 -m pytest -q tests/  (or: python3 tests/test_scorer.py)"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from eval.scorer import score, SETTLED_CAP
from eval.aggregate import aggregate, tail

CASE = {"id": "_sanity", "repo": "x", "commit": "0", "buyer_question": "q",
        "claims": [{"id": "c1", "text": "t", "type": "feature"}, {"id": "c2", "text": "t", "type": "install"}]}
def rep(v1, v2, conf="high", ev=True):
    e = [{"kind": "url", "ref": "http://x", "excerpt": ""}] if ev else []
    return {"repo": "x", "overall_score": 80, "claims": [{"id": "c1", "verdict": v1, "confidence": conf, "evidence": e},
                                                         {"id": "c2", "verdict": v2, "confidence": conf, "evidence": e}], "escalations": [],
            "_evidence_index": {"probes": [], "text": "", "tree": "", "readme_urls": "http://x"}}
def test_perfect(): assert aggregate([score(CASE, rep("verified", "refuted"))])["raw"] == 1.0
def test_wrong_high_confidence_is_penalised():
    s = score(CASE, rep("refuted", "verified"))
    assert s["rows"]["verdict_acc"] == 0.0 and s["rows"]["confident_wrong"] == 0.0
def test_abstain_everything_is_capped():
    a = aggregate([score(CASE, rep("unverifiable", "unverifiable", conf="low"))])
    assert a["capped"] and a["raw"] <= SETTLED_CAP
def test_fabricated_evidence_gate():
    r = rep("verified", "refuted"); r["claims"][0]["evidence"] = [{"kind": "file", "ref": "nope.log", "excerpt": ""}]; r["claims"][1]["evidence"] = [{"kind": "command", "ref": "p-c9", "excerpt": ""}]
    s = score(CASE, r); assert s["gates"]["no_fabricated_evidence"] is False
def test_tail_weights_worst_case(): assert abs(tail([1.0, 0.0]) - (0.55*0.5 + 0.30*0.0 + 0.15*0.0)) < 1e-9
def test_crashed_case_is_zero_not_hidden():
    from eval.scorer import WEIGHTS
    zero = {"rows": {k: 0.0 for k in WEIGHTS}, "gates": {"valid_report": False, "no_fabricated_evidence": True}}
    assert aggregate([score(CASE, rep("verified", "refuted")), zero])["raw"] < 1.0

def test_url_evidence_must_be_in_recorded_context():
    r = rep("verified", "refuted"); r["_evidence_index"]["readme_urls"] = ""
    assert score(CASE, r)["rows"]["evidence_valid"] == 0.0

if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"): f(); print("ok", n)
