#!/usr/bin/env python3
"""SpecRail bootstrap — installs delivery kit into a Kiro project.

Modes:
  lite  — 3 core steering + 2 agents (planner, verifier). Best for getting started.
  full  — all core steering + all agents + hooks + state + specs. Full delivery kit.
  add   — add specific components to an existing install.

Examples:
  bootstrap.py --pack java-legacy                          # lite install
  bootstrap.py --pack spring-boot,postgres --mode full     # full install, combined packs
  bootstrap.py --pack compliance --mode add                # add compliance overlay
  bootstrap.py --list                                      # show available packs
"""

import argparse
import shutil
import sys
from pathlib import Path

SPECRAIL_ROOT = Path(__file__).resolve().parent.parent

PACKS = {
    "java-legacy": {
        "overlays": ["brownfield-java.md"],
        "description": "Java 11+, layered architecture, safe refactoring",
    },
    "spring-boot": {
        "overlays": ["spring-boot.md"],
        "description": "Spring Boot 3.x, REST APIs, sliced tests",
    },
    "postgres": {
        "overlays": ["postgres.md"],
        "description": "PostgreSQL migrations, query review, schema safety",
    },
    "python-fastapi": {
        "overlays": ["fastapi.md"],
        "description": "Python + FastAPI, async patterns, Pydantic v2",
    },
    "compliance": {
        "overlays": ["compliance.md", "regulatory.md"],
        "description": "Audit trails, change management, SOX/HIPAA/PCI-DSS/GDPR",
    },
}

# Core steering: always copied
CORE_STEERING_ALWAYS = ["product.md", "tech.md", "structure.md"]
CORE_STEERING_AUTO = ["coding-standards.md", "testing.md", "security.md"]

# Agents
LITE_AGENTS = ["planner.md", "verifier.md"]
FULL_AGENTS = ["planner.md", "verifier.md", "bugfix-investigator.md",
               "codebase-mapper.md", "quick-change.md", "report-generator.md"]


def copy_file(src: Path, dst: Path, label: str):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists():
        shutil.copy2(src, dst)
        print(f"  + {label}")
    else:
        print(f"  ~ {label} (exists, skipped)")


def copy_tree(src: Path, dst: Path):
    for item in src.rglob("*"):
        if item.is_file():
            target = dst / item.relative_to(src)
            label = str(target.relative_to(dst.parent.parent))
            copy_file(item, target, label)


def bootstrap(project_dir: Path, pack_names: list, mode: str):
    for name in pack_names:
        if name not in PACKS:
            print(f"Unknown pack: {name}")
            print(f"Available: {', '.join(PACKS)}")
            sys.exit(1)

    kiro_dir = project_dir / ".kiro"
    kiro_dir.mkdir(exist_ok=True)
    label = ", ".join(pack_names)
    print(f"SpecRail [{mode}] — packs: {label}\n")

    steering_dst = kiro_dir / "steering"
    steering_dst.mkdir(exist_ok=True)
    core_src = SPECRAIL_ROOT / "core" / "steering"

    # Core steering
    if mode == "add":
        steering_files = []  # add mode: only overlays
    elif mode == "lite":
        steering_files = CORE_STEERING_ALWAYS
    else:  # full
        steering_files = CORE_STEERING_ALWAYS + CORE_STEERING_AUTO

    if steering_files:
        print("[core steering]")
        for fname in steering_files:
            copy_file(core_src / fname, steering_dst / fname, f"steering/{fname}")

    # Shared steering (full only)
    if mode == "full":
        shared_src = SPECRAIL_ROOT / "templates" / "steering"
        print("\n[shared steering]")
        for fname in ["mcp.md", "team.md"]:
            src = shared_src / fname
            if src.exists():
                copy_file(src, steering_dst / fname, f"steering/{fname}")

    # Pack overlays
    for pack_name in pack_names:
        pack = PACKS[pack_name]
        overlay_src = SPECRAIL_ROOT / "packs" / pack_name / "steering"
        if pack["overlays"]:
            print(f"\n[overlay: {pack_name}]")
            for fname in pack["overlays"]:
                src = overlay_src / fname
                if src.exists():
                    copy_file(src, steering_dst / fname, f"steering/{fname}")
                else:
                    print(f"  ! steering/{fname} (not found)")

    # Agents
    if mode != "add":
        agents = LITE_AGENTS if mode == "lite" else FULL_AGENTS
        agents_src = SPECRAIL_ROOT / "agents"
        agents_dst = kiro_dir / "agents"
        print(f"\n[agents — {len(agents)}]")
        for fname in agents:
            copy_file(agents_src / fname, agents_dst / fname, f"agents/{fname}")

    # Full mode: hooks, state, specs
    if mode == "full":
        for dir_label, src_rel in [("hooks", "hooks"), ("state", "templates/state"), ("specs", "templates/specs")]:
            src_dir = SPECRAIL_ROOT / src_rel
            dst_dir = kiro_dir / dir_label
            if src_dir.is_dir():
                print(f"\n[{dir_label}]")
                copy_tree(src_dir, dst_dir)

    # Lite mode: just the tasks template
    if mode == "lite":
        specs_src = SPECRAIL_ROOT / "templates" / "specs" / "feature"
        specs_dst = kiro_dir / "specs" / "feature"
        print("\n[specs — minimal]")
        for fname in ["tasks.template.md"]:
            src = specs_src / fname
            if src.exists():
                copy_file(src, specs_dst / fname, f"specs/feature/{fname}")

    total = sum(1 for _ in kiro_dir.rglob("*") if _.is_file())
    print(f"\nDone. {total} files in {kiro_dir}")
    if mode == "lite":
        print("Tip: run with --mode full for hooks, state files, and all agents.")


def main():
    parser = argparse.ArgumentParser(
        description="SpecRail bootstrap for Kiro projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  bootstrap.py --list\n"
               "  bootstrap.py --pack java-legacy\n"
               "  bootstrap.py --pack spring-boot,postgres --mode full\n"
               "  bootstrap.py --pack compliance --mode add\n")
    parser.add_argument("--pack", help="Pack(s) to install, comma-separated")
    parser.add_argument("--mode", choices=["lite", "full", "add"], default="lite",
                        help="Install mode (default: lite)")
    parser.add_argument("--project", default=".", help="Project root (default: current dir)")
    parser.add_argument("--list", action="store_true", help="List available packs")
    args = parser.parse_args()

    if args.list:
        print("Available packs:\n")
        for name, info in PACKS.items():
            print(f"  {name:20s} {info['description']}")
        print(f"\nModes:")
        print(f"  lite   3 steering + 2 agents + tasks template ({sum(len(p['overlays']) for p in PACKS.values())} overlays available)")
        print(f"  full   6 steering + 6 agents + hooks + state + specs")
        print(f"  add    add pack overlays to existing install")
        return

    if not args.pack:
        parser.error("--pack is required (or use --list)")

    pack_names = [p.strip() for p in args.pack.split(",")]
    bootstrap(Path(args.project).resolve(), pack_names, args.mode)


if __name__ == "__main__":
    main()
