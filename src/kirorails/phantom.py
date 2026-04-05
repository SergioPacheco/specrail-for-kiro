"""Phantom completion detection — finds tasks marked done with no real implementation."""

import re
import subprocess
from pathlib import Path


def _git_changed_files(project_dir: Path, since_commits: int = 20) -> set[str]:
    """Get files changed in recent commits."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"HEAD~{since_commits}", "HEAD"],
            cwd=project_dir, capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            # Fewer commits than requested — get all changed files
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR"],
                cwd=project_dir, capture_output=True, text=True, timeout=10
            )
        files = {f.strip() for f in result.stdout.splitlines() if f.strip()}
        # Also include uncommitted changes
        staged = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            cwd=project_dir, capture_output=True, text=True, timeout=10
        )
        files |= {f.strip() for f in staged.stdout.splitlines() if f.strip()}
        return files
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return set()


def _parse_done_tasks(tasks_file: Path) -> list[dict]:
    """Parse tasks.md and return tasks marked as done with their metadata."""
    content = tasks_file.read_text()
    tasks = []

    # Match ### [x] Task N: Title blocks
    pattern = re.compile(
        r'### \[(?:x|X)\] (.+?)\n(.*?)(?=### \[|$)',
        re.DOTALL
    )
    for match in pattern.finditer(content):
        title = match.group(1).strip()
        body = match.group(2)

        # Extract files listed in the task
        files_match = re.search(r'\*\*Files:\*\*\s*(.+?)(?:\n|$)', body)
        files_raw = files_match.group(1).strip() if files_match else ""

        # Parse file list — could be comma-separated, space-separated, or a comment
        listed_files = []
        if files_raw and "<!--" not in files_raw:
            # Split by comma or space, clean up
            for f in re.split(r'[,\s]+', files_raw):
                f = f.strip().strip('`')
                if f and not f.startswith('#'):
                    listed_files.append(f)

        tasks.append({
            "title": title,
            "listed_files": listed_files,
            "has_files_field": bool(files_raw and "<!--" not in files_raw),
        })

    return tasks


def _verdict(task: dict, changed_files: set[str]) -> tuple[str, str]:
    """Return (verdict_emoji, reason) for a task."""
    listed = task["listed_files"]

    if not task["has_files_field"] or not listed:
        return "⚠️", "No files listed — cannot verify"

    # Check if any listed file appears in changed files (basename match)
    changed_basenames = {Path(f).name for f in changed_files}
    changed_paths = changed_files

    matched = []
    for lf in listed:
        lf_base = Path(lf).name
        if lf in changed_paths or lf_base in changed_basenames:
            matched.append(lf)

    if not matched:
        return "👻", f"No matching changes found for: {', '.join(listed)}"

    # Check for test files
    has_test = any(
        "test" in f.lower() or "spec" in f.lower()
        for f in changed_files
    )
    if not has_test:
        return "⚠️", f"Files changed ({', '.join(matched)}) but no test changes found"

    return "✅", f"Files changed: {', '.join(matched)}"


def check_phantom_tasks(project_dir: Path, spec_name: str | None = None,
                        since_commits: int = 20) -> list[dict]:
    """
    Check for phantom completions in tasks.md files.
    Returns list of results with verdict per task.
    """
    kiro = project_dir / ".kiro" / "specs"
    if not kiro.exists():
        return []

    changed_files = _git_changed_files(project_dir, since_commits)

    results = []
    if spec_name:
        candidates = [kiro / spec_name / "tasks.md"]
    else:
        candidates = sorted(kiro.rglob("tasks.md"))

    for tasks_file in candidates:
        if not tasks_file.exists():
            continue
        spec = tasks_file.parent.name
        done_tasks = _parse_done_tasks(tasks_file)
        if not done_tasks:
            continue

        spec_results = []
        for task in done_tasks:
            emoji, reason = _verdict(task, changed_files)
            spec_results.append({
                "spec": spec,
                "task": task["title"],
                "verdict": emoji,
                "reason": reason,
            })
        results.extend(spec_results)

    return results
