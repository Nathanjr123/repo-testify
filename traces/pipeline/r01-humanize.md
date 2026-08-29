# Pipeline trajectory — r01-humanize (proof `advanced-v2-1787952546`)

Repository https://github.com/python-humanize/humanize @ `ce4147b6c8f8` · buyer question: _We want to embed humanize in our reporting product's number/date formatting layer — do the README's install instructions, Python-version support, and example outputs actually hold on a current interpreter?_

## Step 1 — instructions
See `arms/PROMPTS.md` (PLAN → EXECUTE → ADJUDICATE). Claims given to the agent:

- **c1** (install): The package 'humanize' can be installed from PyPI with the command `python3 -m pip install --upgrade humanize`, after which `import humanize` succeeds.
- **c2** (install): The package 'humanize' can be installed from source by cloning https://github.com/python-humanize/humanize and running `python3 -m pip install -e .` in the clone.
- **c3** (environment): The 'humanize' package's README displays a PyPI supported-Python-versions badge, asserting that the versions shown by pypi.org metadata (currently requires-python >=3.10) are the supported versions.
- **c4** (quickstart): In Python with the 'humanize' package installed, `humanize.intcomma(12345)` returns the string '12,345'.
- **c5** (quickstart): In Python with the 'humanize' package installed, `humanize.intword(123455913)` returns the string '123.5 million'.
- **c6** (quickstart): In Python with the 'humanize' package installed, `humanize.naturaldelta(datetime.timedelta(seconds=1001))` returns the string '16 minutes'.
- **c7** (quickstart): In Python with the 'humanize' package installed, `humanize.naturalsize(1_000_000)` returns '1.0 MB' and `humanize.naturalsize(1_000_000, binary=True)` returns '976.6 KiB'.
- **c8** (quickstart): In Python with the 'humanize' package installed, `humanize.fractional(1/3)` returns the string '1/3'.
- **c9** (quickstart): In Python with the 'humanize' package installed, `humanize.scientific(0.3)` returns the string '3.00 x 10⁻¹' (with Unicode superscript exponent).
- **c10** (interface): The 'humanize' package ships a Russian locale: after `humanize.i18n.activate('ru_RU')`, `humanize.naturaltime(datetime.timedelta(seconds=3))` returns '3 секунды назад', and `humanize.i18n.deactivate()` restores '3 seconds ago'.
- **c11** (test_ci): The GitHub Actions 'Test' workflow badge in the humanize README asserts that the Test workflow on python-humanize/humanize is currently passing.

## Step 2 — PLAN output: 11 probes (committed as `eval/probes/r01-humanize.json`)

- `p-c1` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/python -m pip install --upgrade humanize`
  - commands: `/tmp/v/bin/python -c 'import humanize; print("HUMANIZE_VERSION", humanize.__version__)' && /tmp/v/bin/python -c 'import humanize' && echo PROBE_OK`
- `p-c2` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq && apt-get install -y -qq git >/dev/null && git clone https://github.com/python-humanize/humanize /tmp/humanize && cd /tmp/humanize && git checkout -q ce4147b6c8f8a132f772be0929d58305eb22c5d9 && cd /tmp/humanize && python3 -m pip install -e .`
  - commands: `cd / && python3 -c 'import humanize, os; print("HUMANIZE_FILE", humanize.__file__); assert humanize.__file__.startswith("/tmp/humanize/"), humanize.__file__' && cd / && python3 -c 'import humanize; print("HUMANIZE_VERSION", humanize.__version__)' && echo PROBE_OK`
- `p-c3` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq && apt-get install -y -qq curl >/dev/null && curl -sf https://pypi.org/pypi/humanize/json -o /tmp/pypi.json`
  - commands: `python3 -c "import json; d=json.load(open('/tmp/pypi.json'))['info']; print('REQUIRES_PYTHON', d['requires_python']); print('CLASSIFIERS', [c for c in d['classifiers'] if 'Python ::' in c])" && python3 -c "import json; d=json.load(open('/tmp/pypi.json'))['info']; assert d['requires_python']=='>=3.10`
- `p-c4` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m pip install --upgrade humanize`
  - commands: `python3 -c "import humanize; r=humanize.intcomma(12345); print('RESULT', repr(r)); assert r == '12,345', repr(r)" && echo PROBE_OK`
- `p-c5` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m pip install --upgrade humanize`
  - commands: `python3 -c "import humanize; r=humanize.intword(123455913); print('RESULT', repr(r)); assert r == '123.5 million', repr(r)" && echo PROBE_OK`
- `p-c6` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m pip install --upgrade humanize`
  - commands: `python3 -c "import humanize, datetime as dt; r=humanize.naturaldelta(dt.timedelta(seconds=1001)); print('RESULT', repr(r)); assert r == '16 minutes', repr(r)" && echo PROBE_OK`
- `p-c7` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m pip install --upgrade humanize`
  - commands: `python3 -c "import humanize; a=humanize.naturalsize(1_000_000); b=humanize.naturalsize(1_000_000, binary=True); print('RESULT', repr(a), repr(b)); assert a == '1.0 MB', repr(a); assert b == '976.6 KiB', repr(b)" && echo PROBE_OK`
- `p-c8` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m pip install --upgrade humanize`
  - commands: `python3 -c "import humanize; r=humanize.fractional(1/3); print('RESULT', repr(r)); assert r == '1/3', repr(r)" && echo PROBE_OK`
- `p-c9` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m pip install --upgrade humanize`
  - commands: `PYTHONIOENCODING=utf-8 python3 -c "import humanize; r=humanize.scientific(0.3); print('RESULT', repr(r)); assert r == '3.00 x 10\u207b\u00b9', repr(r)" && echo PROBE_OK`
- `p-c10` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m pip install --upgrade humanize`
  - commands: `PYTHONIOENCODING=utf-8 python3 -c "import humanize, datetime as dt; before=humanize.naturaltime(dt.timedelta(seconds=3)); _t=humanize.i18n.activate('ru_RU'); ru=humanize.naturaltime(dt.timedelta(seconds=3)); humanize.i18n.deactivate(); after=humanize.naturaltime(dt.timedelta(seconds=3)); print('RESU`
- `p-c11` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq && apt-get install -y -qq curl >/dev/null && curl -sf -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/python-humanize/humanize/actions/workflows' -o /tmp/workflows.json && WF_ID=$(python3 -c "import json; ws=json.load(open('/tmp/workflows.json'))['workflows'`
  - commands: `python3 -c "import json; runs=json.load(open('/tmp/runs.json'))['workflow_runs']; [print('RUN', r['head_sha'][:12], r['created_at'], r['conclusion']) for r in runs]; assert runs, 'no completed Test runs on main'; latest=runs[0]; print('LATEST_CONCLUSION', latest['conclusion']); assert latest['conclu`

## Step 3 — EXECUTE on GitHub Actions: run `33206171217` (artifacts: per-probe cmd/stdout/stderr/exit_code)

Transcript index (probe · command excerpt):
```
p-c1 /tmp/v/bin/python -c 'import humanize; print("HUMANIZE_VERSION", humanize.__version__)' && /tmp/v/bin/python -c 'import humanize' && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c10 PYTHONIOENCODING=utf-8 python3 -c "import humanize, datetime as dt; before=humanize.naturaltime(dt.timedelta(seconds=3)); _t=humanize.i18n.activate('ru_RU'); ru=humanize.naturaltime(dt.timedelta(seconds=3)); humanize.i18n.deactivate(); after=humanize.naturaltime(dt.timedelta(seconds=3)); print('RESULT', repr(before), repr(ru), repr(after)); assert before == '3 seconds ago', repr(before); assert ru cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c11 python3 -c "import json; runs=json.load(open('/tmp/runs.json'))['workflow_runs']; [print('RUN', r['head_sha'][:12], r['created_at'], r['conclusion']) for r in runs]; assert runs, 'no completed Test runs on main'; latest=runs[0]; print('LATEST_CONCLUSION', latest['conclusion']); assert latest['conclusion']=='success', latest['conclusion']" && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c2 cd / && python3 -c 'import humanize, os; print("HUMANIZE_FILE", humanize.__file__); assert humanize.__file__.startswith("/tmp/humanize/"), humanize.__file__' && cd / && python3 -c 'import humanize; print("HUMANIZE_VERSION", humanize.__version__)' && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c3 python3 -c "import json; d=json.load(open('/tmp/pypi.json'))['info']; print('REQUIRES_PYTHON', d['requires_python']); print('CLASSIFIERS', [c for c in d['classifiers'] if 'Python ::' in c])" && python3 -c "import json; d=json.load(open('/tmp/pypi.json'))['info']; assert d['requires_python']=='>=3.10', d['requires_python']" && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c4 python3 -c "import humanize; r=humanize.intcomma(12345); print('RESULT', repr(r)); assert r == '12,345', repr(r)" && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c5 python3 -c "import humanize; r=humanize.intword(123455913); print('RESULT', repr(r)); assert r == '123.5 million', repr(r)" && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c6 python3 -c "import humanize, datetime as dt; r=humanize.naturaldelta(dt.timedelta(seconds=1001)); print('RESULT', repr(r)); assert r == '16 minutes', repr(r)" && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c7 python3 -c "import humanize; a=humanize.naturalsize(1_000_000); b=humanize.naturalsize(1_000_000, binary=True); print('RESULT', repr(a), repr(b)); assert a == '1.0 MB', repr(a); assert b == '976.6 KiB', repr(b)" && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c8 python3 -c "import humanize; r=humanize.fractional(1/3); print('RESULT', repr(r)); assert r == '1/3', repr(r)" && echo PROBE_OK cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c9 PYTHONIOENCODING=utf-8 python3 -c "import humanize; r=humanize.scientific(0.3); print('RESULT', 
```

## Step 4 — ADJUDICATE: votes → verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1` — phase_a_tail: 'Successfully installed humanize-4.16.0'; stdout: 'HUMANIZE_VERSION 4.16.0'  |
| c2 | verified / verified / verified | **verified** | high | `p-c2` — phase_a_tail: "Cloning into '/tmp/humanize'..."; stdout: 'HUMANIZE_FILE /tmp/humanize/src/ |
| c3 | verified / verified / verified | **verified** | high | `p-c3` — stdout: 'REQUIRES_PYTHON >=3.10' with classifiers Python 3.10 through 3.15; assert require |
| c4 | verified / verified / verified | **verified** | high | `p-c4` — stdout: "RESULT '12,345'" / 'PROBE_OK'; exit_code 0 |
| c5 | verified / verified / verified | **verified** | high | `p-c5` — stdout: "RESULT '123.5 million'" / 'PROBE_OK'; exit_code 0 |
| c6 | refuted / refuted / refuted | **refuted** | high | `p-c6` — stdout: "RESULT '17 minutes'"; stderr: "AssertionError: '17 minutes'" (claim says '16 minu |
| c7 | verified / verified / verified | **verified** | high | `p-c7` — stdout: "RESULT '1.0 MB' '976.6 KiB'" / 'PROBE_OK'; exit_code 0 |
| c8 | verified / verified / verified | **verified** | high | `p-c8` — stdout: "RESULT '1/3'" / 'PROBE_OK'; exit_code 0 |
| c9 | verified / verified / verified | **verified** | high | `p-c9` — stdout: "RESULT '3.00 x 10⁻¹'" / 'PROBE_OK' (assert against '3.00 x 10\u207b\u00b9' passed |
| c10 | verified / verified / verified | **verified** | high | `p-c10` — stdout: "RESULT '3 seconds ago' '3 секунды назад' '3 seconds ago'" / 'PROBE_OK' (before/ac |
| c11 | verified / verified / verified | **verified** | high | `p-c11` — stdout: 'RUN ce4147b6c8f8 2026-08-01T09:18:47Z success' ... 'LATEST_CONCLUSION success' /  |

## Step 5 — REPORT
Overall score 91 · escalated to human: none · model calls: nominal 4

_Human checkpoint: the verdicts above were audited against ground truth; disagreements were read from the recorded probe output and resolved in favour of the evidence (CHANGELOG 'Truth audit')._