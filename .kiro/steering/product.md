---
description: Product context — what this project is, who uses it, business rules
inclusion: always
---

# Product Steering

## Product name
KiroRails

## Description
Professional-grade delivery kit for AI-assisted development with [Kiro](https://kiro.dev). Acts as a "Tech Lead" for the AI agent — enforcing coding standards, verifying quality through automated feedback loops, and organizing complex work into atomic, verified micro-tasks. Designed specifically for brownfield (legacy/existing) projects where the risk of AI breaking existing code is high.

## Key users
- **Developers using Kiro** on complex or legacy codebases who need guardrails to keep AI output production-quality
- **Tech leads** who want to enforce standards and verification on AI-assisted work without manual review of every line
- **Teams in regulated industries** (SOX, HIPAA, PCI-DSS, GDPR) who need audit trails and compliance awareness in AI workflows

## Core constraints
- KiroRails installs only into `.kiro/` — never modifies the target project's source code
- Steering files are templates with sensible defaults — users customize for their stack
- Hooks must work with any build tool (Maven, Gradle, npm, cargo, etc.) via `kirorails.conf`
- CLI must work on Python 3.9+ with minimal dependencies (only Click)
- Backward compatibility: blueprint overlays are additive (`--mode add`), never destructive

## Business rules
- `kirorails init` never overwrites existing files — skips with `(exists)` message
- Lite mode is the default — full mode is opt-in
- Every hook script reads from `kirorails.conf` — no hardcoded build commands
- Sprint/backlog management uses markdown files as the source of truth (no database)
- Quick tasks skip the requirements→design flow, going straight to `tasks.md`
- The Ralph Loop (autonomous execution) is experimental and clearly marked as such

## Out of scope
- KiroRails does NOT write application code — it provides the structure and verification for AI to do so
- KiroRails does NOT replace CI/CD — it complements it with pre-commit quality gates
- KiroRails does NOT manage git branches or PRs — it operates at the task/commit level
