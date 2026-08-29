"""Deterministic probe executor — NO LLM in this loop (DESIGN.md stage 4).
Input: a probes JSON file: {"case_id": str, "repo": str, "commit": str,
  "probes": [{"id": str, "claim_id": str, "image": "python:3.11-slim",
              "network": "install-only|none", "setup": [cmds], "commands": [cmds],
              "timeout_s": 120}]}
Each probe runs in a FRESH container: phase A (setup, network on: clone+install),
docker commit snapshot, phase B (commands, --network=none). Artifacts per probe:
probes_out/<probe_id>/{cmd.txt, stdout.log, stderr.log, exit_code, phase_a.log}.
Runs anywhere docker exists (GH Actions ubuntu runner, or any Linux box)."""
import json, pathlib, shlex, subprocess, sys, time

LIMITS = ["--memory=4g", "--cpus=2", "--pids-limit=256"]

def sh(cmd, timeout=None, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kw)

SRC_CACHE = {}

def host_checkout(repo, commit, workdir):
    """Clone once per (repo, commit) on the HOST (has git); containers get a ro-mount.
    Slim images ship without git — probe smoke-install failed exit 127 before this."""
    key = (repo, commit)
    if key in SRC_CACHE:
        return SRC_CACHE[key]
    dst = workdir / f"src-{abs(hash(key)) % 10**8}"
    sh(["git", "clone", "--quiet", repo, str(dst)], timeout=300)
    sh(["git", "-C", str(dst), "checkout", "--quiet", commit], timeout=60)
    SRC_CACHE[key] = dst
    return dst

def run_probe(spec, repo, commit, out_root):
    pid = spec["id"]
    out = out_root / pid
    out.mkdir(parents=True, exist_ok=True)
    tag = f"probe-{pid.lower()}"
    src = host_checkout(repo, commit, out_root.parent)
    setup = ["cp -r /repo-src /repo", "cd /repo"] + spec.get("setup", [])
    a = sh(["docker", "run", "--name", tag, *LIMITS,
            "-v", f"{src.resolve()}:/repo-src:ro", spec["image"],
            "bash", "-lc", " && ".join(setup)], timeout=900)
    (out / "phase_a.log").write_text((a.stdout or "") + "\n--stderr--\n" + (a.stderr or ""))
    if a.returncode != 0:
        (out / "exit_code").write_text(str(a.returncode))
        (out / "cmd.txt").write_text("PHASE_A_FAILED: " + " && ".join(setup))
        sh(["docker", "rm", "-f", tag])
        return a.returncode
    sh(["docker", "commit", tag, tag + "-img"])
    sh(["docker", "rm", "-f", tag])
    net = [] if spec.get("network") in ("on", "install-only") else ["--network=none"]  # "on": URL/badge/CI probes
    cmd = " && ".join(spec["commands"])
    (out / "cmd.txt").write_text(cmd)
    t0 = time.monotonic()
    try:
        b = sh(["docker", "run", "--rm", *net, *LIMITS, tag + "-img",
                "bash", "-lc", f"cd /repo && {cmd}"], timeout=spec.get("timeout_s", 120))
        code, so, se = b.returncode, b.stdout, b.stderr
    except subprocess.TimeoutExpired as e:
        code, so, se = 124, (e.stdout or ""), f"TIMEOUT after {spec.get('timeout_s', 120)}s"
    (out / "stdout.log").write_text((so or "")[:20000])
    (out / "stderr.log").write_text((se or "")[:20000])
    (out / "exit_code").write_text(str(code))
    (out / "wall_s").write_text(f"{time.monotonic()-t0:.1f}")
    sh(["docker", "rmi", "-f", tag + "-img"])
    return code

def main():
    spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out_root = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "probes_out") / spec["case_id"]
    results = {}
    for p in spec["probes"]:
        results[p["id"]] = run_probe(p, spec["repo"], spec["commit"], out_root)
        print(f"{p['id']}: exit={results[p['id']]}", file=sys.stderr)
    (out_root / "summary.json").write_text(json.dumps(results, indent=1))

if __name__ == "__main__":
    main()
