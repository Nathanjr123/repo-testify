# Pipeline trajectory — r02-python-tabulate (proof `advanced-v2-1787952546`)

Repository https://github.com/astanin/python-tabulate @ `268615a5c27d` · buyer question: _We plan to standardize on tabulate for CLI table output across our internal tools — do the README's install story (library + command-line utility), example outputs, and performance claims hold up?_

## Step 1 — instructions
See `arms/PROMPTS.md` (PLAN → EXECUTE → ADJUDICATE). Claims given to the agent:

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

## Step 2 — PLAN output: 11 probes (committed as `eval/probes/r02-python-tabulate.json`)

- `p-c1` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --no-cache-dir tabulate`
  - commands: `/tmp/v/bin/python -c 'from tabulate import tabulate; import tabulate as t; print("tabulate", t.__version__); print(tabulate([[1,2],[3,4]]))' && /tmp/v/bin/pip show tabulate | grep -E '^(Name|Version|Location)'`
- `p-c2` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --no-cache-dir tabulate`
  - commands: `ls -l /tmp/v/bin/ | grep tabulate && test -x /tmp/v/bin/tabulate && echo 'SCRIPT_PRESENT_IN_BIN=yes' || { echo 'SCRIPT_PRESENT_IN_BIN=no'; exit 1; } && export PATH=/tmp/v/bin:$PATH && command -v tabulate && printf '1 2\n3 4\n' | tabulate && printf '1 2\n3 4\n' | tabulate | grep -qE '^1 +2$' && echo `
- `p-c3` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v2 && cd /tmp && TABULATE_INSTALL=lib-only /tmp/v2/bin/pip install --no-cache-dir tabulate && python3 -m venv /tmp/v3 && cd /tmp && TABULATE_INSTALL=lib-only /tmp/v3/bin/pip install --no-cache-dir --no-binary tabulate tabulate || echo 'SDIST_INSTALL_FAILED'`
  - commands: `echo '--- wheel install with TABULATE_INSTALL=lib-only (README literal command) ---' && ls /tmp/v2/bin/ | grep -c '^tabulate$' || true && /tmp/v2/bin/python -c 'import tabulate; print("lib import ok", tabulate.__version__)' && echo '--- sdist (from-source) install with TABULATE_INSTALL=lib-only ---'`
- `p-c4` image `python:3.10-slim` network `install-only`
  - setup: `pip install --no-cache-dir tabulate && python3 - <<'EOF' > /tmp/pypi_requires_python.txt || echo 'PYPI_FETCH_FAILED' > /tmp/pypi_requires_python.txt
import json, urllib.request
req = urllib.request.Request('https://pypi.org/pypi/tabulate/json', headers={'User-Agent': 'probe'})
d = json.load(urllib.r`
  - commands: `python3 --version && echo 'PyPI latest version + requires_python:'; cat /tmp/pypi_requires_python.txt && python3 -c "from importlib.metadata import metadata; m=metadata('tabulate'); print('installed', m['Version'], 'Requires-Python:', m['Requires-Python']); assert m['Requires-Python'].strip()=='>=3.`
- `p-c5` image `python:3.11-slim` network `install-only`
  - setup: `pip install --no-cache-dir tabulate`
  - commands: `python3 - <<'EOF'
from tabulate import tabulate
table = [["Sun",696000,1989100000],["Earth",6371,5973.6],
         ["Moon",1737,73.5],["Mars",3390,641.85]]
out = tabulate(table)
print(out)
expected = """-----  ------  -------------
Sun    696000     1.9891e+09
Earth    6371  5973.6
Moon     1737    `
- `p-c6` image `python:3.11-slim` network `install-only`
  - setup: `pip install --no-cache-dir tabulate`
  - commands: `python3 - <<'EOF'
from tabulate import tabulate
out = tabulate([["Name","Age"],["Alice",24],["Bob",19]],
               headers="firstrow")
print(out)
lines = out.splitlines()
assert lines[0] == 'Name      Age', repr(lines[0])
assert 'Alice      24' in lines, lines
expected = "Name      Age\n------ `
- `p-c7` image `python:3.11-slim` network `install-only`
  - setup: `pip install --no-cache-dir tabulate`
  - commands: `python3 - <<'EOF'
from tabulate import tabulate
out = tabulate({"Name": ["Alice", "Bob"],
                "Age": [24, 19]}, headers="keys")
print(out)
assert out.splitlines()[0] == 'Name      Age', repr(out.splitlines()[0])
expected = "Name      Age\n------  -----\nAlice      24\nBob        19"
asse`
- `p-c8` image `python:3.11-slim` network `install-only`
  - setup: `pip install --no-cache-dir tabulate`
  - commands: `tabulate --help > /tmp/help.txt 2>&1; echo "exit=$?"; cat /tmp/help.txt && tr ',' '\n' < /tmp/help.txt | tr -d ' .' > /tmp/fmts.txt && missing=0; for f in github grid html latex pipe rst simple tsv; do if grep -qx "$f" /tmp/fmts.txt; then echo "present: $f"; else echo "MISSING: $f"; missing=1; fi; d`
- `p-c9` image `python:3.11-slim` network `install-only`
  - setup: `python3 -m venv /tmp/plain && /tmp/plain/bin/pip install --no-cache-dir tabulate && python3 -m venv /tmp/wide && /tmp/wide/bin/pip install --no-cache-dir 'tabulate[widechars]'`
  - commands: `/tmp/wide/bin/python -c 'import wcwidth; print("wcwidth", wcwidth.__version__)' && /tmp/wide/bin/pip show wcwidth | grep -E '^Version' && /tmp/wide/bin/python - <<'EOF'
import tabulate
print('WIDE_CHARS_MODE =', tabulate.WIDE_CHARS_MODE)
assert tabulate.WIDE_CHARS_MODE is True
out = tabulate.tabulat`
- `p-c10` image `python:3.11-slim` network `install-only`
  - setup: `pip install --no-cache-dir pytest && python3 - <<'EOF'
import json, urllib.request
H = {'User-Agent': 'probe', 'Accept': 'application/vnd.github+json'}
url = 'https://api.github.com/repos/astanin/python-tabulate/actions/workflows/tabulate.yml/runs?per_page=5'
try:
    d = json.load(urllib.request.ur`
  - commands: `echo '--- GitHub Actions tabulate.yml: latest 5 runs ---'; cat /tmp/ci_runs.txt && grep -q 'conclusion=success' /tmp/ci_runs.txt && echo 'LATEST_RUNS_INCLUDE_SUCCESS' || echo 'NO_SUCCESSFUL_RUN_IN_LATEST_5' && echo '--- independent check: run the test suite at pinned commit 268615a5 (pyproject addop`
- `p-c11` image `python:3.11-slim` network `install-only`
  - setup: `pip install --no-cache-dir tabulate prettytable texttable`
  - commands: `python3 -c 'import tabulate, prettytable, texttable, platform; print("tabulate", tabulate.__version__, "prettytable", prettytable.__version__, "texttable", texttable.__version__, "python", platform.python_version())' && python3 - <<'EOF'
import timeit
# mirrors the repo's benchmark.py: 10x10 mixed t`

## Step 3 — EXECUTE on GitHub Actions: run `33207614025` (artifacts: per-probe cmd/stdout/stderr/exit_code)

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

## Step 4 — ADJUDICATE: votes → verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1` — observed: tabulate version 0.10.0 callable True / VERDICT_LINE: PASS pip install tabulate  |
| c2 | verified / verified / verified | **verified** | high | `p-c2` — -rwxr-xr-x 1 root root 211 Aug 28 20:18 /tmp/v/bin/tabulate / observed: rc=0 output=-  -/1 |
| c3 | refuted / refuted / refuted | **refuted** | high | `p-c3` — observed: tabulate scripts in venv bin = 1 (README says lib-only should install none) / VE |
| c4 | verified / verified / verified | **verified** | high | `p-c4` — observed: http 200 version 0.10.0 requires_python '>=3.10' py2 classifiers [] + exit_code  |
| c5 | verified / verified / verified | **verified** | high | `p-c5` — observed: first data line = 'Sun    696000     1.9891e+09' / VERDICT_LINE: PASS output mat |
| c6 | verified / verified / verified | **verified** | high | `p-c6` — observed: lines = ['Name      Age', '------  -----', 'Alice      24', 'Bob        19'] + e |
| c7 | verified / verified / verified | **verified** | high | `p-c7` — observed: lines = ['Name      Age', '------  -----', 'Alice      24', 'Bob        19'] / V |
| c8 | refuted / refuted / refuted | **refuted** | high | `p-c8` — -f FMT, --format FMT      set output table format; supported formats: plain, simple, grid, |
| c9 | verified / verified / verified | **verified** | high | `p-c9` — observed: wcwidth 0.8.3 WIDE_CHARS_MODE True display widths per line [9, 9, 9, 9] / VERDIC |
| c10 | verified / verified / verified | **verified** | high | `p-c10` — observed: badge http 200 badge text = passing svg bytes 2276 / observed: run 272 268615a5  |
| c11 | verified / verified / verified | **verified** | low | `p-c11` — observed: tabulate     0.10.0      478.1 us/call / observed: prettytable  3.18.0      501. |

## Step 5 — REPORT
Overall score 82 · escalated to human: none · model calls: nominal 4

_Human checkpoint: the verdicts above were audited against ground truth; disagreements were read from the recorded probe output and resolved in favour of the evidence (CHANGELOG 'Truth audit')._