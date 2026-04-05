# KiroRails Delivery Workflow

## The workflow

```
clarify → plan → analyze → implement → verify → learn
```

## Step 1: Clarify (optional but recommended)

Use the clarifier agent for Socratic questioning before planning. It scores clarity across 5 weighted dimensions (Functional 30%, Technical 25%, UX 20%, Data 15%, Non-functional 10%) and exposes hidden assumptions.

Threshold: clarity must reach 70/100 before planning. Output: `CLARIFICATIONS.md`.

## Step 2: Plan

Use the planner agent to break features into risk-scored atomic tasks. Each task must be small enough for one context window (max 5 files). Risk scored 1-5, ordered risk-first.

Output: `requirements.md`, `design.md`, `tasks.md`.

## Step 3: Analyze (optional but recommended)

Use the analyzer agent to check consistency between requirements, design, and tasks BEFORE implementation. Catches orphan requirements, dependency ordering issues, and missing rollback strategies.

Output: `ANALYSIS.md` with verdict: READY / READY WITH WARNINGS / NOT READY.

## Step 4: Implement

One task at a time. Each task = one commit. Follow steering files and matching skills. Run feedback loops after every task via `.kiro/hooks-exec/post-task.sh`.

## Step 5: Verify

Use the verifier agent for the Truth Loop. Checks done criteria, feedback loops, regressions, steering compliance, and phantom completions (tasks marked done with no real code changes).

Output: `VERIFICATION.md` with verdict: PASS / PASS WITH NOTES / FAIL.

## Step 6: Learn

Use the learner agent to extract reusable patterns from verified specs into `.kiro/skills/`. Only patterns from PASS-verified specs that appeared in 2+ tasks qualify.

## Core principles

- **Small steps** — one task = one commit. Never outrun your feedback loops.
- **Risk-first** — hard problems first, easy wins last.
- **Feedback loops** — tests, types, lint after every task. Nothing committed if they fail.
- **The codebase wins** — existing patterns are respected. AI adapts to your code.
