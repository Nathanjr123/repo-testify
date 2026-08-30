# Pipeline trajectory: r10-requests-html (proof `advanced-v3-heldout-rescored-1788058984`)

Repository https://github.com/psf/requests-html @ `075ac162dc62`. Buyer question: _We are considering requests-html for scraping JavaScript-heavy pages. Does the advertised 'Full JavaScript support' via render() actually work today on a supported Python, and is the project's CI alive?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The package requests-html can be installed with the exact command `pipenv install requests-html` (equivalently `pip install requests-html`).
- **c2** (environment): requests-html supports Python 3.6 and above (i.e. it installs and imports on any Python >= 3.6, including current releases).
- **c3** (interface): The library provides full JavaScript support: calling `r.html.render()` downloads Chromium (via pyppeteer) and renders the page's dynamic JavaScript content.
- **c4** (environment): The first time `render()` is run it downloads Chromium into the user's home directory (~/.pyppeteer/), and this happens only once.
- **c5** (test_ci): The Travis CI badge asserts the master branch currently builds and passes on travis-ci.com.
- **c6** (quickstart): A GET request via `HTMLSession` exposes `r.html.links`, which returns the set of all links on the page (anchors excluded).
- **c7** (quickstart): `r.html.search('Python is a {} language')[0]` on the python.org homepage returns the string 'programming'.
- **c8** (interface): Async is supported: `AsyncHTMLSession().run(coro1, coro2, coro3)` executes multiple async GET requests and returns a list of Response objects.
- **c9** (quickstart): The library works without Requests: `HTML(html="<a href='https://httpbin.org'>").links` returns `{'https://httpbin.org'}`.
- **c10** (interface): XPath selectors are supported via `r.html.xpath(...)`, returning matching Element objects.
- **c11** (interface): CSS selectors are supported via `r.html.find(selector, first=True)`, and element `.text`, `.attrs`, and `.absolute_links` work as shown.

## Step 2: PLAN output, 11 probes (`eval/probes/r10-requests-html.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `none`
  - setup: `pip install -q requests-html`
  - commands: `pip show requests-html | head -3 && python3 -c 'import requests_html; print("import_ok:", requests_html.__file__); print("VERDICT_LINE: PASS pip install requests-html succeeded and import requests_html works")' || echo "VERDICT_LINE: FAIL pip install requests-html failed or import requests_html rais`
- `p-c2` image `python:3.13-slim` network `none`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `python3 --version && (pip show requests-html | head -3 || true) && python3 -c 'import sys, requests_html; print("python:", sys.version.split()[0]); print("import_ok:", requests_html.__file__); print("VERDICT_LINE: PASS pinned commit installs and imports on current Python " + sys.version.split()[0])'`
- `p-c3` image `python:3.11-slim` network `on`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `mkdir -p /tmp/site && printf '%s' '<html><body><div id="clock">NOT_RENDERED</div><script>document.getElementById("clock").innerHTML="RENDERED_BY_JS";</script></body></html>' > /tmp/site/js.html && (python3 -m http.server 8765 --directory /tmp/site >/tmp/srv.log 2>&1 &) && sleep 2 && printf '%b' 'fro`
- `p-c4` image `python:3.11-slim` network `on`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `printf '%b' 'import os, urllib.request, urllib.error\nfrom pyppeteer import chromium_downloader as cd\nhome = os.path.expanduser("~")\nprint("home:", home)\nprint("home_dot_pyppeteer_exists_before:", os.path.exists(os.path.join(home, ".pyppeteer")))\nfolder = str(getattr(cd, "DOWNLOADS_FOLDER", "<no`
- `p-c5` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `printf '%b' 'import re, urllib.request, urllib.error\nu = "https://travis-ci.com/psf/requests-html.svg?branch=master"\nreq = urllib.request.Request(u, headers={"User-Agent": "probe"})\ntry:\n    r = urllib.request.urlopen(req, timeout=30)\n    status, body, final = r.status, r.read().decode("utf-8",`
- `p-c6` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `mkdir -p /tmp/site && printf '%s' '<html><head><title>T</title></head><body><div><a href="/about/">About</a><a href="https://example.com/x">X</a><a href="//cdn.example.com/y">Y</a><a href="#top">Top</a></div><ul><li id="about" class="tier-1 element-1" aria-haspopup="true"><a href="/about/">About</a>`
- `p-c7` image `python:3.11-slim` network `on`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `python3 -c 'from requests_html import HTMLSession; session = HTMLSession(); r = session.get("https://python.org/"); print("status:", r.status_code, "url:", r.html.url); res = r.html.search("Python is a {} language"); print("search_result:", res); v = res[0]; print("captured:", repr(v)); assert v == `
- `p-c8` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `mkdir -p /tmp/site && printf '%s' '<html><body><p>index</p></body></html>' > /tmp/site/index.html && printf '%s' '<html><body><p>a</p></body></html>' > /tmp/site/a.html && printf '%s' '<html><body><p>b</p></body></html>' > /tmp/site/b.html && (python3 -m http.server 8765 --directory /tmp/site >/tmp/`
- `p-c9` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `python3 -c 'from requests_html import HTML; doc = """<a href=\x27https://httpbin.org\x27>"""; html = HTML(html=doc); l = html.links; print("links:", l); assert l == {"https://httpbin.org"}, l; print("VERDICT_LINE: PASS HTML(html=doc).links == {https://httpbin.org} without Requests")' || echo "VERDIC`
- `p-c10` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `mkdir -p /tmp/site && printf '%s' '<html><head><title>T</title></head><body><div><a href="/about/">About</a><a href="https://example.com/x">X</a><a href="//cdn.example.com/y">Y</a><a href="#top">Top</a></div><ul><li id="about" class="tier-1 element-1" aria-haspopup="true"><a href="/about/">About</a>`
- `p-c11` image `python:3.11-slim` network `none`
  - setup: `pip install -q https://github.com/psf/requests-html/archive/075ac162dc62fc532037df0d98954ab840a97516.zip`
  - commands: `mkdir -p /tmp/site && printf '%s' '<html><head><title>T</title></head><body><div><a href="/about/">About</a></div><ul><li id="about" class="tier-1 element-1" aria-haspopup="true"><a href="/about/">About</a><a href="/about/apps/">Applications</a></li></ul></body></html>' > /tmp/site/index.html && (py`

## Step 3: EXECUTE on GitHub Actions, run `33270014892` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 pip show requests-html | head -3 && python3 -c 'import requests_html; print("import_ok:", requests_html.__file__); print("VERDICT_LINE: PASS pip install requests-html succeeded and import requests_html works")' || echo "VERDICT_LINE: FAIL pip install requests-html failed or import requests_html raised (pipenv form not exercised; pip equivalent used)"
STDOUT Name: requests-html
Version: 0.10.0
Summary: HTML Parsing for Humans.
VERDICT_LINE: FAIL pip install requests-html failed or import requests_html raised (pipenv form not exercised; pip equivalent used)

STDERR ERROR: Pipe to stdout was broken
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
BrokenPipeError: [Errno 32] Broken pipe
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/repo/requests_html.py", line 15, in <module>
    from lxml.html.clean import Cleaner
  File "/usr/local/lib/python3.11/site-packages/lxml/html/clean.py", line 18, in <module>
    raise ImportError(
ImportError: lxml.html.clean module is now a separate project lxml_html_clean.
Install lxml[html-clean] or lxml_html_clean directly.

PHASE_A  layer
a14578096eda: Waiting
87e1b7cce023: Verifying Checksum
87e1b7cce023: Download complete
c86306e32cd0: Verifying Checksum
c86306e32cd0: Download complete
6310eb16bf42: Download complete
a14578096eda: Download complete
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
p-c10 mkdir -p /tmp/site && printf '%s' '<html><head><title>T</title></head><body><div><a href="/about/">About</a><a href="https://example.com/x">X</a><a href="//cdn.example.com/y">Y</a><a href="#top">Top</a></div><ul><li id="about" class="tier-1 element-1" aria-haspopup="true"><a href="/about/">About</a><a href="/about/apps/">Applications</a></li></ul></body></html>' > /tmp/site/index.html && (python3 -m http.server 8765 --directory /tmp/site >/tmp/srv.log 2>&1 &) && sleep 2 && python3 -c 'from requests_html import HTMLSession, Element; r = HTMLSession().get("http://127.0.0.1:8765/"); els = r.html.
STDOUT VERDICT_LINE: FAIL xpath() did not return the expected Element list or raised

STDERR Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/repo/requests_html.py", line 15, in <module>
    from lxml.html.clean import Cleaner
  File "/usr/local/lib/python3.11/site-packages/lxml/html/clean.py", line 18, in <module>
    raise ImportError(
ImportError: lxml.html.clean module is now a separate pr
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | refuted / refuted / refuted | **refuted** | high | `p-c1`: pip show: 'Name: requests-html / Version: 0.10.0' but 'ImportError: lxml.html.clean module |
| c2 | refuted / refuted / refuted | **refuted** | high | `p-c2`: 'Python 3.13.15' ... 'ImportError: lxml.html.clean module is now a separate project lxml_h |
| c3 | refuted / refuted / refuted | **refuted** | high | `p-c3`: 'File "/tmp/c3.py", line 1, in <module> from requests_html import HTMLSession' -> 'ImportE |
| c4 | refuted / refuted / refuted | **refuted** | high | `p-c4`: 'download_folder: /root/.local/share/pyppeteer/local-chromium' / 'folder_is_home_dot_pyppe |
| c5 | refuted / refuted / refuted | **refuted** | high | `p-c5`: 'badge_status: 404' / 'body_head: file not found' / 'AssertionError: badge HTTP 404' -> 'V |
| c6 | refuted / refuted / refuted | **refuted** | high | `p-c6`: 'File "/repo/requests_html.py", line 15, in <module> from lxml.html.clean import Cleaner'  |
| c7 | refuted / refuted / refuted | **refuted** | high | `p-c7`: 'from requests_html import HTMLSession' -> 'ImportError: lxml.html.clean module is now a s |
| c8 | refuted / refuted / refuted | **refuted** | high | `p-c8`: 'File "/tmp/c8.py", line 1, in <module> from requests_html import AsyncHTMLSession' -> 'Im |
| c9 | refuted / refuted / refuted | **refuted** | high | `p-c9`: 'from requests_html import HTML' -> 'ImportError: lxml.html.clean module is now a separate |
| c10 | refuted / refuted / refuted | **refuted** | high | `p-c10`: 'File "/repo/requests_html.py", line 15, in <module> from lxml.html.clean import Cleaner'  |
| c11 | refuted / refuted / refuted | **refuted** | high | `p-c11`: 'File "/repo/requests_html.py", line 15, in <module> from lxml.html.clean import Cleaner'  |

## Step 5: REPORT
Overall score 0. Escalated to a human: none. Model calls: 4. Verdicts disagreeing with audited truth: none.

Human checkpoint for this repository: c1: was verified; Executed as written: `pip install requests-html` then import raises ImportError (lxml.html.clean is now a separate project) on current lxml (recorded by advanced-v3-heldout probe p-c1). Draft had guessed verified. Toward the pipeline.; c6: was verified; Executed as written: `pip install requests-html` then import raises ImportError (lxml.html.clean is now a separate project) on current lxml (recorded by advanced-v3-heldout probe p-c6). Draft had guessed verified. Toward the pipeline.; c8: was verified; Executed as written: `pip install requests-html` then import raises ImportError (lxml.html.clean is now a separate project) on current lxml (recorded by advanced-v3-heldout probe p-c8). Draft had guessed verified. Toward the pipeline.; c9: was verified; Executed as written: `pip install requests-html` then import raises ImportError (lxml.html.clean is now a separate project) on current lxml (recorded by advanced-v3-heldout probe p-c9). Draft had guessed verified. Toward the pipeline.; c10: was verified; Executed as written: `pip install requests-html` then import raises ImportError (lxml.html.clean is now a separate project) on current lxml (recorded by advanced-v3-heldout probe p-c10). Draft had guessed verified. Toward the pipeline.; c11: was verified; Executed as written: `pip install requests-html` then import raises ImportError (lxml.html.clean is now a separate project) on current lxml (recorded by advanced-v3-heldout probe p-c11). Draft had guessed verified. Toward the pipeline.