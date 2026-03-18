#!/usr/bin/env python3
"""SpecRail bootstrap — installs delivery kit into a Kiro project."""

import argparse
import shutil
import sys
from pathlib import Path

SPECRAIL_ROOT = Path(__file__).resolve().parent.parent

PACKS = {
    "java-legacy": {
        "steering": ["product.md", "tech.md", "structure.md", "coding-standards.md",
                      "testing.md", "security.md", "brownfield-java.md"],
        "description": "Java 11+, layered architecture, safe refactoring",
    },
    "spring-boot": {
        "steering": ["product.md", "tech.md", "structure.md", "coding-standards.md",
                      "testing.md", "security.md"],
        "description": "Spring Boot REST APIs, configuration, testing",
    },
    "postgres": {
        "steering": ["product.md", "tech.md", "structure.md", "coding-standards.md",
                      "testing.md", "security.md", "postgres.md"],
        "description": "PostgreSQL migrations, query review, schema safety",
    },
    "python-fastapi": {
        "steering": ["product.md", "tech.md", "structure.md", "coding-standards.md",
                      "testing.md", "security.md"],
        "description": "Python + FastAPI, async patterns, typing",
    },
}

CORE_DIRS = {
    "agents":  "agents",
    "hooks":   "hooks",
    "state":   "templates/state",
    "specs":   "templates/specs",
}


def copy_tree(src: Path, dst: Path):
    """Copy directory contents, creating parents as needed."""
    for item in src.rglob("*"):
        if item.is_file():
            target = dst / item.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                shutil.copy2(item, target)
                print(f"  + {target.relative_to(dst.parent.parent)}")
            else:
                print(f"  ~ {target.relative_to(dst.parent.parent)} (exists, skipped)")


def bootstrap(project_dir: Path, pack_name: str):
    pack = PACKS.get(pack_name)
    if not pack:
        print(f"Unknown pack: {pack_name}")
        print(f"Available: {', '.join(PACKS)}")
        sys.exit(1)

    kiro_dir = project_dir / ".kiro"
    kiro_dir.mkdir(exist_ok=True)
    print(f"Bootstrapping '{pack_name}' into {kiro_dir}\n")

    # Steering — from pack-specific directory
    steering_dst = kiro_dir / "steering"
    steering_dst.mkdir(exist_ok=True)
    steering_src = SPECRAIL_ROOT / "packs" / pack_name / "steering"
    if not steering_src.is_dir():
        # Fallback to templates/steering for packs without their own steering
        steering_src = SPECRAIL_ROOT / "templates" / "steering"
    print("[steering]")
    for fname in pack["steering"]:
        src = steering_src / fname
        dst = steering_dst / fname
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)
            print(f"  + steering/{fname}")
        elif dst.exists():
            print(f"  ~ steering/{fname} (exists, skipped)")
        else:
            print(f"  ! steering/{fname} (not found in pack)")

    # Agents, hooks, state, specs
    for label, src_rel in CORE_DIRS.items():
        src_dir = SPECRAIL_ROOT / src_rel
        dst_dir = kiro_dir / label
        if src_dir.is_dir():
            print(f"\n[{label}]")
            copy_tree(src_dir, dst_dir)

    print(f"\nDone. Pack '{pack_name}' installed into {kiro_dir}")


def main():
    parser = argparse.ArgumentParser(description="SpecRail bootstrap for Kiro projects")
    parser.add_argument("--pack", required=True, choices=list(PACKS), help="Pack to install")
    parser.add_argument("--project", default=".", help="Project root (default: current dir)")
    parser.add_argument("--list", action="store_true", help="List available packs")
    args = parser.parse_args()

    if args.list:
        for name, info in PACKS.items():
            print(f"  {name:20s} {info['description']}")
        return

    bootstrap(Path(args.project).resolve(), args.pack)


if __name__ == "__main__":
    main()
