# Pipeline trajectory: r00-repo-testify (self-run, CI run 33259186251)

Repository https://github.com/Nathanjr123/repo-testify @ `42bb1ca3556a`. Buyer question: _A hackathon judge asks: does this repository actually do what its README claims, from a clean clone, with no credentials?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): From a clean clone, `./repro.sh` runs to completion with exit code 0 using only Python 3.10+ (no make, no docker, no credentials).
- **c2** (test_ci): `python3 tests/test_scorer.py` passes all six scorer contract tests.
- **c3** (quickstart): `python3 eval/validate_cases.py` reports every case file valid.
- **c4** (quickstart): `python3 -m eval.replay --run <the advanced-v2-rescored run id>` reproduces the stored raw score 0.817 exactly.
- **c5** (quickstart): Regenerating RESULTS.md and the README tables from proof/ yields files byte-identical to the committed ones.
- **c6** (environment): The shipped Dockerfile builds and its default command runs the Level-1 reproduction successfully.
- **c7** (quantitative): On the public split the pipeline's raw per-claim accuracy is 0.83 (62 of 75) against the baseline's 0.13 (10 of 75), as generated from proof/build_proof.json.
- **c8** (interface): Every row of RESULTS.md carries a proof id, a git hash and a UTC timestamp, and each cited git hash exists in the repository history.
- **c9** (test_ci): The README's `repro` workflow badge asserts the latest run of that workflow on master succeeded.
- **c10** (interface): `arms/PROMPTS.md` is generated from the arm sources: running `python3 tools/render_prompts.py` leaves it unchanged.

## Step 2: PLAN output, 10 probes (committed as `eval/probes/r00-repo-testify.json`)

- `p-c1` image `python:3.10-slim` network `none`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && (command -v make >/dev/null 2>&1 && echo 'note: make present' || echo 'make absent'); (command -v docker >/dev/null 2>&1 && echo 'note: docker present' || echo 'docker absent'); ls -l repro.sh && cd /work/repo-testify && ./repro.sh > /tmp/repro.log 2>&1; rc=$?; tail -20 /tmp`
- `p-c2` image `python:3.11-slim` network `none`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && python3 - <<'EOF'
import re, subprocess
p = subprocess.run(['python3', 'tests/test_scorer.py'], capture_output=True, text=True, timeout=100)
out = p.stdout + p.stderr
print(out[-2000:])
names = sorted(set(re.findall(r'\bok (test_\w+)', out)))
fails = re.findall(r'(?i)\b(FAIL`
- `p-c3` image `python:3.11-slim` network `none`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && python3 - <<'EOF'
import subprocess
p = subprocess.run(['python3', 'eval/validate_cases.py'], capture_output=True, text=True, timeout=100)
out = (p.stdout + p.stderr).strip()
print(out[-1500:])
last = out.splitlines()[-1] if out else ''
print('exit=%d last_line=%r' % (p.retu`
- `p-c4` image `python:3.11-slim` network `none`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && python3 - <<'EOF'
import re, subprocess
from collections import Counter
raw = open('proof/build_proof.json').read()
c = Counter(re.findall(r'advanced-v2-rescored-[A-Za-z0-9_:-]+', raw))
print('candidate run ids:', c.most_common(5))
if not c:
    print('VERDICT_LINE: FAIL no `
- `p-c5` image `python:3.11-slim` network `none`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && git status --porcelain -- README.md RESULTS.md && echo 'pre-state clean check done' && cd /work/repo-testify && python3 -m eval.report > RESULTS.md; r1=$?; python3 eval/render_readme.py; r2=$?; git --no-pager diff --stat -- README.md RESULTS.md; git --no-pager diff -- README`
- `p-c6` image `python:3.11-slim` network `on`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && python3 - <<'EOF'
import json, os, re, shutil, urllib.request
print('docker binary in sandbox:', shutil.which('docker'))
print('NOTE: docker build cannot run inside this sandbox; verdict is indirect via Dockerfile contents + CI repro workflow status')
ok = True
if not os.pat`
- `p-c7` image `python:3.11-slim` network `none`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && python3 - <<'EOF'
import re, subprocess
p = subprocess.run(['python3', 'eval/render_readme.py'], capture_output=True, text=True, timeout=100)
print((p.stdout + p.stderr)[-800:]); print('render exit=', p.returncode)
txt = open('README.md').read()
block = txt.split('<!-- RESUL`
- `p-c8` image `python:3.11-slim` network `none`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && python3 - <<'EOF'
import re, subprocess
lines = open('RESULTS.md').read().splitlines()
rows = []
in_table = False
for l in lines:
    if re.match(r'^\|\s*:?-{3,}', l):
        in_table = True; continue
    if in_table and l.startswith('|'):
        rows.append(l)
    elif no`
- `p-c9` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python3 - <<'EOF'
import json, urllib.request
ok = True
conclusion = None
badge_text = None
try:
    req = urllib.request.Request('https://github.com/Nathanjr123/repo-testify/actions/workflows/repro.yml/badge.svg', headers={'User-Agent': 'repo-testify-probe'})
    with urllib.request.urlopen(req, ti`
- `p-c10` image `python:3.11-slim` network `none`
  - setup: `apt-get update -qq >/dev/null 2>&1 && apt-get install -y -qq git >/dev/null 2>&1 || echo 'setup: apt-get git failed' && git config --global --add safe.directory '*' && git clone -q https://github.com/Nathanjr123/repo-testify.git /work/repo-testify && cd /work/repo-testify && git checkout -q 42bb1ca3`
  - commands: `cd /work/repo-testify && head -3 arms/PROMPTS.md; ls -l tools/render_prompts.py && cd /work/repo-testify && python3 tools/render_prompts.py; r=$?; git --no-pager diff --stat -- arms/PROMPTS.md; git --no-pager diff -- arms/PROMPTS.md | head -30; git diff --quiet -- arms/PROMPTS.md; d=$?; echo "render`

## Step 3: EXECUTE on GitHub Actions, run `33259186251`

Transcript index:
```
p-c1 cd /work/repo-testify && (command -v make >/dev/null 2>&1 && echo 'note: make present' || echo 'make absent'); (command -v docker >/dev/null 2>&1 && echo 'note: docker present' || echo 'docker absent'); ls -l repro.sh && cd /work/repo-testify && ./repro.sh > /tmp/repro.log 2>&1; rc=$?; tail -20 /tmp/repro.log; echo "repro.sh exit=$rc"; if [ "$rc" -eq 0 ]; then echo 'VERDICT_LINE: PASS ./repro.sh e cmd.txt exit_code stdout.log phase_a.log
p-c10 cd /work/repo-testify && head -3 arms/PROMPTS.md; ls -l tools/render_prompts.py && cd /work/repo-testify && python3 tools/render_prompts.py; r=$?; git --no-pager diff --stat -- arms/PROMPTS.md; git --no-pager diff -- arms/PROMPTS.md | head -30; git diff --quiet -- arms/PROMPTS.md; d=$?; echo "render_exit=$r git_diff_exit=$d"; if [ $r -eq 0 ] && [ $d -eq 0 ]; then echo 'VERDICT_LINE: PASS render_pr cmd.txt exit_code stdout.log phase_a.log
p-c2 cd /work/repo-testify && python3 - <<'EOF'
import re, subprocess
p = subprocess.run(['python3', 'tests/test_scorer.py'], capture_output=True, text=True, timeout=100)
out = p.stdout + p.stderr
print(out[-2000:])
names = sorted(set(re.findall(r'\bok (test_\w+)', out)))
fails = re.findall(r'(?i)\b(FAIL|ERROR|Traceback|AssertionError)\b', out)
print('exit=%d ok_tests=%d %s fail_markers=%d' % (p.return cmd.txt exit_code stdout.log phase_a.log
p-c3 cd /work/repo-testify && python3 - <<'EOF'
import subprocess
p = subprocess.run(['python3', 'eval/validate_cases.py'], capture_output=True, text=True, timeout=100)
out = (p.stdout + p.stderr).strip()
print(out[-1500:])
last = out.splitlines()[-1] if out else ''
print('exit=%d last_line=%r' % (p.returncode, last))
if p.returncode == 0 and 'all valid' in last:
    print('VERDICT_LINE: PASS validate_ cmd.txt exit_code stdout.log phase_a.log
p-c4 cd /work/repo-testify && python3 - <<'EOF'
import re, subprocess
from collections import Counter
raw = open('proof/build_proof.json').read()
c = Counter(re.findall(r'advanced-v2-rescored-[A-Za-z0-9_:-]+', raw))
print('candidate run ids:', c.most_common(5))
if not c:
    print('VERDICT_LINE: FAIL no advanced-v2-rescored run id found in proof/build_proof.json')
    raise SystemExit
rid = c.most_comm cmd.txt exit_code stdout.log phase_a.log
p-c5 cd /work/repo-testify && git status --porcelain -- README.md RESULTS.md && echo 'pre-state clean check done' && cd /work/repo-testify && python3 -m eval.report > RESULTS.md; r1=$?; python3 eval/render_readme.py; r2=$?; git --no-pager diff --stat -- README.md RESULTS.md; git --no-pager diff -- README.md RESULTS.md | head -40; git diff --quiet -- README.md RESULTS.md; d=$?; echo "report_exit=$r1 ren cmd.txt exit_code stdout.log phase_a.log
p-c6 cd /work/repo-testify && python3 - <<'EOF'
import json, os, re, shutil, urllib.request
print('docker binary in sandbox:', shutil.which('docker'))
print('NOTE: docker build cannot run inside this sandbox; verdict is indirect via Dockerfile contents + CI repro workflow status')
ok = True
if not os.path.exists('Do
```

## Step 4: ADJUDICATE, votes then verdict per claim

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: make absent / docker absent / REPRO OK: README/RESULTS regenerate byte-identically from proof / repr |
| c2 | verified / verified / verified | **verified** | high | `p-c2`: exit=0 ok_tests=6 [...] fail_markers=0 / VERDICT_LINE: PASS 6 scorer tests reported ok, exit 0 + exi |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: 14 case files checked / all valid / exit=0 last_line='all valid' / VERDICT_LINE: PASS validate_cases |
| c4 | verified / verified / verified | **verified** | high | `p-c4`: replay ok: advanced-v2-rescored-1787952712 raw 0.817 / exit=0 / VERDICT_LINE: PASS replay of advance |
| c5 | verified / verified / verified | **verified** | high | `p-c5`: report_exit=0 render_exit=0 git_diff_exit=0 / VERDICT_LINE: PASS README.md and RESULTS.md byte-ident |
| c6 | verified / unverifiable / verified | **verified** | low | `p-c6`: docker binary in sandbox: None / NOTE: docker build cannot run inside this sandbox; verdict is indir |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: render exit= 0 / primary row: '/ Primary outcome: per-claim accuracy, 95% Wilson interval / 0.13 (10 |
| c8 | refuted / refuted / refuted | **refuted** | high | `p-c8`: data rows found: 10 / rows missing hash/timestamp/proof id: 0 / distinct hashes cited: 4, not in his |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: badge status: 200 badge text: passing / latest master run: id=33259186237 head_sha=3e4ad3d... status |
| c10 | verified / verified / verified | **verified** | high | `p-c10`: arms/PROMPTS.md rendered by name / render_exit=0 git_diff_exit=0 / VERDICT_LINE: PASS render_prompts |

## Step 5: REPORT
Overall score 90. Escalated: none. Model calls: 4.

Human checkpoint: c8 was refuted at high confidence (a cited commit hash no longer existed after a history rewrite). We confirmed the finding against `git cat-file`, fixed the proof entry, and kept the refuted row in the README. See CHANGELOG iteration 10.