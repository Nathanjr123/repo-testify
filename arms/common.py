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

import json, os, subprocess, sys, time

class LimitBlocked(RuntimeError):
    """Usage/rate limit: an INFRASTRUCTURE condition, never a verdict. Arms exit 75 (EX_TEMPFAIL)."""

LIMIT_MARKERS = ("rate limit", "rate_limit", "usage limit", "http 429", "status 429", "overloaded", "limit reached", "try again later", "out of extra usage")

CALLS = {"n": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0}

def llm(prompt, model="claude-fable-5", retries=2, backoff=(60, 300)):
    CALLS["n"] += 1
    """claude -p with limit detection. Empty stdout is treated as a limit signal (observed 2026-08-28:
    the CLI returned empty output for 3 consecutive calls when the session limit hit)."""
    claude = resolve_claude()
    for i in range(retries + 1):
        r = subprocess.run([claude, "-p", prompt, "--model", model, "--output-format", "json"], capture_output=True, text=True, timeout=600)
        out = (r.stdout or "").strip(); is_error = False
        try:  # JSON envelope carries the answer plus cost and token usage; fall back to raw text if absent
            env = json.loads(out)
            if isinstance(env, dict) and "result" in env:
                CALLS["cost_usd"] += float(env.get("total_cost_usd") or 0.0)
                u = env.get("usage") or {}
                CALLS["input_tokens"] += int(u.get("input_tokens") or 0) + int(u.get("cache_read_input_tokens") or 0) + int(u.get("cache_creation_input_tokens") or 0); CALLS["output_tokens"] += int(u.get("output_tokens") or 0)
                is_error = bool(env.get("is_error"))
                out = str(env["result"]).strip()
        except (ValueError, TypeError):
            pass
        # Limit detection looks ONLY at stderr and at an error result, never at the JSON envelope (its token
        # counts contain digit runs like "429" that produced false limit signals on 2026-08-29).
        blob = ((out if is_error else "") + " " + (r.stderr or "")).lower()
        limited = (not out) or any(m in blob for m in LIMIT_MARKERS)
        # A non-zero exit with nothing useful on stderr is what the CLI produces when a usage window closes
        # (seen 2026-08-30 on three consecutive plan calls); treat it as a limit and retry with backoff.
        if r.returncode != 0 and not (r.stderr or "").strip():
            limited = True
        if limited or r.returncode != 0:  # keep the raw envelope for diagnosis (outside the repo)
            try:
                with open(os.environ.get("LLM_DEBUG_LOG", os.devnull), "a") as f:  # opt-in diagnostics file
                    f.write(f"--- {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} try {i} rc={r.returncode} model={model} prompt_chars={len(prompt)}\nSTDOUT[:800]={r.stdout[:800]!r}\nSTDERR[:800]={r.stderr[:800]!r}\n")
            except OSError:
                pass
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
