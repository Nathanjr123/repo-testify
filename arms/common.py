"""Shared arm helpers. The Claude Code CLI is not on PATH in non-interactive shells on this
machine (it ships inside the VS Code extension); resolve it explicitly so background runs work."""
import glob, os, shutil

def resolve_claude() -> str:
    env = os.environ.get("CLAUDE_BIN")
    if env and os.path.exists(env):
        return env
    on_path = shutil.which("claude")
    if on_path:
        return on_path
    cands = sorted(glob.glob(os.path.expanduser(
        "~/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude")),
        key=os.path.getmtime, reverse=True)
    if cands:
        return cands[0]
    raise FileNotFoundError("claude CLI not found; set CLAUDE_BIN")
