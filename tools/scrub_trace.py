"""Scrub the authoring trajectory: drop any '## Step' block that contains a blocked identifier or
private-client term, strip control chars, and fail loudly if anything survives. Allowlist-by-exclusion
is deliberately blunt: a build step that happens to mention a blocked word is dropped rather than risk a leak."""
import re, sys, pathlib
import os
_terms = [r"/home/[a-z0-9_-]+", r"\S+@\S+\.\S+"]  # generic only; the real denylist stays OUT of tracked source
_f = os.environ.get("REDACT_FILE", os.path.expanduser("~/.repo-testify-redact"))
if os.path.exists(_f):
    _terms += [l.strip() for l in open(_f) if l.strip() and not l.startswith("#")]
BLOCK = re.compile("|".join(_terms), re.I)
src = pathlib.Path(sys.argv[1]); dst = pathlib.Path(sys.argv[2])
raw = re.sub(r"[\x00-\x08\x0e-\x1f]", "", src.read_text(errors="replace"))
parts = re.split(r"(?=^## Step )", raw, flags=re.M)
head, steps = parts[0], parts[1:]
kept, dropped = [], 0
for s in steps:
    if BLOCK.search(s): dropped += 1
    else: kept.append(s)
note = (f"_Curated authoring trajectory. {len(kept)} build steps kept, {dropped} dropped: any step mentioning "
        f"a private path, personal identifier, or an unrelated client/project was removed wholesale rather than "
        f"partially redacted. User turns that survive are marked HUMAN CHECKPOINT. The CLI session log does not "
        f"capture the model's private reasoning. Full model input/output for the pipeline runs lives in "
        f"proof/build_proof.json._\n\n")
out = head.split("\n", 1)[0] + "\n\n" + note + "".join(kept)
dst.write_text(out)
low = out.lower()
_check = ["nate", "/home/", "@gmail", "@campus"] + [l.strip() for l in (open(_f) if os.path.exists(_f) else []) if l.strip() and not l.startswith("#")]
    _check = [re.sub(r"[^a-z0-9]", "", w.lower()) for w in _check if len(re.sub(r"[^a-z0-9]", "", w)) >= 4]
    resid = {w: low.count(w) for w in _check if low.count(w)}
print(f"kept {len(kept)}, dropped {dropped}, checkpoints {low.count('human checkpoint')}, residual: {resid or 'NONE'}")
sys.exit(1 if resid else 0)
