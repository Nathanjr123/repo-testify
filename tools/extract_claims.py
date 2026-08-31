"""Extract a checkable claim list from a repository's README + file tree, so the tool can run from a URL
with no hand-written case file. One model call. Output is a case file the arms consume.
Usage: python3 tools/extract_claims.py https://github.com/owner/repo [--commit SHA] > case.json
This is the real-world entry point; the scored evaluation uses fixed claim lists instead (DECISIONS #2)."""
import base64, json, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from arms.common import llm

def gh(args):
    return subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)

def main():
    url = sys.argv[1].rstrip("/")
    owner_repo = url.split("github.com/")[-1]
    commit = sys.argv[sys.argv.index("--commit") + 1] if "--commit" in sys.argv else \
        gh(["api", f"repos/{owner_repo}/commits/HEAD", "--jq", ".sha"]).stdout.strip()
    rd = gh(["api", f"repos/{owner_repo}/readme?ref={commit}", "--jq", ".content"])
    readme = base64.b64decode(rd.stdout).decode(errors="replace") if rd.returncode == 0 else ""
    tr = gh(["api", f"repos/{owner_repo}/git/trees/{commit}?recursive=1"])
    paths = [e["path"] for e in json.loads(tr.stdout).get("tree", [])][:300] if tr.returncode == 0 else []
    prompt = f"""Extract the CHECKABLE claims a README makes about this repository, the kind a technical buyer could be misled by and that a sandbox probe could settle by executing something. Repository {url} @ {commit}.
Rules: 8-12 claims; one claim = one thing a single probe can check; decontextualize each (name the exact package, command, expected output); include the install command, a quickstart snippet with its expected output, any Python/version support claim, badge/CI claims, and any dependency or feature claim. Skip pure marketing with no testable content. Give each a verbatim source_quote from the README.
Claim types: install | environment | quickstart | interface | test_ci | quantitative | feature.
README:\n{readme[:18000]}\nFile tree (first 300): {json.dumps(paths)}
Reply with ONLY JSON: {{"id": "<short-slug>", "repo": "{url}", "commit": "{commit}", "buyer_question": "<one sentence a real evaluator would ask>", "claims": [{{"id": "c1", "type": "...", "text": "...", "source_quote": "...", "probe_hint": "<the shell command that would check it>"}}]}}"""
    out = llm(prompt)
    s, e = out.find("{"), out.rfind("}")
    case = json.loads(out[s:e + 1])
    case["commit"] = commit
    print(json.dumps(case, indent=1))

if __name__ == "__main__":
    main()
