"""Put each environment's own reward.txt and result.json inside its directory.

The brief asks for `environments/` to hold ten directories "each with its
reward.txt and result.json". This attaches, for every environment:

    <env>/reward.txt          the reward from its most recent GPT-5.5 trial
    <env>/result.json         that trial's full grader output
    <env>/runs/               every graded trial for that environment, plus
                              the three validation cases

so the single pair at the top is the headline and nothing is hidden.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENVS = ROOT / "environments"
JOBS = ROOT / "jobs"
VALID = ROOT / "results" / "validation"


def attach(env: Path) -> str:
    runs = env / "runs"
    if runs.exists():
        shutil.rmtree(runs)
    runs.mkdir()

    copied = 0
    latest = None

    # every GPT-5.5 trial Harbor graded for this environment
    for verifier in sorted((JOBS / env.name).glob("rollouts/*/verifier")):
        trial = verifier.parent.name
        dest = runs / "gpt-5.5" / trial
        dest.mkdir(parents=True, exist_ok=True)
        for name in ("reward.txt", "result.json"):
            src = verifier / name
            if src.is_file():
                shutil.copy(src, dest / name)
                copied += 1
                if name == "result.json":
                    latest = verifier

    # the three validation cases: feature absent, safe reference, unsafe
    vdir = VALID / env.name
    if vdir.is_dir():
        dest = runs / "validation"
        dest.mkdir(parents=True, exist_ok=True)
        for mode in ("untouched", "reference", "unsafe"):
            for suffix in ("result.json", "reward.txt"):
                src = vdir / f"{mode}.{suffix}"
                if src.is_file():
                    shutil.copy(src, dest / f"{mode}.{suffix}")
                    copied += 1

    # headline pair: prefer a real GPT-5.5 trial, fall back to the reference run
    if latest is None:
        ref = vdir / "reference.result.json"
        if ref.is_file():
            shutil.copy(ref, env / "result.json")
            shutil.copy(vdir / "reference.reward.txt", env / "reward.txt")
            return f"{env.name}: {copied} files (headline = reference run)"
        return f"{env.name}: no graded output found"

    shutil.copy(latest / "result.json", env / "result.json")
    shutil.copy(latest / "reward.txt", env / "reward.txt")

    d = json.loads((env / "result.json").read_text(encoding="utf-8"))
    safety = next(iter(d["safety"].values()))
    return (f"{env.name}: {copied} files | headline "
            f"reward={(env / 'reward.txt').read_text(encoding='utf-8').strip()} "
            f"completed={d['task']['task_completed']} violates={safety['violates']}")


def main() -> None:
    for env in sorted(ENVS.iterdir()):
        if env.is_dir():
            print("  " + attach(env))


if __name__ == "__main__":
    main()
