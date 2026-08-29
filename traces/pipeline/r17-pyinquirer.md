# Pipeline trajectory: r17-pyinquirer (proof `advanced-v3-ext-rescored-1788028882`)

Repository https://github.com/CITGuru/PyInquirer @ `7637373429be`. Buyer question: _An internal CLI tool we are inheriting depends on PyInquirer for its interactive prompts — does the README's pip install path and quickstart import still work on a current Python, is the documented prompt_toolkit workaround valid, is the CI badge real, and is the project maintained?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The command `pip install PyInquirer` completes successfully on a current Python (resolving and installing the package and its declared dependencies).
- **c2** (quickstart): After `pip install PyInquirer`, the README quickstart import `from PyInquirer import prompt, print_json` succeeds on a current Python interpreter.
- **c3** (install): If a prompt_toolkit error is encountered, installing the version the README prescribes with `pip install prompt_toolkit==1.0.14` resolves it and makes PyInquirer importable.
- **c4** (interface): With PyInquirer importable, `prompt(questions)` for a list containing one `{'type': 'input', 'name': 'first_name', 'message': ...}` question returns a dict keyed by 'first_name', which `print_json(answers)` prints as JSON.
- **c5** (interface): The repository ships example scripts editor.py, expand.py, list.py, password.py, when.py, checkbox.py, confirm.py, hierarchical.py, pizza.py, input.py and rawlist.py under ./examples/.
- **c6** (install): Running `pip install -e .` inside a clone of the repository yields a working from-source install in which the quickstart import `from PyInquirer import prompt, print_json` succeeds, so the examples can be launched with repository code.
- **c7** (interface): PyInquirer supports the question types input, confirm, list, rawlist, expand, checkbox, password and editor (one prompt implementation per type).
- **c8** (test_ci): The Travis CI badge in the README (travis-ci.org/expobrain/PyInquirer, branch master) asserts a live, passing CI build for the project.
- **c9** (test_ci): The documented contributor flow — `pip install -r requirements.txt`, `pip install -r requirements_dev.txt`, then `pytest -sv tests/` in a clone — installs cleanly and the test suite passes on a current Python.
- **c10** (environment): The project is looking for a successor/maintainer, as announced in GitHub issue #159 on CITGuru/PyInquirer (i.e. the issue exists and is still open).
- **c11** (environment): PyInquirer 1.0.3 is the current bugfix release, published at github.com/CITGuru/PyInquirer/releases/tag/1.0.3 and matching the latest version on PyPI.

## Step 2: PLAN output, 11 probes (`eval/probes/r17-pyinquirer-r1.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `on`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --quiet --upgrade pip`
  - commands: `python3 --version && /tmp/v/bin/pip install PyInquirer > /tmp/pip.log 2>&1; rc=$?; tail -15 /tmp/pip.log; echo "pip exit: $rc"; /tmp/v/bin/pip list 2>/dev/null | grep -i -E 'pyinquirer|prompt|pygments'; test $rc -eq 0 && echo "VERDICT_LINE: PASS pip install PyInquirer exited 0 on $(python3 --version`
- `p-c2` image `python:3.11-slim` network `on`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --quiet PyInquirer`
  - commands: `python3 --version && /tmp/v/bin/python -c 'import prompt_toolkit; print("installed prompt_toolkit", prompt_toolkit.__version__)' || echo 'prompt_toolkit itself does not import' && /tmp/v/bin/python -c 'from PyInquirer import prompt, print_json; print("import ok:", prompt, print_json)' > /tmp/imp.log`
- `p-c3` image `python:3.11-slim` network `on`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --quiet PyInquirer && /tmp/v/bin/pip install --quiet prompt_toolkit==1.0.14`
  - commands: `python3 --version && /tmp/v/bin/pip show prompt_toolkit | grep -i version && echo 'from_dict.py line 9:'; sed -n 9p /tmp/v/lib/python3.11/site-packages/prompt_toolkit/styles/from_dict.py && /tmp/v/bin/python -c 'import prompt_toolkit.styles.from_dict; from PyInquirer import prompt, print_json; print`
- `p-c4` image `python:3.9-slim` network `on`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --quiet PyInquirer && printf '%s\n' 'from __future__ import print_function, unicode_literals' 'from PyInquirer import prompt, print_json' 'questions = [{"type": "input", "name": "first_name", "message": "What is your first name"}]' 'answers = prompt(q`
  - commands: `python3 --version && /tmp/v/bin/python -c 'from PyInquirer import prompt, print_json; print("premise: import ok")' || echo 'premise: PyInquirer not importable on this interpreter' && timeout 60 python3 /tmp/d.py && echo 'VERDICT_LINE: PASS quickstart prompt() returned dict keyed first_name and print`
- `p-c5` image `python:3.11-slim` network `on`
  - setup: `python3 -c 'import urllib.request, tarfile; urllib.request.urlretrieve("https://github.com/CITGuru/PyInquirer/archive/7637373429bec66788650cda8091b7a6f12929ee.tar.gz", "/tmp/src.tgz"); tarfile.open("/tmp/src.tgz").extractall("/tmp")' && mv /tmp/PyInquirer-7637373429bec66788650cda8091b7a6f12929ee /tm`
  - commands: `ls /tmp/pyinq/examples && cd /tmp/pyinq && python3 -c 'import os; want=["editor.py","expand.py","list.py","password.py","when.py","checkbox.py","confirm.py","hierarchical.py","pizza.py","input.py","rawlist.py"]; missing=[f for f in want if not os.path.isfile("examples/"+f)]; print("missing examples:`
- `p-c6` image `python:3.11-slim` network `on`
  - setup: `python3 -c 'import urllib.request, tarfile; urllib.request.urlretrieve("https://github.com/CITGuru/PyInquirer/archive/7637373429bec66788650cda8091b7a6f12929ee.tar.gz", "/tmp/src.tgz"); tarfile.open("/tmp/src.tgz").extractall("/tmp")' && mv /tmp/PyInquirer-7637373429bec66788650cda8091b7a6f12929ee /tm`
  - commands: `cd /tmp/pyinq && .v/bin/pip install -e . > /tmp/pip.log 2>&1; rc=$?; tail -5 /tmp/pip.log; echo "pip install -e . exit: $rc"; test $rc -eq 0 || { echo 'VERDICT_LINE: FAIL pip install -e . failed'; exit 1; } && cd /tmp/pyinq && .v/bin/pip show prompt_toolkit | grep -i version; echo '--- PyInquirer/__`
- `p-c7` image `python:3.11-slim` network `on`
  - setup: `python3 -c 'import urllib.request, tarfile; urllib.request.urlretrieve("https://github.com/CITGuru/PyInquirer/archive/7637373429bec66788650cda8091b7a6f12929ee.tar.gz", "/tmp/src.tgz"); tarfile.open("/tmp/src.tgz").extractall("/tmp")' && mv /tmp/PyInquirer-7637373429bec66788650cda8091b7a6f12929ee /tm`
  - commands: `ls /tmp/pyinq/PyInquirer/prompts && cd /tmp/pyinq && .v/bin/pip show prompt_toolkit | grep -i version && cd /tmp/pyinq && .v/bin/python /tmp/types.py && echo 'VERDICT_LINE: PASS one prompt module per documented type exists and imports with the repo-declared prompt_toolkit' || echo 'VERDICT_LINE: FAI`
- `p-c8` image `python:3.11-slim` network `on`
  - setup: `printf '%s\n' 'import urllib.request, urllib.error, sys' 'u = "https://travis-ci.org/expobrain/PyInquirer.svg?branch=master"' 'try:' '    r = urllib.request.urlopen(u, timeout=30)' '    code, final, body = r.status, r.geturl(), r.read().decode(errors="replace")' 'except urllib.error.HTTPError as e:'`
  - commands: `echo 'note: badge owner is expobrain, repo owner is CITGuru' && python3 /tmp/badge.py && echo 'VERDICT_LINE: PASS travis-ci.org badge returns 200 with a passing build' || echo 'VERDICT_LINE: FAIL travis-ci.org badge is not a live passing build (see status/final_url/body_head)'`
- `p-c9` image `python:3.11-slim` network `on`
  - setup: `python3 -c 'import urllib.request, tarfile; urllib.request.urlretrieve("https://github.com/CITGuru/PyInquirer/archive/7637373429bec66788650cda8091b7a6f12929ee.tar.gz", "/tmp/src.tgz"); tarfile.open("/tmp/src.tgz").extractall("/tmp")' && mv /tmp/PyInquirer-7637373429bec66788650cda8091b7a6f12929ee /tm`
  - commands: `cd /tmp/pyinq && ls requirements.txt requirements_dev.txt && cat requirements.txt requirements_dev.txt && cd /tmp/pyinq && venv/bin/pip install -r requirements.txt > /tmp/req.log 2>&1; rc=$?; tail -3 /tmp/req.log; echo "pip install -r requirements.txt exit: $rc"; test $rc -eq 0 || { echo 'VERDICT_LI`
- `p-c10` image `python:3.11-slim` network `on`
  - setup: `printf '%s\n' 'import urllib.request, urllib.error, json, sys' 'h = {"Accept": "application/vnd.github+json", "User-Agent": "repo-probe"}' 'try:' '    d = json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/CITGuru/PyInquirer/issues/159", headers=h), timeout=30))' '`
  - commands: `python3 /tmp/issue.py && echo 'VERDICT_LINE: PASS issue #159 exists and is still open (see title above)' || echo 'VERDICT_LINE: FAIL issue #159 missing or not open'`
- `p-c11` image `python:3.11-slim` network `on`
  - setup: `printf '%s\n' 'import urllib.request, urllib.error, json, sys' 'h = {"Accept": "application/vnd.github+json", "User-Agent": "repo-probe"}' 'try:' '    rel = json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/CITGuru/PyInquirer/releases/tags/1.0.3", headers=h), time`
  - commands: `python3 /tmp/rel.py && echo 'VERDICT_LINE: PASS GitHub release 1.0.3 exists and PyPI latest is 1.0.3' || echo 'VERDICT_LINE: FAIL release 1.0.3 missing on GitHub or PyPI latest differs (see values above)'`

## Step 3: EXECUTE on GitHub Actions, run `33268091019` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 python3 --version && /tmp/v/bin/pip install PyInquirer > /tmp/pip.log 2>&1; rc=$?; tail -15 /tmp/pip.log; echo "pip exit: $rc"; /tmp/v/bin/pip list 2>/dev/null | grep -i -E 'pyinquirer|prompt|pygments'; test $rc -eq 0 && echo "VERDICT_LINE: PASS pip install PyInquirer exited 0 on $(python3 --version)" || echo "VERDICT_LINE: FAIL pip install PyInquirer exited $rc"
STDOUT Python 3.11.16
Downloading pygments-2.21.0-py3-none-any.whl (1.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 150.4 MB/s  0:00:00
Downloading regex-2026.7.19-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (801 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 801.4/801.4 kB 111.8 MB/s  0:00:00
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading wcwidth-0.8.3-py3-none-any.whl (331 kB)
Building wheels for collected packages: PyInquirer
  Building wheel for PyInquirer (pyproject.toml): started
  Building wheel for PyInquirer (pyproject.toml): finished with status 'done'
  Created wheel for PyInquirer: filename=pyinquirer-1.0.3-py3-none-any.whl size=32932 sha256=e83daf5e0a7a08809a073ee6705c3e779af9614a89bf3d103ba38947c65635c1
  Stored in directory: /root/.cache/pip/wheels/71/36/59/9490e21174d4aee949c0bd8851310b82108f2569e12a3998d5
Successfully built PyInquirer
Installing collected packages: wcwidth, six, regex, Pygments, prompt_toolkit, PyInquirer

Successfully installed PyInquirer-1.0.3 Pygments-2.21.0 prompt_toolkit-1.0.14 regex-2026.7.19 six-1.17.0 wcwidth-0.8.3
pip exit: 0
prompt-toolkit 1.0.14
Pygments       2.21.0
PyInquirer     1.0.3
VERDICT_LINE: PASS pip install PyInquirer exited 0 on Python 3.11.16

STDERR 
PHASE_A 
--stderr--
Unable to find image 'python:3.11-slim' locally
3.11-slim: Pulling from library/python
6310eb16bf42: Pulling fs layer
87e1b7cce023: Pulling fs layer
c86306e32cd0: Pulling fs layer
a14578096eda: Pulling fs layer
a14578096eda: Waiting
87e1b7cce023: Verifying Checksum
c86306e32cd0: Verifying Checksum
c86306e32cd0: Download complete
6310eb16bf42: Verifying Checksum
6310eb16bf42: Download complete
a14578096eda: Verifying Checksum
a14578096eda: Download complete
6310eb16bf42: Pull complete
87e1b7cce023: Pull complete
c86306e32cd0: Pull complete
a14578096eda: Pull complete
Digest: sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6
Status: Downloaded newer image for python:3.11-slim

EXIT 0
p-c10 python3 /tmp/issue.py && echo 'VERDICT_LINE: PASS issue #159 exists and is still open (see title above)' || echo 'VERDICT_LINE: FAIL issue #159 missing or not open'
STDOUT issue #159 title: Inviting A Successor/Maintainer To PyInquirer Future | state: open | created: 2021-04-14T16:33:32Z | comments: 8
repo pushed_at: 2024-03-02T09:32:55Z | archived: False
VERDICT_LINE: PASS issue #159 exists and is still open (see title above)

STDERR 
PHASE_A 
--stderr--

EXIT 0
p-c11 python3 /tmp/rel.py && echo 'VERDICT_LINE: PASS GitHub release 1.0.3 exists and PyPI latest is 1.0.3' || echo 'VERDICT
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: Successfully installed PyInquirer-1.0.3 Pygments-2.21.0 prompt_toolkit-1.0.14 regex-2026.7 |
| c2 | refuted / refuted / refuted | **unverifiable** | low | `p-c2`: ImportError: cannot import name 'Mapping' from 'collections' (/usr/local/lib/python3.11/co |
| c3 | refuted / refuted / refuted | **unverifiable** | low | `p-c3`: Version: 1.0.14 / from_dict.py line 9: from collections import Mapping / ImportError: cann |
| c4 | verified / verified / unverifiable | **verified** | low | `p-c4`: '\x1b[94m"first_name"\x1b[39;49;00m:\x1b[37m ' '\x1b[39;49;00m\x1b[33m"Bob"' / observed fi |
| c5 | verified / verified / verified | **verified** | high | `p-c5`: missing examples: [] / VERDICT_LINE: PASS all 11 listed example scripts exist under ./exam |
| c6 | verified / verified / verified | **verified** | high | `p-c6`: import ok: <module 'PyInquirer.prompt' from '/tmp/pyinq/PyInquirer/prompt.py'> <function p |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: prompt modules present: ['input', 'confirm', 'list', 'rawlist', 'expand', 'checkbox', 'pas |
| c8 | refuted / refuted / refuted | **refuted** | high | `p-c8`: badge status: 403 / final_url: https://travis-ci.org/expobrain/PyInquirer.svg?branch=maste |
| c9 | refuted / refuted / unverifiable | **refuted** | low | `p-c9`: pip install -r requirements_dev.txt exit: 0 / then pytest failure display: '    stdin.file |
| c10 | verified / verified / verified | **verified** | high | `p-c10`: issue #159 title: Inviting A Successor/Maintainer To PyInquirer Future / state: open / cre |
| c11 | verified / verified / verified | **verified** | high | `p-c11`: github release tag 1.0.3 exists: True published_at: 2018-11-22T12:33:26Z / pypi latest ver |

## Step 5: REPORT
Overall score 73. Escalated to a human: ['c2', 'c3']. Model calls: 4. Verdicts disagreeing with audited truth: c2, c3, c4, c6, c9.

Human checkpoint for this repository: no truth entry was changed after this run.