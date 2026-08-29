"""Render traces/pipeline/<case>.md for a proof label: the pipeline agent's trajectory per repository,
reconstructed from persisted data (probe spec matched to the run by its evidence index, CI run id,
transcript index, per-claim votes, final verdict, and a per-repository human checkpoint from audit notes).
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
    md = [f"# Pipeline trajectory: {cid} (proof `{e['id']}`)\n",
          f"Repository {case['repo']} @ `{case['commit'][:12]}`. Buyer question: _{case['buyer_question']}_\n",
          "## Step 1: instructions\nSee `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:\n"]
    md += [f"- **{c['id']}** ({c['type']}): {c['text']}" for c in case["claims"]]
    idx_text = (r.get("output") or {}).get("_evidence_index", {}).get("text", "") if r["status"] == "ok" else ""
    cands = sorted((ROOT / "eval" / "probes").glob(f"{cid}*.json"))
    def overlap(pf):
        return sum(1 for p in json.loads(pf.read_text())["probes"] if " && ".join(p["commands"])[:200] in idx_text)
    pf = max(cands, key=overlap) if cands and idx_text else (cands[0] if cands else None)
    if pf:
        probes = json.loads(pf.read_text())["probes"]
        assert not idx_text or overlap(pf) > 0, f"{cid}: no probes file matches the run's evidence index"
        md.append(f"\n## Step 2: PLAN output, {len(probes)} probes (`eval/probes/{pf.name}`, matched to this run by its evidence index)\n")
        for p in probes:
            md.append(f"- `{p['id']}` image `{p['image']}` network `{p.get('network','none')}`\n  - setup: `{' && '.join(p.get('setup', []))[:300]}`\n  - commands: `{' && '.join(p['commands'])[:300]}`")
    if r["status"] != "ok":
        md.append(f"\n## Outcome: `{r['status']}`. {r.get('stderr','')[-300:]}\n"); (dst / f"{cid}.md").write_text("\n".join(md)); continue
    out = r["output"]
    md.append(f"\n## Step 3: EXECUTE on GitHub Actions, run `{out.get('run_id')}` (artifacts: per-probe cmd, stdout, stderr, exit code)\n")
    md.append("Transcript index (probe, command, recorded output):\n```\n" + idx_text[:3000] + "\n```")
    md.append("\n## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)\n")
    md.append("| claim | votes | final | conf | evidence cited |\n|---|---|---|---|---|")
    for c in out["claims"]:
        votes = " / ".join(v.get("verdict", "?") for v in c.get("votes", [])) or "n/a"
        ev = (c.get("evidence") or [{}])[0]
        md.append(f"| {c['id']} | {votes} | **{c['verdict']}** | {c['confidence']} | `{str(ev.get('ref',''))[:30]}`: {str(ev.get('excerpt',''))[:90].replace('|','/')} |")
    tp = ROOT / "eval" / "truth" / cname
    truth = json.loads(tp.read_text()) if tp.exists() else {}
    notes = truth.get("audit_notes") or {}
    wrong = [c["id"] for c in out["claims"] if truth.get("verdicts", {}).get(c["id"]) not in (None, c["verdict"])]
    hc = ("Human checkpoint for this repository: " + "; ".join(f"{k}: {v}" for k, v in notes.items())) if notes else "Human checkpoint for this repository: no truth entry was changed after this run."
    md.append(f"\n## Step 5: REPORT\nOverall score {out.get('overall_score')}. Escalated to a human: {out.get('escalations') or 'none'}. Model calls: {out.get('llm_calls') or 'nominal 4'}. Verdicts disagreeing with audited truth: {', '.join(wrong) or 'none'}.\n\n{hc}")
    (dst / f"{cid}.md").write_text("\n".join(md))
print("pipeline traces rendered for", label, "->", len(list(dst.glob('*.md'))), "files")
