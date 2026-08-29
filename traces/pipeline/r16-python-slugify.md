# Pipeline trajectory: r16-python-slugify (proof `advanced-v3-ext-rescored-1788028882`)

Repository https://github.com/un33k/python-slugify @ `7b6d5d96c199`. Buyer question: _We plan to use python-slugify for URL slugs in a CMS we will support for years — do the install variants, the Python support matrix, the status/coverage badges and the README usage examples (unicode transliteration, max_length, stopwords, CLI) still hold on a current interpreter?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The package can be installed from PyPI with `pip install python-slugify`, after which `from slugify import slugify` succeeds (the default install pulls in text-unidecode).
- **c2** (install): The alternative extra `pip install python-slugify[unidecode]` installs the Unidecode package alongside python-slugify.
- **c3** (environment): Per the README's 'Official Support Matrix', the current python-slugify release line (>= 7.0.0) supports Python >= 3.7, i.e. the latest PyPI release declares requires-python >= 3.7.
- **c4** (environment): The README's support matrix (Python >= 3.7 for slugify >= 7.0.0) matches the repository's own python_requires declaration at the pinned commit.
- **c5** (test_ci): The README's build-status badge asserts that the GitHub Actions workflow it links to (actions/workflows/ci.yml on un33k/python-slugify) is currently passing.
- **c6** (test_ci): The README's Coveralls badge asserts that live test-coverage data is reported for un33k/python-slugify on coveralls.io (currently ~97%).
- **c7** (quickstart): With python-slugify installed, `slugify("This is a test ---")` returns 'this-is-a-test'.
- **c8** (quickstart): With python-slugify installed (default text-unidecode backend), `slugify('影師嗎')` returns 'ying-shi-ma', and `slugify('影師嗎', allow_unicode=True)` returns '影師嗎'.
- **c9** (quickstart): With python-slugify installed, `slugify("C'est déjà l'été.")` returns 'c-est-deja-l-ete' and `slugify('Компьютер')` returns 'kompiuter'.
- **c10** (interface): With python-slugify installed, for txt = 'jaja---lol-méméméoo--a': `slugify(txt, max_length=9)` returns 'jaja-lol'; `slugify(txt, max_length=15, word_boundary=True)` returns 'jaja-lol-a'; `slugify(txt, max_length=20, word_boundary=True, separator=".")` returns 'jaja.lol.mememeoo.a'.
- **c11** (interface): With python-slugify installed, `slugify('the quick brown fox jumps over the lazy dog', stopwords=['the'])` returns 'quick-brown-fox-jumps-over-lazy-dog' and `slugify('10 | 20 %', replacements=[['|', 'or'], ['%', 'percent']])` returns '10-or-20-percent'.
- **c12** (interface): Installing python-slugify also installs a command-line tool named `slugify`: `echo "Taking input from STDIN" | slugify --stdin` prints 'taking-input-from-stdin' and `slugify taking input from the command line` prints 'taking-input-from-the-command-line'.

## Step 2: PLAN output, 12 probes (`eval/probes/r16-python-slugify.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `none`
  - setup: `python -m pip install --quiet --disable-pip-version-check python-slugify`
  - commands: `python - <<'EOF' && echo "VERDICT_LINE: PASS pip install python-slugify; from slugify import slugify and import text_unidecode both succeed" || echo "VERDICT_LINE: FAIL import of slugify or text_unidecode failed after pip install python-slugify (see traceback above)"
import importlib.metadata as m
f`
- `p-c2` image `python:3.11-slim` network `none`
  - setup: `python -m pip install --quiet --disable-pip-version-check 'python-slugify[unidecode]'`
  - commands: `python - <<'EOF' && echo "VERDICT_LINE: PASS python-slugify[unidecode] installs Unidecode alongside slugify" || echo "VERDICT_LINE: FAIL unidecode or slugify not importable after pip install python-slugify[unidecode] (see traceback above)"
import importlib.metadata as m
import unidecode
from slugify`
- `p-c3` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed (pypi.org unreachable or unexpected JSON)"
import json, re, urllib.request
d = json.load(urllib.request.urlopen('https://pypi.org/pypi/python-slugify/json', timeout=30))['info']
rp = (d.get('requires_python') or '').strip()
print('observed: `
- `p-c4` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed (raw.githubusercontent.com unreachable)"
import re, urllib.request
sha = '7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4'
base = 'https://raw.githubusercontent.com/un33k/python-slugify/%s/' % sha
setup = urllib.request.urlopen(base + 'setup.py', t`
- `p-c5` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed (github.com unreachable)"
import json, re, urllib.request, urllib.error
def get(url, accept='*/*'):
    req = urllib.request.Request(url, headers={'User-Agent': 'probe/1.0', 'Accept': accept})
    try:
        r = urllib.request.urlopen(req,`
- `p-c6` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python - <<'EOF' || echo "VERDICT_LINE: FAIL probe crashed (coveralls.io unreachable)"
import re, urllib.request, urllib.error
req = urllib.request.Request('https://coveralls.io/repos/un33k/python-slugify/badge.svg', headers={'User-Agent': 'probe/1.0'})
try:
    r = urllib.request.urlopen(req, timeo`
- `p-c7` image `python:3.11-slim` network `none`
  - setup: `python -m pip install --quiet --disable-pip-version-check python-slugify`
  - commands: `python - <<'EOF' && echo "VERDICT_LINE: PASS slugify('This is a test ---') == 'this-is-a-test'" || echo "VERDICT_LINE: FAIL slugify('This is a test ---') did not return 'this-is-a-test' (see observed value above)"
from slugify import slugify
r = slugify("This is a test ---")
print('observed:', repr(`
- `p-c8` image `python:3.11-slim` network `none`
  - setup: `python -m pip install --quiet --disable-pip-version-check python-slugify`
  - commands: `python - <<'EOF' && echo "VERDICT_LINE: PASS slugify('影師嗎') == 'ying-shi-ma' and allow_unicode=True returns '影師嗎' with default text-unidecode backend" || echo "VERDICT_LINE: FAIL CJK example does not match README (see observed values above)"
from slugify import slugify
try:
    import unidecode; bac`
- `p-c9` image `python:3.11-slim` network `none`
  - setup: `python -m pip install --quiet --disable-pip-version-check python-slugify`
  - commands: `python - <<'EOF' && echo "VERDICT_LINE: PASS French and Cyrillic README examples match ('c-est-deja-l-ete', 'kompiuter')" || echo "VERDICT_LINE: FAIL French/Cyrillic example does not match README (see observed values above)"
from slugify import slugify
r1 = slugify('C\'est déjà l\'été.')
r2 = slugif`
- `p-c10` image `python:3.11-slim` network `none`
  - setup: `python -m pip install --quiet --disable-pip-version-check python-slugify`
  - commands: `python - <<'EOF' && echo "VERDICT_LINE: PASS max_length / word_boundary / separator examples all match README" || echo "VERDICT_LINE: FAIL a max_length/word_boundary/separator example does not match README (see observed values above)"
from slugify import slugify
txt = 'jaja---lol-méméméoo--a'
r1 = s`
- `p-c11` image `python:3.11-slim` network `none`
  - setup: `python -m pip install --quiet --disable-pip-version-check python-slugify`
  - commands: `python - <<'EOF' && echo "VERDICT_LINE: PASS stopwords and replacements examples match README" || echo "VERDICT_LINE: FAIL stopwords or replacements example does not match README (see observed values above)"
from slugify import slugify
r1 = slugify('the quick brown fox jumps over the lazy dog', stop`
- `p-c12` image `python:3.11-slim` network `none`
  - setup: `python -m pip install --quiet --disable-pip-version-check python-slugify`
  - commands: `echo "observed: slugify binary = $(command -v slugify || echo NOT-ON-PATH)" && out1=$(echo 'Taking input from STDIN' | slugify --stdin 2>&1); echo "observed stdin: '$out1'"; out2=$(slugify taking input from the command line 2>&1); echo "observed argv: '$out2'"; if [ "$out1" = 'taking-input-from-stdi`

## Step 3: EXECUTE on GitHub Actions, run `33265035896` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 python - <<'EOF' && echo "VERDICT_LINE: PASS pip install python-slugify; from slugify import slugify and import text_unidecode both succeed" || echo "VERDICT_LINE: FAIL import of slugify or text_unidecode failed after pip install python-slugify (see traceback above)"
import importlib.metadata as m
from slugify import slugify
import text_unidecode
print('observed: python-slugify', m.version('python-slugify'), '| text-unidecode', m.version('text-unidecode'), '| slugify("Hello World")=', repr(slugify('Hello World')))
EOF
STDOUT observed: python-slugify 8.0.4 | text-unidecode 1.3 | slugify("Hello World")= 'hello-world'
VERDICT_LINE: PASS pip install python-slugify; from slugify import slugify and import text_unidecode both succeed

STDERR 
PHASE_A d0: Pulling fs layer
a14578096eda: Pulling fs layer
a14578096eda: Waiting
87e1b7cce023: Verifying Checksum
87e1b7cce023: Download complete
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
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

EXIT 0
p-c10 python - <<'EOF' && echo "VERDICT_LINE: PASS max_length / word_boundary / separator examples all match README" || echo "VERDICT_LINE: FAIL a max_length/word_boundary/separator example does not match README (see observed values above)"
from slugify import slugify
txt = 'jaja---lol-méméméoo--a'
r1 = slugify(txt, max_length=9)
r2 = slugify(txt, max_length=15, word_boundary=True)
r3 = slugify(txt, max_length=20, word_boundary=True, separator='.')
print('observed: max_length=9', repr(r1), '| max_length=15,word_boundary', repr(r2), '| max_length=20,word_boundary,sep=.', repr(r3))
assert r1 == 'jaja-
STDOUT observed: max_length=9 'jaja-lol' | max_length=15,word_boundary 'jaja-lol-a' | max_length=20,word_boundary,sep=. 'jaja.lol.mememeoo.a'
VERDICT_LINE: PASS max_length / word_boundary / separator examples all match README

STDERR 
PHASE_A 
--stderr--
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

EXIT 0
p-c11 python - <<'EOF' && echo "VERDICT_LINE: PASS stopwords and replacements examples match README" || echo "VERDICT_LINE: FAIL stopwords or replacements example does not match README (see observed values above)"
from slugify import slugify
r1 = slugify('the quick brown fox jumps over the lazy dog', stopwords=['the'])
r2 = slugify('10 | 2
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: observed: python-slugify 8.0.4 / text-unidecode 1.3 / slugify("Hello World")= 'hello-world |
| c2 | verified / verified / verified | **verified** | high | `p-c2`: observed: python-slugify 8.0.4 / Unidecode 1.4.0 / VERDICT_LINE: PASS python-slugify[unide |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: observed: latest_pypi_version 8.0.4 / requires_python '>=3.7' / VERDICT_LINE: PASS latest  |
| c4 | refuted / refuted / refuted | **refuted** | high | `p-c4`: observed: setup.py python_requires '>=3.10' / package version at pinned commit 8.0.4 / REA |
| c5 | refuted / refuted / refuted | **refuted** | high | `p-c5`: observed: badge ci.yml http 200 title 'CI - failing' / observed: run CI ci push failure 20 |
| c6 | verified / verified / verified | **verified** | high | `p-c6`: observed: http 200 / final_url https://s3.amazonaws.com/assets.coveralls.io/badges/coveral |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: observed: 'this-is-a-test' / VERDICT_LINE: PASS slugify('This is a test ---') == 'this-is- |
| c8 | verified / verified / verified | **verified** | high | `p-c8`: observed: backend text-unidecode (default) / default 'ying-shi-ma' / allow_unicode '影師嗎' / |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: observed: french 'c-est-deja-l-ete' / cyrillic 'kompiuter' / VERDICT_LINE: PASS French and |
| c10 | verified / verified / verified | **verified** | high | `p-c10`: observed: max_length=9 'jaja-lol' / max_length=15,word_boundary 'jaja-lol-a' / max_length= |
| c11 | verified / verified / verified | **verified** | high | `p-c11`: observed: stopwords 'quick-brown-fox-jumps-over-lazy-dog' / replacements '10-or-20-percent |
| c12 | verified / verified / verified | **verified** | high | `p-c12`: observed: slugify binary = /usr/local/bin/slugify / observed stdin: 'taking-input-from-std |

## Step 5: REPORT
Overall score 83. Escalated to a human: none. Model calls: 4. Verdicts disagreeing with audited truth: none.

Human checkpoint for this repository: no truth entry was changed after this run.