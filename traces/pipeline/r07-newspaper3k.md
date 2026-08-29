# Pipeline trajectory: r07-newspaper3k (proof `advanced-v2-1787952546`)

Repository https://github.com/codelucas/newspaper @ `1618b547f31c`. Buyer question: _We are acquiring a news-monitoring pipeline built on newspaper3k — does the library still install and import cleanly on a current Python with current lxml, is its CI badge meaningful, and do the README's scraping examples still work?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): Installing the package with `pip3 install newspaper3k` on a current Python yields a working library: `import newspaper` and `from newspaper import Article` succeed.
- **c2** (environment): Newspaper (newspaper3k) is a Python 3 library; the python2 branch is deprecated and the python2 package on PyPI is named 'newspaper', not 'newspaper3k'.
- **c3** (test_ci): The newspaper README displays a Travis CI build-status badge served from travis-ci.org, asserting a live, passing CI build for codelucas/newspaper.
- **c4** (quickstart): With newspaper3k installed, downloading and parsing the URL http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/ via Article(url); article.download(); article.parse() yields article.authors == ['Leigh Ann Caldwell', 'John Honway'] and article.publish_date == datetime.datetime(2013, 12, 30, 0, 0).
- **c5** (interface): With newspaper3k installed and NLP corpora available, calling article.nlp() after download() and parse() populates article.keywords (a list of keyword strings) and article.summary (a summary string).
- **c6** (install): The NLP corpora required by newspaper3k can be installed by piping the repository script to python3: `curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3`.
- **c7** (install): On Debian/Ubuntu, the README's listed image-processing prerequisite `sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev` works as written (i.e. the package libpng12-dev is installable).
- **c8** (interface): With newspaper3k importable, `newspaper.languages()` prints the table of available input language codes (ar, be, bg, da, de, el, en, es, ...).
- **c9** (interface): newspaper3k provides a multi-threaded article download framework importable as `from newspaper import news_pool`.
- **c10** (quickstart): With newspaper3k installed, `newspaper.build('http://cnn.com')` returns a Source object whose .articles list contains Article objects with populated .url attributes.
- **c11** (quantitative): The newspaper README claims the Swiftproxy residential-proxy service offers '80M+ residential IPs across 195+ countries' and 'a 99.89% success rate' for use with newspaper3k pipelines.

## Step 2: PLAN output, 11 probes (`eval/probes/r07-newspaper3k.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.12-slim` network `install-only`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install --quiet newspaper3k 2>&1 | tail -5; echo "pip_rc=${PIPESTATUS[0]}" && /tmp/v/bin/pip freeze | grep -iE '^(newspaper3k|lxml|lxml-html-clean|nltk|Pillow)=' || true`
  - commands: `/tmp/v/bin/python --version && /tmp/v/bin/python -c 'import newspaper; print("import newspaper OK", newspaper.__version__)' && /tmp/v/bin/python -c 'from newspaper import Article; print("from newspaper import Article OK")' && /tmp/v/bin/python -c 'from newspaper import Article; print("C1_OK")' 2>&1 `
- `p-c2` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq >/dev/null && apt-get install -y -qq curl >/dev/null && curl -sf https://pypi.org/pypi/newspaper3k/json -o /tmp/n3k.json; echo "newspaper3k_rc=$?" && curl -sf https://pypi.org/pypi/newspaper/json -o /tmp/n2.json; echo "newspaper_rc=$?" && curl -sf -o /dev/null -w '%{http_code}\n' `
  - commands: `python3 -c "import json; d=json.load(open('/tmp/n3k.json'))['info']; print('newspaper3k', d['version'], 'requires_python=', d.get('requires_python')); cls=[c for c in d['classifiers'] if 'Python' in c]; print(cls); assert any(':: 3' in c for c in cls), 'no Python 3 classifier'; assert not any(':: 2'`
- `p-c3` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq >/dev/null && apt-get install -y -qq curl >/dev/null && curl -sIL -o /dev/null -w 'http=%{http_code} final_url=%{url_effective} type=%{content_type}\n' https://travis-ci.org/codelucas/newspaper.svg > /tmp/c3_head.txt 2>&1; echo "curl_rc=$?" >> /tmp/c3_head.txt && curl -sL --max-ti`
  - commands: `cat /tmp/c3_head.txt /tmp/c3_target.txt && echo "badge body bytes: $(wc -c < /tmp/c3_badge.body)"; head -c 400 /tmp/c3_badge.body; echo && grep -qi '<svg' /tmp/c3_badge.body && echo BADGE_IS_SVG || echo BADGE_NOT_SVG && grep -qiE 'passing' /tmp/c3_badge.body && echo BADGE_SAYS_PASSING || echo BADGE_`
- `p-c4` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq >/dev/null && apt-get install -y -qq curl >/dev/null && pip install --quiet newspaper3k 2>&1 | tail -3 && echo 'NOTE: installing lxml[html_clean] so this probe tests the quickstart, not c1 import failure'; pip install --quiet 'lxml[html_clean]' 2>&1 | tail -2 && curl -sIL -A 'Mozi`
  - commands: `python3 -c "import datetime
from newspaper import Article
url='http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
html=open('/tmp/fox.html').read()
print('html_len', len(html))
assert html, 'download returned empty html'
a=Article(url)
a.download(input_html=html)
a.pars`
- `p-c5` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq >/dev/null && apt-get install -y -qq curl >/dev/null && pip install --quiet newspaper3k 2>&1 | tail -3 && echo 'NOTE: installing lxml[html_clean] so this probe tests nlp(), not c1 import failure'; pip install --quiet 'lxml[html_clean]' 2>&1 | tail -2 && curl -s https://raw.githubu`
  - commands: `python3 -c "import nltk
for r in ['tokenizers/punkt','corpora/stopwords']:
    try: print(r, '->', nltk.data.find(r))
    except LookupError as e: print(r, 'MISSING')" && python3 -c "from newspaper import Article
a=Article('http://example.com/2013/12/30/new-year-new-laws/')
a.download(input_html=ope`
- `p-c6` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq >/dev/null && apt-get install -y -qq curl >/dev/null && curl -sf https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py -o /tmp/download_corpora.py; echo "script_fetch_rc=$?"; wc -c /tmp/download_corpora.py && echo '--- README ordering: corpora step prece`
  - commands: `echo '== bare interpreter =='; tail -5 /tmp/c6_bare.log && echo '== after pip install newspaper3k =='; tail -8 /tmp/c6_after.log && grep -q 'after_install_rc=0' /tmp/c6_after.log && echo C6_SCRIPT_EXIT0 || echo C6_SCRIPT_FAILED && python3 -c "import nltk
missing=[]
for r in ['corpora/brown','tokeniz`
- `p-c7` image `python:3.11-slim` network `install-only`
  - setup: `cat /etc/os-release | grep -E '^(PRETTY_NAME|VERSION_CODENAME)=' && apt-get update -qq > /tmp/c7_update.log 2>&1; echo "update_rc=$?" && apt-get install -y libjpeg-dev zlib1g-dev libpng12-dev > /tmp/c7_install.log 2>&1; echo $? > /tmp/c7_install.rc && apt-get install -y libjpeg-dev zlib1g-dev libpng`
  - commands: `echo "verbatim install rc=$(cat /tmp/c7_install.rc)"; tail -5 /tmp/c7_install.log && apt-cache policy libpng12-dev 2>&1 | head -5; apt-cache show libpng12-dev >/dev/null 2>&1 && echo LIBPNG12_DEV_AVAILABLE || echo LIBPNG12_DEV_NOT_IN_APT && echo "README fallback (libpng-dev) rc=$(cat /tmp/c7_fallbac`
- `p-c8` image `python:3.11-slim` network `install-only`
  - setup: `pip install --quiet newspaper3k 2>&1 | tail -3 && echo 'NOTE: installing lxml[html_clean] so this probe tests languages(), not c1 import failure'; pip install --quiet 'lxml[html_clean]' 2>&1 | tail -2`
  - commands: `python3 -c 'import newspaper; newspaper.languages()' > /tmp/c8.txt 2>&1; echo "rc=$?"; cat /tmp/c8.txt && grep -q 'Your available languages are' /tmp/c8.txt && echo HEADER_OK && for code in ar be bg da de el en es; do grep -qE "^\s*${code}\s+" /tmp/c8.txt && echo "has $code" || echo "MISSING $code";`
- `p-c9` image `python:3.11-slim` network `install-only`
  - setup: `pip install --quiet newspaper3k 2>&1 | tail -3 && echo 'NOTE: installing lxml[html_clean] so this probe tests news_pool, not c1 import failure'; pip install --quiet 'lxml[html_clean]' 2>&1 | tail -2`
  - commands: `python3 -c "from newspaper import news_pool
print(type(news_pool), news_pool.__class__.__module__)
print('methods', [m for m in dir(news_pool) if not m.startswith('_')])
assert callable(getattr(news_pool,'set',None)), 'no set()'
assert callable(getattr(news_pool,'join',None)), 'no join()'
import ins`
- `p-c10` image `python:3.11-slim` network `install-only`
  - setup: `pip install --quiet newspaper3k 2>&1 | tail -3 && echo 'NOTE: installing lxml[html_clean] so this probe tests build(), not c1 import failure'; pip install --quiet 'lxml[html_clean]' 2>&1 | tail -2 && timeout 95 python3 -c "import newspaper, json, time
from newspaper import Config
c=Config(); c.reque`
  - commands: `python3 -c "import json
d=json.load(open('/tmp/c10.json'))
print(d)
assert d['ok'], d.get('err')
assert d['type']=='Source', d['type']
assert d['n']>0, 'articles list EMPTY'
assert d['article_types']==['Article'], d['article_types']
assert all(u.startswith('http') and 'cnn' in u for u in d['urls']),`
- `p-c11` image `python:3.11-slim` network `install-only`
  - setup: `apt-get update -qq >/dev/null && apt-get install -y -qq curl >/dev/null && curl -sf https://raw.githubusercontent.com/codelucas/newspaper/1618b547f31c2d1fd19ae3b6afd8f7542dd02074/README.rst -o /tmp/README.rst; echo "readme_rc=$?" && curl -sL -A 'Mozilla/5.0' --max-time 30 -o /tmp/swift.html -w 'vend`
  - commands: `echo '== claims of success rate in README at pinned commit =='; grep -noE '[0-9]+\.[0-9]+% success rate|[0-9]+M\+ residential IPs across [0-9]+\+ countries' /tmp/README.rst && echo '== vendor page: is the number present, is any methodology present =='; echo "bytes=$(wc -c < /tmp/swift.html)"; echo "`

## Step 3: EXECUTE on GitHub Actions, run `33209972786` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 /tmp/v/bin/python --version && /tmp/v/bin/python -c 'import newspaper; print("import newspaper OK", newspaper.__version__)' && /tmp/v/bin/python -c 'from newspaper import Article; print("from newspaper import Article OK")' && /tmp/v/bin/python -c 'from newspaper import Article; print("C1_OK")' 2>&1 | grep -E 'C1_OK|ModuleNotFoundError|ImportError|lxml.html.clean'
STDOUT Python 3.12.14

STDERR /repo/newspaper/urls.py:117: SyntaxWarning: invalid escape sequence '\.'
  Separators can be [\.-/_]. Years can be 2 or 4 digits, must
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/repo/newspaper/__init__.py", line 10, in <module>
    from .api import (build, build_article, fulltext, hot, languages,
  File "/repo/newspaper/api.py", line 14, in <module>
    from .article import Article
  File "/repo/newspaper/article.py", line 16, in <module>
    from . import network
  File "/repo/newspaper/network.py", line 14, in <module>
    from .configuration import Configuration
  File "/repo/newspaper/configuration.py", line 15, in <module>
    from .parsers import Parser
  File "/repo/newspaper/parsers.py", line 12, in <module>
    import lxml.html.clean
  File "/tmp/v/lib/python3.12/site-packages/lxml/html/clean.py", line 18, in <module>
    raise ImportError(
ImportError: lxml.html.clean module is now a separate project lxml_html_clean.
Install lxml[html-clean] or lxml_html_clean directly.

PHASE_A 
[notice] A new release of pip is available: 25.0.1 -> 26.2.1
[notice] To update, run: python3 -m pip install --upgrade pip
pip_rc=0
lxml==6.1.2
newspaper3k==0.2.8
nltk==3.10.3
pillow==12.3.0

--stderr--

EXIT 1
p-c10 python3 -c "import json
d=json.load(open('/tmp/c10.json'))
print(d)
assert d['ok'], d.get('err')
assert d['type']=='Source', d['type']
assert d['n']>0, 'articles list EMPTY'
assert d['article_types']==['Article'], d['article_types']
assert all(u.startswith('http') and 'cnn' in u for u in d['urls']), d['urls']
print('C10_OK', d['n'], 'articles')"
STDOUT {'ok': True, 'type': 'Source', 'n': 378, 'urls': ['https://www.cnn.com/business/media', 'https://www.cnn.com/weather/video', 'https://www.cnn.com/audio/podcasts/all-there-is-with-anderson-cooper', 'https://www.cnn.com/audio/podcasts/terms-of-service-with-clare-duffy', 'http://cnn.com/2026/08/28/asia/map-nepal-china-flood-landslide-damage-vis'], 'article_types': ['Article'], 'cats': ['http://cnn.com', 'https://us.cnn.com', 'https://cnnespanol.cnn.com', 'https://cnn.it', 'http://cnn.com/follow'], 'secs': 1.9}
C10_OK 378 articles

STDERR 
PHASE_A e: 24.0 -> 26.2.1
[notice] To update, run: pip install --upgrade pip
NOTE: installing lxml[html_clean] so this probe tests build(), not c1 import failure
[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: pip install --upgrade pip
{'ok': True, 'type': 'Source', 'n': 378, 'urls': ['https://www.cnn.com/business/media', 'https://www.cnn.com/weather/video', 'https://www.cnn.com/audio/podcasts/all-the
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | refuted / refuted / refuted | **refuted** | high | `p-c1`: Python 3.12.14 ... pip_rc=0, newspaper3k==0.2.8, lxml==6.1.2 installed; then `import newsp |
| c2 | verified / verified / verified | **verified** | high | `p-c2`: newspaper3k 0.2.8 classifiers ['Programming Language :: Python :: 3'] C2_PY3_OK; PyPI 'new |
| c3 | refuted / refuted / refuted | **refuted** | high | `p-c3`: http=200 final_url=https://api.travis-ci.com/codelucas/newspaper.svg (travis-ci.org redire |
| c4 | refuted / refuted / refuted | **refuted** | high | `p-c4`: html_len 102350; title 'New Year, new laws: Obamacare, pot, guns and drones'; authors ['Cn |
| c5 | refuted / refuted / refuted | **refuted** | high | `p-c5`: tokenizers/punkt -> /root/nltk_data/tokenizers/punkt; corpora/stopwords present; text_len  |
| c6 | refuted / refuted / refuted | **refuted** | low | `p-c6`: bare interpreter: ModuleNotFoundError: No module named 'nltk' bare_rc=1; after pip install |
| c7 | refuted / refuted / refuted | **refuted** | high | `p-c7`: Debian 13 (trixie), update_rc=0; verbatim install rc=100; "E: Package 'libpng12-dev' has n |
| c8 | verified / verified / verified | **verified** | high | `p-c8`: rc=0; 'Your available languages are:' HEADER_OK; has ar be bg da de el en es; language row |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: <class 'newspaper.mthreading.NewsPool'> newspaper.mthreading; methods ['config', 'join', ' |
| c10 | verified / verified / verified | **verified** | high | `p-c10`: {'ok': True, 'type': 'Source', 'n': 378, 'urls': ['https://www.cnn.com/business/media', .. |
| c11 | verified / unverifiable / unverifiable | **unverifiable** | low | `p-c11`: README.rst line 251: "80M+ residential IPs across 195+ countries" and "99.89% success rate |

## Step 5: REPORT
Overall score 41. Escalated to a human: ['c11']. Model calls: nominal 4. Verdicts disagreeing with audited truth: c6, c8, c9.

Human checkpoint for this repository: c4: was unverifiable; README example output stale: executed authors == ['Cnn Wire'], README states a different author (advanced-v1 p-c4 AssertionError authors mismatch).; c5: was unverifiable; nlp() raises LookupError on current nltk despite punkt+stopwords present (advanced-v1 p-c5 stderr) — the README's download_corpora path no longer suffices.; c10: was unverifiable; Live probe with network built Source(cnn.com): 369 article urls (advanced-v1 p-c10). Draft had marked unverifiable.