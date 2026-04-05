---
description: Tech stack — language, frameworks, database, build, deployment
inclusion: always
---

# Tech Steering

## Language and runtime
- Python 3.9+
- No type stubs required — standard library typing only

## Frameworks
- Click ≥ 8.0 (CLI framework — only runtime dependency)
- No web framework — this is a CLI tool

## Database
- None — all state is stored in markdown files (`.kiro/specs/`)
- No migrations, no ORM, no database driver

## Build and packaging
- Hatchling (PEP 517 build backend)
- `pyproject.toml` as single source of config (no setup.py, no setup.cfg)
- Published to PyPI as `kirorails`
- Entry point: `kirorails = "kirorails.cli:cli"`

## Project structure
```
src/kirorails/
├── __init__.py       version
├── __main__.py       python -m kirorails support
├── cli.py            Click commands (init, sprint, quick, status, map, plan, verify)
├── installer.py      copies data/ templates into target .kiro/
├── sprint.py         backlog and sprint management (markdown-based)
└── data/             all templates, agents, steering, hooks, blueprints
```

## Deployment
- `pip install kirorails` — single command install
- No CI/CD for the tool itself yet — manual PyPI publish
- Works on Linux, macOS, Windows (bash hooks require Git Bash on Windows)

## Monitoring
- N/A — CLI tool, no long-running process
