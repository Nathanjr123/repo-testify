"""Shared arm helpers. The pipeline calls the Claude CLI (`claude -p`) for its model calls; resolve the binary
explicitly (PATH, CLAUDE_BIN, or the VS Code extension bundle) so non-interactive runs work."""
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

import json, subprocess, sys, time

class LimitBlocked(RuntimeError):
    """Usage/rate limit: an INFRASTRUCTURE condition, never a verdict. Arms exit 75 (EX_TEMPFAIL)."""

LIMIT_MARKERS = ("rate limit", "usage limit", "429", "overloaded", "limit reached", "try again later", "out of extra usage")

CALLS = {"n": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0}

def llm(prompt, model="claude-fable-5", retries=2, backoff=(60, 300)):
    CALLS["n"] += 1
    """claude -p with limit detection. Empty stdout is treated as a limit signal (observed 2026-08-28:
    the CLI returned empty output for 3 consecutive calls when the session limit hit)."""
    claude = resolve_claude()
    for i in range(retries + 1):
        r = subprocess.run([claude, "-p", prompt, "--model", model, "--output-format", "json"], capture_output=True, text=True, timeout=600)
        out = (r.stdout or "").strip()
        try:  # JSON envelope carries the answer plus cost and token usage; fall back to raw text if absent
            env = json.loads(out)
            if isinstance(env, dict) and "result" in env:
                CALLS["cost_usd"] += float(env.get("total_cost_usd") or 0.0)
                u = env.get("usage") or {}
                CALLS["input_tokens"] += int(u.get("input_tokens") or 0); CALLS["output_tokens"] += int(u.get("output_tokens") or 0)
                out = str(env["result"]).strip()
        except (ValueError, TypeError):
            pass
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
