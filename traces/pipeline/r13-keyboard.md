# Pipeline trajectory: r13-keyboard (proof `advanced-v3-heldout-rescored-1788058984`)

Repository https://github.com/boppreh/keyboard @ `d232de09bda5`. Buyer question: _We want the keyboard library for cross-platform hotkeys (Windows, Linux, and ideally macOS). The feature list and tests look reassuring — but do passing tests actually prove the OS integration works, and are the platform and dependency claims true?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The package keyboard installs from PyPI with the exact command `pip install keyboard`.
- **c2** (environment): The library works with Windows and Linux (Linux requires sudo/root), with experimental OS X (macOS) support.
- **c3** (environment): The library has zero dependencies: installation pulls in no other packages.
- **c4** (environment): The library supports both Python 2 and Python 3.
- **c5** (environment): The library is pure Python with no C modules to be compiled.
- **c6** (test_ci): The library is 'Tested and documented' — it ships a test suite whose passing validates the library's functionality.
- **c7** (quickstart): Run standalone, `python -m keyboard > events.txt` writes one JSON object per keyboard event, e.g. {"event_type": "down", "scan_code": 25, "name": "p", ...}, and `python -m keyboard < events.txt` replays them.
- **c8** (interface): `keyboard.write('...')` types an arbitrary string by simulating key presses.
- **c9** (interface): `keyboard.add_hotkey('ctrl+shift+a', print, args=('triggered', 'hotkey'))` registers a global hotkey that fires the callback when the combination is pressed, and complex multi-step hotkeys like 'ctrl+shift+m, ctrl+space' are supported.
- **c10** (environment): On Linux the library avoids depending on X by reading raw device files (/dev/input/input*), which is why root is required.
- **c11** (environment): The project banner states it is currently unmaintained ('you might encounter some friction and limited features using it').
- **c12** (interface): Key suppression/blocking is only available on Windows.

## Step 2: PLAN output, 12 probes (`eval/probes/r13-keyboard.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install keyboard`
  - commands: `/tmp/v/bin/pip show keyboard 2>&1 | head -3 && /tmp/v/bin/python -c 'import keyboard, sys; print("import ok: keyboard " + keyboard.version + " on python " + sys.version.split()[0])' && echo "VERDICT_LINE: PASS pip install keyboard exited 0 in a fresh venv and import keyboard succeeds" || echo "VERDI`
- `p-c2` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install keyboard`
  - commands: `printf 'import keyboard, sys, os, platform\nprint("platform " + sys.platform + " " + platform.platform() + " euid " + str(os.geteuid()))\ntry:\n    keyboard.hook(lambda e: None)\n    print("hook: ok")\n    keyboard.unhook_all()\nexcept BaseException as e:\n    print("hook: " + type(e).__name__ + ": `
- `p-c3` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install keyboard`
  - commands: `printf 'import subprocess, sys, shutil\nfrom importlib import metadata\nfrozen = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True).split()\nprint("pip freeze after pip install keyboard: " + str(frozen))\nreq = metadata.requires("keyboard")\nprint("Requires-Dist metadata: " `
- `p-c4` image `python:2.7-slim` network `none`
  - setup: `pip install https://github.com/boppreh/keyboard/archive/d232de09bda50ecb5211ebcc59b85bc6da6aaa24.zip`
  - commands: `python -c 'import sys, keyboard; print("python " + sys.version.split()[0] + " keyboard " + keyboard.version + " normalize_name(Left Control)=" + keyboard.normalize_name("Left Control"))' > /tmp/imp.txt 2>&1; echo "exit=$?" >> /tmp/imp.txt; cat /tmp/imp.txt && python -c 'import keyboard, os, compilea`
- `p-c5` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip download keyboard --no-deps -d /tmp/dl && /tmp/v/bin/pip install --no-index --find-links /tmp/dl keyboard`
  - commands: `printf 'import glob, os\nfrom importlib import metadata\nw = [os.path.basename(x) for x in glob.glob("/tmp/dl/*")]\nprint("downloaded artifact: " + str(w))\nfiles = [str(f) for f in metadata.files("keyboard")]\nexts = sorted(set(os.path.splitext(f)[1] for f in files))\nprint("installed file extensio`
- `p-c6` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install https://github.com/boppreh/keyboard/archive/d232de09bda50ecb5211ebcc59b85bc6da6aaa24.zip`
  - commands: `/tmp/v/bin/python -c 'import keyboard, os; d=os.path.dirname(keyboard.__file__); print("test files shipped in package: " + str(sorted(f for f in os.listdir(d) if "test" in f)))' && echo '--- running keyboard._keyboard_tests as unprivileged user nobody (no /dev/input access possible) ---'; cd /tmp &&`
- `p-c7` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install https://github.com/boppreh/keyboard/archive/d232de09bda50ecb5211ebcc59b85bc6da6aaa24.zip`
  - commands: `echo '--- keyboard/__main__.py at pinned sha ---'; /tmp/v/bin/python -c 'import keyboard, os; print(open(os.path.join(os.path.dirname(keyboard.__file__), "__main__.py")).read())' && /tmp/v/bin/python -c 'import json, keyboard; e=keyboard.KeyboardEvent(event_type="down", scan_code=25, name="p", time=`
- `p-c8` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install https://github.com/boppreh/keyboard/archive/d232de09bda50ecb5211ebcc59b85bc6da6aaa24.zip`
  - commands: `printf 'import keyboard, sys, time\nseen = []\ntry:\n    keyboard.hook(lambda e: seen.append((e.event_type, e.name)))\n    keyboard.write("The quick brown fox jumps over the lazy dog.")\n    time.sleep(1)\n    typed = "".join(n for t, n in seen if t == "down" and n and len(n) == 1)\n    print("hooke`
- `p-c9` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install https://github.com/boppreh/keyboard/archive/d232de09bda50ecb5211ebcc59b85bc6da6aaa24.zip`
  - commands: `printf 'import keyboard, sys, time\nfired = []\ntry:\n    keyboard.add_hotkey("ctrl+shift+a", lambda *a: fired.append(a), args=("triggered", "hotkey"))\n    keyboard.add_hotkey("ctrl+shift+m, ctrl+space", lambda: fired.append("multistep"))\n    keyboard.send("ctrl+shift+a")\n    keyboard.send("ctrl+`
- `p-c10` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install https://github.com/boppreh/keyboard/archive/d232de09bda50ecb5211ebcc59b85bc6da6aaa24.zip`
  - commands: `echo '--- headless env: DISPLAY, /dev/input, /proc/bus/input/devices ---'; echo "DISPLAY=${DISPLAY:-<unset>}"; ls -la /dev/input 2>&1 | head -5; head -5 /proc/bus/input/devices 2>&1; true && echo '--- hook as unprivileged user nobody ---'; cd /tmp && timeout 30 runuser -u nobody -- /tmp/v/bin/python`
- `p-c11` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `printf 'import json, urllib.request\ndef get(u):\n    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "repo-probe"}), timeout=30)\n    return r.status, r.read().decode("utf-8", "replace")\nsha = "d232de09bda50ecb5211ebcc59b85bc6da6aaa24"\ns, readme = get("https://raw.gith`
- `p-c12` image `python:3.11-slim` network `none`
  - setup: `python3 -m venv /tmp/v && /tmp/v/bin/pip install https://github.com/boppreh/keyboard/archive/d232de09bda50ecb5211ebcc59b85bc6da6aaa24.zip`
  - commands: `printf 'import keyboard, inspect, os\nd = os.path.dirname(keyboard.__file__)\nnix = open(os.path.join(d, "_nixkeyboard.py")).read()\nwin = open(os.path.join(d, "_winkeyboard.py")).read()\nlsrc = inspect.getsource(keyboard._nixkeyboard.listen)\nprint("---- _nixkeyboard.listen source ----")\nprint(lsr`

## Step 3: EXECUTE on GitHub Actions, run `33287944553` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 /tmp/v/bin/pip show keyboard 2>&1 | head -3 && /tmp/v/bin/python -c 'import keyboard, sys; print("import ok: keyboard " + keyboard.version + " on python " + sys.version.split()[0])' && echo "VERDICT_LINE: PASS pip install keyboard exited 0 in a fresh venv and import keyboard succeeds" || echo "VERDICT_LINE: FAIL pip install keyboard or import keyboard failed in fresh venv"
STDOUT Name: keyboard
Version: 0.13.5
Summary: Hook and simulate keyboard events on Windows and Linux
import ok: keyboard 0.13.5 on python 3.11.16
VERDICT_LINE: PASS pip install keyboard exited 0 in a fresh venv and import keyboard succeeds

STDERR 
PHASE_A on:3.11-slim' locally
3.11-slim: Pulling from library/python
6310eb16bf42: Pulling fs layer
87e1b7cce023: Pulling fs layer
c86306e32cd0: Pulling fs layer
a14578096eda: Pulling fs layer
a14578096eda: Waiting
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

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: python3 -m pip install --upgrade pip

EXIT 0
p-c10 echo '--- headless env: DISPLAY, /dev/input, /proc/bus/input/devices ---'; echo "DISPLAY=${DISPLAY:-<unset>}"; ls -la /dev/input 2>&1 | head -5; head -5 /proc/bus/input/devices 2>&1; true && echo '--- hook as unprivileged user nobody ---'; cd /tmp && timeout 30 runuser -u nobody -- /tmp/v/bin/python -c 'import keyboard; keyboard.hook(lambda e: None); print("hook ok")' > /tmp/nr.txt 2>&1; echo "exit=$?" >> /tmp/nr.txt; tail -2 /tmp/nr.txt && printf 'import keyboard, os, re\nd = os.path.dirname(keyboard.__file__)\nnix = open(os.path.join(d, "_nixcommon.py")).read() + open(os.path.join(d, "_nixke
STDOUT --- headless env: DISPLAY, /dev/input, /proc/bus/input/devices ---
DISPLAY=<unset>
ls: cannot access '/dev/input': No such file or directory
I: Bus=0011 Vendor=0001 Product=0001 Version=ab00
N: Name="AT Translated Set 2 keyboard"
P: Phys=d34b2567-b9b6-42b9-8778-0a4ec0b
S: Sysfs=/devices/LNXSYSTM:00/LNXSYBUS:00/ACPI0004:00/MSFT1000:00/d34b2567-b9b6-42b9-8778-0a4ec0b955bf/serio0/input/input0
U: Uniq=
--- hook as unprivileged user nobody ---
FileNotFoundError: [Errno 2] No such file or directory: 'dumpkeys'
exit=1
device paths in linux backend: ['/dev/input/', '/dev/input/by-id', '/dev/input/event'] (README says /dev/input/input*)
/proc/bus/input/devices used: True
root check text: []
X references anywhere in package: []
non-root hook refused with root error: False
VERDICT_LINE: FAIL dev_input_paths=['/dev/input/', '/dev/input/by-id', '/dev/input/event'] nonroot_refused=False X_refs=[]

STDERR 
PHASE_A ata (pyproject.toml): star
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | verified / verified / verified | **verified** | high | `p-c1`: import ok: keyboard 0.13.5 on python 3.11.16 / VERDICT_LINE: PASS pip install keyboard exi |
| c2 | refuted / refuted / refuted | **refuted** | high | `p-c2`: --- as root --- euid 0 / hook: FileNotFoundError: [Errno 2] No such file or directory: 'du |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: pip freeze after pip install keyboard: ['keyboard==0.13.5'] / Requires-Dist metadata: ['py |
| c4 | verified / verified / verified | **verified** | high | `p-c4`: python 2.7.18 keyboard 0.13.5 normalize_name(Left Control)=left ctrl / Ran 148 tests in 0. |
| c5 | verified / verified / verified | **verified** | high | `p-c5`: downloaded artifact: ['keyboard-0.13.5-py3-none-any.whl'] / compiled/native files: [] / VE |
| c6 | verified / verified / verified | **verified** | high | `p-c6`: test files shipped in package: ['_keyboard_tests.py', '_mouse_tests.py'] / Ran 148 tests i |
| c7 | refuted / refuted / refuted | **refuted** | high | `p-c7`: to_json: {"event_type": "down", "scan_code": 25, "name": "p", "time": ...} json_fields_ok; |
| c8 | refuted / refuted / refuted | **refuted** | high | `p-c8`: --- real keyboard.write through a real hook (root, headless) --- real_write_error: FileNot |
| c9 | refuted / refuted / refuted | **refuted** | high | `p-c9`: real_hotkey_error: FileNotFoundError: [Errno 2] No such file or directory: 'dumpkeys'; --- |
| c10 | refuted / refuted / verified | **refuted** | low | `p-c10`: device paths in linux backend: ['/dev/input/', '/dev/input/by-id', '/dev/input/event'] (RE |
| c11 | verified / verified / verified | **verified** | high | `p-c11`: README at pinned sha: http 200, unmaintained banner present: True / VERDICT_LINE: PASS unm |
| c12 | verified / verified / verified | **verified** | high | `p-c12`: linux listen consults hook return value (required to block a key): False / windows backend |

## Step 5: REPORT
Overall score 58. Escalated to a human: none. Model calls: 4. Verdicts disagreeing with audited truth: c3, c7, c8, c9, c10.

Human checkpoint for this repository: c4: was refuted; Executed on python 2.7.18 and 3.x: import and the shipped tests pass (recorded by advanced-v3-heldout probe p-c4). Draft had guessed refuted. Toward the pipeline.; c6: was refuted; The package ships _keyboard_tests.py/_mouse_tests.py and 148 tests pass (recorded by advanced-v3-heldout probe p-c6); the claim 'tested' is literally true even though the tests mock the OS layer, which is the point of this hard case. Toward the pipeline.