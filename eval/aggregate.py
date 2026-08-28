# PROVENANCE — read before modifying.
# Written during the competition (2026-08-28/31) by Claude Code (claude-fable-5) under Nathan Obiekwe's
# direction; every design decision it encodes is recorded in DESIGN.md / DECISIONS.md / CHANGELOG.md, and the
# session trajectory that produced it is in traces/. Pre-existing before kickoff: only the problem-agnostic
# skeleton (Makefile targets, eval/ layout, trace exporter). Human review: Nathan audits truth files and results.
"""ONE aggregate function. The grader, the report and replay all call THIS (never a copy)."""
from .scorer import WEIGHTS, SETTLED_MIN, SETTLED_CAP

def tail(vals):
    if not vals:
        return 0.0
    s = sorted(vals)
    k = max(1, round(0.3 * len(s)))
    return 0.55 * (sum(s) / len(s)) + 0.30 * (sum(s[:k]) / k) + 0.15 * s[0]

def aggregate(per_case: list[dict]) -> dict:
    rows = {}
    for name in WEIGHTS:
        rows[name] = round(tail([c["rows"].get(name, 0.0) for c in per_case]), 3)
    gate_names = sorted({g for c in per_case for g in c.get("gates", {})})
    gates = {g: sum(1 for c in per_case if c["gates"].get(g, False)) / len(per_case)
             for g in gate_names} if per_case else {}
    raw = sum(WEIGHTS[n] * rows[n] for n in WEIGHTS)
    for g, frac in gates.items():
        raw *= frac
    settled = sum(c.get("settled_fraction", 0.0) for c in per_case) / len(per_case) if per_case else 0.0
    capped = settled < SETTLED_MIN and raw > SETTLED_CAP
    if capped:
        raw = SETTLED_CAP
    return {"rows": rows, "gates": gates, "raw": round(raw, 3), "n_cases": len(per_case),
            "settled_fraction": round(settled, 3), "capped": capped}
