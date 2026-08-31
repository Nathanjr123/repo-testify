"""Render traces/single_shot/<case>.md for the single-shot baseline arm: the agent-vs-agent
trajectory per repository, reconstructed from persisted proof data (the one bash script the agent
wrote, the recorded per-claim output, and its single adjudication). No model calls; deterministic.
Mirrors tools/render_pipeline_traces.py so both arms have follow-able trajectories."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
label = sys.argv[1] if len(sys.argv) > 1 else "single-shot-baseline"
proof = json.loads((ROOT / "proof" / "build_proof.json").read_text())
e = [x for x in proof if x["label"] == label][-1]
dst = ROOT / "traces" / "single_shot"; dst.mkdir(parents=True, exist_ok=True)
for cname, r in e["per_case"].items():
    cid = cname[:-5]
    case = json.loads(next(ROOT.glob(f"eval/cases/*/{cname}")).read_text())
    md = [f"# Single-shot trajectory: {cid} (proof `{e['id']}`)\n",
          f"Repository {case['repo']} @ `{case['commit'][:12]}`. Buyer question: _{case.get('buyer_question','')}_\n",
          "This is the **fair execution baseline** (arms/single_shot): one agent is handed the repository and all "
          "the claims, writes **one** bash script, runs it **once** in the same sandbox, and returns **one** judgment. "
          "It can run code, but it has none of the pipeline's structure (one probe per claim, VERDICT_LINE contract, "
          "per-claim adjudication, escalation). This trace exists to make that contrast follow-able.\n",
          "## Step 1: instructions\nSee `arms/PROMPTS.md` (single-shot arm). Claims given to the agent:\n"]
    md += [f"- **{c['id']}** ({c['type']}): {c['text']}" for c in case["claims"]]
    if r["status"] != "ok":
        md.append(f"\n## Outcome: `{r['status']}`. {str(r.get('stderr',''))[-300:]}\n")
        (dst / f"{cid}.md").write_text("\n".join(md)); continue
    out = r["output"]
    idx = (out.get("_evidence_index") or {}).get("text", "")
    # the evidence text is "ss <script...>"; strip the probe-id prefix to show the script the agent wrote
    script = idx[3:] if idx.startswith("ss ") else idx
    md.append("\n## Step 2: the ONE script the agent wrote (executed once, in the sandbox)\n")
    md.append("```bash\n" + script[:6000] + ("\n... (truncated)" if len(script) > 6000 else "") + "\n```")
    md.append("\n## Step 3: the ONE judgment (all claims adjudicated together, from that single run)\n")
    md.append("| claim | verdict | conf | evidence excerpt |\n|---|---|---|---|")
    for c in out["claims"]:
        ev = (c.get("evidence") or [{}])[0]
        md.append(f"| {c['id']} | **{c['verdict']}** | {c.get('confidence','')} | {str(ev.get('excerpt',''))[:110].replace('|','/')} |")
    nver = sum(x["verdict"] == "verified" for x in out["claims"])
    nref = sum(x["verdict"] == "refuted" for x in out["claims"])
    nesc = sum(x["verdict"] == "unverifiable" for x in out["claims"])
    acc = r["rows"]["verdict_acc"]
    md.append(f"\n## Step 4: outcome\n{nver} verified, {nref} refuted, {nesc} unverifiable/escalated. "
              f"Verdict accuracy vs audited truth: **{acc:.2f}**. "
              "Contrast with the pipeline trajectory for the same repository in `traces/pipeline/` — where a single "
              "monolithic script stalls or mis-handles one claim, every downstream claim inherits the failure, which "
              "is the structural weakness the per-claim pipeline removes.\n")
    (dst / f"{cid}.md").write_text("\n".join(md))
print(f"single-shot traces rendered for {label} -> {len(list(dst.glob('*.md')))} files")
