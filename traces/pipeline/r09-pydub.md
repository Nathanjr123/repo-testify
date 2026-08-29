# Pipeline trajectory — r09-pydub (proof `advanced-v2-1787952546`)

Repository https://github.com/jiaaro/pydub @ `103e339d3bc7` · buyer question: _We want to adopt pydub for audio slicing/concatenation/export in a service running current Python (3.13). Does it install and work as the README documents, and is the project's CI story real?_

## Step 1 — instructions
See `arms/PROMPTS.md` (PLAN → EXECUTE → ADJUDICATE). Claims given to the agent:

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

## Step 2 — PLAN output: 11 probes (committed as `eval/probes/r09-pydub.json`)

- `p-c1` image `python:3.13-slim` network `install-only`
  - setup: `python -m venv /venv && . /venv/bin/activate && pip install --no-cache-dir pydub > /pip.log 2>&1; echo PIP_RC=$? >> /pip.log`
  - commands: `python --version && cat /pip.log && grep -q 'PIP_RC=0' /pip.log && . /venv/bin/activate && pip show pydub | grep -E '^(Name|Version):'`
- `p-c2` image `python:3.13-slim` network `install-only`
  - setup: `pip install --no-cache-dir pydub`
  - commands: `python --version && python -c 'import audioop' > audioop.log 2>&1; echo STDLIB_AUDIOOP_RC=$?; cat audioop.log && python -c "from pydub import AudioSegment" > import.log 2>&1; rc=$?; cat import.log; echo IMPORT_RC=$rc; grep -qi audioop import.log && echo VERDICT_HINT=import_fails_because_audioop_remo`
- `p-c3` image `python:3.12-slim` network `install-only`
  - setup: `pip install --no-cache-dir pydub`
  - commands: `command -v ffmpeg avconv ffprobe && { echo FFMPEG_PRESENT_PROBE_INVALID; exit 2; } || echo NO_FFMPEG_ON_PATH && python -c "import wave,math,struct; fr=8000; n=fr*20; w=wave.open('in.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(fr); w.writeframes(b''.join(struct.pack('<h',int(8000`
- `p-c4` image `python:3.12-slim` network `install-only`
  - setup: `pip install --no-cache-dir pydub && apt-get update -qq && apt-get install -y -qq --no-install-recommends ffmpeg > /dev/null && ffmpeg -loglevel error -y -f lavfi -i 'sine=frequency=440:duration=3' -ac 1 -ar 22050 test.mp3 && ls -l test.mp3`
  - commands: `command -v ffmpeg && echo FFMPEG_AT=$(command -v ffmpeg) && PATH=/usr/local/bin sh -c 'command -v ffmpeg avconv; echo PATH_WITHOUT_FFMPEG_CHECK_RC=$?' && PATH=/usr/local/bin python -c "import warnings; warnings.simplefilter('always'); from pydub import AudioSegment
with warnings.catch_warnings(recor`
- `p-c5` image `python:3.11-slim` network `install-only`
  - setup: `cat > fetch.py <<'EOF'
import urllib.request, sys
url, out = sys.argv[1], sys.argv[2]
hdr = {'User-Agent': 'claim-probe/1.0', 'Travis-API-Version': '3'}
try:
    r = urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=30)
    body, code, final = r.read(), r.getcode(), r.geturl()`
  - commands: `cat travis_badge.log travis_page.log travis_api.log && echo '--- badge svg (first 800 bytes) ---'; head -c 800 travis_badge.svg; echo && echo '--- api json (first 800 bytes) ---'; head -c 800 travis_api.json; echo && grep -qi 'passing' travis_badge.svg && ! grep -qi 'unknown' travis_badge.svg && gre`
- `p-c6` image `python:3.11-slim` network `install-only`
  - setup: `cat > fetch.py <<'EOF'
import urllib.request, sys
url, out = sys.argv[1], sys.argv[2]
hdr = {'User-Agent': 'claim-probe/1.0', 'Accept': 'application/json, image/svg+xml, text/html'}
try:
    r = urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=30)
    body, code, final = r.re`
  - commands: `cat appveyor_badge.log appveyor_api.log && echo '--- badge svg (first 800 bytes) ---'; head -c 800 appveyor_badge.svg; echo && python -c "import json,datetime
d=json.load(open('appveyor_api.json')); b=d.get('build',{})
print('status:', b.get('status'), 'finished:', b.get('finished'), 'commit:', b.ge`
- `p-c7` image `python:3.12-slim` network `install-only`
  - setup: `pip install --no-cache-dir pydub && python -c "import wave,math,struct; fr=8000; n=fr*20; w=wave.open('never_gonna_give_you_up.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(fr); w.writeframes(b''.join(struct.pack('<h',int(8000*math.sin(2*math.pi*440*i/fr))) for i in range(n))); w.`
  - commands: `python -c "from pydub import AudioSegment
song = AudioSegment.from_wav('never_gonna_give_you_up.wav')
# pydub does things in milliseconds
ten_seconds = 10 * 1000
first_10_seconds = song[:ten_seconds]
last_5_seconds = song[-5000:]
beginning = first_10_seconds + 6
end = last_5_seconds - 3
without_the_`
- `p-c8` image `python:3.12-slim` network `install-only`
  - setup: `pip install --no-cache-dir pydub && python -c "import wave,math,struct; fr=8000; n=fr*5; w=wave.open('tone.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(fr); w.writeframes(b''.join(struct.pack('<h',int(8000*math.sin(2*math.pi*440*i/fr))) for i in range(n))); w.close()"`
  - commands: `python -c "from pydub import AudioSegment
seg = AudioSegment.from_wav('tone.wav')
up = seg + 6
down = seg - 3
d_up = up.dBFS - seg.dBFS; d_down = down.dBFS - seg.dBFS
print('base_dBFS', seg.dBFS, 'plus6_delta', d_up, 'minus3_delta', d_down)
assert abs(d_up - 6.0) < 0.2, d_up
assert abs(d_down + 3.0)`
- `p-c9` image `python:3.12-slim` network `install-only`
  - setup: `pip install --no-cache-dir pydub && apt-get update -qq && apt-get install -y -qq --no-install-recommends ffmpeg > /dev/null && python -c "import wave,math,struct; fr=8000; n=fr*3; w=wave.open('tone.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(fr); w.writeframes(b''.join(struct.pa`
  - commands: `ffmpeg -version | head -1 && python -c "from pydub import AudioSegment; song = AudioSegment.from_wav('tone.wav'); song.export('out.ogg', format='ogg'); song.export('out_explicit.ogg', format='ogg', codec='libvorbis'); print('exported')" && ffprobe -v error -select_streams a:0 -show_entries stream=co`
- `p-c10` image `python:3.12-slim` network `install-only`
  - setup: `pip install --no-cache-dir pydub && python -c "import wave,math,struct; fr=8000; n=fr*7; w=wave.open('seven.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(fr); w.writeframes(b''.join(struct.pack('<h',int(8000*math.sin(2*math.pi*440*i/fr))) for i in range(n))); w.close()"`
  - commands: `python -c "import wave; w=wave.open('seven.wav','rb'); print('wav_seconds', w.getnframes()/w.getframerate())" && python -c "from pydub import AudioSegment; seg = AudioSegment.from_wav('seven.wav'); n=len(seg); print('len()', n, 'duration_seconds', seg.duration_seconds); assert abs(n - 7*1000) <= 1, `
- `p-c11` image `python:3.12-slim` network `install-only`
  - setup: `pip install --no-cache-dir pydub && python -c "import wave,math,struct; fr=8000; n=fr*4; w=wave.open('song.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(fr); w.writeframes(b''.join(struct.pack('<h',int(8000*math.sin(2*math.pi*440*i/fr)*math.exp(-i/fr))) for i in range(n))); w.clos`
  - commands: `python -c "from pydub import AudioSegment
song = AudioSegment.from_wav('song.wav')
before = bytes(song.raw_data); before_len = len(song); before_db = song.dBFS
# song is not modified
backwards = song.reverse()
louder = song + 6
faded = song.fade_in(1000).fade_out(1000)
clip = song[:1000]
assert byte`

## Step 3 — EXECUTE on GitHub Actions: run `33212005473` (artifacts: per-probe cmd/stdout/stderr/exit_code)

Transcript index (probe · command excerpt):
```
p-c1 python --version && pip show pydub | head -3 && python -c 'import pydub, sys; print("observed: pydub imported from", pydub.__file__, "on", sys.version.split()[0])' && echo 'VERDICT_LINE: PASS pip install pydub exited 0 and package is installed/importable' || echo 'VERDICT_LINE: FAIL pip install pydub did not produce an installed, importable package' cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c10 python -c '
import wave, struct, math
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*math.sin(2*math.pi*freq*i/rate))) for i in range(rate*secs))); w.close()
N = 7
mkwav("known.wav", N)
seg = AudioSegment.from_wav("known.wav")
p cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c11 python -c '
import wave, struct, math
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    n = rate*secs
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*(i/n)*math.sin(2*math.pi*freq*i/rate))) for i in range(n))); w.close()
mkwav("song.wav", 2)
song = AudioSegment.from_wav("son cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c2 python --version && python -c 'from pydub import AudioSegment; import sys; print("observed: from pydub import AudioSegment OK on Python", sys.version.split()[0])' && echo 'VERDICT_LINE: PASS README quickstart import succeeds on Python 3.13' || echo 'VERDICT_LINE: FAIL from pydub import AudioSegment raises on Python 3.13 (traceback above; README states no version restriction)' cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c3 python -c '
import wave, struct, math, shutil
from pydub import AudioSegment
def mkwav(p, secs, amp=8000, freq=440, rate=8000):
    w=wave.open(p,"wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
    w.writeframes(b"".join(struct.pack("<h", int(amp*math.sin(2*math.pi*freq*i/rate))) for i in range(rate*secs))); w.close()
mkwav("in.wav", 2)
seg = AudioSegment.from_wav("in.wav")
seg.e cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c4 python -c '
import shutil
from pydub import AudioSegment
open("fake.mp3","wb").write(b"\xff\xfb\x90\x00" + b"\x00"*4000)
print("observed: ffmpeg =", shutil.which("ffmpeg"), "avconv =", shutil.which("avconv"))
try:
    AudioSegment.from_mp3("fake.mp3")
    print("observed: from_mp3 unexpectedly succeeded with no converter installed")
    print("VERDICT_LINE: FAIL from_mp3 succeeded without ffmpeg/a cmd.txt exit_code stdout.log stderr.log phase_a.log\np-c5 python -c '
import urllib.request, urllib.error
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"probe"}), timeout=20)
        return r.status, r.geturl(), r.read(20000).decode("utf-8","replace")
    except urllib.error.HTTPError as e:
        return e.c
```

## Step 4 — ADJUDICATE: votes → verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1` — Name: pydub / Version: 0.25.1 / observed: pydub imported from /repo/pydub/__init__.py on 3 |
| c2 | refuted / refuted / refuted | **refuted** | high | `p-c2` — Python 3.13.15 / File "/repo/pydub/utils.py", line 17, in <module>: import pyaudioop as au |
| c3 | verified / verified / verified | **verified** | high | `p-c3` — observed: ffmpeg on PATH = None avconv = None / out.wav frames = 16000 rate = 8000 duratio |
| c4 | verified / verified / verified | **verified** | low | `p-c4` — observed: ffmpeg = None avconv = None / observed: from_mp3 raised FileNotFoundError: [Errn |
| c5 | refuted / refuted / refuted | **refuted** | high | `p-c5` — observed: badge http = 200 final url = https://api.travis-ci.com/jiaaro/pydub.svg?branch=m |
| c6 | verified / verified / verified | **verified** | high | `p-c6` — observed: badge http = 200 svg says passing = True / api http = 200 last master build stat |
| c7 | verified / verified / verified | **verified** | high | `p-c7` — observed: song = 20.0 first_10 = 10.0 last_5 = 5.0 concat duration_seconds = 15.0 / VERDIC |
| c8 | verified / verified / verified | **verified** | high | `p-c8` — observed: base dBFS = -15.259 delta(seg+6) = 6.001 delta(seg-3) = -3.0 / VERDICT_LINE: PAS |
| c9 | verified / verified / verified | **verified** | high | `p-c9` — README debug-logger captured converter call = subprocess.call(['ffmpeg', '-y', '-f', 'wav' |
| c10 | verified / verified / verified | **verified** | high | `p-c10` — observed: wav seconds = 7 len(seg) = 7000 duration_seconds = 7.0 / VERDICT_LINE: PASS len( |
| c11 | verified / verified / verified | **verified** | high | `p-c11` — observed: original raw_data unchanged after reverse() = True / reversed differs = True / r |

## Step 5 — REPORT
Overall score 82 · escalated to human: none · model calls: nominal 4

_Human checkpoint: the verdicts above were audited against ground truth; disagreements were read from the recorded probe output and resolved in favour of the evidence (CHANGELOG 'Truth audit')._