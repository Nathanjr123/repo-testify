# Pipeline trajectory: r03-funcy (proof `advanced-v3-heldout-rescored-1788058984`)

Repository https://github.com/Suor/funcy @ `19e9617383cd`. Buyer question: _We are considering funcy as a utility dependency in a Python 3.12 codebase — is the README's stated Python support accurate and do its overview examples actually run as shown?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The package 'funcy' can be installed from PyPI with `pip install funcy`, after which `import funcy` succeeds.
- **c2** (environment): The 'funcy' package works with Python 3.4 and all later Python 3 versions, and with PyPy3.
- **c3** (quickstart): In Python with 'funcy' installed, `funcy.walk(str.upper, {'a', 'b'})` returns the set {'A', 'B'} (walk preserves the collection type).
- **c4** (quickstart): In Python with 'funcy' installed, `funcy.select(funcy.even, {1,2,3,10,20})` returns the set {2, 10, 20}.
- **c5** (quickstart): In Python with 'funcy' installed, `funcy.lsplit(funcy.odd, range(5))` returns the tuple ([1, 3], [0, 2, 4]).
- **c6** (quickstart): In Python with 'funcy' installed, `list(funcy.chunks(2, range(5)))` yields [[0, 1], [2, 3], [4]].
- **c7** (interface): In Python with 'funcy' installed, `funcy.curry(operator.add)(1)(2)` returns 3.
- **c8** (interface): In Python with 'funcy' installed, `funcy.walk_values(funcy.silent(int), {'a': '1', 'b': 'no'})` returns {'a': 1, 'b': None} (silent swallows the ValueError and yields None).
- **c9** (test_ci): The funcy repository's test suite can be run by installing `pip install -r test_requirements.txt` and then invoking `pytest`, and the tests pass on a current default Python.
- **c10** (test_ci): The funcy README's Build Status badge (GitHub Actions workflows/test.yml, master branch) asserts that funcy's CI test workflow is currently passing on master.

## Step 2: PLAN output, 10 probes (`eval/probes/r03-funcy.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `on`
  - setup: `python3 -m pip install --quiet funcy`
  - commands: `python3 -c 'import sys, funcy; print("installed funcy", funcy.__version__, "on python", sys.version.split()[0])' && echo "VERDICT_LINE: PASS pip install funcy from PyPI succeeded and import funcy works" || echo "VERDICT_LINE: FAIL import funcy failed after pip install funcy"`
- `p-c2` image `python:3.4-slim` network `on`
  - setup: `python3 -m pip install --quiet funcy`
  - commands: `python3 -c 'import sys, funcy; from operator import add; from funcy import walk, select, even, curry, lsplit, odd; assert walk(str.upper, {"a","b"}) == {"A","B"}; assert select(even, {1,2,3,10,20}) == {2,10,20}; assert curry(add)(1)(2) == 3; assert tuple(lsplit(odd, range(5))) == ([1,3],[0,2,4]); pr`
- `p-c3` image `python:3.11-slim` network `none`
  - setup: `python3 -m pip install --quiet funcy`
  - commands: `python3 -c 'from funcy import walk; r = walk(str.upper, {"a", "b"}); print("observed", repr(r), type(r).__name__); assert r == {"A", "B"} and isinstance(r, set), r' && echo "VERDICT_LINE: PASS walk(str.upper, {a,b}) returned set {A,B}" || echo "VERDICT_LINE: FAIL walk did not return set {A,B}"`
- `p-c4` image `python:3.11-slim` network `none`
  - setup: `python3 -m pip install --quiet funcy`
  - commands: `python3 -c 'from funcy import select, even; r = select(even, {1,2,3,10,20}); print("observed", repr(r), type(r).__name__); assert r == {2,10,20} and isinstance(r, set), r' && echo "VERDICT_LINE: PASS select(even, {1,2,3,10,20}) returned set {2,10,20}" || echo "VERDICT_LINE: FAIL select(even, ...) di`
- `p-c5` image `python:3.11-slim` network `none`
  - setup: `python3 -m pip install --quiet funcy`
  - commands: `python3 -c 'from funcy import lsplit, odd; r = lsplit(odd, range(5)); print("observed", repr(r), type(r).__name__); assert tuple(r) == ([1, 3], [0, 2, 4]), r' && echo "VERDICT_LINE: PASS lsplit(odd, range(5)) returned ([1, 3], [0, 2, 4])" || echo "VERDICT_LINE: FAIL lsplit(odd, range(5)) did not ret`
- `p-c6` image `python:3.11-slim` network `none`
  - setup: `python3 -m pip install --quiet funcy`
  - commands: `python3 -c 'from funcy import chunks; it = chunks(2, range(5)); r = list(it); print("observed", repr(r), "from", type(it).__name__); assert r == [[0, 1], [2, 3], [4]], r' && echo "VERDICT_LINE: PASS list(chunks(2, range(5))) == [[0, 1], [2, 3], [4]]" || echo "VERDICT_LINE: FAIL chunks(2, range(5)) d`
- `p-c7` image `python:3.11-slim` network `none`
  - setup: `python3 -m pip install --quiet funcy`
  - commands: `python3 -c 'from operator import add; from funcy import curry; r = curry(add)(1)(2); print("observed", repr(r)); assert r == 3, r' && echo "VERDICT_LINE: PASS curry(add)(1)(2) == 3" || echo "VERDICT_LINE: FAIL curry(add)(1)(2) != 3"`
- `p-c8` image `python:3.11-slim` network `none`
  - setup: `python3 -m pip install --quiet funcy`
  - commands: `python3 -c 'from funcy import walk_values, silent; r = walk_values(silent(int), {"a": "1", "b": "no"}); print("observed", repr(r)); assert r == {"a": 1, "b": None}, r' && echo "VERDICT_LINE: PASS walk_values(silent(int), ...) returned {a: 1, b: None}" || echo "VERDICT_LINE: FAIL walk_values(silent(i`
- `p-c9` image `python:3.11-slim` network `on`
  - setup: `python3 -c 'import urllib.request; urllib.request.urlretrieve("https://github.com/Suor/funcy/archive/19e9617383cd48dfbc4074dab11df9157ece98b0.tar.gz", "/tmp/funcy.tar.gz")' && mkdir -p /tmp/src && tar -xzf /tmp/funcy.tar.gz -C /tmp/src --strip-components=1 && cd /tmp/src && ls test_requirements.txt `
  - commands: `cd /tmp/src && python3 --version && pytest -q > /tmp/pytest.log 2>&1; rc=$?; tail -n 8 /tmp/pytest.log; echo "pytest exit code $rc"; if [ $rc -eq 0 ]; then echo "VERDICT_LINE: PASS pip install -r test_requirements.txt then pytest passed at pinned commit"; else echo "VERDICT_LINE: FAIL pytest exited `
- `p-c10` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python3 -c 'import urllib.request, json; r = urllib.request.urlopen(urllib.request.Request("https://github.com/Suor/funcy/actions/workflows/test.yml/badge.svg", headers={"User-Agent": "probe"}), timeout=30); svg = r.read().decode(); print("badge_http", r.status, "passing_in_svg", "passing" in svg, "`

## Step 3: EXECUTE on GitHub Actions, run `33269255643` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 python3 -c 'import sys, funcy; print("installed funcy", funcy.__version__, "on python", sys.version.split()[0])' && echo "VERDICT_LINE: PASS pip install funcy from PyPI succeeded and import funcy works" || echo "VERDICT_LINE: FAIL import funcy failed after pip install funcy"
STDOUT VERDICT_LINE: FAIL import funcy failed after pip install funcy

STDERR Traceback (most recent call last):
  File "<string>", line 1, in <module>
AttributeError: module 'funcy' has no attribute '__version__'

PHASE_A b7cce023: Download complete
6310eb16bf42: Verifying Checksum
6310eb16bf42: Download complete
a14578096eda: Verifying Checksum
a14578096eda: Download complete
c86306e32cd0: Verifying Checksum
c86306e32cd0: Download complete
6310eb16bf42: Pull complete
87e1b7cce023: Pull complete
c86306e32cd0: Pull complete
a14578096eda: Pull complete
Digest: sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6
Status: Downloaded newer image for python:3.11-slim
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: pip install --upgrade pip

EXIT 0
p-c10 python3 -c 'import urllib.request, json; r = urllib.request.urlopen(urllib.request.Request("https://github.com/Suor/funcy/actions/workflows/test.yml/badge.svg", headers={"User-Agent": "probe"}), timeout=30); svg = r.read().decode(); print("badge_http", r.status, "passing_in_svg", "passing" in svg, "failing_in_svg", "failing" in svg); a = urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/Suor/funcy/actions/workflows/test.yml/runs?branch=master&per_page=3", headers={"User-Agent": "probe", "Accept": "application/vnd.github+json"}), timeout=30); d = json.load(a); runs = [
STDOUT badge_http 200 passing_in_svg False failing_in_svg True
latest_master_runs [('19e9617', 'cancelled', '2026-08-17T01:46:50Z'), ('2c9535a', 'cancelled', '2026-07-03T16:31:20Z'), ('9eb0447', 'cancelled', '2026-02-26T04:14:02Z')]
VERDICT_LINE: FAIL badge not passing or latest master test.yml run not success (see values above)

STDERR Traceback (most recent call last):
  File "<string>", line 1, in <module>
AssertionError: ('<svg xmlns="http://www.w3.org/2000/svg" width="83" height="20">\n  <title>CI - failing</title>\n  <defs>\n    <linearGradient id="workflow-fill" x1="50%" y1="0%" x2="50%" y2="100%">\n      <stop stop-colo', [('19e9617', 'cancelled', '2026-08-17T01:46:50Z'), ('2c9535a', 'cancelled', '2026-07-03T16:31:20Z'), ('9eb0447', 'cancelled', '2026-02-26T04:14:02Z')])

PHASE_A 
--stderr--

EXIT 0
p-c2 python3 -c 'import sys, funcy; from operator import add; from funcy import walk, select, even, curry, lsplit, odd; assert walk(str.upper, {"a","b"}) == {"A","B"}; assert select(even, {1,2,3,10,20}) == {2,10,20}; assert curry(add)(1)(2) == 3; assert tuple(ls
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: VERDICT_LINE: FAIL is overridden by the probe's own stderr: `AttributeError: module 'funcy |
| c2 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c2`: On python:3.4-slim pip install succeeded (phase A: pip 19.0.3, 3.4 deprecation notice only |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: `observed {'A', 'B'} set` / `VERDICT_LINE: PASS walk(str.upper, {a,b}) returned set {A,B}` |
| c4 | verified / verified / verified | **verified** | high | `p-c4`: `observed {2, 10, 20} set` / `VERDICT_LINE: PASS select(even, {1,2,3,10,20}) returned set  |
| c5 | verified / verified / verified | **verified** | high | `p-c5`: `observed ([1, 3], [0, 2, 4]) tuple` / `VERDICT_LINE: PASS lsplit(odd, range(5)) returned  |
| c6 | refuted / refuted / refuted | **refuted** | low | `p-c6`: `observed [range(0, 2), range(2, 4), range(4, 5)] from generator` / `AssertionError: [rang |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: `observed 3` / `VERDICT_LINE: PASS curry(add)(1)(2) == 3`; exit_code 0. |
| c8 | verified / verified / verified | **verified** | high | `p-c8`: `observed {'a': 1, 'b': None}` / `VERDICT_LINE: PASS walk_values(silent(int), ...) returne |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: Phase A installed test_requirements.txt as documented (tail shows `whatever==0.7`, `typing |
| c10 | refuted / refuted / refuted | **refuted** | high | `p-c10`: `badge_http 200 passing_in_svg False failing_in_svg True` (stderr shows the SVG title `CI  |

## Step 5: REPORT
Overall score 75. Escalated to a human: ['c2']. Model calls: 4. Verdicts disagreeing with audited truth: c2.

Human checkpoint for this repository: c2: was refuted; On python:3.4-slim pip install succeeded and the four assertions passed (recorded by advanced-v3-heldout probe p-c2): the 'Python 3.4+' claim holds. Draft had guessed refuted; the arm abstained. Against the pipeline's verdict.; c6: was verified; README chunks example: executing it yields range objects from a generator, not the documented lists (recorded by advanced-v3-heldout probe p-c6). Toward the pipeline.; c9: was unverifiable; test_requirements.txt installed as documented and tests ran (recorded by advanced-v3-heldout probe p-c9). Toward the pipeline.