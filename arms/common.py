# PROVENANCE — read before modifying.
# Written during the competition (2026-08-28/31) by Claude Code (claude-fable-5) under Nathan Obiekwe's
# direction; every design decision it encodes is recorded in DESIGN.md / DECISIONS.md / CHANGELOG.md, and the
# session trajectory that produced it is in traces/. Pre-existing before kickoff: only the problem-agnostic
# skeleton (Makefile targets, eval/ layout, trace exporter). Human review: Nathan audits truth files and results.
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

import subprocess, sys, time

class LimitBlocked(RuntimeError):
    """Usage/rate limit: an INFRASTRUCTURE condition, never a verdict. Arms exit 75 (EX_TEMPFAIL)."""

LIMIT_MARKERS = ("rate limit", "usage limit", "429", "overloaded", "limit reached", "try again later", "out of extra usage")

def llm(prompt, model="claude-fable-5", retries=2, backoff=(60, 300)):
    """claude -p with limit detection. Empty stdout is treated as a limit signal (observed 2026-08-28:
    the CLI returned empty output for 3 consecutive calls when the session limit hit)."""
    claude = resolve_claude()
    for i in range(retries + 1):
        r = subprocess.run([claude, "-p", prompt, "--model", model], capture_output=True, text=True, timeout=600)
        out = (r.stdout or "").strip()
        blob = (out + " " + (r.stderr or "")).lower()
        limited = (not out) or any(m in blob for m in LIMIT_MARKERS)
        if r.returncode == 0 and out and not limited:
            return out
        if limited and i < retries:
            time.sleep(backoff[min(i, len(backoff) - 1)]); continue
        if limited:
            raise LimitBlocked(f"claude -p blocked (empty/limit) after {retries+1} tries: {(r.stderr or '')[:200]}")
        raise RuntimeError(f"llm failed rc={r.returncode}: {(r.stderr or '')[:300]}")

def exit_if_limited(fn):
    """Run fn(); on LimitBlocked exit 75 so the runner marks the case limit_blocked and halts the sweep."""
    try:
        return fn()
    except LimitBlocked as e:
        print(f"LIMIT_BLOCKED: {e}", file=sys.stderr); sys.exit(75)
