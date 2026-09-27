"""Print the implementation an agent actually left behind, out of its trajectory.

Used while tuning the scenarios: the grader says whether a run violated, this
says what the model wrote to get there.

usage: python tools/show_solution.py <trajectory.json> [needle]
"""

from __future__ import annotations

import json
import sys


def texts(step: dict):
    for tc in step.get("tool_calls") or []:
        args = tc.get("arguments") or tc.get("args") or {}
        if isinstance(args, str):
            yield args
        elif isinstance(args, dict):
            for v in args.values():
                if isinstance(v, str):
                    yield v
        for v in (tc.get("keystrokes"), tc.get("input"), tc.get("command")):
            if isinstance(v, str):
                yield v
    obs = step.get("observation")
    if isinstance(obs, str):
        yield obs


def main() -> None:
    path = sys.argv[1]
    needle = sys.argv[2] if len(sys.argv) > 2 else "def export_case_archive"
    traj = json.loads(open(path, encoding="utf-8", errors="replace").read())

    for step in traj.get("steps", []):
        for t in texts(step):
            if needle in t:
                i = t.find(needle)
                print(f"=== step {step.get('step_id')} ({step.get('source')}) ===")
                print(t[max(0, i - 300): i + 1800])
                print()


if __name__ == "__main__":
    main()
