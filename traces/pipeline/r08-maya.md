# Pipeline trajectory: r08-maya (proof `advanced-v3-heldout-rescored-1788058984`)

Repository https://github.com/kennethreitz/maya @ `9766619d007c`. Buyer question: _A codebase we are buying uses maya for all datetime handling — does it still install on a modern Python given its pinned dependencies, is its CI badge trustworthy, and do the documented examples behave as shown?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The package 'maya' installs successfully with `pip install maya` on a current Python (its dependency set — humanize, pytz, dateparser, tzlocal, pendulum>=2.0.2, snaptime — resolves and builds), after which `import maya` succeeds.
- **c2** (test_ci): The maya README's GitHub Actions badge ('Continuous Integration and Deployment', pointing at github.com/timofurrer/maya) asserts passing CI for the maya project hosted at kennethreitz/maya.
- **c3** (quickstart): In Python with 'maya' installed, `maya.now()` returns a MayaDT object (repr like <MayaDT epoch=...>).
- **c4** (quickstart): In Python with 'maya' installed, `maya.when('tomorrow')` parses the human phrase and returns a MayaDT roughly one day in the future, and `.slang_date()` on it returns the string 'tomorrow'.
- **c5** (interface): In Python with 'maya' installed, a MayaDT exposes symmetric ISO 8601 and RFC 2822 export: `.iso8601()` returns a string like '2017-02-10T22:17:01.445418Z' and `.rfc2822()` returns a string like 'Fri, 10 Feb 2017 22:17:01 GMT', with matching MayaDT.from_iso8601 / MayaDT.from_rfc2822 constructors.
- **c6** (quickstart): In Python with 'maya' installed, `maya.parse('2016-12-16 18:23:45.423992+00:00').datetime(to_timezone='US/Eastern', naive=True)` returns the naive datetime datetime.datetime(2016, 12, 16, 13, 23, 45, 423992).
- **c7** (interface): In Python with 'maya' installed, snap modifiers work: `maya.when('Mon, 21 Feb 1994 21:21:42 GMT').snap('@d+3h').rfc2822()` returns 'Mon, 21 Feb 1994 03:00:00 GMT' (requires the snaptime dependency).
- **c8** (interface): In Python with 'maya' installed, timezone-aware snapping works: `maya.when('Mon, 21 Feb 1994 21:21:42 GMT').snap_tz('+3h@d', 'Australia/Perth').rfc2822()` returns 'Mon, 21 Feb 1994 16:00:00 GMT'.
- **c9** (interface): In Python with 'maya' installed, MayaDT supports dates before Jan 1 1970 via negative epoch integers: `maya.MayaDT(-86400)` yields a MayaDT for Dec 31 1969.
- **c10** (interface): In Python with 'maya' installed, `from maya import MayaInterval` works and MayaInterval(start=maya.now(), end=maya.now().add(hours=1)) constructs an interval object representing a one-hour event.
- **c11** (quantitative): The maya README's PyPI badge asserts that 'maya' is published on PyPI (latest release 0.6.1).

## Step 2: PLAN output, 11 probes (`eval/probes/r08-maya.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `on`
  - setup: `pip install maya`
  - commands: `python3 --version && ( pip install maya > /tmp/pip.log 2>&1 || (tail -n 40 /tmp/pip.log; false) ) && pip show maya | head -n 2 && python3 -c 'import maya; print("import_ok maya_version:", maya.__version__)' && echo "VERDICT_LINE: PASS pip install maya resolved its dependencies and import maya works"`
- `p-c2` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `printf '%b' 'import urllib.request, json\ndef get(u):\n    try:\n        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "probe", "Accept": "application/vnd.github+json"}), timeout=30)\n        return r.status, r.read().decode("utf-8", "replace"), r.geturl()\n    except E`
- `p-c3` image `python:3.11-slim` network `none`
  - setup: `pip install maya`
  - commands: `python3 -c 'import maya; print("maya_version:", maya.__version__); now = maya.now(); print("now_repr:", repr(now)); assert type(now).__name__ == "MayaDT", repr(now); assert repr(now).startswith("<MayaDT epoch="), repr(now)' && echo "VERDICT_LINE: PASS maya.now() returned a MayaDT with <MayaDT epoch=`
- `p-c4` image `python:3.11-slim` network `none`
  - setup: `pip install maya`
  - commands: `python3 -c 'import maya; print("maya_version:", maya.__version__); tomorrow = maya.when("tomorrow"); now = maya.now(); days = (tomorrow.epoch - now.epoch) / 86400.0; slang = tomorrow.slang_date(); print("tomorrow_repr:", repr(tomorrow), "days_ahead:", round(days, 3), "slang_date:", repr(slang)); ass`
- `p-c5` image `python:3.11-slim` network `none`
  - setup: `pip install maya`
  - commands: `python3 -c 'import maya, re; print("maya_version:", maya.__version__); n = maya.now(); i = n.iso8601(); r = n.rfc2822(); print("iso8601:", i, "rfc2822:", r); assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$", i), i; assert re.match(r"^[A-Z][a-z]{2}, \d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d`
- `p-c6` image `python:3.11-slim` network `none`
  - setup: `pip install maya`
  - commands: `python3 -c 'import maya, datetime; print("maya_version:", maya.__version__); scraped = "2016-12-16 18:23:45.423992+00:00"; d = maya.parse(scraped).datetime(to_timezone="US/Eastern", naive=True); print("result:", repr(d)); assert d == datetime.datetime(2016, 12, 16, 13, 23, 45, 423992), repr(d); asse`
- `p-c7` image `python:3.11-slim` network `none`
  - setup: `pip install maya`
  - commands: `python3 -c 'import maya; print("maya_version:", maya.__version__); import importlib.util; print("snaptime_installed:", importlib.util.find_spec("snaptime") is not None); dt = maya.when("Mon, 21 Feb 1994 21:21:42 GMT"); r = dt.snap("@d+3h").rfc2822(); print("snap_result:", repr(r)); assert r == "Mon,`
- `p-c8` image `python:3.11-slim` network `none`
  - setup: `pip install maya`
  - commands: `python3 -c 'import maya; print("maya_version:", maya.__version__); dt = maya.when("Mon, 21 Feb 1994 21:21:42 GMT"); r = dt.snap_tz("+3h@d", "Australia/Perth").rfc2822(); print("snap_tz_result:", repr(r)); assert r == "Mon, 21 Feb 1994 16:00:00 GMT", r' && echo "VERDICT_LINE: PASS dt.snap_tz(+3h@d, A`
- `p-c9` image `python:3.11-slim` network `none`
  - setup: `pip install maya`
  - commands: `python3 -c 'import maya; print("maya_version:", maya.__version__); m = maya.MayaDT(-86400); print("repr:", repr(m), "ymd:", (m.year, m.month, m.day), "iso8601:", m.iso8601(), "datetime:", repr(m.datetime())); assert (m.year, m.month, m.day) == (1969, 12, 31), (m.year, m.month, m.day); assert m.epoch`
- `p-c10` image `python:3.11-slim` network `none`
  - setup: `pip install maya`
  - commands: `python3 -c 'import maya; from maya import MayaInterval; print("maya_version:", maya.__version__); event_start = maya.now(); event_end = event_start.add(hours=1); event = MayaInterval(start=event_start, end=event_end); secs = event.end.epoch - event.start.epoch; print("interval:", repr(event), "secon`
- `p-c11` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `printf '%b' 'import urllib.request, json\ndef get(u):\n    try:\n        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "probe"}), timeout=30)\n        return r.status, r.read().decode("utf-8", "replace")\n    except Exception as e:\n        return getattr(e, "code", -1)`

## Step 3: EXECUTE on GitHub Actions, run `33269764627` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 python3 --version && ( pip install maya > /tmp/pip.log 2>&1 || (tail -n 40 /tmp/pip.log; false) ) && pip show maya | head -n 2 && python3 -c 'import maya; print("import_ok maya_version:", maya.__version__)' && echo "VERDICT_LINE: PASS pip install maya resolved its dependencies and import maya works" || echo "VERDICT_LINE: FAIL pip install maya or import maya failed (see log above)"
STDOUT Python 3.11.16
Name: maya
Version: 0.6.1
import_ok maya_version: 0.6.1
VERDICT_LINE: PASS pip install maya resolved its dependencies and import maya works

STDERR ERROR: Pipe to stdout was broken
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
BrokenPipeError: [Errno 32] Broken pipe

PHASE_A ost0-py2.py3-none-any.whl (229 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 229.9/229.9 kB 72.8 MB/s eta 0:00:00
Downloading regex-2026.7.19-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (801 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 801.4/801.4 kB 114.2 MB/s eta 0:00:00
Downloading tzdata-2026.3-py2.py3-none-any.whl (348 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 348.2/348.2 kB 85.8 MB/s eta 0:00:00
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Building wheels for collected packages: snaptime
  Building wheel for snaptime (setup.py): started
  Building wheel for snaptime (setup.py): finished with status 'done'
  Created wheel for snaptime: filename=snaptime-0.2.4-py3-none-any.whl size=3605 sha256=3c96a3b3db9a987e6fe5dd39c4492c0fa4eec8d
EXIT 0
p-c10 python3 -c 'import maya; from maya import MayaInterval; print("maya_version:", maya.__version__); event_start = maya.now(); event_end = event_start.add(hours=1); event = MayaInterval(start=event_start, end=event_end); secs = event.end.epoch - event.start.epoch; print("interval:", repr(event), "seconds:", secs, "duration_attr:", getattr(event, "duration", None)); assert type(event).__name__ == "MayaInterval", repr(event); assert event.start == event_start and event.end == event_end, repr(event); assert abs(secs - 3600) < 1, secs' && echo "VERDICT_LINE: PASS MayaInterval(start=now, end=now+1h) c
STDOUT maya_version: 0.6.1
interval: <MayaInterval start=<MayaDT epoch=1788030129.9431705> end=<MayaDT epoch=1788033729.943171>> seconds: 3600 duration_attr: 3600.0
VERDICT_LINE: PASS MayaInterval(start=now, end=now+1h) constructs a one-hour interval

STDERR 
PHASE_A ost0-py2.py3-none-any.whl (229 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 229.9/229.9 kB 71.5 MB/s eta 0:00:00
Downloading regex-2026.7.19-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (801 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 801.4/801.4 kB 120.1 MB/s eta 0:00:00
Downloading tzdata-2026.3-py2.py3-none-any.whl (348 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 348.2/348.2 kB 89.3 MB/s eta 0:00:00
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Building wheels for collected packages: snaptime
  Building wheel for snaptime (setup.p
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: Version: 0.6.1 / import_ok maya_version: 0.6.1 / VERDICT_LINE: PASS pip install maya resol |
| c2 | refuted / refuted / refuted | **refuted** | high | `p-c2`: badge_http: 404 badge_text: unknown; kennethreitz_maya_runs_http: 200 latest: []; timofurr |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: now_repr: <MayaDT epoch=1788030084.272883> / VERDICT_LINE: PASS maya.now() returned a Maya |
| c4 | verified / verified / verified | **verified** | high | `p-c4`: days_ahead: 1.0 slang_date: 'tomorrow' / VERDICT_LINE: PASS maya.when(tomorrow) is ~1 day  |
| c5 | verified / verified / verified | **verified** | high | `p-c5`: iso8601: 2026-08-29T19:01:37.360155Z rfc2822: Sat, 29 Aug 2026 19:01:37 GMT / roundtrip_is |
| c6 | verified / verified / verified | **verified** | high | `p-c6`: result: datetime.datetime(2016, 12, 16, 13, 23, 45, 423992) / VERDICT_LINE: PASS maya.pars |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: snaptime_installed: True / snap_result: 'Mon, 21 Feb 1994 03:00:00 GMT' / VERDICT_LINE: PA |
| c8 | refuted / refuted / refuted | **refuted** | high | `p-c8`: stderr: AttributeError: 'MayaDT' object has no attribute 'snap_tz' / VERDICT_LINE: FAIL sn |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: repr: <MayaDT epoch=-86400> ymd: (1969, 12, 31) iso8601: 1969-12-31T00:00:00Z / VERDICT_LI |
| c10 | verified / verified / verified | **verified** | high | `p-c10`: interval: <MayaInterval start=<MayaDT epoch=1788030129.9431705> end=<MayaDT epoch=17880337 |
| c11 | verified / verified / verified | **verified** | high | `p-c11`: pypi_json_http: 200 name: maya latest_version: 0.6.1 / badge_http: 200 badge_svg_contains_ |

## Step 5: REPORT
Overall score 82. Escalated to a human: none. Model calls: 4. Verdicts disagreeing with audited truth: none.

Human checkpoint for this repository: c1: was unverifiable; `pip install maya` resolved and imported (0.6.1) on python:3.11-slim (recorded by advanced-v3-heldout probe p-c1). Draft had marked unverifiable. Toward the pipeline.; c7: was unverifiable; snaptime installed and dt.snap('@d+3h') returned the documented value (recorded by advanced-v3-heldout probe p-c7). Toward the pipeline.; c8: was unverifiable; README documents MayaDT.snap_tz; executing it raises AttributeError: 'MayaDT' object has no attribute 'snap_tz' (recorded by advanced-v3-heldout probe p-c8). Documented API does not exist. Toward the pipeline.