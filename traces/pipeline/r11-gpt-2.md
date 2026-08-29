# Pipeline trajectory: r11-gpt-2 (proof `advanced-v2-1787952546`)

Repository https://github.com/openai/gpt-2 @ `9b63575ef427`. Buyer question: _We want to reproduce GPT-2 sample generation from this repo today for a research baseline. Can the documented install path (DEVELOPERS.md) actually be executed on a current machine, and do the model downloads still work?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The documented TensorFlow dependency installs with the exact command `pip3 install tensorflow==1.12.0` (CPU) or `pip3 install tensorflow-gpu==1.12.0` (GPU).
- **c2** (install): The remaining Python dependencies install with `pip3 install -r requirements.txt` (fire>=0.1.3, regex==2017.4.5, requests==2.21.0, tqdm==4.31.1).
- **c3** (quickstart): Model weights are downloaded by running `python3 download_model.py 124M` (and likewise 355M, 774M, 1558M).
- **c4** (quickstart): Unconditional samples are generated from the small model with the exact command `python3 src/generate_unconditional_samples.py | tee /tmp/samples`, which prints generated text samples.
- **c5** (interface): Custom-prompt generation works via `python3 src/interactive_conditional_samples.py --top_k 40`.
- **c6** (environment): A Docker path exists: `docker build --tag gpt-2 -f Dockerfile.gpu .` (or Dockerfile.cpu) builds an image from which the samples can be run.
- **c7** (environment): The repository is archived: code is provided as-is with no updates expected.
- **c8** (interface): A model card with basic model information exists at ./model_card.md in the repository.
- **c9** (quantitative): The README notes the originally published parameter counts (117M small, 345M medium) were wrong; the corrected sizes used by the code are 124M and 355M.
- **c10** (environment): Setting the environment variable PYTHONIOENCODING=UTF-8 is documented as required to handle Unicode output from the sample scripts.

## Step 2: PLAN output, 10 probes (`eval/probes/r11-gpt-2-r1.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `install-only`
  - setup: `python3 -c "import sys;print('python',sys.version.split()[0])"`
  - commands: `pip3 install tensorflow==1.12.0 > /tmp/tf.log 2>&1; rc=$?; grep -iE 'ERROR|No matching|Could not find|Successfully installed' /tmp/tf.log | tail -3; if [ $rc -eq 0 ]; then python3 -c 'import tensorflow as tf;print("observed tf.__version__=",tf.__version__)' && echo 'VERDICT_LINE: PASS pip3 install t`
- `p-c2` image `python:3.11-slim` network `install-only`
  - setup: `mkdir -p /w && cd /w && printf 'fire>=0.1.3\nregex==2017.4.5\nrequests==2.21.0\ntqdm==4.31.1\n' > requirements.txt && cat requirements.txt`
  - commands: `cd /w && pip3 install -r requirements.txt > /tmp/req.log 2>&1; rc=$?; grep -iE 'error|gcc|Successfully installed|Failed building' /tmp/req.log | tail -4; if [ $rc -eq 0 ]; then python3 -c 'import fire,regex,requests,tqdm;print("observed regex",regex.__version__,"requests",requests.__version__,"tqdm"`
- `p-c3` image `python:3.11-slim` network `on`
  - setup: `mkdir -p /w && cd /w && python3 -c "import urllib.request;sha='9b63575ef42771a015060c964af2c3da4cf7c8ab';open('download_model.py','wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/openai/gpt-2/'+sha+'/download_model.py',timeout=30).read())" && head -20 download_model.py && pip3 i`
  - commands: `cd /w && python3 -c "import urllib.request;r=urllib.request.urlopen(urllib.request.Request('https://openaipublic.blob.core.windows.net/gpt-2/models/124M/hparams.json'),timeout=20);print('observed endpoint status',r.status,r.read()[:80])" || echo 'observed endpoint unreachable' && cd /w && timeout 90`
- `p-c4` image `python:3.11-slim` network `on`
  - setup: `mkdir -p /w && cd /w && python3 -c "import urllib.request,os;sha='9b63575ef42771a015060c964af2c3da4cf7c8ab';[ (os.makedirs(os.path.dirname(p) or '.',exist_ok=True), open(p,'wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/openai/gpt-2/'+sha+'/'+p,timeout=30).read())) for p in ['d`
  - commands: `cd /w && python3 -c 'import tensorflow as tf;print("observed tf",tf.__version__)' > /tmp/tfimp.log 2>&1 || { tail -1 /tmp/tfimp.log; echo 'VERDICT_LINE: FAIL cannot run generate_unconditional_samples.py: tensorflow (1.12.0) is not installable/importable on this python, README prerequisite unmet'; ex`
- `p-c5` image `python:3.11-slim` network `on`
  - setup: `mkdir -p /w && cd /w && python3 -c "import urllib.request,os;sha='9b63575ef42771a015060c964af2c3da4cf7c8ab';[ (os.makedirs(os.path.dirname(p) or '.',exist_ok=True), open(p,'wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/openai/gpt-2/'+sha+'/'+p,timeout=30).read())) for p in ['d`
  - commands: `cd /w && python3 -c 'import tensorflow as tf;print("observed tf",tf.__version__)' > /tmp/tfimp.log 2>&1 || { tail -1 /tmp/tfimp.log; echo 'VERDICT_LINE: FAIL cannot run interactive_conditional_samples.py --top_k 40: tensorflow (1.12.0) is not installable/importable on this python, README prerequisit`
- `p-c6` image `python:3.11-slim` network `on`
  - setup: `mkdir -p /w && cd /w && python3 -c "import urllib.request;sha='9b63575ef42771a015060c964af2c3da4cf7c8ab';[open(p,'wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/openai/gpt-2/'+sha+'/'+p,timeout=30).read()) for p in ['Dockerfile.cpu','Dockerfile.gpu']]" && echo '--- Dockerfile.c`
  - commands: `cd /w && echo "observed docker binary: $(command -v docker || echo none)"; python3 - <<'EOF'
import re,json,urllib.request
ok=True
for f in ['Dockerfile.cpu','Dockerfile.gpu']:
    m=re.search(r'^FROM\s+(\S+)',open(f).read(),re.M)
    base=m.group(1); repo,_,tag=base.partition(':'); tag=tag or 'late`
- `p-c7` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python3 - <<'EOF'
import json,urllib.request
r=urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/openai/gpt-2',headers={'User-Agent':'probe','Accept':'application/vnd.github+json'}),timeout=20)
d=json.load(r)
print('observed status',r.status,'archived=',d.get('archived'),'p`
- `p-c8` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python3 - <<'EOF'
import urllib.request
sha='9b63575ef42771a015060c964af2c3da4cf7c8ab'
url=f'https://raw.githubusercontent.com/openai/gpt-2/{sha}/model_card.md'
r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'probe'}),timeout=20)
body=r.read().decode('utf-8','replace')
pri`
- `p-c9` image `python:3.11-slim` network `on`
  - setup: `mkdir -p /w && cd /w && python3 -c "import urllib.request;sha='9b63575ef42771a015060c964af2c3da4cf7c8ab';[open(p,'wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/openai/gpt-2/'+sha+'/'+p,timeout=30).read()) for p in ['download_model.py','DEVELOPERS.md','README.md']]" && grep -nE`
  - commands: `cd /w && python3 - <<'EOF'
import json,urllib.request,re
docs=open('download_model.py').read()+open('DEVELOPERS.md').read()+open('README.md').read()
print('observed doc mentions: 124M' , '124M' in docs, '355M', '355M' in docs, '117M', '117M' in docs, '345M', '345M' in docs)
assert '124M' in docs and`
- `p-c10` image `python:3.11-slim` network `on`
  - setup: `mkdir -p /w && cd /w && python3 -c "import urllib.request;sha='9b63575ef42771a015060c964af2c3da4cf7c8ab';[open(p,'wb').write(urllib.request.urlopen('https://raw.githubusercontent.com/openai/gpt-2/'+sha+'/'+p,timeout=30).read()) for p in ['README.md','DEVELOPERS.md']]" && grep -n 'PYTHONIOENCODING' R`
  - commands: `cd /w && grep -q 'export PYTHONIOENCODING=UTF-8' README.md DEVELOPERS.md && echo 'observed: instruction present in repo docs' || { echo 'observed: instruction absent from README.md/DEVELOPERS.md'; echo 'VERDICT_LINE: FAIL PYTHONIOENCODING instruction not found in docs'; exit 0; }; env -u PYTHONIOENC`

## Step 3: EXECUTE on GitHub Actions, run `33212514162` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 pip3 install tensorflow==1.12.0 > /tmp/tf.log 2>&1; rc=$?; grep -iE 'ERROR|No matching|Could not find|Successfully installed' /tmp/tf.log | tail -3; if [ $rc -eq 0 ]; then python3 -c 'import tensorflow as tf;print("observed tf.__version__=",tf.__version__)' && echo 'VERDICT_LINE: PASS pip3 install tensorflow==1.12.0 installed and imports' || echo 'VERDICT_LINE: FAIL tensorflow==1.12.0 installed but import failed'; else echo "observed pip rc=$rc python=$(python3 -c 'import sys;print(sys.version.split()[0])')"; echo 'VERDICT_LINE: FAIL pip3 install tensorflow==1.12.0 has no distribution for this
STDOUT ERROR: Could not find a version that satisfies the requirement tensorflow==1.12.0 (from versions: 2.12.0rc0, 2.12.0rc1, 2.12.0, 2.12.1, 2.13.0rc0, 2.13.0rc1, 2.13.0rc2, 2.13.0, 2.13.1, 2.14.0rc0, 2.14.0rc1, 2.14.0, 2.14.1, 2.15.0rc0, 2.15.0rc1, 2.15.0, 2.15.0.post1, 2.15.1, 2.16.0rc0, 2.16.1, 2.16.2, 2.17.0rc0, 2.17.0rc1, 2.17.0, 2.17.1, 2.18.0rc0, 2.18.0rc1, 2.18.0rc2, 2.18.0, 2.18.1, 2.19.0rc0, 2.19.0, 2.19.1, 2.20.0rc0, 2.20.0, 2.21.0rc0, 2.21.0rc1, 2.21.0)
ERROR: No matching distribution found for tensorflow==1.12.0
observed pip rc=1 python=3.11.16
VERDICT_LINE: FAIL pip3 install tensorflow==1.12.0 has no distribution for this python (README command as written does not work)

STDERR 
PHASE_A python 3.11.16

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

EXIT 0
p-c10 cd /w && grep -q 'export PYTHONIOENCODING=UTF-8' README.md DEVELOPERS.md && echo 'observed: instruction present in repo docs' || { echo 'observed: instruction absent from README.md/DEVELOPERS.md'; echo 'VERDICT_LINE: FAIL PYTHONIOENCODING instruction not found in docs'; exit 0; }; env -u PYTHONIOENCODING LC_ALL=C LANG=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 python3 -c 'import sys;print(sys.stdout.encoding);print("\u00e9\u2014\u4e2d")' > /tmp/without.out 2>&1; w=$?; echo "observed WITHOUT var (C locale, coercion off): rc=$w $(tr '\n' ' ' < /tmp/without.out | head -c 120)"; export PYTHONIOENCODING=
STDOUT observed: instruction present in repo docs
observed WITHOUT var (C locale, coercion off): rc=1 Traceback (most recent call last):   File "<string>", line 1, in <module> UnicodeEncodeError: 'ascii' codec can't encode
observed WITH var: rc=0 utf-8 é—中 
VERDICT_LINE: PASS export PYTHONIOENCODING=UT
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | refuted / refuted / refuted | **refuted** | high | `p-c1`: "ERROR: No matching distribution found for tensorflow==1.12.0" / "observed pip rc=1 python |
| c2 | refuted / refuted / refuted | **refuted** | low | `p-c2`: "error: command 'gcc' failed: No such file or directory" / "ERROR: Failed building wheel f |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: "observed download rc=0" / "observed files ['checkpoint', 'encoder.json', 'hparams.json']" |
| c4 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c4`: "ModuleNotFoundError: No module named 'tensorflow'" / "VERDICT_LINE: FAIL cannot run gener |
| c5 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c5`: "ModuleNotFoundError: No module named 'tensorflow'" / "VERDICT_LINE: FAIL cannot run inter |
| c6 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c6`: "observed docker binary: none" / "Dockerfile.cpu: FROM tensorflow/tensorflow:1.12.0-py3 -> |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: "observed status 200 archived= True pushed_at= 2024-08-14T10:50:53Z" / "VERDICT_LINE: PASS |
| c8 | verified / verified / verified | **verified** | high | `p-c8`: "observed status 200 bytes 4975 first line: # GPT-2 model card" at pinned SHA 9b63575; exi |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: phase_a: "README.md:11: *Note that our original parameter counts were wrong ... small refe |
| c10 | verified / verified / verified | **verified** | high | `p-c10`: phase_a: "DEVELOPERS.md:58:export PYTHONIOENCODING=UTF-8" / "observed WITHOUT var (C local |

## Step 5: REPORT
Overall score 65. Escalated to a human: ['c4', 'c5', 'c6']. Model calls: nominal 4. Verdicts disagreeing with audited truth: c2, c4, c5, c6.

Human checkpoint for this repository: c2: verified as written on a standard developer image (v1 probe: requirements installed on python:3.11 with build tools); on python:3.11-slim the regex sdist needs gcc and fails (v2 probe). Environment-dependent; the README assumes a normal dev machine, so verified stands, with this note.; c10: was refuted; the claim (Setting the environment variable PYTHONIOENCODING=UTF-8 is documented as require...) is about what DEVELOPERS.md documents, and probe p-c10 recorded the documented line verbatim (DEVELOPERS.md:58). Corrected from evidence; this correction goes AGAINST the draft, not for the pipeline.