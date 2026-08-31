"""Render a single self-contained report.html from proof/build_proof.json (and optionally one report.json).
Stdlib only. Everything inline: no server, no CDN, no external files. Opens by double-click via file://.
Usage:
  python3 eval/render_html.py                 -> report.html from the shipped results (the demo view)
  python3 eval/render_html.py --report R.json -> add a live run's per-claim page from R.json
Deterministic: no timestamps or absolute paths in the body, keys sorted, so two runs diff clean."""
import html, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
PROOF = json.loads((ROOT / "proof" / "build_proof.json").read_text())
GH = "https://github.com/Nathanjr123/repo-testify"

def esc(x): return html.escape(str(x))
def chip(n, kind): return f'<span class="chip {kind}">{n}</span>'

def latest(label):
    xs = [e for e in PROOF if e["label"] == label and not e.get("discarded")]
    return xs[-1] if xs else None

def arm_rows():
    order = [("baseline-v2-n1-rescored","baseline (reading only)"),("advanced-v2-rescored","pipeline v2 (public)"),
             ("advanced-v3-ext-rescored","pipeline v3 (extension)"),("advanced-v3-heldout-rescored","pipeline v3 (held-out, corrected truth)"),
             ("advanced-v3-heldout-drafttruth","pipeline v3 (held-out, draft truth)"),("ablate-no-execution-rescored","ablation: no execution")]
    out = []
    for lbl, name in order:
        e = latest(lbl)
        if not e: continue
        a = e["agg"]; acc = a["rows"].get("verdict_acc", 0)
        out.append(f"<tr><td>{esc(name)}</td><td class='num'>{acc:.3f}</td><td class='num'><b>{a['raw']:.3f}</b>{' (capped)' if a.get('capped') else ''}</td>"
                   f"<td class='num'>{a.get('settled_fraction',0):.2f}</td><td class='num'>{e.get('cost_usd') or '—'}</td></tr>")
    return "\n".join(out)

def claim_page(report):
    r = report; rows = []
    for c in sorted(r["claims"], key=lambda c: c["id"]):
        v = c["verdict"]; kind = {"verified":"ok","refuted":"fail","unverifiable":"warn"}.get(v,"warn")
        ev = "; ".join(esc(str(e.get("excerpt",""))[:400]) for e in (c.get("evidence") or []))
        votes = " / ".join(esc(x.get("verdict","?")) for x in c.get("votes",[])) or "—"
        openattr = "open" if v in ("refuted",) else ""
        rows.append(f"""<details class="row {kind}" {openattr} data-v="{v}">
<summary><span class="tag {kind}">{esc(v)}</span> <span class="cid">{esc(c['id'])}</span> <span class="conf">{esc(c.get('confidence',''))}</span></summary>
<div class="detail"><div class="ev"><b>evidence:</b> {ev or '(none)'}</div><div class="votes">votes: {votes}</div></div></details>""")
    nver = sum(c["verdict"]=="verified" for c in r["claims"]); nref = sum(c["verdict"]=="refuted" for c in r["claims"]); nesc = len(r.get("escalations",[]))
    return f"""<section class="run"><h2>Live run: {esc(r['repo'])}</h2>
<div class="summary">{chip(len(r['claims']),'muted')} claims · {chip(nver,'ok')} verified · {chip(nref,'fail')} refuted · {chip(nesc,'warn')} escalated · score <b>{r['overall_score']}/100</b>
· <a href="{GH}/actions/runs/{esc(r.get('run_id',''))}" target="_blank">CI run {esc(r.get('run_id',''))}</a></div>
<div class="controls"><input id="q" placeholder="filter claims..." oninput="flt()"><button onclick="only('refuted')">refuted only</button><button onclick="only('')">all</button></div>
{''.join(rows)}
<div class="memo"><b>Memo</b><pre>{esc(r.get('memo_md','')[:2500])}</pre></div></section>"""

def main():
    runs_dir = ROOT / "runs"; runs_dir.mkdir(exist_ok=True)
    if "--report" in sys.argv:
        rp = json.loads(pathlib.Path(sys.argv[sys.argv.index("--report")+1]).read_text())
        slug = "".join(ch if ch.isalnum() else "-" for ch in rp["repo"].split("github.com/")[-1])[:60]
        (runs_dir / f"{slug}.json").write_text(json.dumps(rp))  # accumulate every audited repo
    saved = sorted(runs_dir.glob("*.json"))
    if saved:
        live = "".join(claim_page(json.loads(f.read_text())) for f in saved)
    else:
        ex = ROOT / "eval/cases/self/report-run33298981599.json"
        live = claim_page(json.loads(ex.read_text())) if ex.exists() else ""
    b = latest("baseline-v2-n1-rescored"); a = latest("advanced-v2-rescored")
    ba = b["agg"]["rows"]["verdict_acc"] if b else 0; aa = a["agg"]["rows"]["verdict_acc"] if a else 0
    page = f"""<!doctype html><html><head><meta charset=utf-8><title>repo-testify report</title>
<style>
body{{font:15px/1.5 system-ui,sans-serif;margin:0;background:#0f1115;color:#e6e6e6}}
.wrap{{max-width:1000px;margin:0 auto;padding:20px}}
h1{{margin:.2em 0}} a{{color:#6ea8fe}}
.hero{{background:#171a21;border:1px solid #262b36;border-radius:10px;padding:16px 18px;margin:12px 0}}
.chip{{display:inline-block;min-width:1.6em;text-align:center;border-radius:12px;padding:1px 9px;font-weight:700;margin:0 2px}}
.ok{{background:#12331d;color:#57d977;border-color:#1c5c31}} .fail{{background:#3a1618;color:#ff7b7b}} .warn{{background:#3a3313;color:#e8c95a}} .muted{{background:#232833;color:#9aa4b2}}
table{{width:100%;border-collapse:collapse;margin:8px 0}} th,td{{padding:7px 10px;border-bottom:1px solid #262b36;text-align:left}} td.num{{text-align:right;font-variant-numeric:tabular-nums}}
.summary{{margin:8px 0}} .controls{{margin:10px 0}} .controls input{{background:#0f1115;border:1px solid #333;color:#eee;padding:6px 8px;border-radius:6px;width:220px}} .controls button{{background:#222836;color:#ddd;border:1px solid #333;border-radius:6px;padding:6px 10px;margin-left:6px;cursor:pointer}}
details.row{{border:1px solid #262b36;border-left:4px solid #444;border-radius:6px;margin:6px 0;padding:6px 10px;background:#141821}}
details.row.ok{{border-left-color:#2ea043}} details.row.fail{{border-left-color:#e5534b}} details.row.warn{{border-left-color:#d4a72c}}
summary{{cursor:pointer}} .tag{{padding:1px 8px;border-radius:10px;font-size:12px;font-weight:700;margin-right:6px}} .cid{{font-weight:700}} .conf{{color:#9aa4b2;font-size:12px}}
.detail{{margin-top:8px;font-size:13px}} .ev{{background:#0d1017;padding:8px;border-radius:5px;white-space:pre-wrap;word-break:break-word}} .votes{{color:#9aa4b2;margin-top:4px}}
.memo pre{{background:#0d1017;padding:10px;border-radius:6px;white-space:pre-wrap;overflow:auto}}
.big{{font-size:26px;font-weight:800}}
</style></head><body><div class=wrap>
<h1>repo-testify — audit report</h1>
<div class=hero>The tool executes a repository's README claims in a clean sandbox and returns a verdict per claim with recorded evidence.
Reading a README (baseline) settles almost nothing; executing the claims does. <span class=big>{ba:.2f} → {aa:.2f}</span> per-claim accuracy, baseline → pipeline (public split).
Full numbers regenerate from <code>proof/build_proof.json</code>; this page is a view of them. <a href="{GH}">source</a>.</div>
<h2>Arms compared</h2>
<table><tr><th>arm</th><th class=num>claim accuracy</th><th class=num>composite</th><th class=num>settled</th><th class=num>cost/repo</th></tr>
{arm_rows()}</table>
<div class="paste"><b>Audit your own repositories</b> — paste a public GitHub URL for the command (execution runs sandboxed on CI, not in the browser):
<div style="display:flex;gap:8px;margin-top:8px"><input id="repo" placeholder="https://github.com/owner/repo" style="flex:1;background:#0f1115;border:1px solid #333;color:#eee;padding:7px 9px;border-radius:6px;font-family:monospace">
<button onclick="gen()" style="background:#37c2c4;color:#001416;border:0;border-radius:6px;padding:7px 12px;font-weight:700;cursor:pointer">command</button></div>
<div id="cmd" style="display:none;font-family:monospace;background:#0d1017;border:1px solid #262b36;border-radius:6px;padding:9px;margin-top:8px;white-space:pre-wrap;word-break:break-word"></div>
<div style="color:#8a95a6;font-size:12px;margin-top:6px">Each run you do is collected on this page — many repos, one view.</div></div>
<p style="color:#9aa4b2">Reproduce every number: <code>./repro.sh</code>. Run it yourself: <code>./run.sh https://github.com/owner/repo</code> or <code>./run.sh --demo</code>.</p>
{live}
</div>
<script>
function gen(){{var v=document.getElementById('repo').value.trim();var o=document.getElementById('cmd');if(!/^https?:\/\/github\.com\//.test(v)){{o.style.display='block';o.textContent='Enter a full https://github.com/owner/repo URL.';return}}o.style.display='block';o.textContent='./run.sh '+v;}}
function flt(){{{let q=document.getElementById('q').value.toLowerCase();document.querySelectorAll('details.row').forEach(d=>{{d.style.display=d.textContent.toLowerCase().includes(q)?'':'none'}})}}
function only(v){{document.querySelectorAll('details.row').forEach(d=>{{d.style.display=(!v||d.dataset.v===v)?'':'none';if(v&&d.dataset.v===v)d.open=true}})}}
</script></body></html>"""
    (ROOT / "report.html").write_text(page)
    print(f"wrote report.html ({len(page)//1024} KB)")

if __name__ == "__main__":
    main()
