# Pipeline trajectory, r02-python-tabulate (proof `advanced-v2-1787952546`)

Repository https://github.com/astanin/python-tabulate @ `268615a5c27d` · buyer question: _We plan to standardize on tabulate for CLI table output across our internal tools — do the README's install story (library + command-line utility), example outputs, and performance claims hold up?_

## Step 1, instructions
See `arms/PROMPTS.md` (PLAN -> EXECUTE -> ADJUDICATE). Claims given to the agent:

- **c1** (install): The package 'tabulate' can be installed from PyPI with `pip install tabulate`, after which `from tabulate import tabulate` succeeds.
- **c2** (install): Installing the 'tabulate' package with pip on Linux also installs a command-line utility named `tabulate` onto the PATH (in the environment's bin directory).
- **c3** (install): Setting the environment variable TABULATE_INSTALL=lib-only during `pip install tabulate` installs only the library, without the `tabulate` command-line script.
- **c4** (environment): The 'tabulate' package is a Python 3 library (no Python 2 support); its current PyPI release declares requires-python >=3.10.
- **c5** (quickstart): In Python with 'tabulate' installed, `print(tabulate([["Sun",696000,1989100000],["Earth",6371,5973.6],["Moon",1737,73.5],["Mars",3390,641.85]]))` prints a simple-format table whose first data line is 'Sun    696000     1.9891e+09'.
- **c6** (interface): In Python with 'tabulate' installed, calling tabulate with headers="firstrow" on [["Name","Age"],["Alice",24],["Bob",19]] uses the first row as the header, producing lines 'Name      Age' and 'Alice      24'.
- **c7** (interface): In Python with 'tabulate' installed, passing a dict of iterables with headers="keys" uses the dictionary keys as column headers: tabulate({"Name": ["Alice", "Bob"], "Age": [24, 19]}, headers="keys") starts with 'Name      Age'.
- **c8** (interface): The `tabulate` command-line utility's --help output lists 'github', 'grid', 'html', 'latex', 'pipe', 'rst', 'simple', and 'tsv' among the supported output formats for the -f/--format option.
- **c9** (install): Installing the extra `pip install tabulate[widechars]` enables wide-character (East-Asian) alignment support via the wcwidth dependency.
- **c10** (test_ci): The python-tabulate README's GitHub Actions badge (workflows/tabulate.yml) asserts that the repository's CI workflow on astanin/python-tabulate is currently passing.
- **c11** (quantitative): In a mini-benchmark on a 10x10 table of mixed text and numeric data, the tabulate library formats the table faster than PrettyTable and texttable (README cites tabulate 0.10.0 at 553.4 μs vs PrettyTable 3.17.0 at 468.0 μs and texttable 1.7.0 at 1071.4 μs on Python 3.13.7/Windows 11 — note the table itself shows PrettyTable FASTER than tabulate).

## Step 2, PLAN output: 11 probes (committed as `eval/probes/r02-python-tabulate-r1.json`; matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --quiet tabulate`
  - commands: `/tmp/v/bin/python - <<'EOF' || echo "VERDICT_LINE: FAIL import or install crashed"
try:
    from tabulate import tabulate
    import tabulate as t
    print('observed: tabulate version', t.__version__, 'callable', callable(tabulate))
    print('VERDICT_LINE: PASS pip install tabulate + from tabulate`
- `p-c2` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --quiet tabulate`
  - commands: `ls -l /tmp/v/bin/tabulate 2>&1 && if test -x /tmp/v/bin/tabulate; then OUT=$(printf '1 2\n3 4\n' | /tmp/v/bin/tabulate 2>&1); RC=$?; echo "observed: rc=$RC output=$(echo "$OUT" | tr '\n' '|')"; if [ $RC -eq 0 ] && echo "$OUT" | grep -q '^ *1 *2'; then echo 'VERDICT_LINE: PASS bin/tabulate exists, ex`
- `p-c3` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v2 && TABULATE_INSTALL=lib-only /tmp/v2/bin/pip install --quiet tabulate`
  - commands: `/tmp/v2/bin/python -c 'import tabulate; print("observed: library importable, version", tabulate.__version__)' || echo 'observed: library NOT importable' && N=$(ls /tmp/v2/bin 2>/dev/null | grep -c '^tabulate$'); echo "observed: tabulate scripts in venv bin = $N (README says lib-only should install n`
- `p-c4` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed (network?)"
import json, urllib.request
try:
    req = urllib.request.Request('https://pypi.org/pypi/tabulate/json', headers={'User-Agent': 'claim-probe'})
    with urllib.request.urlopen(req, timeout=30) as r:
        status = r.status
   `
- `p-c5` image `python:3.11-slim` network `install-only`
  - setup: `pip install --quiet tabulate`
  - commands: `python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed"
from tabulate import tabulate
table = [["Sun",696000,1989100000],["Earth",6371,5973.6],
         ["Moon",1737,73.5],["Mars",3390,641.85]]
out = tabulate(table)
print(out)
lines = out.splitlines()
expected = ['-----  ------  -------------',`
- `p-c6` image `python:3.11-slim` network `install-only`
  - setup: `pip install --quiet tabulate`
  - commands: `python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed"
from tabulate import tabulate
out = tabulate([["Name","Age"],["Alice",24],["Bob",19]],
               headers="firstrow")
print(out)
lines = out.splitlines()
expected = ['Name      Age', '------  -----', 'Alice      24', 'Bob        19']
p`
- `p-c7` image `python:3.11-slim` network `install-only`
  - setup: `pip install --quiet tabulate`
  - commands: `python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed"
from tabulate import tabulate
out = tabulate({"Name": ["Alice", "Bob"],
                "Age": [24, 19]}, headers="keys")
print(out)
lines = out.splitlines()
expected = ['Name      Age', '------  -----', 'Alice      24', 'Bob        19']
p`
- `p-c8` image `python:3.11-slim` network `install-only`
  - setup: `pip install --quiet tabulate`
  - commands: `python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed"
import re, shutil, subprocess
exe = shutil.which('tabulate')
print('observed: tabulate on PATH =', exe)
if not exe:
    print('VERDICT_LINE: FAIL tabulate CLI not on PATH')
    raise SystemExit(0)
p = subprocess.run([exe, '--help'], captur`
- `p-c9` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v3 && /tmp/v3/bin/pip install --quiet 'tabulate[widechars]'`
  - commands: `/tmp/v3/bin/python - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed"
try:
    import wcwidth
except ImportError as e:
    print('observed: wcwidth missing', e)
    print('VERDICT_LINE: FAIL tabulate[widechars] did not install wcwidth')
    raise SystemExit(0)
import tabulate as t
from tabulate im`
- `p-c10` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed (network?)"
import json, urllib.request, urllib.error
UA = {'User-Agent': 'claim-probe', 'Accept': 'application/vnd.github+json'}
badge_url = 'https://github.com/astanin/python-tabulate/actions/workflows/tabulate.yml/badge.svg'
status = Non`
- `p-c11` image `python:3.11-slim` network `install-only`
  - setup: `pip install --quiet tabulate prettytable texttable`
  - commands: `python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed"
import timeit, importlib.metadata as md
from tabulate import tabulate
import prettytable, texttable
headers = ['col%d' % i for i in range(10)]
table = [['some text'] + list(range(i, i + 9)) for i in range(10)]  # 10x10 mixed text/numeric, `

## Step 3, EXECUTE on GitHub Actions: run `33207614025` (artifacts: per-probe cmd/stdout/stderr/exit_code)

Transcript index (probe · command excerpt):
```
p-c1 /tmp/v/bin/python - <<'EOF' || echo "VERDICT_LINE: FAIL import or install crashed"
try:
    from tabulate import tabulate
    import tabulate as t
    print('observed: tabulate version', t.__version__, 'callable', callable(tabulate))
    print('VERDICT_LINE: PASS pip install tabulate + from tabulate import tabulate ok, version', t.__version__)
except Exception as e:
    print('observed:', repr(e)) cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c10 python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed (network?)"
import json, urllib.request, urllib.error
UA = {'User-Agent': 'claim-probe', 'Accept': 'application/vnd.github+json'}
badge_url = 'https://github.com/astanin/python-tabulate/actions/workflows/tabulate.yml/badge.svg'
status = None; body = ''
try:
    with urllib.request.urlopen(urllib.request.Request(badge_url, headers=UA), tim cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c11 python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed"
import timeit, importlib.metadata as md
from tabulate import tabulate
import prettytable, texttable
headers = ['col%d' % i for i in range(10)]
table = [['some text'] + list(range(i, i + 9)) for i in range(10)]  # 10x10 mixed text/numeric, as in benchmark/benchmark.py
def run_tabulate():
    return tabulate(table, headers)
def run_prettyt cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c2 ls -l /tmp/v/bin/tabulate 2>&1 && if test -x /tmp/v/bin/tabulate; then OUT=$(printf '1 2\n3 4\n' | /tmp/v/bin/tabulate 2>&1); RC=$?; echo "observed: rc=$RC output=$(echo "$OUT" | tr '\n' '|')"; if [ $RC -eq 0 ] && echo "$OUT" | grep -q '^ *1 *2'; then echo 'VERDICT_LINE: PASS bin/tabulate exists, executable, formats stdin'; else echo 'VERDICT_LINE: FAIL bin/tabulate exists but did not format stdin cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c3 /tmp/v2/bin/python -c 'import tabulate; print("observed: library importable, version", tabulate.__version__)' || echo 'observed: library NOT importable' && N=$(ls /tmp/v2/bin 2>/dev/null | grep -c '^tabulate$'); echo "observed: tabulate scripts in venv bin = $N (README says lib-only should install none)"; if [ "$N" -eq 0 ]; then echo 'VERDICT_LINE: PASS TABULATE_INSTALL=lib-only suppressed the CLI cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c4 python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed (network?)"
import json, urllib.request
try:
    req = urllib.request.Request('https://pypi.org/pypi/tabulate/json', headers={'User-Agent': 'claim-probe'})
    with urllib.request.urlopen(req, timeout=30) as r:
        status = r.status
        info = json.load(r)['info']
except Exception as e:
    print('observed: pypi fetch failed', rep cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c5 python3 - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed"
from tabulate import tabulate
table = [["Sun",696000,1989100000],["Earth",6371,5973.6],
         ["Moon",1737,73.5],["Mars",3390,641.85]]
out = tabulate(table)
print(out)
lines =
```

## Step 4, ADJUDICATE: votes -> verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`, observed: tabulate version 0.10.0 callable True / VERDICT_LINE: PASS pip install tabulate  |
| c2 | verified / verified / verified | **verified** | high | `p-c2`, -rwxr-xr-x 1 root root 211 Aug 28 20:18 /tmp/v/bin/tabulate / observed: rc=0 output=-  -/1 |
| c3 | refuted / refuted / refuted | **refuted** | high | `p-c3`, observed: tabulate scripts in venv bin = 1 (README says lib-only should install none) / VE |
| c4 | verified / verified / verified | **verified** | high | `p-c4`, observed: http 200 version 0.10.0 requires_python '>=3.10' py2 classifiers [] + exit_code  |
| c5 | verified / verified / verified | **verified** | high | `p-c5`, observed: first data line = 'Sun    696000     1.9891e+09' / VERDICT_LINE: PASS output mat |
| c6 | verified / verified / verified | **verified** | high | `p-c6`, observed: lines = ['Name      Age', '------  -----', 'Alice      24', 'Bob        19'] + e |
| c7 | verified / verified / verified | **verified** | high | `p-c7`, observed: lines = ['Name      Age', '------  -----', 'Alice      24', 'Bob        19'] / V |
| c8 | refuted / refuted / refuted | **refuted** | high | `p-c8`, -f FMT, --format FMT      set output table format; supported formats: plain, simple, grid, |
| c9 | verified / verified / verified | **verified** | high | `p-c9`, observed: wcwidth 0.8.3 WIDE_CHARS_MODE True display widths per line [9, 9, 9, 9] / VERDIC |
| c10 | verified / verified / verified | **verified** | high | `p-c10`, observed: badge http 200 badge text = passing svg bytes 2276 / observed: run 272 268615a5  |
| c11 | verified / verified / verified | **verified** | low | `p-c11`, observed: tabulate     0.10.0      478.1 us/call / observed: prettytable  3.18.0      501. |

## Step 5, REPORT
Overall score 82 · escalated to human: none · model calls: nominal 4

_Human checkpoint: the verdicts above were audited against ground truth; disagreements were read from the recorded probe output and resolved in favour of the evidence (CHANGELOG 'Truth audit')._