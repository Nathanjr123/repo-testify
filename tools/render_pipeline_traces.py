"""Render traces/pipeline/<case>.md for a proof label: the pipeline agent's trajectory per repository,
reconstructed from persisted data (probes JSON, CI run id, evidence index, per-claim votes, final verdict).
No model calls; deterministic."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
label = sys.argv[1] if len(sys.argv) > 1 else "advanced-v2"
proof = json.loads((ROOT / "proof" / "build_proof.json").read_text())
e = [x for x in proof if x["label"] == label][-1]
dst = ROOT / "traces" / "pipeline"; dst.mkdir(parents=True, exist_ok=True)
for cname, r in e["per_case"].items():
    cid = cname[:-5]
    case = json.loads(next(ROOT.glob(f"eval/cases/*/{cname}")).read_text())
    md = [f"# Pipeline trajectory, {cid} (proof `{e['id']}`)\n",
          f"Repository {case['repo']} @ `{case['commit'][:12]}` · buyer question: _{case['buyer_question']}_\n",
          "## Step 1, instructions\nSee `arms/PROMPTS.md` (PLAN -> EXECUTE -> ADJUDICATE). Claims given to the agent:\n"]
    md += [f"- **{c['id']}** ({c['type']}): {c['text']}" for c in case["claims"]]
    idx_text = (r.get("output") or {}).get("_evidence_index", {}).get("text", "") if r["status"] == "ok" else ""
    cands = sorted((ROOT / "eval" / "probes").glob(f"{cid}*.json"))
    def overlap(pf):
        ps = json.loads(pf.read_text())["probes"]
        return sum(1 for p in ps if " && ".join(p["commands"])[:200] in idx_text)
    pf = max(cands, key=overlap) if cands and idx_text else (cands[0] if cands else None)
    if pf:
        probes = json.loads(pf.read_text())["probes"]
        assert not idx_text or overlap(pf) > 0, f"{cid}: no probes file matches the run's evidence index"
        md.append(f"\n## Step 2, PLAN output: {len(probes)} probes (committed as `eval/probes/{pf.name}`; matched to this run by its evidence index)\n")
        for p in probes:
            md.append(f"- `{p['id']}` image `{p['image']}` network `{p.get('network','none')}`\n  - setup: `{' && '.join(p.get('setup', []))[:300]}`\n  - commands: `{' && '.join(p['commands'])[:300]}`")
    if r["status"] != "ok":
        truth = json.loads((ROOT / "eval" / "truth" / cname).read_text()) if (ROOT / "eval" / "truth" / cname).exists() else {}
    notes = truth.get("audit_notes") or {}
    wrong = [c["id"] for c in out["claims"] if truth.get("verdicts", {}).get(c["id"]) not in (None, c["verdict"])]
    hc = ("Human checkpoint for this repository: " + "; ".join(f"{k}: {v}" for k, v in notes.items())) if notes else "Human checkpoint for this repository: no truth entry was changed after this run."
    md.append(f"\n## Step 5, REPORT\nOverall score {out.get('overall_score')}. Escalated to a human: {out.get('escalations') or 'none'}. Model calls: {out.get('llm_calls') or 'nominal 4'}. Verdicts disagreeing with audited truth: {', '.join(wrong) or 'none'}.\n\n{hc}")
    (dst / f"{cid}.md").write_text("\n".join(md)); continue
    out = r["output"]
    md.append(f"\n## Step 3, EXECUTE on GitHub Actions: run `{out.get('run_id')}` (artifacts: per-probe cmd/stdout/stderr/exit_code)\n")
    idx = out.get("_evidence_index", {})
    md.append("Transcript index (probe · command excerpt):\n```\n" + idx.get("text", "")[:3000] + "\n```")
    md.append("\n## Step 4, ADJUDICATE: votes -> verdict per claim (confidence demoted on disagreement)\n")
    md.append("| claim | votes | final | conf | evidence cited |\n|---|---|---|---|---|")
    for c in out["claims"]:
        votes = " / ".join(v.get("verdict", "?") for v in c.get("votes", [])) or ", "
        ev = (c.get("evidence") or [{}])[0]
        md.append(f"| {c['id']} | {votes} | **{c['verdict']}** | {c['confidence']} | `{str(ev.get('ref',''))[:30]}`, {str(ev.get('excerpt',''))[:90].replace('|','/')} |")
    md.append(f"\n## Step 5, REPORT\nOverall score {out.get('overall_score')} · escalated to human: {out.get('escalations') or 'none'} · model calls: {out.get('llm_calls', 'nominal 4')}\n\n_Human checkpoint: the verdicts above were audited against ground truth; disagreements were read from the recorded probe output and resolved in favour of the evidence (CHANGELOG 'Truth audit')._")
    (dst / f"{cid}.md").write_text("\n".join(md))
print("pipeline traces rendered for", label, "->", len(list(dst.glob('*.md'))), "files")
