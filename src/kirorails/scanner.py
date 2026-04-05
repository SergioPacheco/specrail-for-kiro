"""KiroRails scanner — auto-detects project stack and fills steering files."""

import json
import re
import subprocess
from pathlib import Path


# ── Stack detection ──────────────────────────────────────────────────────────

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _run(cmd: list[str], cwd: Path) -> str:
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=5)
        return r.stdout.strip()
    except Exception:
        return ""


def detect_stack(project_dir: Path) -> dict:
    """Detect language, frameworks, build tool, test framework, and database."""
    info = {
        "language": None, "runtime_version": None,
        "frameworks": [], "build_tool": None, "build_cmd": None,
        "test_cmd": None, "lint_cmd": None,
        "database": [], "test_framework": None,
        "structure": [], "has_docker": False, "has_ci": False,
    }

    p = project_dir

    # ── Java / JVM ──────────────────────────────────────────────────────────
    if (p / "pom.xml").exists():
        info["language"] = "Java"
        info["build_tool"] = "Maven"
        pom = _read(p / "pom.xml")
        # Detect Java version
        m = re.search(r'<java\.version>(\d+)', pom) or re.search(r'<maven\.compiler\.source>(\d+)', pom)
        if m:
            info["runtime_version"] = f"Java {m.group(1)}"
        # Detect Spring Boot
        if "spring-boot" in pom:
            m = re.search(r'spring-boot[^<]*<version>([^<]+)', pom)
            ver = m.group(1) if m else ""
            info["frameworks"].append(f"Spring Boot {ver}".strip())
        # Detect database
        if "postgresql" in pom.lower() or "postgres" in pom.lower():
            info["database"].append("PostgreSQL")
        if "mysql" in pom.lower():
            info["database"].append("MySQL")
        if "flyway" in pom.lower():
            info["database"].append("Flyway (migrations)")
        if "liquibase" in pom.lower():
            info["database"].append("Liquibase (migrations)")
        # Build commands
        wrapper = "./mvnw" if (p / "mvnw").exists() else "mvn"
        info["build_cmd"] = f"{wrapper} compile -q"
        info["test_cmd"] = f"{wrapper} test -q"
        if "checkstyle" in pom.lower():
            info["lint_cmd"] = f"{wrapper} checkstyle:check -q"
        info["test_framework"] = "JUnit"

    elif (p / "build.gradle").exists() or (p / "build.gradle.kts").exists():
        info["language"] = "Java/Kotlin"
        info["build_tool"] = "Gradle"
        gradle_file = p / "build.gradle.kts" if (p / "build.gradle.kts").exists() else p / "build.gradle"
        gradle = _read(gradle_file)
        if "kotlin" in gradle.lower():
            info["language"] = "Kotlin"
        if "spring-boot" in gradle.lower():
            info["frameworks"].append("Spring Boot")
        wrapper = "./gradlew" if (p / "gradlew").exists() else "gradle"
        info["build_cmd"] = f"{wrapper} compileJava -q"
        info["test_cmd"] = f"{wrapper} test -q"
        info["test_framework"] = "JUnit"

    # ── Python ──────────────────────────────────────────────────────────────
    elif (p / "pyproject.toml").exists() or (p / "setup.py").exists() or (p / "requirements.txt").exists():
        info["language"] = "Python"
        # Detect version
        ver = _run(["python3", "--version"], p)
        if ver:
            info["runtime_version"] = ver
        # Read pyproject.toml
        if (p / "pyproject.toml").exists():
            pyproject = _read(p / "pyproject.toml")
            if "fastapi" in pyproject.lower():
                info["frameworks"].append("FastAPI")
            if "django" in pyproject.lower():
                info["frameworks"].append("Django")
            if "flask" in pyproject.lower():
                info["frameworks"].append("Flask")
            if "sqlalchemy" in pyproject.lower():
                info["database"].append("SQLAlchemy")
            if "alembic" in pyproject.lower():
                info["database"].append("Alembic (migrations)")
            # Build tool
            if "uv" in pyproject.lower() or (p / "uv.lock").exists():
                info["build_tool"] = "uv"
                info["build_cmd"] = "uv run python -c 'import src'"
                info["test_cmd"] = "uv run pytest"
                info["lint_cmd"] = "uv run ruff check src/"
            elif "poetry" in pyproject.lower() or (p / "poetry.lock").exists():
                info["build_tool"] = "Poetry"
                info["test_cmd"] = "poetry run pytest"
                info["lint_cmd"] = "poetry run ruff check src/"
            else:
                info["build_tool"] = "pip"
                info["test_cmd"] = "pytest"
                info["lint_cmd"] = "ruff check src/"
        if "pytest" in _read(p / "requirements.txt") or (p / "pytest.ini").exists() or (p / "pyproject.toml").exists():
            info["test_framework"] = "pytest"

    # ── Node.js / TypeScript ─────────────────────────────────────────────────
    elif (p / "package.json").exists():
        pkg = {}
        try:
            pkg = json.loads(_read(p / "package.json"))
        except Exception:
            pass
        info["language"] = "TypeScript" if (p / "tsconfig.json").exists() else "JavaScript"
        # Runtime version
        engines = pkg.get("engines", {})
        if "node" in engines:
            info["runtime_version"] = f"Node.js {engines['node']}"
        # Frameworks
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        for fw, name in [("next", "Next.js"), ("react", "React"), ("express", "Express"),
                         ("fastify", "Fastify"), ("nestjs/core", "NestJS"), ("vue", "Vue")]:
            if any(fw in k for k in deps):
                info["frameworks"].append(name)
        # Database
        for db, name in [("pg", "PostgreSQL"), ("mysql2", "MySQL"), ("mongoose", "MongoDB"),
                         ("prisma", "Prisma"), ("typeorm", "TypeORM")]:
            if db in deps:
                info["database"].append(name)
        # Build tool
        scripts = pkg.get("scripts", {})
        pm = "pnpm" if (p / "pnpm-lock.yaml").exists() else "yarn" if (p / "yarn.lock").exists() else "npm"
        info["build_tool"] = pm
        info["build_cmd"] = f"{pm} run build" if "build" in scripts else f"{pm} run typecheck"
        info["test_cmd"] = f"{pm} test" if "test" in scripts else f"{pm} run test"
        info["lint_cmd"] = f"{pm} run lint" if "lint" in scripts else None
        # Test framework
        for tf in ["jest", "vitest", "mocha"]:
            if tf in deps:
                info["test_framework"] = tf
                break

    # ── Go ───────────────────────────────────────────────────────────────────
    elif (p / "go.mod").exists():
        info["language"] = "Go"
        info["build_tool"] = "go"
        gomod = _read(p / "go.mod")
        m = re.search(r'^go (\d+\.\d+)', gomod, re.MULTILINE)
        if m:
            info["runtime_version"] = f"Go {m.group(1)}"
        info["build_cmd"] = "go build ./..."
        info["test_cmd"] = "go test ./..."
        info["lint_cmd"] = "golangci-lint run"
        info["test_framework"] = "testing (stdlib)"

    # ── Rust ─────────────────────────────────────────────────────────────────
    elif (p / "Cargo.toml").exists():
        info["language"] = "Rust"
        info["build_tool"] = "cargo"
        info["build_cmd"] = "cargo build"
        info["test_cmd"] = "cargo test"
        info["lint_cmd"] = "cargo clippy"
        info["test_framework"] = "cargo test"

    # ── Infrastructure ───────────────────────────────────────────────────────
    info["has_docker"] = (p / "Dockerfile").exists() or (p / "docker-compose.yml").exists()
    info["has_ci"] = (p / ".github" / "workflows").exists() or (p / ".gitlab-ci.yml").exists()

    # ── Directory structure ──────────────────────────────────────────────────
    for d in sorted(p.iterdir()):
        if d.is_dir() and not d.name.startswith(".") and d.name not in {"node_modules", "target", "dist", "build", "__pycache__", ".git"}:
            info["structure"].append(d.name)

    return info


# ── Steering file writers ────────────────────────────────────────────────────

def _fill_tech_md(path: Path, info: dict) -> bool:
    """Fill tech.md with detected stack info. Returns True if changed."""
    content = path.read_text()

    # Only fill if still has placeholder comments
    if "<!-- e.g.," not in content and "<!-- " not in content:
        return False  # Already customized

    lang = info["language"] or "Unknown"
    ver = info.get("runtime_version") or ""
    frameworks = ", ".join(info["frameworks"]) if info["frameworks"] else "None detected"
    database = ", ".join(info["database"]) if info["database"] else "None detected"
    build = info["build_tool"] or "Unknown"

    new_content = f"""---
description: Tech stack — language, frameworks, database, build, deployment
inclusion: always
---

# Tech Steering

## Language and runtime
- {lang}{f" ({ver})" if ver else ""}

## Frameworks
- {frameworks}

## Database
- {database if database != "None detected" else "None detected — add if applicable"}
- Migrations managed by a versioned tool (Flyway, Alembic, Prisma)
- All DDL changes go through migration scripts, never manual ALTER in production

## Build and packaging
- {build}
- Pin all dependency versions explicitly
- CI builds must be reproducible

## Deployment
{"- Docker: yes" if info["has_docker"] else "- Docker: not detected"}
{"- CI/CD: configured" if info["has_ci"] else "- CI/CD: not detected — consider adding"}
- Rollback strategy documented for every release

## Monitoring
- Structured logging with correlation IDs
- Health check endpoint
- Alerting on error rate spikes and latency degradation
"""
    path.write_text(new_content)
    return True


def _fill_structure_md(path: Path, info: dict) -> bool:
    """Fill structure.md with detected directory layout."""
    content = path.read_text()
    if "<!-- Document your project" not in content:
        return False

    dirs = info.get("structure", [])
    layout = "\n".join(f"  {d}/" for d in dirs[:15]) if dirs else "  (run from project root)"

    new_content = content.replace(
        "## Project layout\n<!-- Document your project's directory structure here -->",
        f"## Project layout\n```\n{layout}\n```\n<!-- Add descriptions for each directory -->"
    )
    if new_content != content:
        path.write_text(new_content)
        return True
    return False


def _fill_kirorails_conf(path: Path, info: dict) -> bool:
    """Fill kirorails.conf with detected build commands."""
    content = path.read_text()

    # Only fill empty commands
    lines = content.splitlines()
    new_lines = []
    changed = False
    for line in lines:
        if line.startswith("compile=") and not line.split("=", 1)[1].strip() and info.get("build_cmd"):
            new_lines.append(f"compile={info['build_cmd']}")
            changed = True
        elif line.startswith("test=") and not line.split("=", 1)[1].strip() and info.get("test_cmd"):
            new_lines.append(f"test={info['test_cmd']}")
            changed = True
        elif line.startswith("lint=") and not line.split("=", 1)[1].strip() and info.get("lint_cmd"):
            new_lines.append(f"lint={info['lint_cmd']}")
            changed = True
        else:
            new_lines.append(line)

    if changed:
        path.write_text("\n".join(new_lines) + "\n")
    return changed


def scan_and_fill(project_dir: Path) -> dict:
    """Scan project and fill steering files. Returns scan results."""
    info = detect_stack(project_dir)
    kiro = project_dir / ".kiro"
    filled = []

    if not kiro.exists():
        return {"info": info, "filled": [], "error": ".kiro/ not found — run kirorails init first"}

    tech_md = kiro / "steering" / "tech.md"
    if tech_md.exists() and _fill_tech_md(tech_md, info):
        filled.append("steering/tech.md")

    structure_md = kiro / "steering" / "structure.md"
    if structure_md.exists() and _fill_structure_md(structure_md, info):
        filled.append("steering/structure.md")

    conf = kiro / "kirorails.conf"
    if conf.exists() and _fill_kirorails_conf(conf, info):
        filled.append("kirorails.conf")

    return {"info": info, "filled": filled}
