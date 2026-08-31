# Single-shot trajectory: r07-newspaper3k (proof `single-shot-baseline-1788167374`)

Repository https://github.com/codelucas/newspaper @ `1618b547f31c`. Buyer question: _We are acquiring a news-monitoring pipeline built on newspaper3k — does the library still install and import cleanly on a current Python with current lxml, is its CI badge meaningful, and do the README's scraping examples still work?_

This is the **fair execution baseline** (arms/single_shot): one agent is handed the repository and all the claims, writes **one** bash script, runs it **once** in the same sandbox, and returns **one** judgment. It can run code, but it has none of the pipeline's structure (one probe per claim, VERDICT_LINE contract, per-claim adjudication, escalation). This trace exists to make that contrast follow-able.

## Step 1: instructions
See `arms/PROMPTS.md` (single-shot arm). Claims given to the agent:

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

## Step 2: the ONE script the agent wrote (executed once, in the sandbox)

```bash
printf '%s\n' 'import sys' 'try:' '    import newspaper' '    from newspaper import Article' '    print("CLAIM c1: PASS import newspaper and from newspaper import Article succeed, version", getattr(newspaper,"__version__","?"))' 'except Exception as e:' '    print("CLAIM c1: FAIL import failed:", re
STDOUT CLAIM c1: PASS import newspaper and from newspaper import Article succeed, version 0.2.8
CLAIM c2: PASS newspaper3k imports on py3.11; PyPI newspaper (py2 legacy) exists at version 0.1.0.7; README marks python-2-head branch deprecated
CLAIM c3: FAIL badge_in_readme=True travis-ci.org fetch=200 passing_svg=False (travis-ci.org shut down; badge is dead/unknown, not a live passing build)
CLAIM c4: FAIL authors=['Cnn Wire'] publish_date=datetime.datetime(2013, 12, 30, 0, 0) html_len=102351 title='New Year, new laws: Obamacare, pot, guns and drones'
CLAIM c7: FAIL apt-get install as written fails on Debian GNU/Linux 13 (trixie): E: Package 'libpng12-dev' has no installation candidate (libpng12-dev was dropped after Ubuntu 16.04/Debian 9; current package is libpng-dev)
CLAIM c8: PASS newspaper.languages() printed table with 41 lines incl. codes ['ar', 'be', 'bg', 'da', 'de', 'el', 'en', 'es']
CLAIM c9: PASS from newspaper import news_pool works; has set()/join(); newspaper.mthreading uses threading
CLAIM c10: PASS build returned Source with 359 Article objects; sample urls ['https://www.cnn.com/business/media', 'https://www.cnn.com/weather/video', 'https://www.cnn.com/audio/podcasts/all-there-is-with-anderson-cooper']
CLAIM c11: PASS README (cloned master) contains the Swiftproxy text verbatim: ['Swiftproxy', '80M+ residential IPs across 195+ countries', '99.89% success rate'] -- note this verifies the README makes the claim, not that the proxy figures are true

STDERR   File "/tmp/c5.py", line 2
    gher. The fee increases every year. Some new laws in 2014 are going to be about the states responding to the federal government, and the regulations that they are sending down to the states.</p></article></body></html>"
                                                                                                            ^
SyntaxError: unexpected character after line continuation character

EXIT 0
```

## Step 3: the ONE judgment (all claims adjudicated together, from that single run)

| claim | verdict | conf | evidence excerpt |
|---|---|---|---|
| c1 | **verified** | high | CLAIM c1: PASS import newspaper and from newspaper import Article succeed, version 0.2.8 |
| c2 | **verified** | high | CLAIM c2: PASS newspaper3k imports on py3.11; PyPI newspaper (py2 legacy) exists at version 0.1.0.7; README ma |
| c3 | **refuted** | high | CLAIM c3: FAIL badge_in_readme=True travis-ci.org fetch=200 passing_svg=False (travis-ci.org shut down; badge  |
| c4 | **refuted** | high | CLAIM c4: FAIL authors=['Cnn Wire'] publish_date=datetime.datetime(2013, 12, 30, 0, 0) html_len=102351 title=' |
| c5 | **unverifiable** | high | File "/tmp/c5.py", line 2 ... SyntaxError: unexpected character after line continuation character |
| c6 | **unverifiable** | high | (no CLAIM c6 line in STDOUT; the download_corpora.py pipe was never run) |
| c7 | **refuted** | high | CLAIM c7: FAIL apt-get install as written fails on Debian GNU/Linux 13 (trixie): E: Package 'libpng12-dev' has |
| c8 | **verified** | high | CLAIM c8: PASS newspaper.languages() printed table with 41 lines incl. codes ['ar', 'be', 'bg', 'da', 'de', 'e |
| c9 | **verified** | high | CLAIM c9: PASS from newspaper import news_pool works; has set()/join(); newspaper.mthreading uses threading |
| c10 | **verified** | high | CLAIM c10: PASS build returned Source with 359 Article objects; sample urls ['https://www.cnn.com/business/med |
| c11 | **verified** | high | CLAIM c11: PASS README (cloned master) contains the Swiftproxy text verbatim: ['Swiftproxy', '80M+ residential |

## Step 4: outcome
6 verified, 3 refuted, 2 unverifiable/escalated. Verdict accuracy vs audited truth: **0.46**. Contrast with the pipeline trajectory for the same repository in `traces/pipeline/` — where a single monolithic script stalls or mis-handles one claim, every downstream claim inherits the failure, which is the structural weakness the per-claim pipeline removes.
