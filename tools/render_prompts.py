"""Render arms/PROMPTS.md from the arm sources: every prompt template that shapes an agent, verbatim."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
out = ["# Instructions that shape each agent (rendered from source by tools/render_prompts.py — do not edit by hand)\n"]
for name, path in (("Baseline arm — one-shot read of README + tree", "arms/baseline/baseline.py"),
                   ("Pipeline — stage PLAN (one probe per claim)", "arms/advanced/advanced.py"),
                   ("Pipeline — stage REPAIR (one round, environment failures only)", "arms/advanced/advanced.py"),
                   ("Pipeline — stage ADJUDICATE (k votes, evidence-only, v3 rules)", "arms/advanced/advanced.py")):
    src = (ROOT / path).read_text()
    blocks = re.findall(r'(?:prompt|fix_prompt) = f"""(.*?)"""', src, flags=re.S)
    key = {"Baseline": 0, "PLAN": 0, "REPAIR": 1, "ADJUDICATE": 2}
    idx = 0 if "Baseline" in name else key[[k for k in key if k in name][0]]
    if idx < len(blocks):
        out.append(f"## {name}\n`{path}`\n\n```text\n{blocks[idx].strip()}\n```\n")
    if "ADJUDICATE" in name:
        few = re.search(r'FEWSHOT = """(.*?)"""', src, flags=re.S)
        if few: out.append("### Few-shot verdict examples injected into ADJUDICATE\n```text\n" + few.group(1).strip() + "\n```\n")
out.append("## Coding agent (authoring)\nClaude Code (claude-fable-5), directed interactively; its standing instructions for this repository are `CLAUDE.md`. The authoring trajectory is exported to `traces/` with `tools/export_traces.py`.\n")
(ROOT / "arms" / "PROMPTS.md").write_text("\n".join(out)); print("arms/PROMPTS.md rendered")
