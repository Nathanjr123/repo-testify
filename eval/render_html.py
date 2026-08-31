"""Render a single self-contained report.html from proof/build_proof.json (and optionally live runs).
Stdlib only. Everything inline: no server, no CDN, no external files. Opens by double-click via file://.
Usage:
  python3 eval/render_html.py                 -> report.html from the shipped results (the demo view)
  python3 eval/render_html.py --report R.json -> add R.json (a live run) to runs/ and render all of them
A judge can `./run.sh <url>` several repos; every result is saved under runs/ and shown together.
Deterministic body (no timestamps, no absolute paths), so two runs diff clean.
Implementation note: the big HTML block uses .replace() placeholders, not an f-string, so CSS/JS braces need no escaping."""
import html as _html, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROOF = json.loads((ROOT / "proof" / "build_proof.json").read_text())
GH = "https://github.com/Nathanjr123/repo-testify"
esc = lambda x: _html.escape(str(x))


def latest(label):
    xs = [e for e in PROOF if e["label"] == label and not e.get("discarded")]
    return xs[-1] if xs else None


def arm_rows():
    order = [("baseline-v2-n1-rescored", "baseline (reading only)"),
             ("advanced-v2-rescored", "pipeline v2 (public)"),
             ("advanced-v3-ext-rescored", "pipeline v3 (extension)"),
             ("advanced-v3-heldout-rescored", "pipeline v3 (held-out, corrected)"),
             ("advanced-v3-heldout-drafttruth", "pipeline v3 (held-out, draft)"),
             ("ablate-no-execution-rescored", "ablation: no execution")]
    out = []
    for lbl, name in order:
        e = latest(lbl)
        if not e:
            continue
        a = e["agg"]
        acc = a["rows"].get("verdict_acc", 0)
        cap = " <span class='cap'>capped</span>" if a.get("capped") else ""
        n_ok = max(1, sum(1 for r in e.get("per_case",{}).values() if r.get("status")=="ok"))
        cost = ("$%.2f" % (e["cost_usd"]/n_ok)) if e.get("cost_usd") else "&mdash;"
        out.append("<tr><td>%s</td><td class='num'>%.3f</td><td class='num'><b>%.3f</b>%s</td>"
                   "<td class='num'>%.2f</td><td class='num'>%s</td></tr>"
                   % (esc(name), acc, a["raw"], cap, a.get("settled_fraction", 0), cost))
    return "\n".join(out)


def claim_page(report):
    sem = {"verified": "ok", "refuted": "fail", "unverifiable": "warn"}
    order = {"refuted": 0, "unverifiable": 1, "verified": 2}
    rows = []
    for c in sorted(report["claims"], key=lambda c: (order.get(c["verdict"], 3), c["id"])):
        v = c["verdict"]
        k = sem.get(v, "warn")
        ev = "; ".join(esc(str(e.get("excerpt", ""))[:400]) for e in (c.get("evidence") or [])) or "(none)"
        votes = " / ".join(esc(x.get("verdict", "?")) for x in c.get("votes", [])) or "&mdash;"
        opn = "open" if v == "refuted" else ""
        rows.append(
            '<details class="row %s" %s data-v="%s"><summary><span class="tag %s">%s</span> '
            '<span class="cid">%s</span> <span class="conf">%s</span></summary>'
            '<div class="detail"><div class="ev"><b>evidence:</b> %s</div>'
            '<div class="votes">votes: %s</div></div></details>'
            % (k, opn, v, k, esc(v), esc(c["id"]), esc(c.get("confidence", "")), ev, votes))
    nver = sum(c["verdict"] == "verified" for c in report["claims"])
    nref = sum(c["verdict"] == "refuted" for c in report["claims"])
    nesc = len(report.get("escalations", []))
    rid = esc(report.get("run_id", ""))
    head = (
        '<section class="run"><h2>%s</h2>'
        '<div class="summary"><span class="chip muted">%d</span> claims &middot; '
        '<span class="chip ok">%d</span> verified &middot; <span class="chip fail">%d</span> refuted &middot; '
        '<span class="chip warn">%d</span> escalated &middot; score <b>%s/100</b> &middot; '
        '<a href="%s/actions/runs/%s" target="_blank" rel="noopener">CI run %s</a></div>'
        '<div class="controls"><input placeholder="filter claims..." oninput="flt(this)">'
        '<button type="button" data-only="refuted">refuted only</button>'
        '<button type="button" data-only="">all</button></div>'
        % (esc(report["repo"]), len(report["claims"]), nver, nref, nesc, report["overall_score"], GH, rid, rid))
    memo = '<div class="memo"><b>Memo</b><pre>%s</pre></div></section>' % esc(report.get("memo_md", "")[:2500])
    return head + "".join(rows) + memo


CSS = """
body{font:15px/1.5 system-ui,-apple-system,sans-serif;margin:0;background:#0f1115;color:#e6e6e6}
.wrap{max-width:1000px;margin:0 auto;padding:22px}
h1{margin:.2em 0} h2{font-size:16px} a{color:#37c2c4}
.hero{background:#171a21;border:1px solid #262b36;border-radius:10px;padding:16px 18px;margin:12px 0}
.big{font-size:26px;font-weight:800;color:#4bbf6b}
.chip{display:inline-block;min-width:1.4em;text-align:center;border-radius:12px;padding:1px 9px;font-weight:700;margin:0 1px}
.chip.ok,.tag.ok{background:#0f2a1a;color:#4bbf6b} .chip.fail,.tag.fail{background:#2c1418;color:#f0616d}
.chip.warn,.tag.warn{background:#2c2410;color:#e3b341} .chip.muted{background:#232833;color:#9aa4b2}
table{width:100%;border-collapse:collapse;margin:8px 0}
th,td{padding:7px 10px;border-bottom:1px solid #262b36;text-align:left} td.num{text-align:right;font-variant-numeric:tabular-nums}
.cap{font-size:10px;color:#e3b341;text-transform:uppercase;letter-spacing:.04em}
.paste{background:#171a21;border:1px solid #262b36;border-radius:10px;padding:14px 16px;margin:14px 0}
.paste input{background:#0f1115;border:1px solid #333;color:#eee;padding:7px 9px;border-radius:6px;font-family:ui-monospace,monospace;width:min(360px,70%)}
.paste button{background:#37c2c4;color:#001416;border:0;border-radius:6px;padding:7px 12px;font-weight:700;cursor:pointer;margin-left:6px}
.cmd{display:none;font-family:ui-monospace,monospace;background:#0d1017;border:1px solid #262b36;border-radius:6px;padding:9px;margin-top:8px;white-space:pre-wrap;word-break:break-word}
.summary{margin:8px 0} .controls{margin:10px 0}
.controls input{background:#0f1115;border:1px solid #333;color:#eee;padding:6px 8px;border-radius:6px;width:220px;font-family:ui-monospace,monospace}
.controls button{background:#222836;color:#ddd;border:1px solid #333;border-radius:6px;padding:6px 10px;margin-left:6px;cursor:pointer}
details.row{border:1px solid #262b36;border-left:4px solid #444;border-radius:6px;margin:6px 0;padding:6px 10px;background:#141821}
details.row.ok{border-left-color:#2ea043} details.row.fail{border-left-color:#e5534b} details.row.warn{border-left-color:#d4a72c}
summary{cursor:pointer;list-style:none} summary::-webkit-details-marker{display:none}
.tag{padding:1px 8px;border-radius:10px;font-size:12px;font-weight:700;margin-right:6px} .cid{font-weight:700} .conf{color:#9aa4b2;font-size:12px}
.detail{margin-top:8px;font-size:13px} .ev{background:#0d1017;padding:8px;border-radius:5px;white-space:pre-wrap;word-break:break-word} .votes{color:#9aa4b2;margin-top:4px}
.memo pre{background:#0d1017;padding:10px;border-radius:6px;white-space:pre-wrap;overflow:auto}
"""

JS = r"""
function flt(inp){var q=(inp.value||'').toLowerCase();var s=inp.closest('.run');s.querySelectorAll('details.row').forEach(function(d){d.style.display=d.textContent.toLowerCase().indexOf(q)>=0?'':'none';});}
document.addEventListener('click',function(e){var b=e.target.closest('button[data-only]');if(!b)return;var v=b.getAttribute('data-only');b.closest('.run').querySelectorAll('details.row').forEach(function(d){var m=!v||d.dataset.v===v;d.style.display=m?'':'none';if(v&&d.dataset.v===v)d.open=true;});});
function gen(){var v=document.getElementById('repo').value.trim();var o=document.getElementById('cmd');if(!/^https?:\/\/github\.com\//.test(v)){o.style.display='block';o.textContent='Enter a full https://github.com/owner/repo URL.';return;}o.style.display='block';o.textContent='./run.sh '+v;}
"""

TEMPLATE = """<title>repo-testify report</title>
<style>__CSS__</style>
<div class="wrap">
<h1>repo-testify &mdash; audit report</h1>
<div class="hero">The tool executes a repository's README claims in a clean sandbox and returns a verdict per claim with recorded evidence. Reading a README (baseline) settles almost nothing; executing them does.
<div style="margin-top:8px"><span class="big">__BA__ &rarr; __AA__</span> per-claim accuracy, baseline &rarr; pipeline (public split). Every number regenerates from <code>proof/build_proof.json</code>. <a href="__GH__">source</a>.</div></div>
<h2>Arms compared</h2>
<table><tr><th>arm</th><th class="num">claim accuracy</th><th class="num">composite</th><th class="num">settled</th><th class="num">cost/repo</th></tr>
__ARMS__</table>
<div class="paste"><b>Audit your own repositories.</b> Paste a public GitHub URL for the command &mdash; execution runs sandboxed on CI behind an approval gate, never in this browser, and no credentials live in the page.
<div style="margin-top:8px"><input id="repo" placeholder="https://github.com/owner/repo" spellcheck="false"><button type="button" onclick="gen()">command</button></div>
<div class="cmd" id="cmd"></div>
<div style="color:#8a95a6;font-size:12px;margin-top:6px">Each <code>./run.sh</code> you do is saved to <code>runs/</code> and collected on this page &mdash; many repos, one view.</div></div>
<p style="color:#9aa4b2">Reproduce every number: <code>./repro.sh</code>. Run the tool: <code>./run.sh https://github.com/owner/repo</code> or <code>./run.sh --demo</code>.</p>
__LIVE__
</div>
<script>__JS__</script>"""


def main():
    runs_dir = ROOT / "runs"
    runs_dir.mkdir(exist_ok=True)
    if "--report" in sys.argv:
        rp = json.loads(pathlib.Path(sys.argv[sys.argv.index("--report") + 1]).read_text())
        slug = "".join(ch if ch.isalnum() else "-" for ch in rp["repo"].split("github.com/")[-1])[:60]
        (runs_dir / (slug + ".json")).write_text(json.dumps(rp))
    saved = sorted(runs_dir.glob("*.json"))
    if saved:
        live = "".join(claim_page(json.loads(f.read_text())) for f in saved)
    else:
        ex = ROOT / "eval/cases/self/report-run33298981599.json"
        live = claim_page(json.loads(ex.read_text())) if ex.exists() else ""
    b, a = latest("baseline-v2-n1-rescored"), latest("advanced-v2-rescored")
    ba = "%.2f" % (b["agg"]["rows"]["verdict_acc"] if b else 0)
    aa = "%.2f" % (a["agg"]["rows"]["verdict_acc"] if a else 0)
    body = (TEMPLATE.replace("__CSS__", CSS).replace("__JS__", JS).replace("__ARMS__", arm_rows())
            .replace("__LIVE__", live).replace("__BA__", ba).replace("__AA__", aa).replace("__GH__", GH))
    (ROOT / "report.html").write_text(body)
    print("wrote report.html (%d KB, %d run view(s))" % (len(body) // 1024, len(saved) or 1))


if __name__ == "__main__":
    main()
