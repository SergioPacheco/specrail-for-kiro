"""SpecRail CLI — Professional-grade delivery for AI-assisted development."""

import click
from pathlib import Path
from datetime import date
from specrail.installer import BLUEPRINTS, install
from specrail.sprint import init_backlog, new_sprint, read_sprint_status, read_backlog


@click.group()
@click.version_option()
def cli():
    """🛤️  SpecRail — The Tech Lead your AI agent needs."""


# ── init ────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--pack", help="Stack blueprint(s), comma-separated")
@click.option("--mode", type=click.Choice(["lite", "full", "add"]), default="lite", help="Install mode")
@click.option("--project", default=".", help="Project root directory")
@click.option("--list", "list_packs", is_flag=True, help="List available stack blueprints")
def init(pack, mode, project, list_packs):
    """Install SpecRail into your project.

    \b
    Examples:
      specrail init                          # interactive
      specrail init --pack java-legacy       # direct
      specrail init --pack spring-boot,postgres --mode full
      specrail init --list
    """
    if list_packs:
        click.echo("\n📦 Available Stack Blueprints:\n")
        for name, info in BLUEPRINTS.items():
            click.echo(f"  {name:20s} {info['desc']}")
        click.echo(f"\n  Modes: lite (default) | full | add\n")
        return

    if not pack:
        click.echo("\n🛤️  SpecRail Setup\n")
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

        mode = click.prompt("Install mode", type=click.Choice(["lite", "full", "add"]), default="lite")

    packs = [p.strip() for p in pack.split(",")]
    install(Path(project).resolve(), packs, mode)


# ── map / plan / verify ────────────────────────────────────────────────────

@cli.command()
def map():
    """Trigger codebase mapping (generates CODEBASE.md)."""
    if not Path(".kiro/agents/codebase-mapper.md").exists():
        click.echo("❌ codebase-mapper not installed. Run: specrail init --mode full")
        raise SystemExit(1)
    click.echo("""
🗺️  Tell Kiro:
  "Map this codebase using the codebase-mapper agent.
   Save the result to .kiro/specs/CODEBASE.md"
""")


@cli.command()
@click.argument("feature", required=False)
def plan(feature):
    """Trigger the planner specialist persona."""
    if not Path(".kiro/agents/planner.md").exists():
        click.echo("❌ Planner not installed. Run: specrail init")
        raise SystemExit(1)
    prompt = f'Plan the feature: "{feature}"' if feature else "Plan the next feature"
    click.echo(f"""
📋 Tell Kiro:
  "{prompt} using the planner agent.
   Follow Ralph principles: small tasks, risk-first, feedback loops."
""")


@cli.command()
def verify():
    """Trigger the Truth Loop (verification)."""
    if not Path(".kiro/agents/verifier.md").exists():
        click.echo("❌ Verifier not installed. Run: specrail init")
        raise SystemExit(1)
    click.echo("""
🔍 Tell Kiro:
  "Verify the current work using the verifier agent.
   Check all done criteria, run feedback loops, produce VERIFICATION.md"
""")


# ── sprint ──────────────────────────────────────────────────────────────────

@cli.group()
def sprint():
    """Sprint and backlog management.

    \b
    Examples:
      specrail sprint init                    # create backlog.md
      specrail sprint new sprint-1-foundation # create sprint dir
      specrail sprint list                    # show all sprints
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
        click.echo("No sprints found. Run: specrail sprint init")
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
      specrail quick "Add CRUD for Product entity"
      specrail quick "Fix date format in reports" --sprint sprint-3
    """
    p = Path(project).resolve()
    kiro = p / ".kiro"

    if not kiro.exists():
        click.echo("⚠️  SpecRail not initialized. Run: specrail init")
        click.echo("   Creating quick task anyway...\n")

    if sprint_name:
        target = kiro / "specs" / sprint_name / "tasks.md"
        if not target.exists():
            click.echo(f"❌ Sprint not found: {sprint_name}. Run: specrail sprint new {sprint_name}")
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
        slug = description.lower().replace(" ", "-")[:40]
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
./mvnw compile
./mvnw test
```
""")
        click.echo(f"✅ Quick task created: .kiro/specs/quick/{slug}.md")


# ── status ──────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--project", default=".", help="Project root directory")
def status(project):
    """Show consolidated progress dashboard."""
    p = Path(project).resolve()
    backlog = read_backlog(p)
    sprints = read_sprint_status(p)

    click.echo("\n🛤️  SpecRail Status Dashboard")
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
    conf = p / ".kiro" / "specrail.conf"
    if conf.exists():
        click.echo(f"🔧 Hooks: configured ({conf})")
    else:
        click.echo(f"🔧 Hooks: not configured (run specrail init --mode full)")

    click.echo("\n═══════════════════════════════════════\n")

    if not backlog and not sprints:
        click.echo("No data yet. Try:")
        click.echo("  specrail sprint init          # create backlog")
        click.echo("  specrail sprint new sprint-1   # create first sprint")
        click.echo("  specrail quick 'task desc'     # quick task without planning\n")


def _progress_bar(done: int, total: int, width: int = 15) -> str:
    if total == 0:
        return "░" * width
    filled = int(width * done / total)
    return "█" * filled + "░" * (width - filled)
