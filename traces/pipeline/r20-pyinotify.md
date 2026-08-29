# Pipeline trajectory: r20-pyinotify (proof `advanced-v3-ext-rescored-1788028882`)

Repository https://github.com/seb-m/pyinotify @ `0f3f8950d12e`. Buyer question: _A file-sync daemon we are taking over uses pyinotify for filesystem watching — does the README's install path still produce an importable module on a current Python 3, does the documented `python -m pyinotify` watcher run, is the Python-version support statement true, and do the documentation links still resolve?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The package can be installed from PyPI with `pip install pyinotify` (the README uses `sudo pip install pyinotify`) on a current Python — the sdist builds and pip reports success.
- **c2** (environment): pyinotify supports Python >= 2.4 including any Python 3.x: after installation, `import pyinotify` succeeds on a current Python 3 interpreter.
- **c3** (environment): pyinotify requires Linux (kernel >= 2.6.13, i.e. inotify support); its setup.py refuses to install on non-Linux platforms.
- **c4** (install): pyinotify can be installed from a source checkout with `sudo pythonXXX setup.py install` (XXX = the chosen interpreter, e.g. python3) on a current Python 3.
- **c5** (quickstart): With pyinotify installed, `python -m pyinotify -v /my-dir-to-watch` watches the given directory and prints filesystem events as they occur.
- **c6** (environment): pyinotify is released under the MIT license (repository COPYING file and PyPI metadata both say MIT).
- **c7** (interface): The API documentation link given in the README, http://seb-m.github.com/pyinotify, resolves to a live documentation page.
- **c8** (environment): The project wiki link given in the README, http://github.com/seb-m/pyinotify/wiki, resolves to an existing GitHub wiki.
- **c9** (quantitative): The version distributed on PyPI as the 'current stable version' is 0.9.6, matching `__version__` in python3/pyinotify.py at the pinned commit.

## Step 2: PLAN output, 9 probes (`eval/probes/r20-pyinotify.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.13-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/python -V`
  - commands: `/tmp/v/bin/pip install pyinotify > /tmp/pip.log 2>&1; rc=$?; tail -8 /tmp/pip.log; echo "observed: pip_exit=$rc installed=$(/tmp/v/bin/pip show pyinotify 2>/dev/null | grep -m1 '^Version' || echo none)"; [ "$rc" = 0 ] && /tmp/v/bin/pip show pyinotify >/dev/null 2>&1 && echo "VERDICT_LINE: PASS pip i`
- `p-c2` image `python:3.13-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install pyinotify`
  - commands: `/tmp/v/bin/python -c 'import pyinotify; print("observed __version__:", pyinotify.__version__)' > /tmp/imp.log 2>&1; rc=$?; tail -4 /tmp/imp.log; echo "import_exit=$rc"; grep -q 'observed __version__' /tmp/imp.log && echo "VERDICT_LINE: PASS import pyinotify succeeds on $(/tmp/v/bin/python -V)" || ec`
- `p-c3` image `python:3.11-slim` network `on`
  - setup: `mkdir -p /tmp/src && python -c "import urllib.request; open('/tmp/src/setup.py','wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/seb-m/pyinotify/0f3f8950d12e4a6534320153eed1a90a778da4ae/setup.py', timeout=30).read())"`
  - commands: `cd /tmp/src && echo '--- guard in setup.py:' && grep -n -A2 'not platform.startswith' setup.py; echo "kernel: $(uname -r)"; ls /proc/sys/fs/inotify/ 2>&1; python -c "import distutils.util as u; u.get_platform=lambda: 'macosx-10.9-x86_64'; import sys; sys.argv=['setup.py','--name']; exec(open('setup.`
- `p-c4` image `python:3.13-slim` network `on`
  - setup: `python -c "import urllib.request,tarfile,io; d=urllib.request.urlopen('https://github.com/seb-m/pyinotify/archive/0f3f8950d12e4a6534320153eed1a90a778da4ae.tar.gz', timeout=60).read(); tarfile.open(fileobj=io.BytesIO(d)).extractall('/tmp'); print(len(d),'bytes')" && mv /tmp/pyinotify-0f3f8950d12e4a65`
  - commands: `cd /tmp/pyin && .v/bin/python setup.py install > /tmp/inst.log 2>&1; rc=$?; tail -6 /tmp/inst.log; echo "setup_py_install_exit=$rc"; .v/bin/python -c 'import pyinotify; print("observed: installed __version__", pyinotify.__version__)' > /tmp/imp.log 2>&1; irc=$?; tail -2 /tmp/imp.log; [ "$rc" = 0 ] &`
- `p-c5` image `python:3.13-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install pyinotify && mkdir -p /my-dir-to-watch`
  - commands: `(timeout 8 /tmp/v/bin/python -m pyinotify -v /my-dir-to-watch > /tmp/watch.log 2>&1 &); sleep 3; touch /my-dir-to-watch/x; echo hi > /my-dir-to-watch/x; sleep 6; echo '--- watcher output (head):'; head -20 /tmp/watch.log; /tmp/v/bin/python -c "s=open('/tmp/watch.log').read(); print('observed: IN_CRE`
- `p-c6` image `python:3.13-slim` network `on`
  - setup: ``
  - commands: `python - <<'EOF'
import json, urllib.request
def get(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'probe/1'}), timeout=20)
    return r.status, r.read()
try:
    s1, b1 = get('https://api.github.com/repos/seb-m/pyinotify/license'); gh = json.loads(b1)['license'`
- `p-c7` image `python:3.13-slim` network `on`
  - setup: ``
  - commands: `python - <<'EOF'
import urllib.request, urllib.error, re
url = 'http://seb-m.github.com/pyinotify'
try:
    r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'probe/1'}), timeout=20)
    body = r.read().decode('utf-8', 'replace')
    title = re.search(r'<title>(.*?)</titl`
- `p-c8` image `python:3.13-slim` network `on`
  - setup: ``
  - commands: `python - <<'EOF'
import json, urllib.request, urllib.error
hdr = {'User-Agent': 'probe/1'}
try:
    api = json.loads(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/seb-m/pyinotify', headers=hdr), timeout=20).read())
    has_wiki = api.get('has_wiki')
except Exception as `
- `p-c9` image `python:3.13-slim` network `on`
  - setup: ``
  - commands: `python - <<'EOF'
import json, re, urllib.request
hdr = {'User-Agent': 'probe/1'}
try:
    d = json.loads(urllib.request.urlopen(urllib.request.Request('https://pypi.org/pypi/pyinotify/json', headers=hdr), timeout=20).read())
    pv = d['info']['version']
    files = d['releases'].get(pv, [])
    upl`

## Step 3: EXECUTE on GitHub Actions, run `33266463031` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 /tmp/v/bin/pip install pyinotify > /tmp/pip.log 2>&1; rc=$?; tail -8 /tmp/pip.log; echo "observed: pip_exit=$rc installed=$(/tmp/v/bin/pip show pyinotify 2>/dev/null | grep -m1 '^Version' || echo none)"; [ "$rc" = 0 ] && /tmp/v/bin/pip show pyinotify >/dev/null 2>&1 && echo "VERDICT_LINE: PASS pip install pyinotify exited 0 on $(/tmp/v/bin/python -V) and pip show finds it" || echo "VERDICT_LINE: FAIL pip install pyinotify exited $rc on $(/tmp/v/bin/python -V) (see log tail above)"
STDOUT Building wheels for collected packages: pyinotify
  Building wheel for pyinotify (pyproject.toml): started
  Building wheel for pyinotify (pyproject.toml): finished with status 'done'
  Created wheel for pyinotify: filename=pyinotify-0.9.6-py3-none-any.whl size=25418 sha256=ab467c6d2974c5122885a77005a19d78f24e32509250533025253e25a27039cd
  Stored in directory: /root/.cache/pip/wheels/be/e0/29/d237cd80907dd5699eeee0237d136eae049d8edef6f5a6a6fa
Successfully built pyinotify
Installing collected packages: pyinotify
Successfully installed pyinotify-0.9.6
observed: pip_exit=0 installed=Version: 0.9.6
VERDICT_LINE: PASS pip install pyinotify exited 0 on Python 3.13.15 and pip show finds it

STDERR 
PHASE_A Python 3.13.15

--stderr--
Unable to find image 'python:3.13-slim' locally
3.13-slim: Pulling from library/python
6310eb16bf42: Pulling fs layer
64c7e6efa7cd: Pulling fs layer
357a46282089: Pulling fs layer
d64904dff413: Pulling fs layer
d64904dff413: Waiting
64c7e6efa7cd: Verifying Checksum
64c7e6efa7cd: Download complete
357a46282089: Verifying Checksum
357a46282089: Download complete
d64904dff413: Verifying Checksum
d64904dff413: Download complete
6310eb16bf42: Verifying Checksum
6310eb16bf42: Download complete
6310eb16bf42: Pull complete
64c7e6efa7cd: Pull complete
357a46282089: Pull complete
d64904dff413: Pull complete
Digest: sha256:7ce4b6dfe35e55397b7cda544f8a13f191b7ae28dc5aad71fe664dbc9bc2623f
Status: Downloaded newer image for python:3.13-slim

EXIT 0
p-c2 /tmp/v/bin/python -c 'import pyinotify; print("observed __version__:", pyinotify.__version__)' > /tmp/imp.log 2>&1; rc=$?; tail -4 /tmp/imp.log; echo "import_exit=$rc"; grep -q 'observed __version__' /tmp/imp.log && echo "VERDICT_LINE: PASS import pyinotify succeeds on $(/tmp/v/bin/python -V)" || echo "VERDICT_LINE: FAIL import pyinotify on $(/tmp/v/bin/python -V) raised: $(tail -1 /tmp/imp.log)"
STDOUT     ^^^^^^^^^^^^^^^^
  File "/tmp/v/lib/python3.13/site-packages/pyinotify.py", line 71, in <module>
    import asyncore
ModuleNotFoundError: No module named 'asyncore'
import_exit=1
VERDICT_LINE: PASS import pyinotify succeeds on Python 3.13.15

STDERR 
PHASE_A ne'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: pyinotify
  Building wheel for pyinotify (pyproject.toml): started
  Build
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: Successfully installed pyinotify-0.9.6 / observed: pip_exit=0 installed=Version: 0.9.6 / V |
| c2 | refuted / refuted / refuted | **refuted** | high | `p-c2`: File "/tmp/v/lib/python3.13/site-packages/pyinotify.py", line 71, in <module>: import asyn |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: setup.py:28 if not platform.startswith('linux') and not platform.startswith('freebsd'): sy |
| c4 | refuted / refuted / refuted | **refuted** | high | `p-c4`: File "/tmp/pyin/setup.py", line 11, in <module>: import distutils.extension / ModuleNotFou |
| c5 | refuted / refuted / refuted | **refuted** | high | `p-c5`: python -m pyinotify -v /my-dir-to-watch -> ModuleNotFoundError: No module named 'asyncore' |
| c6 | verified / verified / verified | **verified** | high | `p-c6`: observed: github_spdx='MIT' pypi_license='MIT License' COPYING_has_MIT_grant=True / VERDIC |
| c7 | refuted / refuted / refuted | **refuted** | high | `p-c7`: VERDICT_LINE: FAIL http://seb-m.github.com/pyinotify unreachable: URLError(gaierror(-5, 'N |
| c8 | verified / verified / verified | **verified** | high | `p-c8`: observed: status=200 final_url=https://github.com/seb-m/pyinotify/wiki has_wiki=True page_ |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: observed: pypi_version='0.9.6' uploaded='2015-06-04T15:50:23' repo_python3_version='0.9.6' |

## Step 5: REPORT
Overall score 56. Escalated to a human: none. Model calls: 4. Verdicts disagreeing with audited truth: none.

Human checkpoint for this repository: no truth entry was changed after this run.