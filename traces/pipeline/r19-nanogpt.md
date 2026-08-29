# Pipeline trajectory: r19-nanogpt (proof `advanced-v3-ext-rescored-1788028882`)

Repository https://github.com/karpathy/nanoGPT @ `3adf61e154c3`. Buyer question: _We want to use nanoGPT as the reference training loop for an internal LLM course and cite its numbers — does the documented pip install and Shakespeare quick start actually run on a CPU-only machine today, which of the README's loss/timing figures are reproducible without an A100 cluster, and is the project still maintained?_

## Step 1: instructions
See `arms/PROMPTS.md` (PLAN, EXECUTE, ADJUDICATE). Claims given to the agent:

- **c1** (install): The documented dependency set installs with the single command `pip install torch numpy transformers datasets tiktoken wandb tqdm` on a current CPU-only Python.
- **c2** (quickstart): Running `python data/shakespeare_char/prepare.py` in a clone downloads the ~1 MB tiny-shakespeare text and creates the files train.bin and val.bin in data/shakespeare_char/.
- **c3** (interface): The config file config/train_shakespeare_char.py specifies a GPT with block_size 256 (context of up to 256 characters), n_embd 384, n_layer 6 and n_head 6.
- **c4** (quantitative): On a single A100 GPU, `python train.py config/train_shakespeare_char.py` takes about 3 minutes and reaches a best validation loss of 1.4697.
- **c5** (quickstart): On a CPU-only machine, the exact command `python train.py config/train_shakespeare_char.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0` runs to completion and writes a checkpoint to out-shakespeare-char/ckpt.pt.
- **c6** (quantitative): The CPU command in c5 runs in about 3 minutes and reaches a validation loss of about 1.88.
- **c7** (quickstart): After the CPU training run, `python sample.py --out_dir=out-shakespeare-char --device=cpu` loads the checkpoint and prints generated text samples.
- **c8** (quantitative): train.py is approximately a 300-line training loop and model.py approximately a 300-line GPT model definition (each within ~15% of 300 lines at the pinned commit).
- **c9** (quantitative): Evaluating the OpenAI GPT-2 checkpoints on OpenWebText with `python train.py config/eval_gpt2.py` (and the _medium/_large/_xl variants) yields train/val losses of 3.11/3.12 (gpt2, 124M), 2.85/2.84 (gpt2-medium, 350M), 2.66/2.67 (gpt2-large, 774M) and 2.56/2.54 (gpt2-xl, 1558M).
- **c10** (quantitative): Reproducing GPT-2 (124M) with `torchrun --standalone --nproc_per_node=8 train.py config/train_gpt2.py` on an 8xA100 40GB node takes about 4 days and reaches a loss of about 2.85.
- **c11** (interface): `sample.py` can sample from OpenAI's released GPT-2 models via `--init_from=gpt2-xl` (or any gpt2 variant) with `--start="..." --num_samples=5 --max_new_tokens=100`, and `--start=FILE:prompt.txt` reads the prompt from a file.
- **c12** (environment): nanoGPT is declared old and deprecated by its author, with a successor project karpathy/nanochat that exists on GitHub.

## Step 2: PLAN output, 12 probes (`eval/probes/r19-nanogpt.json`, matched to this run by its evidence index)

- `p-c1` image `python:3.11-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install -q torch numpy transformers datasets tiktoken wandb tqdm --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple`
  - commands: `/tmp/v/bin/pip check || true && /tmp/v/bin/python -c "import torch,numpy,transformers,datasets,tiktoken,wandb,tqdm;print('torch',torch.__version__,'numpy',numpy.__version__,'transformers',transformers.__version__,'datasets',datasets.__version__,'tiktoken',tiktoken.__version__,'wandb',wandb.__version`
- `p-c2` image `python:3.11-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install -q torch numpy transformers datasets tiktoken wandb tqdm --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple && python -c "import urllib.request,tarfile,io;d=urllib.request.urlopen('https://github.com/karpathy/nan`
  - commands: `cd /tmp/ng && grep -n '^import' data/shakespeare_char/prepare.py; /tmp/v/bin/pip show requests 2>/dev/null | head -2 || echo 'requests NOT installed' && cd /tmp/ng && /tmp/v/bin/python data/shakespeare_char/prepare.py; echo prepare_exit=$? && cd /tmp/ng && ls -l data/shakespeare_char/input.txt data/`
- `p-c3` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python -c "import urllib.request,re;s=urllib.request.urlopen('https://raw.githubusercontent.com/karpathy/nanoGPT/3adf61e154c3fe3fca428ad6bc3818b27a3b8291/config/train_shakespeare_char.py',timeout=30).read().decode();v={k:int(re.search(r'^%s\s*=\s*(\d+)'%k,s,re.M).group(1)) for k in ['block_size','n_`
- `p-c4` image `python:3.11-slim` network `none`
  - setup: ``
  - commands: `ls /dev/nvidia* 2>/dev/null || echo 'no /dev/nvidia* devices'; command -v nvidia-smi >/dev/null && nvidia-smi -L || echo 'nvidia-smi absent' && python -c "import glob;g=glob.glob('/dev/nvidia*');print('nvidia_devices',g);assert g,'no GPU'" && echo "VERDICT_LINE: PASS a GPU is present (unexpected) - `
- `p-c5` image `python:3.11-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install -q torch numpy transformers tiktoken --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple && python -c "import urllib.request,tarfile,io;d=urllib.request.urlopen('https://github.com/karpathy/nanoGPT/archive/3adf61e`
  - commands: `cd /tmp/ng && nproc && timeout 100 /tmp/v/bin/python train.py config/train_shakespeare_char.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=100 --lr_decay_iters=100 --eval_interval=50 --dropout=0.0 > /tm`
- `p-c6` image `python:3.11-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install -q torch numpy transformers tiktoken --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple && python -c "import urllib.request,tarfile,io;d=urllib.request.urlopen('https://github.com/karpathy/nanoGPT/archive/3adf61e`
  - commands: `cd /tmp/ng && echo cpus=$(nproc); START=$(date +%s); timeout 100 /tmp/v/bin/python train.py config/train_shakespeare_char.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=200 --lr_decay_iters=2000 --eval_`
- `p-c7` image `python:3.11-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install -q torch numpy transformers tiktoken --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple && python -c "import urllib.request,tarfile,io;d=urllib.request.urlopen('https://github.com/karpathy/nanoGPT/archive/3adf61e`
  - commands: `cd /tmp/ng && timeout 60 /tmp/v/bin/python train.py config/train_shakespeare_char.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=100 --lr_decay_iters=100 --eval_interval=50 --dropout=0.0 > /tmp/train.lo`
- `p-c8` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python -c "import urllib.request;b='https://raw.githubusercontent.com/karpathy/nanoGPT/3adf61e154c3fe3fca428ad6bc3818b27a3b8291/';n={f:len(urllib.request.urlopen(b+f,timeout=30).read().decode().splitlines()) for f in ['train.py','model.py']};print('line_counts',n,'window 255-345');bad=[f for f,c in `
- `p-c9` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python -c "import urllib.request,re;b='https://raw.githubusercontent.com/karpathy/nanoGPT/3adf61e154c3fe3fca428ad6bc3818b27a3b8291/';[print(f,re.findall(r'^(init_from|dataset|eval_iters|batch_size)\s*=\s*(.+)$',urllib.request.urlopen(b+f,timeout=30).read().decode(),re.M)) for f in ['config/eval_gpt2`
- `p-c10` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python -c "import urllib.request,re;b='https://raw.githubusercontent.com/karpathy/nanoGPT/3adf61e154c3fe3fca428ad6bc3818b27a3b8291/';s=urllib.request.urlopen(b+'config/train_gpt2.py',timeout=30).read().decode();print('train_gpt2_config',re.findall(r'^(batch_size|block_size|gradient_accumulation_step`
- `p-c11` image `python:3.11-slim` network `on`
  - setup: `python -m venv /tmp/v && /tmp/v/bin/pip install -q torch numpy transformers tiktoken --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple && python -c "import urllib.request,tarfile,io;d=urllib.request.urlopen('https://github.com/karpathy/nanoGPT/archive/3adf61e`
  - commands: `cd /tmp/ng && /tmp/v/bin/python -c "s=open('sample.py').read();need=['init_from','start','num_samples','max_new_tokens','FILE:'];miss=[k for k in need if k not in s];print('sample.py missing_tokens',miss)" && cd /tmp/ng && echo 'Once upon a time' > prompt.txt && timeout 100 /tmp/v/bin/python sample.`
- `p-c12` image `python:3.11-slim` network `on`
  - setup: ``
  - commands: `python -c "import urllib.request,json;h={'User-Agent':'probe'};r=urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/karpathy/nanochat',headers=h),timeout=30);j=json.load(r);print('nanochat http',r.status,j['full_name'],'created',j['created_at'],'stars',j.get('stargazers_coun`

## Step 3: EXECUTE on GitHub Actions, run `33265940112` (artifacts: per-probe cmd, stdout, stderr, exit code)

Transcript index (probe, command, recorded output):
```
p-c1 /tmp/v/bin/pip check || true && /tmp/v/bin/python -c "import torch,numpy,transformers,datasets,tiktoken,wandb,tqdm;print('torch',torch.__version__,'numpy',numpy.__version__,'transformers',transformers.__version__,'datasets',datasets.__version__,'tiktoken',tiktoken.__version__,'wandb',wandb.__version__,'tqdm',tqdm.__version__,'cuda_available',torch.cuda.is_available())" && echo "VERDICT_LINE: PASS all 7 documented packages install and import in a CPU-only venv (torch taken from the pytorch CPU wheel index because a bare 'pip install torch' on Linux pulls multi-GB CUDA wheels; claim is read as C
STDOUT No broken requirements found.
torch 2.13.0+cpu numpy 2.4.6 transformers 5.16.1 datasets 5.0.1 tiktoken 0.14.0 wandb 0.29.0 tqdm 4.70.0 cuda_available False
VERDICT_LINE: PASS all 7 documented packages install and import in a CPU-only venv (torch taken from the pytorch CPU wheel index because a bare 'pip install torch' on Linux pulls multi-GB CUDA wheels; claim is read as CPU-only)

STDERR 
PHASE_A  Pulling from library/python
6310eb16bf42: Pulling fs layer
87e1b7cce023: Pulling fs layer
c86306e32cd0: Pulling fs layer
a14578096eda: Pulling fs layer
a14578096eda: Waiting
87e1b7cce023: Verifying Checksum
87e1b7cce023: Download complete
a14578096eda: Verifying Checksum
a14578096eda: Download complete
c86306e32cd0: Verifying Checksum
c86306e32cd0: Download complete
6310eb16bf42: Verifying Checksum
6310eb16bf42: Download complete
6310eb16bf42: Pull complete
87e1b7cce023: Pull complete
c86306e32cd0: Pull complete
a14578096eda: Pull complete
Digest: sha256:1042b61448fef4ba92d16a8c7eb4996d027568ce64792a7877fd88511e0af7c6
Status: Downloaded newer image for python:3.11-slim

[notice] A new release of pip is available: 24.0 -> 26.2.1
[notice] To update, run: python -m pip install --upgrade pip

EXIT 0
p-c10 python -c "import urllib.request,re;b='https://raw.githubusercontent.com/karpathy/nanoGPT/3adf61e154c3fe3fca428ad6bc3818b27a3b8291/';s=urllib.request.urlopen(b+'config/train_gpt2.py',timeout=30).read().decode();print('train_gpt2_config',re.findall(r'^(batch_size|block_size|gradient_accumulation_steps|max_iters|lr_decay_iters)\s*=\s*(.+)$',s,re.M));r=urllib.request.urlopen(b+'assets/gpt2_124M_loss.png',timeout=30);print('loss_curve_png http',r.status,len(r.read()),'bytes')" && echo "VERDICT_LINE: FAIL unverifiable in sandbox: config/train_gpt2.py and the loss-curve PNG exist, but the ~4 day 8xA
STDOUT train_gpt2_config [('batch_size', '12'), ('block_size', '1024'), ('gradient_accumulation_steps', '5 * 8'), ('max_iters', '600000'), ('lr_decay_iters', '600000')]
loss_curve_png http 200 110433 bytes
VERDICT_LINE: FAIL unverifiable in sandbox: config/train_gpt2.py and the loss-curve PNG exist, but the ~4 day 8xA100 DDP run cannot be executed here (no GPU, 120s budget); wall-clock and ~2.85 loss unmeasured

STDERR 
PHASE_A 
--stderr--

EXIT 0
p-c11 cd /tmp/ng && /tmp/v/bin/python -c "s=open('sample.py').read();need=['init_from','start','num_samples','max_new_t
```

## Step 4: ADJUDICATE, votes then verdict per claim (confidence demoted on disagreement)

| claim | votes | final | conf | evidence cited |
|---|---|---|---|---|
| c1 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c1`: torch 2.13.0+cpu numpy 2.4.6 transformers 5.16.1 datasets 5.0.1 tiktoken 0.14.0 wandb 0.29 |
| c2 | verified / verified / verified | **verified** | high | `p-c2`: length of dataset in characters: 1,115,394 / train has 1,003,854 tokens / val has 111,540  |
| c3 | verified / verified / verified | **verified** | high | `p-c3`: observed {'block_size': 256, 'n_embd': 384, 'n_layer': 6, 'n_head': 6}; exit_code 0 |
| c4 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c4`: no /dev/nvidia* devices / nvidia-smi absent / nvidia_devices [] / VERDICT_LINE: FAIL unver |
| c5 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c5`: train_exit=1 / ZeroDivisionError: division by zero in get_lr: decay_ratio = (it - warmup_i |
| c6 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c6`: exit=0 wall_200_iters=12s / step 200: train loss 2.4804, val loss 2.4894 / mean_ms_per_ite |
| c7 | verified / verified / verified | **verified** | high | `p-c7`: sample_exit=0 / number of parameters: 0.80M / Loading meta from data/shakespeare_char/meta |
| c8 | verified / verified / verified | **verified** | high | `p-c8`: line_counts {'train.py': 336, 'model.py': 330} window 255-345; exit_code 0 |
| c9 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c9`: config/eval_gpt2.py ... init_from 'gpt2' (and _medium/_large/_xl configs present) / openwe |
| c10 | unverifiable / unverifiable / unverifiable | **unverifiable** | low | `p-c10`: train_gpt2_config [('batch_size','12'),('block_size','1024'),('gradient_accumulation_steps |
| c11 | verified / verified / verified | **verified** | high | `p-c11`: sample.py missing_tokens [] / sample_exit=0 / number of parameters: 123.65M / No meta.pkl  |
| c12 | verified / verified / verified | **verified** | high | `p-c12`: nanochat http 200 karpathy/nanochat created 2025-10-13T13:46:35Z stars 57628 / pinned_READ |

## Step 5: REPORT
Overall score 75. Escalated to a human: ['c1', 'c4', 'c5', 'c6', 'c9', 'c10']. Model calls: 4. Verdicts disagreeing with audited truth: c1.

Human checkpoint for this repository: c5: was verified; The probe scaled --max_iters/--lr_decay_iters from 2000 to 100 to fit the 120 s budget and crashed in get_lr (ZeroDivisionError: lr_decay_iters == warmup_iters), a failure the probe caused, not the README. The as-written command was not executed within budget, so the honest verdict is unverifiable (the arm abstained; the draft had guessed verified). Neutral correction.; c1: Probe installed torch from the CPU wheel index instead of the bare `pip install torch` the README gives (the bare command pulls multi-GB CUDA wheels but does succeed). Under rule (c) the arm marked this unverifiable-as-written; truth stays verified because the documented command does work. Counted against the pipeline's accuracy.