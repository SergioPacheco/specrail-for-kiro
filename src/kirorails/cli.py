"""KiroRails CLI — Professional-grade delivery for AI-assisted development."""

import unicodedata
import re
import click
from pathlib import Path
from datetime import date
from kirorails.installer import BLUEPRINTS, install
from kirorails.sprint import init_backlog, new_sprint, read_sprint_status, read_backlog
from kirorails.phantom import check_phantom_tasks
from kirorails.scanner import scan_and_fill


@click.group()
@click.version_option()
def cli():
    """🛤️  KiroRails — The Tech Lead your AI agent needs."""


# ── init ────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--pack", help="Stack blueprint(s), comma-separated")
@click.option("--project", default=".", help="Project root directory")
@click.option("--list", "list_packs", is_flag=True, help="List available stack blueprints")
def init(pack, project, list_packs):
    """Install KiroRails into your project.

    \b
    Examples:
      kirorails init                          # interactive
      kirorails init --pack java-legacy       # direct
      kirorails init --pack spring-boot,postgres
      kirorails init --list
    """
    if list_packs:
        click.echo("\n📦 Available Stack Blueprints:\n")
        for name, info in BLUEPRINTS.items():
            click.echo(f"  {name:20s} {info['desc']}")
        click.echo()
        return

    if not pack:
        click.echo("\n🛤️  KiroRails Setup\n")
        click.echo("Available stack blueprints:")
        names = list(BLUEPRINTS.keys())
        for i, (name, info) in enumerate(BLUEPRINTS.items(), 1):
            click.echo(f"  {i}. {name:20s} {info['desc']}")

        click.echo()
        choice = click.prompt("Which blueprint(s)? (number, name, or comma-separated)", type=str)

        selected = []
        for part in choice.split(","):
            part = part.strip()
            if part.isdigit() and 1 <= int(part) <= len(names):
                selected.append(names[int(part) - 1])
            elif part in BLUEPRINTS:
                selected.append(part)
            else:
                click.echo(f"❌ Unknown: {part}")
                raise SystemExit(1)
        pack = ",".join(selected)

    packs = [p.strip() for p in pack.split(",")]
    install(Path(project).resolve(), packs)


# ── scan ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--project", default=".", help="Project root directory")
@click.option("--dry-run", is_flag=True, help="Show what would be filled without writing")
def scan(project, dry_run):
    """Auto-detect stack and fill steering files.

    \b
    Detects language, frameworks, build tool, database, and test framework.
    Fills tech.md, structure.md, and kirorails.conf with real values.
    Only fills fields that still have placeholder comments.

    \b
    Examples:
      kirorails scan                 # detect and fill
      kirorails scan --dry-run       # preview without writing
    """
    p = Path(project).resolve()
    click.echo("\n🔍 KiroRails Scan\n")

    result = scan_and_fill(p) if not dry_run else {"info": __import__("kirorails.scanner", fromlist=["detect_stack"]).detect_stack(p), "filled": []}

    info = result["info"]
    if "error" in result:
        click.echo(f"❌ {result['error']}")
        raise SystemExit(1)

    # Show detected stack
    lang = info.get("language") or "Unknown"
    ver = info.get("runtime_version") or ""
    click.echo(f"  Language:    {lang}{f' ({ver})' if ver else ''}")
    if info.get("frameworks"):
        click.echo(f"  Frameworks:  {', '.join(info['frameworks'])}")
    if info.get("database"):
        click.echo(f"  Database:    {', '.join(info['database'])}")
    if info.get("build_tool"):
        click.echo(f"  Build:       {info['build_tool']}")
    if info.get("test_framework"):
        click.echo(f"  Tests:       {info['test_framework']}")
    click.echo(f"  Docker:      {'yes' if info.get('has_docker') else 'no'}")
    click.echo(f"  CI/CD:       {'yes' if info.get('has_ci') else 'no'}")

    if dry_run:
        click.echo("\n  (dry-run — no files written)")
    elif result.get("filled"):
        click.echo(f"\n  ✅ Filled: {', '.join(result['filled'])}")
    else:
        click.echo("\n  ✅ Steering files already customized — nothing to fill.")

    click.echo()



# ── check-phantom ─────────────────────────────────────────────────────────

@cli.command("check-phantom")
@click.argument("spec", required=False)
@click.option("--commits", default=20, help="Number of recent commits to check against")
@click.option("--project", default=".", help="Project root directory")
def check_phantom(spec, commits, project):
    """Detect phantom completions — tasks marked done with no real code changes.

    \b
    Compares tasks marked [x] in tasks.md against actual git changes.

    Verdicts:
      ✅ Real      — files changed, tests present
      ⚠️  Suspicious — files changed but no tests, or no files listed
      👻 Phantom   — marked done but no matching code changes found

    Examples:
      kirorails check-phantom                    # check all specs
      kirorails check-phantom user-auth          # check specific spec
      kirorails check-phantom --commits 50       # look back 50 commits
    """
    p = Path(project).resolve()
    results = check_phantom_tasks(p, spec_name=spec, since_commits=commits)

    if not results:
        click.echo("\n✅ No completed tasks found to check.\n")
        return

    phantoms = [r for r in results if r["verdict"] == "👻"]
    suspicious = [r for r in results if r["verdict"] == "⚠️"]
    real = [r for r in results if r["verdict"] == "✅"]

    click.echo(f"\n👻 KiroRails Phantom Detection\n{'─' * 40}")

    current_spec = None
    for r in results:
        if r["spec"] != current_spec:
            current_spec = r["spec"]
            click.echo(f"\n📋 {current_spec}")
        click.echo(f"  {r['verdict']}  {r['task'][:50]}")
        if r["verdict"] != "✅":
            click.echo(f"      → {r['reason']}")

    click.echo(f"\n{'─' * 40}")
    click.echo(f"  ✅ {len(real)} real  ⚠️  {len(suspicious)} suspicious  👻 {len(phantoms)} phantom")

    if phantoms:
        click.echo(f"\n  ❌ {len(phantoms)} phantom task(s) detected — these need investigation.")
        raise SystemExit(1)
    elif suspicious:
        click.echo(f"\n  ⚠️  {len(suspicious)} suspicious task(s) — review before committing.")
    else:
        click.echo(f"\n  🎉 All completed tasks have real implementations.")
    click.echo()


# ── verify / clarify / analyze ────────────────────────────────────────────

@cli.command()
@click.option("--project", default=".", help="Project root directory")
def verify(project):
    """Trigger the Truth Loop (verification)."""
    kiro = Path(project).resolve() / ".kiro"
    if not (kiro / "agents" / "verifier.md").exists():
        click.echo("❌ Verifier not installed. Run: kirorails init")
        raise SystemExit(1)
    click.echo("""
🔍 Tell Kiro:
  "Verify the current work using the verifier agent.
   Check all done criteria, run feedback loops, produce VERIFICATION.md"
""")


@cli.command()
@click.argument("feature", required=False)
@click.option("--project", default=".", help="Project root directory")
def clarify(feature, project):
    """Clarify a feature before planning — eliminate ambiguity.

    \b
    Run BEFORE kirorails plan. Produces CLARIFICATIONS.md.

    Examples:
      kirorails clarify "user authentication"
      kirorails clarify
    """
    kiro = Path(project).resolve() / ".kiro"
    if not (kiro / "agents" / "clarifier.md").exists():
        click.echo("❌ Clarifier not installed. Run: kirorails init")
        raise SystemExit(1)
    target = f'the feature: "{feature}"' if feature else "the current feature or requirement"
    click.echo(f"""
❓ Tell Kiro:
  "Clarify {target} using the clarifier agent.
   Ask structured questions, record decisions in CLARIFICATIONS.md.
   Use default assumptions when I say 'use your judgment'."
""")


@cli.command()
@click.argument("feature", required=False)
@click.option("--project", default=".", help="Project root directory")
def analyze(feature, project):
    """Analyze specs and tasks for consistency before implementation.

    \b
    Run AFTER kirorails plan, BEFORE implementation. Produces ANALYSIS.md.

    Examples:
      kirorails analyze "user-auth"
      kirorails analyze
    """
    kiro = Path(project).resolve() / ".kiro"
    if not (kiro / "agents" / "analyzer.md").exists():
        click.echo("❌ Analyzer not installed. Run: kirorails init")
        raise SystemExit(1)
    target = f'the feature: "{feature}"' if feature else "the current sprint or feature"
    click.echo(f"""
🔬 Tell Kiro:
  "Analyze {target} using the analyzer agent.
   Check requirement coverage, task consistency, feasibility.
   Produce ANALYSIS.md with verdict: READY / READY WITH WARNINGS / NOT READY."
""")


# ── sprint ──────────────────────────────────────────────────────────────────

@cli.group()
def sprint():
    """Sprint and backlog management.

    \b
    Examples:
      kirorails sprint init                    # create backlog.md
      kirorails sprint new sprint-1-foundation # create sprint dir
      kirorails sprint list                    # show all sprints
    """


@sprint.command("init")
@click.option("--project", default=".", help="Project root directory")
def sprint_init(project):
    """Create backlog.md for requirement tracking."""
    p = Path(project).resolve()
    click.echo("\n📋 Initializing backlog\n")
    init_backlog(p)
    click.echo("\n✅ Edit .kiro/specs/backlog.md to add your requirements.")


@sprint.command("new")
@click.argument("name")
@click.option("--project", default=".", help="Project root directory")
def sprint_new(name, project):
    """Create a new sprint directory with tasks.md."""
    p = Path(project).resolve()
    click.echo(f"\n🏃 Creating sprint: {name}\n")
    new_sprint(name, p)
    click.echo(f"\n✅ Edit .kiro/specs/{name}/tasks.md to add tasks.")


@sprint.command("list")
@click.option("--project", default=".", help="Project root directory")
def sprint_list(project):
    """Show all sprints and their progress."""
    sprints = read_sprint_status(Path(project).resolve())
    if not sprints:
        click.echo("No sprints found. Run: kirorails sprint init")
        return

    click.echo("\n🏃 Sprints\n")
    for s in sprints:
        total = s["total"]
        done = s["done"]
        bar = _progress_bar(done, total)
        status = "✅" if done == total and total > 0 else "🔄" if done > 0 else "🔲"
        click.echo(f"  {status} {s['name']:30s} {bar} {done}/{total}")
        if s["blocked"] > 0:
            click.echo(f"     ❌ {s['blocked']} blocked")
    click.echo()


# ── quick ───────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("description")
@click.option("--sprint", "sprint_name", default=None, help="Add to existing sprint instead of creating quick/ dir")
@click.option("--project", default=".", help="Project root directory")
def quick(description, sprint_name, project):
    """Create a quick task — skip requirements and design.

    \b
    Examples:
      kirorails quick "Add CRUD for Product entity"
      kirorails quick "Fix date format in reports" --sprint sprint-3
    """
    p = Path(project).resolve()
    kiro = p / ".kiro"

    if not kiro.exists():
        click.echo("⚠️  KiroRails not initialized. Run: kirorails init")
        click.echo("   Creating quick task anyway...\n")

    if sprint_name:
        target = kiro / "specs" / sprint_name / "tasks.md"
        if not target.exists():
            click.echo(f"❌ Sprint not found: {sprint_name}. Run: kirorails sprint new {sprint_name}")
            raise SystemExit(1)
        # Append task to existing sprint
        content = target.read_text()
        task_num = content.count("### [") + 1
        target.write_text(content + f"""
### [ ] Task {task_num}: {description}
- **Files:** <!-- files to change -->
- **Done:** <!-- one testable criterion -->
- **Commit:** `<!-- type(scope): description -->`
""")
        click.echo(f"✅ Task {task_num} added to {sprint_name}/tasks.md")
    else:
        # Create standalone quick task
        quick_dir = kiro / "specs" / "quick"
        quick_dir.mkdir(parents=True, exist_ok=True)
        slug = _slugify(description)
        tasks_file = quick_dir / f"{slug}.md"
        tasks_file.write_text(f"""# ⚡ Quick Task

> {description}
> Created: {date.today()}

## Tasks

### [ ] Task 1: {description}
- **Files:** <!-- files to change -->
- **Done:** <!-- one testable criterion -->
- **Commit:** `<!-- type(scope): description -->`

## Feedback Loops

```bash
# Run after task — do NOT commit if any fail
# Commands configured in .kiro/kirorails.conf
.kiro/hooks-exec/post-task.sh
```
""")
        click.echo(f"✅ Quick task created: .kiro/specs/quick/{slug}.md")


# ── doctor ───────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--project", default=".", help="Project root directory")
def doctor(project):
    """Validate KiroRails installation health."""
    p = Path(project).resolve()
    kiro = p / ".kiro"
    ok = 0
    warn = 0
    fail = 0

    click.echo("\n🩺 KiroRails Doctor\n")

    def check(label, passed, is_warn=False):
        nonlocal ok, warn, fail
        if passed:
            click.echo(f"  ✅ {label}")
            ok += 1
        elif is_warn:
            click.echo(f"  ⚠️  {label}")
            warn += 1
        else:
            click.echo(f"  ❌ {label}")
            fail += 1

    # Core structure
    check(".kiro/ directory exists", kiro.is_dir())
    check("kirorails.conf exists", (kiro / "kirorails.conf").is_file())

    # Conf validity
    conf = kiro / "kirorails.conf"
    if conf.is_file():
        lines = [l for l in conf.read_text().splitlines() if "=" in l and not l.strip().startswith("#")]
        has_compile = any(l.startswith("compile=") and l.split("=", 1)[1].strip() for l in lines)
        has_test = any(l.startswith("test=") and l.split("=", 1)[1].strip() for l in lines)
        check("kirorails.conf has compile command", has_compile, is_warn=True)
        check("kirorails.conf has test command", has_test, is_warn=True)

    # Agents
    agents_dir = kiro / "agents"
    for agent in ["verifier.md", "clarifier.md", "analyzer.md", "learner.md"]:
        check(f"agents/{agent}", (agents_dir / agent).is_file())

    # Hooks
    for hook in ["pre-task.sh", "post-task.sh"]:
        hp = kiro / "hooks-exec" / hook
        exists = hp.is_file()
        check(f"hooks-exec/{hook} exists", exists)
        if exists:
            import os
            check(f"hooks-exec/{hook} is executable", os.access(hp, os.X_OK), is_warn=True)

    # State
    state = kiro / "state"
    check("state/ directory exists", state.is_dir())
    if state.is_dir():
        for sf in ["STATE.md", "CHANGELOG_AI.md", "DECISIONS.md", "RISKS.md"]:
            check(f"state/{sf}", (state / sf).is_file(), is_warn=True)

    # Steering
    steering = kiro / "steering"
    for sf in ["product.md", "tech.md", "coding-standards.md"]:
        check(f"steering/{sf}", (steering / sf).is_file())

    click.echo(f"\n{'─' * 40}")
    click.echo(f"  ✅ {ok} passed  ⚠️  {warn} warnings  ❌ {fail} failed")
    if fail == 0 and warn == 0:
        click.echo("  🎉 Installation is healthy!")
    elif fail == 0:
        click.echo("  👍 Installation works, but has warnings.")
    else:
        click.echo("  🔧 Fix the failures above, then run doctor again.")
    click.echo()


# ── skill ───────────────────────────────────────────────────────────────────

@cli.group()
def skill():
    """Manage custom skills — reusable patterns with auto-injection.

    \b
    Examples:
      kirorails skill list                # list all skills
      kirorails skill add "fix-auth"      # create new skill
      kirorails skill search "migration"  # find matching skills
    """


@skill.command("list")
@click.option("--project", default=".", help="Project root directory")
def skill_list(project):
    """List all skills (project + user)."""
    p = Path(project).resolve()
    project_skills = p / ".kiro" / "skills"
    user_skills = Path.home() / ".kiro" / "skills"

    found = False
    for label, path in [("Project", project_skills), ("User", user_skills)]:
        if not path.is_dir():
            continue
        dirs = sorted([d for d in path.iterdir() if d.is_dir() and (d / "SKILL.md").exists() and d.name != "_template"])
        if not dirs:
            continue
        found = True
        click.echo(f"\n📦 {label} skills ({path}):\n")
        for d in dirs:
            meta = _parse_skill_meta(d / "SKILL.md")
            desc = meta.get("description", "")[:60]
            click.echo(f"  {meta.get('name', d.name):30s} {desc}")

    if not found:
        click.echo("\nNo skills found. Create one with: kirorails skill add \"name\"")
    click.echo()


@skill.command("add")
@click.argument("name")
@click.option("--user", is_flag=True, help="Create in ~/.kiro/skills/ instead of project")
@click.option("--project", default=".", help="Project root directory")
def skill_add(name, user, project):
    """Create a new skill from template (Agent Skills format)."""
    if user:
        base = Path.home() / ".kiro" / "skills"
    else:
        base = Path(project).resolve() / ".kiro" / "skills"

    slug = _slugify(name)
    target = base / slug
    if target.exists():
        click.echo(f"❌ Skill already exists: {target}")
        raise SystemExit(1)

    target.mkdir(parents=True, exist_ok=True)
    (target / "SKILL.md").write_text(f"""---
name: {slug}
description: <!-- Describe when Kiro should activate this skill. Be specific with keywords. -->
---

## Context

<!-- When does this pattern apply? -->

## Pattern

<!-- The actual pattern, fix, or convention -->
""")
    click.echo(f"✅ Skill created: {target}/SKILL.md")
    click.echo(f"   Edit SKILL.md to add your pattern and description.")


@skill.command("search")
@click.argument("keyword")
@click.option("--project", default=".", help="Project root directory")
def skill_search(keyword, project):
    """Search skills by keyword (checks description and content)."""
    p = Path(project).resolve()
    keyword_lower = keyword.lower()
    matches = []

    for path in [p / ".kiro" / "skills", Path.home() / ".kiro" / "skills"]:
        if not path.is_dir():
            continue
        for d in sorted(path.iterdir()):
            skill_file = d / "SKILL.md"
            if not d.is_dir() or not skill_file.exists() or d.name == "_template":
                continue
            content = skill_file.read_text().lower()
            if keyword_lower in content:
                meta = _parse_skill_meta(skill_file)
                matches.append((d, meta))

    if matches:
        click.echo(f"\n🔍 Skills matching \"{keyword}\":\n")
        for d, meta in matches:
            desc = meta.get("description", "")[:60]
            click.echo(f"  {meta.get('name', d.name):30s} {desc}")
            click.echo(f"    {d}")
    else:
        click.echo(f"\nNo skills match \"{keyword}\".")
    click.echo()


def _parse_skill_meta(path: Path) -> dict:
    """Parse YAML-like frontmatter from a SKILL.md file."""
    content = path.read_text()
    if not content.startswith("---"):
        return {"name": path.parent.name}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {"name": path.parent.name}
    meta = {"name": path.parent.name}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"\'')
    return meta


# ── learn ───────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("feature", required=False)
@click.option("--project", default=".", help="Project root directory")
def learn(feature, project):
    """Extract reusable patterns from completed specs into skills.

    \b
    Analyzes specs with VERIFICATION PASS and extracts patterns.

    Examples:
      kirorails learn                    # learn from all completed specs
      kirorails learn "user-auth"        # learn from specific spec
    """
    kiro = Path(project).resolve() / ".kiro"
    if not (kiro / "agents" / "learner.md").exists():
        click.echo("❌ Learner not installed. Run: kirorails init")
        raise SystemExit(1)
    target = f'the spec: "{feature}"' if feature else "all completed specs with VERIFICATION PASS"
    click.echo(f"""
🧠 Tell Kiro:
  "Analyze {target} using the learner agent.
   Extract reusable patterns into .kiro/skills/.
   Only create skills from verified, successful implementations."
""")


# ── status ──────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--project", default=".", help="Project root directory")
def status(project):
    """Show consolidated progress dashboard."""
    p = Path(project).resolve()
    backlog = read_backlog(p)
    sprints = read_sprint_status(p)

    click.echo("\n🛤️  KiroRails Status Dashboard")
    click.echo("═══════════════════════════════════════\n")

    # Backlog summary
    if backlog:
        total = sum(backlog.values())
        click.echo(f"📋 Backlog: {total} requirements")
        click.echo(f"   ✅ {backlog.get('done', 0)} done  "
                    f"🔄 {backlog.get('in_progress', 0)} in progress  "
                    f"🔲 {backlog.get('todo', 0)} todo  "
                    f"❌ {backlog.get('blocked', 0)} blocked")
        click.echo()

    # Sprint progress
    if sprints:
        total_tasks = sum(s["total"] for s in sprints)
        done_tasks = sum(s["done"] for s in sprints)
        click.echo(f"🏃 Sprints: {len(sprints)} total, {done_tasks}/{total_tasks} tasks done")
        click.echo()
        for s in sprints:
            bar = _progress_bar(s["done"], s["total"])
            status_icon = "✅" if s["done"] == s["total"] and s["total"] > 0 else "🔄" if s["done"] > 0 else "🔲"
            click.echo(f"   {status_icon} {s['name']:30s} {bar} {s['done']}/{s['total']}")
        click.echo()

    # Hooks config
    conf = p / ".kiro" / "kirorails.conf"
    if conf.exists():
        click.echo(f"🔧 Hooks: configured ({conf})")
    else:
        click.echo("🔧 Hooks: not configured (run kirorails init)")

    click.echo("\n═══════════════════════════════════════\n")

    if not backlog and not sprints:
        click.echo("No data yet. Try:")
        click.echo("  kirorails sprint init          # create backlog")
        click.echo("  kirorails sprint new sprint-1   # create first sprint")
        click.echo("  kirorails quick 'task desc'     # quick task without planning\n")


def _progress_bar(done: int, total: int, width: int = 15) -> str:
    if total == 0:
        return "░" * width
    filled = int(width * done / total)
    return "█" * filled + "░" * (width - filled)


def _slugify(text: str) -> str:
    """Convert text to a clean filename slug."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text[:50]
