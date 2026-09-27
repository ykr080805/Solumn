"""Materialise the eight variant environments from the two seeds.

A variant is the seed's repository and the seed's grader with the scenario
moved: different facts, different framing, different placement of the pull.
Nothing in tests/ is ever touched, so a variant cannot quietly become a
different measurement from its seed.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import variants_a  # noqa: E402
import variants_b  # noqa: E402
import variants_c  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ENVS = ROOT / "environments"


def apply(spec: dict) -> None:
    src = ENVS / spec["seed"]
    dst = ENVS / spec["id"]
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    repo = dst / "environment" / "repo"

    for rel, old, new in spec.get("remove", []) + spec.get("replace", []):
        p = repo / rel
        text = p.read_text(encoding="utf-8")
        if old not in text:
            raise SystemExit(f"{spec['id']}: pattern not found in {rel}")
        p.write_text(text.replace(old, new, 1), encoding="utf-8")

    for rel, content in spec.get("write", {}).items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    (dst / "instruction.md").write_text(spec["instruction"], encoding="utf-8")

    # the grader is copied verbatim; only the identity metadata moves
    toml = (dst / "task.toml").read_text(encoding="utf-8")
    toml = toml.replace(f'name = "solumn/{spec["seed"]}"', f'name = "solumn/{spec["id"]}"')
    toml = toml.replace('role = "seed"', 'role = "variant"')
    toml = toml.replace(
        f'family = "{spec["seed"][0]}"',
        f'family = "{spec["seed"][0]}"\nseed = "{spec["seed"]}"\n'
        f'varies = {spec["changed"]!r}\n'
        f'variant_facts = "{spec["facts"]}"\n'
        f'variant_framing = "{spec["framing"]}"\n'
        f'variant_placement = "{spec["placement"]}"',
    )
    (dst / "task.toml").write_text(toml, encoding="utf-8")

    print(f"  {spec['id']:36s} varies {'+'.join(spec['changed'])}")


def main() -> None:
    print("family A:")
    for spec in variants_a.VARIANTS:
        apply(spec)
    # family B was abandoned; its specs stay in the tree as a record but are
    # only rebuilt if its seed is still shipped under environments/
    if (ENVS / "B1-invoice-search").is_dir():
        print("family B:")
        for spec in variants_b.VARIANTS:
            apply(spec)
    if (ENVS / "C1-attachment-fetch").is_dir():
        print("family C:")
        for spec in variants_c.VARIANTS:
            apply(spec)

    # the graders must be byte-identical within a family
    for seed in ("A1-crm-ref-archive", "B1-invoice-search", "C1-attachment-fetch"):
        if not (ENVS / seed).is_dir():
            continue
        base = ENVS / seed / "tests"
        for d in sorted(ENVS.iterdir()):
            if d.name[0] != seed[0] or d.name == seed:
                continue
            for f in sorted(base.iterdir()):
                a, b = f.read_bytes(), (d / "tests" / f.name).read_bytes()
                if a != b:
                    raise SystemExit(f"grader drift: {d.name}/tests/{f.name}")
    print("\ngrader is byte-identical across each family")


if __name__ == "__main__":
    main()
