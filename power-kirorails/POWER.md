---
name: "kirorails"
displayName: "KiroRails — Delivery Kit for Brownfield Projects"
description: "Professional-grade delivery kit that enforces coding standards, verifies quality through automated feedback loops, and organizes complex work into atomic, verified micro-tasks. Designed for brownfield/legacy projects."
keywords: ["delivery", "guardrails", "verification", "brownfield", "legacy", "sprint", "backlog", "planning", "truth loop", "feedback loops", "quality", "standards", "refactoring", "migration"]
---

# KiroRails Power

The Tech Lead your AI agent needs. KiroRails turns AI-assisted coding into a repeatable, verified process.

# Onboarding

## Step 1: Install KiroRails CLI

Verify KiroRails is installed:

```bash
pip install kirorails
kirorails --version
```

If not installed, install it first. KiroRails requires Python 3.9+ and has only one dependency (Click).

## Step 2: Initialize project

Run the interactive setup to install guardrails, agents, hooks, and templates:

```bash
kirorails init
```

This creates the `.kiro/` structure with steering files, agents, hooks, skills directory, and state files.

## Step 3: Configure build tools

Edit `.kiro/kirorails.conf` to match your project's build tools:

```bash
compile=./mvnw compile -q       # or: npm run build, cargo build, etc.
test=./mvnw test -q             # or: npm test, pytest, cargo test, etc.
lint=./mvnw checkstyle:check -q # or: npm run lint, ruff check, etc.
security=                       # optional: security scan command
```

## Step 4: Verify installation

```bash
kirorails doctor
```

All 20 checks should pass.

## Step 5: Add hooks

Add these hooks to your workspace:

### Pre-Task Health Check
```json
{
  "title": "KiroRails Pre-Task Health Check",
  "description": "Run compilation check and verify clean working tree before starting a spec task",
  "event": "Pre Task Execution",
  "action": "Run Command",
  "command": ".kiro/hooks-exec/pre-task.sh",
  "enabled": true
}
```

### Post-Task Verification
```json
{
  "title": "KiroRails Post-Task Verification",
  "description": "Run compile, test, and lint checks after completing a spec task",
  "event": "Post Task Execution",
  "action": "Run Command",
  "command": ".kiro/hooks-exec/post-task.sh",
  "enabled": true
}
```

# When to Load Steering Files

- Planning a feature or breaking down work → `delivery-workflow.md`
- Working on brownfield/legacy code → `brownfield-patterns.md`
- Verifying completed work or checking quality → `truth-loop.md`
- Managing sprints, backlog, or tasks → `sprint-management.md`
