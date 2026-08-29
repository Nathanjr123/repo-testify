"""Render arms/PROMPTS.md from the arm sources: every prompt template that shapes an agent, verbatim, selected by name."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
def grab(src, func):
    """Return the f-string prompt inside function `func` (first triple-quoted f-string after its def)."""
    i = src.index(f"def {func}(")
    m = re.search(r'f"""(.*?)"""', src[i:], flags=re.S)
    return m.group(1).strip() if m else "(not found)"
b = (ROOT / "arms/baseline/baseline.py").read_text(); adv = (ROOT / "arms/advanced/advanced.py").read_text()
base_prompt = re.search(r'prompt = f"""(.*?)"""', b, flags=re.S).group(1).strip()
few = re.search(r'FEWSHOT = """(.*?)"""', adv, flags=re.S).group(1).strip()
out = ["# Instructions that shape each agent (rendered from source by tools/render_prompts.py — do not edit by hand)\n",
       "## Baseline arm — one-shot read of README + tree\n`arms/baseline/baseline.py`\n\n```text\n" + base_prompt + "\n```\n",
       "## Pipeline — stage PLAN (one call per repository; one probe per claim)\n`arms/advanced/advanced.py::stage_plan`\n\n```text\n" + grab(adv, "stage_plan") + "\n```\n",
       "## Pipeline — stage REPAIR (one round; environment failures only)\n`arms/advanced/advanced.py::main`\n\n```text\n" + grab(adv, "main") + "\n```\n",
       "## Pipeline — stage ADJUDICATE (k=3 votes, evidence-only, v3 rules)\n`arms/advanced/advanced.py::adjudicate_batch`\n\n```text\n" + grab(adv, "adjudicate_batch") + "\n```\n",
       "### Few-shot verdict examples injected into ADJUDICATE\n```text\n" + few + "\n```\n",
       "## Coding agent (authoring)\nClaude Code (claude-fable-5), directed interactively; its standing instructions for this repository are `CLAUDE.md`. The authoring trajectory is exported to `traces/` with `tools/export_traces.py`.\n"]
(ROOT / "arms" / "PROMPTS.md").write_text("\n".join(out)); print("arms/PROMPTS.md rendered by name")
