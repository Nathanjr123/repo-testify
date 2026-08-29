"""Inject generated result tables into README.md between <!-- RESULTS:START --> / <!-- RESULTS:END -->."""
import json, pathlib, re, statistics as st
ROOT = pathlib.Path(__file__).resolve().parent.parent
proof = [e for e in json.loads((ROOT / "proof" / "build_proof.json").read_text()) if not e.get("discarded") and not e.get("partial")]
latest = {}
for e in proof: latest[e["label"]] = e
def row(label, name):
    e = latest.get(label)
    if not e: return None
    a = e["agg"]; acc = a["rows"]["verdict_acc"]
    ok = [r for r in e["per_case"].values() if r.get("status") == "ok"]
    nominal = {"baseline": 1, "advanced": 4}.get(e["arm"], "n/a")
    if e.get("disable") == "execution": nominal = 3
    calls = e.get("llm_calls") or f"{nominal}*"
    cost = e.get("cost_usd") or 0
    if cost: calls = f"{calls}, ${cost/max(1,len(ok)):.2f}"
    human = e.get("human_min_per_repo") or "pending audit"
    return f"| {name} | {acc:.3f} | {a['rows']['confident_wrong']:.3f} | {a['rows']['evidence_valid']:.3f} | {a['rows']['score_error']:.3f} | {a.get('settled_fraction', 0):.2f} | **{a['raw']:.3f}**{' (capped)' if a.get('capped') else ''} | {calls} | {e['wall_total_s']/max(1,len(e['per_case']))/60:.1f} min | {human} | {len(ok)}/{len(e['per_case'])} |"
hdr = "| arm | claim accuracy (worst-case weighted) | not confidently wrong | evidence valid | score agreement | settled | composite | model calls/repo (cost) | wall/repo | human min/repo | cases ok |\n|---|---|---|---|---|---|---|---|---|---|---|"
rows = [row("baseline-v2-n1-rescored", "baseline (run 1)"), row("baseline-v2-n2-rescored", "baseline (run 2)"),
        row("advanced-v1-rescored", "pipeline v1"), row("advanced-v2-rescored", "pipeline v2 (public, tuned)"),
        row("ablate-k1", "ablation: k=1 votes"), row("ablate-no-execution-rescored", "ablation: no execution"),
        row("baseline-ext2-rescored", "baseline (extension, 6 repos, v3 code)"), row("advanced-v3-ext-rescored", "pipeline v3 (extension, 6 repos)"),
        row("baseline-heldout", "baseline (held-out, run once; provisional truth, audit pending)"), row("advanced-v3-heldout", "pipeline v3 (held-out, run once; provisional truth, audit pending)")]
b = [latest[l]["agg"]["raw"] for l in ("baseline-v2-n1-rescored", "baseline-v2-n2-rescored") if l in latest]
floor = f"Baseline-vs-baseline spread (noise floor): **{max(b)-min(b):.3f}** composite; claim-accuracy spread {abs(latest['baseline-v2-n1-rescored']['agg']['rows']['verdict_acc']-latest['baseline-v2-n2-rescored']['agg']['rows']['verdict_acc']):.3f}." if len(b) == 2 else ""
b1, adv = latest.get("baseline-v2-n1-rescored"), latest.get("advanced-v2-rescored")
import math
def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k / n; d = 1 + z*z/n; c = (p + z*z/(2*n)) / d; h = z * math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (max(0.0, c - h), min(1.0, c + h))
def claim_counts(e):
    k = n = 0
    for cname, r in e["per_case"].items():
        if r.get("status") != "ok": continue
        case = json.loads(next(ROOT.glob(f"eval/cases/*/{cname}")).read_text())
        truth = json.loads((ROOT / "eval/truth" / cname).read_text())["verdicts"]
        pred = {c["id"]: c["verdict"] for c in r["output"]["claims"]}
        for c in case["claims"]:
            n += 1; k += pred.get(c["id"]) == truth.get(c["id"])
    return k, n
def pdf_table():
    if not (b1 and adv): return ""
    ba, aa = b1["agg"]["rows"]["verdict_acc"], adv["agg"]["rows"]["verdict_acc"]
    bw, aw = b1["wall_total_s"]/max(1,len(b1["per_case"]))/60, adv["wall_total_s"]/max(1,len(adv["per_case"]))/60
    hm = adv.get("human_min_per_repo") or "pending audit"
    kb, nb = claim_counts(b1); ka, na = claim_counts(adv); lb, ub = wilson(kb, nb); la, ua = wilson(ka, na)
    ext_line = ""
    bx, ax = latest.get("baseline-ext2-rescored"), latest.get("advanced-v3-ext-rescored")
    if bx and ax:
        kb2, nb2 = claim_counts(bx); ka2, na2 = claim_counts(ax)
        lo_b, hi_b = wilson(kb + kb2, nb + nb2); lo_a, hi_a = wilson(ka + ka2, na + na2)
        ext_line = (f"| Same, public + extension (13 repositories, {nb+nb2} claims) | {(kb+kb2)/(nb+nb2):.2f} ({kb+kb2}/{nb+nb2}; {lo_b:.2f} to {hi_b:.2f}) | {(ka+ka2)/(na+na2):.2f} ({ka+ka2}/{na+na2}; {lo_a:.2f} to {hi_a:.2f}) | +{(ka+ka2)/(na+na2)-(kb+kb2)/(nb+nb2):.2f} |\n")
    return ("The format the challenge asks for, public split:\n\n| Metric | Simple baseline | Agent solution | Change |\n|---|---|---|---|\n"
            f"| Primary outcome: per-claim accuracy, 95% Wilson interval | {kb/nb:.2f} ({kb}/{nb}; {lb:.2f} to {ub:.2f}) | {ka/na:.2f} ({ka}/{na}; {la:.2f} to {ua:.2f}) | +{ka/na-kb/nb:.2f}; intervals do not overlap |\n"
            f"| Same metric, worst-case weighted per repository (0.55 mean, 0.30 worst 30%, 0.15 worst) | {ba:.2f} | {aa:.2f} | +{aa-ba:.2f} |\n" + ext_line +
            f"| Composite score (published rubric) | {b1['agg']['raw']:.3f} | {adv['agg']['raw']:.3f} | +{adv['agg']['raw']-b1['agg']['raw']:.3f} |\n"
            f"| Human time per task | {hm} (manual audit datum) | {aw:.1f} min unattended wall time | see held-out rows |\n"
            f"| Cost per task | 1 model call, {bw:.1f} min | 4 model calls (nominal), {aw:.1f} min | +3 calls |\n\n")
block = "<!-- RESULTS:START -->\n_Generated by `python3 eval/render_readme.py` from proof/build_proof.json. Public split: 7 repositories, 75 claims._\n\n" + pdf_table() + "Full table:\n\n" + hdr + "\n" + "\n".join(r for r in rows if r) + "\n\n" + floor + "\n\n\\* nominal call count per repository (plan, at most one repair, three votes; baseline 1). Exact counts are persisted for runs from v3 onward.\n<!-- RESULTS:END -->"
p = ROOT / "README.md"; t = p.read_text()
if "<!-- RESULTS:START -->" in t:
    t = re.sub(r"<!-- RESULTS:START -->.*?<!-- RESULTS:END -->", block, t, flags=re.S)
else:
    t = t.replace("## Measured improvement\n", "## Measured improvement\n" + block + "\n")
p.write_text(t); print("README results block rendered")
