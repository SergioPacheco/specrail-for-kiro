"""KiroRails installer — copies delivery kit files into a Kiro project."""

import shutil
from pathlib import Path

DATA_ROOT = Path(__file__).parent / "data"

BLUEPRINTS = {
    "java-legacy": {
        "overlays": ["brownfield-java.md"],
        "desc": "Java 11+, layered architecture, safe refactoring",
    },
    "spring-boot": {
        "overlays": ["spring-boot.md"],
        "desc": "Spring Boot 3.x, REST APIs, sliced tests",
    },
    "postgres": {
        "overlays": ["postgres.md"],
        "desc": "PostgreSQL migrations, query review, schema safety",
    },
    "python-fastapi": {
        "overlays": ["fastapi.md"],
        "desc": "Python + FastAPI, async patterns, Pydantic v2",
    },
    "compliance": {
        "overlays": ["compliance.md", "regulatory.md"],
        "desc": "Audit trails, SOX/HIPAA/PCI-DSS/GDPR",
    },
}

CORE_STEERING = ["product.md", "tech.md", "structure.md", "coding-standards.md", "skills.md",
                 "testing.md", "security.md"]
AGENTS = ["verifier.md", "clarifier.md", "analyzer.md", "learner.md", "bugfix-investigator.md"]


def _copy(src: Path, dst: Path, label: str) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        print(f"  ~ {label} (exists)")
        return False
    shutil.copy2(src, dst)
    print(f"  ✓ {label}")
    return True


def install(project_dir: Path, packs: list[str]):
    """Install KiroRails into a project directory."""
    for p in packs:
        if p not in BLUEPRINTS:
            print(f"❌ Unknown blueprint: {p}")
            print(f"   Available: {', '.join(BLUEPRINTS)}")
            raise SystemExit(1)

    kiro = project_dir / ".kiro"
    steering = kiro / "steering"
    steering.mkdir(parents=True, exist_ok=True)
    core_src = DATA_ROOT / "core" / "steering"

    print(f"\n🛤️  KiroRails — blueprints: {', '.join(packs)}\n")

    # ── Steering (guardrails) ───────────────────────────────────────────
    print("[expert guardrails]")
    for f in CORE_STEERING:
        _copy(core_src / f, steering / f, f"steering/{f}")

    # ── Blueprint overlays ──────────────────────────────────────────────
    for name in packs:
        overlay_src = DATA_ROOT / "packs" / name / "steering"
        print(f"\n[blueprint: {name}]")
        for f in BLUEPRINTS[name]["overlays"]:
            src = overlay_src / f
            if src.exists():
                _copy(src, steering / f, f"steering/{f}")
            else:
                print(f"  ✗ steering/{f} (not found)")

    # ── Agents ──────────────────────────────────────────────────────────
    print(f"\n[specialist personas — {len(AGENTS)}]")
    for f in AGENTS:
        _copy(DATA_ROOT / "agents" / f, kiro / "agents" / f, f"agents/{f}")

    # ── Executable hooks + config ───────────────────────────────────────
    hooks_exec = DATA_ROOT / "hooks-exec"
    print("\n[executable hooks]")
    _copy(hooks_exec / "kirorails.conf", kiro / "kirorails.conf", "kirorails.conf")
    for sh in ["pre-task.sh", "post-task.sh"]:
        dst = kiro / "hooks-exec" / sh
        _copy(hooks_exec / sh, dst, f"hooks-exec/{sh}")
        if dst.exists():
            dst.chmod(0o755)

    # ── Kiro-native hooks (JSON) ────────────────────────────────────────
    hooks_src = DATA_ROOT / "hooks-kiro"
    if hooks_src.is_dir():
        print("\n[kiro hooks]")
        for f in sorted(hooks_src.glob("*.json")):
            _copy(f, kiro / "hooks" / f.name, f"hooks/{f.name}")

    # ── Templates ──────────────────────────────────────────────────────
    specs_src = DATA_ROOT / "templates" / "specs"
    print("\n[templates]")
    _copy(specs_src / "feature" / "tasks.template.md",
          kiro / "specs" / "feature" / "tasks.template.md", "specs/feature/tasks.template.md")
    _copy(specs_src / "feature" / "design.template.md",
          kiro / "specs" / "feature" / "design.template.md", "specs/feature/design.template.md")
    bugfix_tmpl = specs_src / "bugfix" / "bugfix.template.md"
    if bugfix_tmpl.exists():
        _copy(bugfix_tmpl, kiro / "specs" / "bugfix" / "bugfix.template.md",
              "specs/bugfix/bugfix.template.md")

    # ── State directory ─────────────────────────────────────────────────
    state = kiro / "state"
    state.mkdir(parents=True, exist_ok=True)
    print("\n[state files]")
    for sf in ["STATE.md", "CHANGELOG_AI.md", "DECISIONS.md", "RISKS.md"]:
        target = state / sf
        if not target.exists():
            target.write_text(f"# {sf.replace('.md', '').replace('_', ' ')}\n\n<!-- Append-only. Updated by agents during execution. -->\n")
            print(f"  ✓ state/{sf}")
        else:
            print(f"  ~ state/{sf} (exists)")

    # ── Skills directory ────────────────────────────────────────────────
    skills_dir = kiro / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    tmpl_src = DATA_ROOT / "skills" / "_template"
    tmpl_dst = skills_dir / "_template"
    if tmpl_src.is_dir() and not tmpl_dst.exists():
        shutil.copytree(tmpl_src, tmpl_dst)
        print(f"  ✓ skills/_template/SKILL.md")
    elif tmpl_dst.exists():
        print(f"  ~ skills/_template/ (exists)")

    total = sum(1 for _ in kiro.rglob("*") if _.is_file())
    print(f"\n✅ Done. {total} files in {kiro}")
    print('\n🚀 Next steps:')
    print('  kirorails sprint init           # create backlog')
    print('  kirorails sprint new sprint-1   # create first sprint')
    print('  kirorails quick "task desc"     # quick task without planning')
    print('  kirorails doctor                # verify installation')
