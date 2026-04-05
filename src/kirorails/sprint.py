"""Sprint and backlog management for KiroRails."""

from pathlib import Path
from datetime import date


def _kiro(project: Path = None) -> Path:
    return (project or Path(".")) / ".kiro"


def init_backlog(project: Path = None):
    """Create backlog.md and first sprint structure."""
    kiro = _kiro(project)
    specs = kiro / "specs"
    specs.mkdir(parents=True, exist_ok=True)

    backlog = specs / "backlog.md"
    if backlog.exists():
        print(f"  ~ backlog.md (exists)")
        return backlog

    backlog.write_text(f"""# 📋 Product Backlog

> Last updated: {date.today()}

## Requirements

<!-- Add requirements here. Format:
| ID | Requirement | Sprint | Status |
-->

| ID | Requirement | Sprint | Status |
|----|-------------|--------|--------|
| R01 | <!-- description --> | — | 🔲 Todo |

## Status Key

- 🔲 Todo — not started
- 🔄 In Progress — assigned to a sprint
- ✅ Done — implemented and verified
- ❌ Blocked — has blockers
- ⏭️ Deferred — moved to later sprint

## Notes

<!-- High-level notes, priorities, dependencies between requirements -->
""")
    print(f"  ✓ specs/backlog.md")
    return backlog


def new_sprint(name: str, project: Path = None):
    """Create a new sprint directory with tasks.md."""
    kiro = _kiro(project)
    sprint_dir = kiro / "specs" / name
    sprint_dir.mkdir(parents=True, exist_ok=True)

    tasks = sprint_dir / "tasks.md"
    if tasks.exists():
        print(f"  ~ {name}/tasks.md (exists)")
        return sprint_dir

    tasks.write_text(f"""# 🏃 {name}

> Created: {date.today()}

## Sprint Goal

<!-- One sentence: what this sprint delivers -->

## Progress

| Metric | Value |
|--------|-------|
| Tasks | 0/0 |
| Status | 🔲 Not started |

## Tasks

<!-- Status: [ ] todo, [x] done, [!] blocked -->

### [ ] Task 1: <!-- title -->
- **Files:** <!-- files to change -->
- **Done:** <!-- one testable criterion -->
- **Commit:** `<!-- type(scope): description -->`

## Feedback Loops

```bash
# Run after every task — do NOT commit if any fail
# Commands configured in .kiro/kirorails.conf
.kiro/hooks-exec/post-task.sh
```

## Retrospective

<!-- Fill after sprint completion -->
""")
    print(f"  ✓ {name}/tasks.md")
    return sprint_dir


def read_sprint_status(project: Path = None) -> list[dict]:
    """Read all sprint directories and return status info."""
    kiro = _kiro(project)
    specs = kiro / "specs"
    if not specs.exists():
        return []

    skip = {"feature", "quick", "archive"}
    sprints = []
    for d in sorted(specs.iterdir()):
        if not d.is_dir() or d.name in skip:
            continue
        tasks_file = d / "tasks.md"
        if not tasks_file.exists():
            continue

        content = tasks_file.read_text()
        # Count tasks by looking for ### [ ] and ### [x] patterns
        total = content.count("### [")
        done = content.count("### [x]") + content.count("### [X]")
        blocked = content.count("### [!]")

        sprints.append({
            "name": d.name,
            "total": total,
            "done": done,
            "blocked": blocked,
            "pending": total - done - blocked,
        })
    return sprints


def read_backlog(project: Path = None) -> dict:
    """Read backlog.md and return counts by status from the table only."""
    kiro = _kiro(project)
    backlog = kiro / "specs" / "backlog.md"
    if not backlog.exists():
        return {}

    content = backlog.read_text()
    # Only count emojis in table rows (lines starting with |)
    table_lines = [l for l in content.splitlines() if l.startswith("|") and "---" not in l]
    table_text = "\n".join(table_lines)
    return {
        "todo": table_text.count("🔲"),
        "in_progress": table_text.count("🔄"),
        "done": table_text.count("✅"),
        "blocked": table_text.count("❌"),
        "deferred": table_text.count("⏭️"),
    }
