# Pipeline trajectory, r04-schedule (proof `advanced-v2-1787952546`)

Repository https://github.com/dbader/schedule @ `82a43db1b938` · buyer question: _We want to use schedule for in-process periodic jobs in a service we will run for years — is the project's CI actually green, are the dependency-free and Python-version claims still true, and do the README examples run?_

## Step 1, instructions
See `arms/PROMPTS.md` (PLAN -> EXECUTE -> ADJUDICATE). Claims given to the agent:

- **c1** (install): The package 'schedule' can be installed from PyPI with `pip install schedule`, after which `import schedule` succeeds.
- **c2** (environment): The 'schedule' package is tested on Python 3.7, 3.8, 3.9, 3.10, 3.11, and 3.12.
- **c3** (test_ci): The schedule README's GitHub Actions 'Tests' badge asserts that the Tests workflow on dbader/schedule master is currently passing.
- **c4** (environment): The 'schedule' package is very lightweight and has no external dependencies (installing it pulls in no other packages).
- **c5** (quickstart): In Python with 'schedule' installed, `schedule.every(10).seconds.do(job)` (where job is any callable) registers a job without raising.
- **c6** (quickstart): In Python with 'schedule' installed, `schedule.every().day.at("10:30").do(job)` registers a daily job at 10:30 without raising.
- **c7** (quickstart): In Python with only 'schedule' installed (fresh environment, no extra packages), the README usage line `schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)` works, i.e. timezone-aware scheduling functions out of the box.
- **c8** (interface): In Python with 'schedule' installed, `schedule.every().minute.at(":17").do(job)` registers a job for the 17th second of every minute without raising.
- **c9** (interface): In Python with 'schedule' installed, `schedule.run_pending()` executes jobs that are due: a job registered with `schedule.every(1).seconds.do(f)` is invoked when run_pending() is called after more than 1 second has elapsed.
- **c10** (quantitative): The schedule README's PyPI version badge asserts that 'schedule' is published on PyPI (latest release 1.2.2).

## Step 2, PLAN output: 10 probes (committed as `eval/probes/r04-schedule.json`; matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `install-only`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install --disable-pip-version-check schedule`
  - commands: `/tmp/v/bin/python -c 'import schedule; print("import ok, version", schedule.__version__)' && /tmp/v/bin/pip show schedule | grep -E '^(Name|Version):' && /tmp/v/bin/pip show schedule | grep -E '^Version: 1\.2\.2$' || echo 'NOTE: PyPI version differs from setup.py at pinned commit (1.2.2)'`
- `p-c2` image `python:3.12-slim` network `install-only`
  - setup: `apt-get update -qq && apt-get install -y -qq curl >/dev/null && mkdir -p /tmp/wf /tmp/src && cd /tmp/wf && curl -sL 'https://api.github.com/repos/dbader/schedule/contents/.github/workflows?ref=82a43db1b938d8fdf60103bd41f329e06c8d3651' -o listing.json && python -c "import json; [print(x['download_url`
  - commands: `cd /tmp/wf && ls -1 *.yml *.yaml 2>/dev/null; grep -n -A10 'python-version' *.yml *.yaml 2>/dev/null && cd /tmp/wf && for v in 3.7 3.8 3.9 3.10 3.11 3.12; do grep -qE "[\"']?$v[\"']?" *.yml *.yaml 2>/dev/null && echo "matrix has $v" || { echo "MISSING $v in CI matrix"; exit 1; }; done && python -c "`
- `p-c3` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq && apt-get install -y -qq curl >/dev/null && curl -sL 'https://github.com/dbader/schedule/workflows/Tests/badge.svg' -o /tmp/badge.svg && curl -sL 'https://api.github.com/repos/dbader/schedule/actions/runs?branch=master&per_page=20' -o /tmp/runs.json`
  - commands: `grep -oE '(passing|failing|no status)' /tmp/badge.svg | head -1 | tee /tmp/badge_state.txt && grep -q 'passing' /tmp/badge.svg && echo 'badge renders: passing' && python -c "import json; rs=[r for r in json.load(open('/tmp/runs.json'))['workflow_runs'] if r['name']=='Tests']; assert rs,'no Tests run`
- `p-c4` image `python:3.11-slim` network `install-only`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install --disable-pip-version-check schedule`
  - commands: `/tmp/v/bin/pip freeze && n=$(/tmp/v/bin/pip freeze | grep -vi '^schedule==' | wc -l); echo "extra_packages=$n"; test "$n" -eq 0 && /tmp/v/bin/pip show schedule | grep -E '^Requires: *$' && echo 'Requires: (empty) confirmed' && du -sh /tmp/v/lib/python*/site-packages/schedule`
- `p-c5` image `python:3.11-slim` network `install-only`
  - setup: `pip install --disable-pip-version-check https://github.com/dbader/schedule/archive/82a43db1b938d8fdf60103bd41f329e06c8d3651.tar.gz`
  - commands: `python -c "import schedule
def job():
    print(\"I'm working...\")
schedule.every(10).seconds.do(job)
n=len(schedule.get_jobs()); print('registered jobs:', n); assert n==1"`
- `p-c6` image `python:3.11-slim` network `install-only`
  - setup: `pip install --disable-pip-version-check https://github.com/dbader/schedule/archive/82a43db1b938d8fdf60103bd41f329e06c8d3651.tar.gz`
  - commands: `python -c "import schedule
def job():
    print(\"I'm working...\")
j=schedule.every().day.at('10:30').do(job)
print('next_run:', j.next_run); assert j.next_run.hour==10 and j.next_run.minute==30; print('ok')"`
- `p-c7` image `python:3.11-slim` network `install-only`
  - setup: `python -m venv /tmp/vtz && /tmp/vtz/bin/pip install --disable-pip-version-check https://github.com/dbader/schedule/archive/82a43db1b938d8fdf60103bd41f329e06c8d3651.tar.gz`
  - commands: `/tmp/vtz/bin/pip freeze && ! /tmp/vtz/bin/pip show pytz >/dev/null 2>&1 && echo 'pytz absent (fresh env confirmed)' && /tmp/vtz/bin/python -c "import schedule
def job():
    print(\"I'm working...\")
try:
    j=schedule.every().day.at('12:42', 'Europe/Amsterdam').do(job)
    print('RESULT: works out`
- `p-c8` image `python:3.11-slim` network `install-only`
  - setup: `pip install --disable-pip-version-check https://github.com/dbader/schedule/archive/82a43db1b938d8fdf60103bd41f329e06c8d3651.tar.gz`
  - commands: `python -c "import schedule
def job():
    print(\"I'm working...\")
j=schedule.every().minute.at(':17').do(job)
print('next_run:', j.next_run); assert j.next_run.second==17; print('ok')"`
- `p-c9` image `python:3.11-slim` network `install-only`
  - setup: `pip install --disable-pip-version-check https://github.com/dbader/schedule/archive/82a43db1b938d8fdf60103bd41f329e06c8d3651.tar.gz`
  - commands: `python -c "import schedule, time
hits=[]
schedule.every(1).seconds.do(lambda: hits.append(1))
schedule.run_pending()
assert not hits, 'job ran before it was due'
time.sleep(1.2)
schedule.run_pending()
assert hits, 'job did not run after 1.2s'
print('job invoked', len(hits), 'time(s) after 1.2s')"`
- `p-c10` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq && apt-get install -y -qq curl >/dev/null && curl -s https://pypi.org/pypi/schedule/json -o /tmp/pypi.json`
  - commands: `python -c "import json; d=json.load(open('/tmp/pypi.json')); v=d['info']['version']; print('PyPI latest:', v); print('1.2.2 uploaded:', d['releases'].get('1.2.2',[{}])[0].get('upload_time')); assert '1.2.2' in d['releases'], '1.2.2 not on PyPI'; assert v=='1.2.2', 'latest is '+v+', not 1.2.2'"`

## Step 3, EXECUTE on GitHub Actions: run `33207924062` (artifacts: per-probe cmd/stdout/stderr/exit_code)

Transcript index (probe · command excerpt):
```
p-c1 /tmp/v/bin/python -c 'import schedule; print("import ok, version", schedule.__version__)' && /tmp/v/bin/pip show schedule | grep -E '^(Name|Version):' && /tmp/v/bin/pip show schedule | grep -E '^Version: 1\.2\.2$' || echo 'NOTE: PyPI version differs from setup.py at pinned commit (1.2.2)' cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c10 python -c "import json; d=json.load(open('/tmp/pypi.json')); v=d['info']['version']; print('PyPI latest:', v); print('1.2.2 uploaded:', d['releases'].get('1.2.2',[{}])[0].get('upload_time')); assert '1.2.2' in d['releases'], '1.2.2 not on PyPI'; assert v=='1.2.2', 'latest is '+v+', not 1.2.2'" cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c2 cd /tmp/wf && ls -1 *.yml *.yaml 2>/dev/null; grep -n -A10 'python-version' *.yml *.yaml 2>/dev/null && cd /tmp/wf && for v in 3.7 3.8 3.9 3.10 3.11 3.12; do grep -qE "[\"']?$v[\"']?" *.yml *.yaml 2>/dev/null && echo "matrix has $v" || { echo "MISSING $v in CI matrix"; exit 1; }; done && python -c "import json; rs=json.load(open('/tmp/wf/runs.json'))['workflow_runs']; [print(r['name'],'|',r['concl cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c3 grep -oE '(passing|failing|no status)' /tmp/badge.svg | head -1 | tee /tmp/badge_state.txt && grep -q 'passing' /tmp/badge.svg && echo 'badge renders: passing' && python -c "import json; rs=[r for r in json.load(open('/tmp/runs.json'))['workflow_runs'] if r['name']=='Tests']; assert rs,'no Tests runs on master'; r=rs[0]; print('latest Tests on master:',r['conclusion'],r['created_at'],r['html_url'] cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c4 /tmp/v/bin/pip freeze && n=$(/tmp/v/bin/pip freeze | grep -vi '^schedule==' | wc -l); echo "extra_packages=$n"; test "$n" -eq 0 && /tmp/v/bin/pip show schedule | grep -E '^Requires: *$' && echo 'Requires: (empty) confirmed' && du -sh /tmp/v/lib/python*/site-packages/schedule cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c5 python -c "import schedule
def job():
    print(\"I'm working...\")
schedule.every(10).seconds.do(job)
n=len(schedule.get_jobs()); print('registered jobs:', n); assert n==1" cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c6 python -c "import schedule
def job():
    print(\"I'm working...\")
j=schedule.every().day.at('10:30').do(job)
print('next_run:', j.next_run); assert j.next_run.hour==10 and j.next_run.minute==30; print('ok')" cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c7 /tmp/vtz/bin/pip freeze && ! /tmp/vtz/bin/pip show pytz >/dev/null 2>&1 && echo 'pytz absent (fresh env confirmed)' && /tmp/vtz/bin/python -c "import schedule
def job():
    print(\"I'm working...\")
try:
    j=schedule.every().day.at('12:42', 'Europe/Amsterdam').do(job)
    print('RESULT: works out of the box; next_run', j.next_run)
except Exception as e:
    print('RESULT: raised', type(e).__nam cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c8 python -c "import schedule
def job():
    print(\"I'm working...\")
j=schedule.eve
```

## Step 4, ADJUDICATE: votes -> verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`, phase_a_tail: 'Successfully installed schedule-1.2.2'; stderr: "AttributeError: module 'sc |
| c2 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c2`, stdout shows only 'python-version: 3.11' for needs/docs/formatting/setuppy jobs; the test  |
| c3 | refuted / refuted / refuted | **refuted** | high | `p-c3`, stdout: 'no status' (badge SVG renders 'no status', not 'passing'; grep -q 'passing' faile |
| c4 | verified / verified / verified | **verified** | high | `p-c4`, stdout: 'schedule==1.2.2' / 'extra_packages=0' / 'Requires: (empty) confirmed' / '80K .../ |
| c5 | verified / verified / verified | **verified** | high | `p-c5`, stdout: 'registered jobs: 1'; exit_code 0 |
| c6 | verified / verified / verified | **verified** | high | `p-c6`, stdout: 'next_run: 2026-08-29 10:30:00' / 'ok'; exit_code 0 |
| c7 | refuted / refuted / refuted | **refuted** | high | `p-c7`, stdout: 'pytz absent (fresh env confirmed)' / "RESULT: raised ModuleNotFoundError: No modu |
| c8 | verified / verified / verified | **verified** | high | `p-c8`, stdout: 'next_run: 2026-08-28 20:28:17' / 'ok' (second==17 asserted); exit_code 0 |
| c9 | verified / verified / verified | **verified** | high | `p-c9`, stdout: 'job invoked 1 time(s) after 1.2s' (and not invoked before due); exit_code 0 |
| c10 | verified / verified / verified | **verified** | high | `p-c10`, stdout: 'PyPI latest: 1.2.2' / '1.2.2 uploaded: 2024-05-25T18:41:59'; exit_code 0 |

## Step 5, REPORT
Overall score 75 · escalated to human: ['c2'] · model calls: nominal 4

_Human checkpoint: the verdicts above were audited against ground truth; disagreements were read from the recorded probe output and resolved in favour of the evidence (CHANGELOG 'Truth audit')._