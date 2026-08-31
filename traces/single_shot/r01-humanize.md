# Single-shot trajectory: r01-humanize (proof `single-shot-baseline-1788167374`)

Repository https://github.com/python-humanize/humanize @ `ce4147b6c8f8`. Buyer question: _We want to embed humanize in our reporting product's number/date formatting layer — do the README's install instructions, Python-version support, and example outputs actually hold on a current interpreter?_

This is the **fair execution baseline** (arms/single_shot): one agent is handed the repository and all the claims, writes **one** bash script, runs it **once** in the same sandbox, and returns **one** judgment. It can run code, but it has none of the pipeline's structure (one probe per claim, VERDICT_LINE contract, per-claim adjudication, escalation). This trace exists to make that contrast follow-able.

## Step 1: instructions
See `arms/PROMPTS.md` (single-shot arm). Claims given to the agent:

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

## Step 2: the ONE script the agent wrote (executed once, in the sandbox)

```bash
export PYTHONUTF8=1 LANG=C.UTF-8; mkdir -p /work; cd /work; if python3 -m pip install --upgrade humanize >/work/c1.log 2>&1 && python3 -c "import humanize" 2>>/work/c1.log; then echo "CLAIM c1: PASS 'python3 -m pip install --upgrade humanize' from PyPI succeeded and import humanize works (version $(
STDOUT CLAIM c1: FAIL pip install from PyPI or import failed: ERROR: No matching distribution found for humanize
CLAIM c2: FAIL clone or editable install failed: fatal: unable to access 'https://github.com/python-humanize/humanize/': Could not resolve host: github.com
CLAIM c3: FAIL README pyversions badge present=False; pypi.org requires_python='unreachable:URLError'; installed metadata Requires-Python=None
CLAIM c4: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'")
CLAIM c5: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'")
CLAIM c6: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'")
CLAIM c7: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'")
CLAIM c8: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'")
CLAIM c9: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'")
CLAIM c10: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'")
CLAIM c11: FAIL Test workflow badge status=None (source: badge fetch error URLError(gaierror(-3, 'Temporary failure in name resolution')); api error URLError(gaierror(-3, 'Temporary failure in name resolution')))

STDERR 
EXIT 0
```

## Step 3: the ONE judgment (all claims adjudicated together, from that single run)

| claim | verdict | conf | evidence excerpt |
|---|---|---|---|
| c1 | **unverifiable** | high | CLAIM c1: FAIL pip install from PyPI or import failed: ERROR: No matching distribution found for humanize |
| c2 | **unverifiable** | high | CLAIM c2: FAIL clone or editable install failed: fatal: unable to access 'https://github.com/python-humanize/h |
| c3 | **unverifiable** | high | CLAIM c3: FAIL README pyversions badge present=False; pypi.org requires_python='unreachable:URLError'; install |
| c4 | **unverifiable** | high | CLAIM c4: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'") |
| c5 | **unverifiable** | high | CLAIM c5: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'") |
| c6 | **unverifiable** | high | CLAIM c6: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'") |
| c7 | **unverifiable** | high | CLAIM c7: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'") |
| c8 | **unverifiable** | high | CLAIM c8: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'") |
| c9 | **unverifiable** | high | CLAIM c9: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'") |
| c10 | **unverifiable** | high | CLAIM c10: FAIL humanize not importable: ModuleNotFoundError("No module named 'humanize'") |
| c11 | **unverifiable** | high | CLAIM c11: FAIL Test workflow badge status=None (source: badge fetch error URLError(gaierror(-3, 'Temporary fa |

## Step 4: outcome
0 verified, 0 refuted, 11 unverifiable/escalated. Verdict accuracy vs audited truth: **0.00**. Contrast with the pipeline trajectory for the same repository in `traces/pipeline/` — where a single monolithic script stalls or mis-handles one claim, every downstream claim inherits the failure, which is the structural weakness the per-claim pipeline removes.
