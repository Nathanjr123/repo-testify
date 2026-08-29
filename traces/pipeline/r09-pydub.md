# Pipeline trajectory: r09-pydub (proof `advanced-v2-1787952546`)

Repository https://github.com/jiaaro/pydub @ `103e339d3bc7`. Buyer question: _We want to adopt pydub for audio slicing/concatenation/export in a service running current Python (3.13). Does it install and work as the README documents, and is the project's CI story real?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The package pydub can be installed from PyPI with the exact command `pip install pydub`.
- **c2** (quickstart): After `pip install pydub`, the import `from pydub import AudioSegment` succeeds on a current Python interpreter (the README quickstart begins with this import, stating no version restriction).
- **c3** (environment): pydub can open and save WAV files with pure Python only, without ffmpeg or libav installed.
- **c4** (environment): Opening non-WAV formats such as mp3 requires ffmpeg or libav to be installed; without them `AudioSegment.from_mp3` fails.
- **c5** (test_ci): The Travis CI badge at the top of the README asserts that the master branch currently builds and passes tests on travis-ci.org.
- **c6** (test_ci): The AppVeyor badge asserts that the master branch currently builds and passes on Windows CI at ci.appveyor.com/project/jiaaro/pydub.
- **c7** (quickstart): Slicing uses milliseconds: for a loaded song, `song[:10*1000]` returns the first 10 seconds and `song[-5000:]` the last 5 seconds, and concatenating a 10 s segment with a 5 s segment gives `duration_seconds == 15.0`.
- **c8** (interface): Adding an integer to an AudioSegment changes gain in dB: `segment + 6` boosts volume by 6 dB and `segment - 3` reduces it by 3 dB.
- **c9** (interface): Exporting with `format="ogg"` and no codec argument defaults to the vorbis (libvorbis) codec.
- **c10** (interface): `len(audio_segment)` returns the segment length in milliseconds.
- **c11** (interface): AudioSegment objects are immutable: operations like `reverse()` return new objects and never modify the original.

## Step 2: PLAN output, 11 probes (`eval/probes/r09-pydub-r1.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python --version && pip show pydub | head -3 && python -c 'import pydub, sys; print("observed: pydub imported from", pydub.__file__, "on", sys.version.split()[0])' && echo 'VERDICT_LINE: PASS pip install pydub exited 0 and package is installed/importable' || echo 'VERDICT_LINE: FAIL pip install pydu`
- `p-c2` image `python:3.13-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python --version && python -c 'from pydub import AudioSegment; import sys; print("observed: from pydub import AudioSegment OK on Python", sys.version.split()[0])' && echo 'VERDICT_LINE: PASS README quickstart import succeeds on Python 3.13' || echo 'VERDICT_LINE: FAIL from pydub import AudioSegment `
- `p-c3` image `python:3.11-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python -c '
import wave, struct, math, shutil
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*math.sin(2*math.pi*freq*i/rate))) f`
- `p-c4` image `python:3.11-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python -c '
import shutil
from pydub import AudioSegment
open("fake.mp3","wb").write(b"\xff\xfb\x90\x00" + b"\x00"*4000)
print("observed: ffmpeg =", shutil.which("ffmpeg"), "avconv =", shutil.which("avconv"))
try:
    AudioSegment.from_mp3("fake.mp3")
    print("observed: from_mp3 unexpectedly succe`
- `p-c5` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python -c '
import urllib.request, urllib.error
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"probe"}), timeout=20)
        return r.status, r.geturl(), r.read(20000).decode("utf-8","replace")
    except urllib.error.HTTPError as e:
        `
- `p-c6` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python -c '
import urllib.request, urllib.error, json, datetime
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"probe","Accept":"application/json"}), timeout=20)
        return r.status, r.read(50000).decode("utf-8","replace")
    except urlli`
- `p-c7` image `python:3.11-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python -c '
import wave, struct, math
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*math.sin(2*math.pi*freq*i/rate))) for i in `
- `p-c8` image `python:3.11-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python -c '
import wave, struct, math
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*math.sin(2*math.pi*freq*i/rate))) for i in `
- `p-c9` image `python:3.11-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python -c '
import wave, struct, math, io, logging, shutil, subprocess
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*math.sin(2`
- `p-c10` image `python:3.11-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python -c '
import wave, struct, math
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*math.sin(2*math.pi*freq*i/rate))) for i in `
- `p-c11` image `python:3.11-slim` network `install-only`
  - setup: `pip install pydub`
  - commands: `python -c '
import wave, struct, math
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    n = rate*secs
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*(i/n)*math.sin(2*math.pi*`

## Step 3: EXECUTE on GitHub Actions, run `33212005473` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 python --version && pip show pydub | head -3 && python -c 'import pydub, sys; print("observed: pydub imported from", pydub.__file__, "on", sys.version.split()[0])' && echo 'VERDICT_LINE: PASS pip install pydub exited 0 and package is installed/importable' || echo 'VERDICT_LINE: FAIL pip install pydub did not produce an installed, importable package'
STDOUT Python 3.11.16
Name: pydub
Version: 0.25.1
Summary: Manipulate audio with an simple and easy high level interface
observed: pydub imported from /repo/pydub/__init__.py on 3.11.16
VERDICT_LINE: PASS pip install pydub exited 0 and package is installed/importable

STDERR ERROR: Pipe to stdout was broken
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
BrokenPipeError: [Errno 32] Broken pipe
/repo/pydub/utils.py:174: RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
  warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning)

PHASE_A b7cce023: Download complete
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

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: pip install --upgrade pip

EXIT 0
p-c10 python -c '
import wave, struct, math
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*math.sin(2*math.pi*freq*i/rate))) for i in range(rate*secs))); w.close()
N = 7
mkwav("known.wav", N)
seg = AudioSegment.from_wav("known.wav")
print("observed: wav seconds =", N, "len(seg) =", len(seg), "duration_seconds =", seg.duration_seconds)
assert abs(len(seg) - N*1000) <= 1, "len(seg) is not milliseconds"
print("VERDICT_LINE: PASS len(
STDOUT observed: wav seconds = 7 len(seg) = 7000 duration_seconds = 7.0
VERDICT_LINE: PASS len(audio_segment) == 7000 for a 7 s WAV (milliseconds)

STDERR /repo/pydub/utils.py:174: RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
  warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning)

PHASE_A Collecting pydub
  Downloading pydub-0.25.1-py2.py3-none-any.whl.metadata (1.4 kB)
Downloading pydub-0.25.1-py2.py3-none-any.whl (32 kB)
Installing collected packages: pydub
Successfully installed p
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: Name: pydub / Version: 0.25.1 / observed: pydub imported from /repo/pydub/__init__.py on 3 |
| c2 | refuted / refuted / refuted | **refuted** | high | `p-c2`: Python 3.13.15 / File "/repo/pydub/utils.py", line 17, in <module>: import pyaudioop as au |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: observed: ffmpeg on PATH = None avconv = None / out.wav frames = 16000 rate = 8000 duratio |
| c4 | verified / verified / verified | **verified** | low | `p-c4`: observed: ffmpeg = None avconv = None / observed: from_mp3 raised FileNotFoundError: [Errn |
| c5 | refuted / refuted / refuted | **refuted** | high | `p-c5`: observed: badge http = 200 final url = https://api.travis-ci.com/jiaaro/pydub.svg?branch=m |
| c6 | verified / verified / verified | **verified** | high | `p-c6`: observed: badge http = 200 svg says passing = True / api http = 200 last master build stat |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: observed: song = 20.0 first_10 = 10.0 last_5 = 5.0 concat duration_seconds = 15.0 / VERDIC |
| c8 | verified / verified / verified | **verified** | high | `p-c8`: observed: base dBFS = -15.259 delta(seg+6) = 6.001 delta(seg-3) = -3.0 / VERDICT_LINE: PAS |
| c9 | verified / verified / verified | **verified** | high | `p-c9`: README debug-logger captured converter call = subprocess.call(['ffmpeg', '-y', '-f', 'wav' |
| c10 | verified / verified / verified | **verified** | high | `p-c10`: observed: wav seconds = 7 len(seg) = 7000 duration_seconds = 7.0 / VERDICT_LINE: PASS len( |
| c11 | verified / verified / verified | **verified** | high | `p-c11`: observed: original raw_data unchanged after reverse() = True / reversed differs = True / r |

## Step 5: REPORT
Overall score 82. Escalated to a human: none. Model calls: nominal 4. Verdicts disagreeing with audited truth: none.

Human checkpoint for this repository: c6: was refuted; Executed with network: AppVeyor API last master build status=success finished 2026-03-19 (161 days), badge svg 'passing' (advanced-v2 p-c6). Draft had assumed a stale mirage; the claim as written is true.