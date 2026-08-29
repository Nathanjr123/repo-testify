# Pipeline trajectory: r15-parse (proof `advanced-v3-ext-rescored-1788028882`)

Repository https://github.com/r1chardj0n3s/parse @ `8059e320eccf`. Buyer question: _We want to use parse as the format-string matcher inside a log-ingestion product — do the README's install line, export list, and interactive examples (typed fields, datetime formats, custom converters) actually reproduce on a current interpreter, and does the documented test flow pass?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The package 'parse' can be installed from PyPI with the command `pip install parse`, after which `import parse` succeeds.
- **c2** (interface): With 'parse' installed, `from parse import *` exports exactly parse, search, findall and with_pattern (compile is deliberately not exported).
- **c3** (quickstart): With 'parse' installed, `parse("It's {}, I love it!", "It's spam, I love it!")` returns a Result whose repr is `<Result ('spam',) {}>` and whose element [0] is 'spam'.
- **c4** (quickstart): With 'parse' installed, `search('Age: {:d}\n', 'Name: Rufus\nAge: 42\nColor: red\n')` returns a Result with repr `<Result (42,) {}>` (an int 42, not the string '42').
- **c5** (quickstart): With 'parse' installed, `''.join(r[0] for r in findall(">{}<", "<p>the <b>bold</b> text</p>"))` evaluates to the string 'the bold text'.
- **c6** (interface): With 'parse' installed, `from parse import compile; p = compile("It's {}, I love it!")` gives an object that prints as `<Parser "It's {}, I love it!">` and whose `p.parse("It's spam, I love it!")` returns `<Result ('spam',) {}>`.
- **c7** (interface): With 'parse' installed, matching is case-insensitive by default and `parse('SPAM', 'spam', case_sensitive=True)` returns None.
- **c8** (interface): With 'parse' installed, `r = parse("Bring out the holy {item}", "Bring out the holy hand grenade")` gives a Result printing as `<Result () {'item': 'hand grenade'}>`, with `r.named == {'item': 'hand grenade'}`, `r['item'] == 'hand grenade'`, and `'item' in r` True.
- **c9** (interface): With 'parse' installed, strptime-style type specs are supported: `parse("{:%Y-%m-%d %H:%M:%S}", "2023-11-23 12:56:47")` yields datetime.datetime(2023, 11, 23, 12, 56, 47), `parse("{:%H:%M}", "10:26")` yields datetime.time(10, 26), and `parse("{:%Y/%m/%d}", "2023/11/25")` yields datetime.date(2023, 11, 25).
- **c10** (interface): With 'parse' installed, width and precision restrict matched text: `parse('{:.2}{:.2}', 'look')` gives ('lo', 'ok'), `parse('{:4}{:.4}', 'look at that')` gives ('look at ', 'that'), and `parse('{:2d}{:2d}', '0440')` gives (4, 40).
- **c11** (interface): With 'parse' installed, a converter decorated with `@with_pattern(r'\d+')` and passed as an extra type works: `parse('Answer: {number:Number}', 'Answer: 42', {"Number": parse_number})` returns `<Result () {'number': 42}>` with an int value.
- **c12** (test_ci): In a clone of the repository, the documented developer flow `pip install -r tests/requirements.txt && pip install -e . && pytest` installs the package in editable mode and the test suite passes.

## Step 2: PLAN output, 12 probes (`eval/probes/r15-parse-r1.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `on`
  - setup: `python3 -m venv /tmp/v`
  - commands: `/tmp/v/bin/pip install parse && /tmp/v/bin/python -c 'import parse; print("installed parse version:", parse.__version__); print("VERDICT_LINE: PASS pip install parse succeeded and import parse works")' || echo "VERDICT_LINE: FAIL pip install parse or import parse failed"`
- `p-c2` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c 'import parse; print("__all__:", parse.__all__); assert set(parse.__all__)=={"parse","search","findall","with_pattern"}, parse.__all__; ns={}; exec("from parse import *", ns); got={k for k in ns if not k.startswith("__")}; print("import * names:", sorted(got)); assert got=={"parse","searc`
- `p-c3` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c "from parse import parse; r=parse(\"It's {}, I love it!\", \"It's spam, I love it!\"); print('repr:', repr(r)); assert repr(r)==\"<Result ('spam',) {}>\", repr(r); assert r[0]=='spam', r[0]; print('VERDICT_LINE: PASS repr and r[0] match README')" || echo "VERDICT_LINE: FAIL parse result d`
- `p-c4` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c 'from parse import search; r=search("Age: {:d}\n", "Name: Rufus\nAge: 42\nColor: red\n"); print("repr:", repr(r), "type:", type(r[0]).__name__); assert repr(r)=="<Result (42,) {}>", repr(r); assert r[0]==42 and isinstance(r[0], int), repr(r[0]); print("VERDICT_LINE: PASS search returns in`
- `p-c5` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c 'from parse import findall; s="".join(r[0] for r in findall(">{}<", "<p>the <b>bold</b> text</p>")); print("joined:", repr(s)); assert s=="the bold text", s; print("VERDICT_LINE: PASS findall join equals the bold text")' || echo "VERDICT_LINE: FAIL findall output differs from README"`
- `p-c6` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c "from parse import compile; p=compile(\"It's {}, I love it!\"); exp='<Parser ' + chr(34) + \"It's {}, I love it!\" + chr(34) + '>'; print('str(p):', str(p)); assert str(p)==exp, str(p); r=p.parse(\"It's spam, I love it!\"); print('repr:', repr(r)); assert repr(r)==\"<Result ('spam',) {}>\`
- `p-c7` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c 'from parse import parse; a=parse("SPAM", "spam"); b=parse("SPAM", "spam", case_sensitive=True); print("default:", repr(a), "case_sensitive=True:", repr(b)); assert a is not None, "default match should be case-insensitive"; assert b is None, repr(b); print("VERDICT_LINE: PASS case-insensi`
- `p-c8` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c "from parse import parse; r=parse('Bring out the holy {item}', 'Bring out the holy hand grenade'); print('str:', str(r), 'named:', r.named); assert str(r)==\"<Result () {'item': 'hand grenade'}>\", str(r); assert r.named=={'item': 'hand grenade'}, r.named; assert r['item']=='hand grenade'`
- `p-c9` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c 'import datetime as dt; from parse import parse; a=parse("{:%Y-%m-%d %H:%M:%S}", "2023-11-23 12:56:47"); b=parse("{:%H:%M}", "10:26"); c=parse("{:%Y/%m/%d}", "2023/11/25"); print("results:", repr(a), repr(b), repr(c)); assert a[0]==dt.datetime(2023,11,23,12,56,47) and type(a[0]) is dt.dat`
- `p-c10` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `python3 -c 'from parse import parse; a=parse("{:.2}{:.2}", "look"); b=parse("{:4}{:.4}", "look at that"); c=parse("{:2d}{:2d}", "0440"); print("results:", repr(a), repr(b), repr(c)); assert a.fixed==("lo","ok"), repr(a); assert b.fixed==("look at ","that"), repr(b); assert c.fixed==(4,40), repr(c); `
- `p-c11` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz`
  - commands: `printf '%s\n' 'from parse import parse, with_pattern' '@with_pattern(r"\d+")' 'def parse_number(text):' '    return int(text)' 'r = parse("Answer: {number:Number}", "Answer: 42", {"Number": parse_number})' 'print("repr:", repr(r), "type:", type(r["number"]).__name__)' 'assert r.fixed == () and r.nam`
- `p-c12` image `python:3.11-slim` network `on`
  - setup: `python3 -c 'import urllib.request, tarfile; urllib.request.urlretrieve("https://github.com/r1chardj0n3s/parse/archive/8059e320eccf40d750843006dd2ef25197bbff74.tar.gz", "/tmp/parse.tgz"); tarfile.open("/tmp/parse.tgz").extractall("/tmp")' && mv /tmp/parse-8059e320eccf40d750843006dd2ef25197bbff74 /tmp`
  - commands: `cd /tmp/parse && .venv/bin/pip install -q -r tests/requirements.txt && .venv/bin/pip install -q -e . && .venv/bin/python -c 'import parse; print("parse imported from:", parse.__file__)' && .venv/bin/pytest -q > /tmp/pytest.log 2>&1; rc=$?; tail -n 12 /tmp/pytest.log; echo "pytest exit code: $rc"; te`

## Step 3: EXECUTE on GitHub Actions, run `33267871577` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 /tmp/v/bin/pip install parse && /tmp/v/bin/python -c 'import parse; print("installed parse version:", parse.__version__); print("VERDICT_LINE: PASS pip install parse succeeded and import parse works")' || echo "VERDICT_LINE: FAIL pip install parse or import parse failed"
STDOUT Collecting parse
  Downloading parse-1.22.1-py2.py3-none-any.whl.metadata (21 kB)
Downloading parse-1.22.1-py2.py3-none-any.whl (20 kB)
Installing collected packages: parse
Successfully installed parse-1.22.1
installed parse version: 1.22.1
VERDICT_LINE: PASS pip install parse succeeded and import parse works

STDERR 
[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: python3 -m pip install --upgrade pip

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
87e1b7cce023: Download complete
a14578096eda: Verifying Checksum
a14578096eda: Download complete
c86306e32cd0: Download complete
6310eb16bf42: Verifying Checksum
6310eb16bf42: Download complete
6310eb16bf42: Pull complete
87e1b7cce023: Pull complete
c86306e32cd0: Pull complete
a14578096eda: Pull complete
Digest: sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6
Status: Downloaded newer image for python:3.11-slim

EXIT 0
p-c10 python3 -c 'from parse import parse; a=parse("{:.2}{:.2}", "look"); b=parse("{:4}{:.4}", "look at that"); c=parse("{:2d}{:2d}", "0440"); print("results:", repr(a), repr(b), repr(c)); assert a.fixed==("lo","ok"), repr(a); assert b.fixed==("look at ","that"), repr(b); assert c.fixed==(4,40), repr(c); print("VERDICT_LINE: PASS width/precision examples match README")' || echo "VERDICT_LINE: FAIL width/precision results differ from README"
STDOUT results: <Result ('lo', 'ok') {}> <Result ('look at ', 'that') {}> <Result (4, 40) {}>
VERDICT_LINE: PASS width/precision examples match README

STDERR 
PHASE_A 
--stderr--
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: pip install --upgrade pip

EXIT 0
p-c11 printf '%s\n' 'from parse import parse, with_pattern' '@with_pattern(r"\d+")' 'def parse_number(text):' '    return int(text)' 'r = parse("Answer: {number:Number}", "Answer: 42", {"Number": parse_number})' 'print("repr:", repr(r), "type:", type(r["number"]).__name__)' 'assert r.fixed == () and r.named == {"number": 42} and isinstance(r["number"], int), repr(r)' 'print("VERDICT_LINE: PASS with_pattern converter yields int 42 in named result")' > /tmp/p11.py && python3 /tmp/p11.py || echo "VERDICT_LINE: FAIL with_pattern example differs from README"
STDOUT repr: <Re
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: Successfully installed parse-1.22.1 / installed parse version: 1.22.1 / VERDICT_LINE: PASS |
| c2 | verified / verified / verified | **verified** | high | `p-c2`: __all__: ['parse', 'search', 'findall', 'with_pattern'] / import * names: ['findall', 'par |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: repr: <Result ('spam',) {}> / VERDICT_LINE: PASS repr and r[0] match README + exit_code 0 |
| c4 | verified / verified / verified | **verified** | high | `p-c4`: repr: <Result (42,) {}> type: int / VERDICT_LINE: PASS search returns int 42 as README sho |
| c5 | verified / verified / verified | **verified** | high | `p-c5`: joined: 'the bold text' / VERDICT_LINE: PASS findall join equals the bold text + exit_code |
| c6 | verified / verified / verified | **verified** | high | `p-c6`: str(p): <Parser "It's {}, I love it!"> / repr: <Result ('spam',) {}> / VERDICT_LINE: PASS  |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: default: <Result () {}> case_sensitive=True: None / VERDICT_LINE: PASS case-insensitive by |
| c8 | verified / verified / verified | **verified** | high | `p-c8`: str: <Result () {'item': 'hand grenade'}> named: {'item': 'hand grenade'} / VERDICT_LINE:  |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: results: <Result (datetime.datetime(2023, 11, 23, 12, 56, 47),) {}> <Result (datetime.time |
| c10 | verified / verified / verified | **verified** | high | `p-c10`: results: <Result ('lo', 'ok') {}> <Result ('look at ', 'that') {}> <Result (4, 40) {}> / V |
| c11 | verified / verified / verified | **verified** | high | `p-c11`: repr: <Result () {'number': 42}> type: int / VERDICT_LINE: PASS with_pattern converter yie |
| c12 | verified / verified / verified | **verified** | high | `p-c12`: parse imported from: /tmp/parse/parse/__init__.py / 99 passed, 1 skipped in 0.56s / pytest |

## Step 5: REPORT
Overall score 100. Escalated to a human: none. Model calls: 4. Verdicts disagreeing with audited truth: none.

Human checkpoint for this repository: no truth entry was changed after this run.