"""THE PROPOSED RUBRIC (PDF p4: "design your own clear scoring rubric and propose it").
score(case, output) -> {"rows": {name: float in [0,1]}, "gates": {name: bool}}
Rows ADD (weighted, each weight <= 0.35 here), gates MULTIPLY (award nothing, only remove).
FRIDAY FILL: the row bodies. Measure row distributions before banding (law 5).
"""
WEIGHTS = {  # fill Friday; keep 3-6 rows, none dominant
    # "primary": 0.35, "secondary": 0.25, ...
}
BANDS = {  # row -> (full_credit_edge, zero_credit_edge); direction-agnostic
}

def band(x, full, zero):
    if x is None:
        return 0.0  # missing measurement clamps to the zero edge (never a sentinel)
    lo, hi = (full, zero) if full < zero else (zero, full)
    t = (x - full) / (zero - full) if zero != full else 0.0
    return max(0.0, min(1.0, 1.0 - t))

def score(case: dict, output: dict) -> dict:
    """FRIDAY FILL. Must be deterministic. Non-finite -> 0. No-op outputs must not score."""
    raise NotImplementedError("write me first, before any solution code")

SANITY_CASE = None   # FRIDAY FILL: (case, output, expected_agg) — law 2
