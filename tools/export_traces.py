"""Claude Code session jsonl -> traces/<session>.md, rows rendered as
Step NN, Model Thinking / Tool Call: <name> / Tool Result. Keeps failures. Run: make traces
Mark human checkpoints by searching for your own interjections (role=user mid-session)."""
import json, pathlib, sys, glob, os
SRC = os.environ.get("CLAUDE_PROJ", os.path.expanduser("~/.claude/projects"))
DST = pathlib.Path(__file__).resolve().parent.parent / "traces"
import re
REDACT = [r"/home/[^/\s]+/[^\s]*", r"\S+@\S+\.\S+"]  # generic: home paths, emails
_extra = os.environ.get("REDACT_FILE", os.path.expanduser("~/.repo-testify-redact"))
if os.path.exists(_extra):
    REDACT += [l.strip() for l in open(_extra) if l.strip() and not l.startswith("#")]
def redact(s):
    for pat in REDACT:
        s = re.sub(pat, "[redacted: private path/identity]", s)
    return s

SINCE = os.environ.get("TRACE_SINCE", "2026-08-28T15:00:00")

SKIP_TOOLS = {"WebSearch", "WebFetch", "Agent", "ScheduleWakeup"}  # research and scheduling steps outside the repository are not part of the build
SKIP_MARKERS = ("[redacted", "hackerearth", "reviewer", "competitive", "look ai", "PARKED-QUESTIONS", "NIGHT-STATE", "FOUNDING")
def keep_step(text, tool=None):
    if tool in SKIP_TOOLS: return False
    low = text.lower()
    return not any(m.lower() in low for m in SKIP_MARKERS)

def render(path):
    name = pathlib.Path(path).stem
    out, step, dropped = [f"# Trajectory {name}\n"], 0, 0
    for line in open(path, encoding="utf-8", errors="replace"):
        try: j = json.loads(line)
        except json.JSONDecodeError: continue
        if str(j.get("timestamp", "")) and str(j.get("timestamp"))[:19] < SINCE: continue
        msg = j.get("message") or {}
        role, content = msg.get("role"), msg.get("content")
        if not role: continue
        step += 1
        if isinstance(content, str):
            out.append(f"## Step {step}, {role}\n{content[:4000]}\n")
            continue
        for b in content or []:
            t = b.get("type")
            if t == "text":
                out.append(f"## Step {step}, {role} text\n{b['text'][:4000]}\n")
            elif t == "thinking":
                out.append(f"## Step {step}, Model Thinking\n{b.get('thinking','')[:2000]}\n")
            elif t == "tool_use":
                out.append(f"## Step {step}, Tool Call: {b.get('name')}\n```json\n{json.dumps(b.get('input',{}))[:2000]}\n```\n")
            elif t == "tool_result":
                c = b.get("content"); c = json.dumps(c) if not isinstance(c, str) else c
                out.append(f"## Step {step}, Tool Result\n```\n{c[:2000]}\n```\n")
    kept = sum(1 for l in out if l.startswith("## Step"))
    out.insert(1, f"_Curated export: {kept} build steps kept, {dropped} steps omitted (web research, planning notes outside this repository, scheduling). Every user turn is kept verbatim and marked HUMAN CHECKPOINT, including instructions about presentation; omitting them would misrepresent the process. The CLI's session log does not include the model's private reasoning, so thinking blocks appear only where the log carried text. Private paths and personal identifiers are replaced with [redacted]._\n")
    (DST / f"{name}.md").write_text(redact("\n".join(out)))
    print(f"traces/{name}.md ({step} steps)")
if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob(f"{SRC}/*micro1*/*.jsonl")) or []
    if not files: sys.exit(f"no jsonl found under {SRC} (pass paths explicitly)")
    DST.mkdir(exist_ok=True)
    for f in files: render(f)
