# PROVENANCE — read before modifying.
# Written during the competition (2026-08-28/31) by Claude Code (claude-fable-5) under Nathan Obiekwe's
# direction; every design decision it encodes is recorded in DESIGN.md / DECISIONS.md / CHANGELOG.md, and the
# session trajectory that produced it is in traces/. Pre-existing before kickoff: only the problem-agnostic
# skeleton (Makefile targets, eval/ layout, trace exporter). Human review: Nathan audits truth files and results.
"""Baseline arm: fetch README + tree via GitHub API (no clone — local disk is tight),
one claude -p call, emit the report schema. This is the honest 'reasonable basic way':
what an engineer does today = read the README and skim the tree, then judge."""
import json, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common import llm, exit_if_limited

case = json.loads(pathlib.Path(sys.argv[1]).read_text())
owner_repo = case["repo"].split("github.com/")[-1].strip("/")

def gh(path):
    return subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60)

readme = gh(f"repos/{owner_repo}/readme?ref={case['commit']}")
import base64
readme_text = base64.b64decode(json.loads(readme.stdout)["content"]).decode(errors="replace") if readme.returncode == 0 else "(no README)"
tree = gh(f"repos/{owner_repo}/git/trees/{case['commit']}?recursive=1")
paths = [e["path"] for e in json.loads(tree.stdout).get("tree", [])][:400] if tree.returncode == 0 else []

claims = json.dumps(case["claims"], indent=1)
prompt = f"""You are doing technical due diligence on a repository for a buyer, from documentation alone.
Buyer question: {case['buyer_question']}
Repository: {case['repo']} at commit {case['commit']}
You may NOT run anything. Judge only from the README and file tree below.
For EVERY claim in this list, give verdict "verified" | "refuted" | "unverifiable" (use unverifiable when reading alone cannot settle it — do not guess), confidence "high"|"low", and evidence (kind "file" = a path from the tree, kind "url" = a link).
Claims: {claims}
README:\n{readme_text[:30000]}\nFile tree (first 400): {json.dumps(paths)}
Reply with ONLY a JSON object: {{"repo": str, "overall_score": 0-100, "claims": [{{"id","verdict","confidence","evidence":[{{"kind","ref","excerpt"}}]}}], "escalations": [ids], "memo_md": "<=300 word due-diligence memo"}}"""

def main():
    out = llm(prompt)
    start, end = out.find("{"), out.rfind("}")
    report = json.loads(out[start:end + 1])
    report.setdefault("usage", {})
    print(json.dumps(report))

exit_if_limited(main)
