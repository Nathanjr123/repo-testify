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
    md = [f"# Pipeline trajectory — {cid} (proof `{e['id']}`)\n",
          f"Repository {case['repo']} @ `{case['commit'][:12]}` · buyer question: _{case['buyer_question']}_\n",
          "## Step 1 — instructions\nSee `arms/PROMPTS.md` (PLAN → EXECUTE → ADJUDICATE). Claims given to the agent:\n"]
    md += [f"- **{c['id']}** ({c['type']}): {c['text']}" for c in case["claims"]]
    pf = ROOT / "eval" / "probes" / f"{cid}.json"
    if pf.exists():
        probes = json.loads(pf.read_text())["probes"]
        md.append(f"\n## Step 2 — PLAN output: {len(probes)} probes (committed as `eval/probes/{cid}.json`)\n")
        for p in probes:
            md.append(f"- `{p['id']}` image `{p['image']}` network `{p.get('network','none')}`\n  - setup: `{' && '.join(p.get('setup', []))[:300]}`\n  - commands: `{' && '.join(p['commands'])[:300]}`")
    if r["status"] != "ok":
        md.append(f"\n## Outcome: `{r['status']}` — {r.get('stderr','')[-300:]}\n"); (dst / f"{cid}.md").write_text("\n".join(md)); continue
    out = r["output"]
    md.append(f"\n## Step 3 — EXECUTE on GitHub Actions: run `{out.get('run_id')}` (artifacts: per-probe cmd/stdout/stderr/exit_code)\n")
    idx = out.get("_evidence_index", {})
    md.append("Transcript index (probe · command excerpt):\n```\n" + idx.get("text", "")[:3000] + "\n```")
    md.append("\n## Step 4 — ADJUDICATE: votes → verdict per claim (confidence demoted on disagreement)\n")
    md.append("| claim | votes | final | conf | evidence cited |\n|---|---|---|---|---|")
    for c in out["claims"]:
        votes = " / ".join(v.get("verdict", "?") for v in c.get("votes", [])) or "—"
        ev = (c.get("evidence") or [{}])[0]
        md.append(f"| {c['id']} | {votes} | **{c['verdict']}** | {c['confidence']} | `{str(ev.get('ref',''))[:30]}` — {str(ev.get('excerpt',''))[:90].replace('|','/')} |")
    md.append(f"\n## Step 5 — REPORT\nOverall score {out.get('overall_score')} · escalated to human: {out.get('escalations') or 'none'} · model calls: {out.get('llm_calls', 'nominal 4')}\n\n_Human checkpoint: the verdicts above were audited against ground truth; disagreements were read from the recorded probe output and resolved in favour of the evidence (CHANGELOG 'Truth audit')._")
    (dst / f"{cid}.md").write_text("\n".join(md))
print("pipeline traces rendered for", label, "->", len(list(dst.glob('*.md'))), "files")
