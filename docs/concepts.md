# Concepts

## Core concepts in SpecRail

### Skill

A skill is a Markdown file that works as a playbook — it teaches Kiro exactly how to execute a specific task, which steps to follow, and what to avoid. In SpecRail, every agent and steering file is a skill.

Kiro doesn't load all skills at once. It sees a list of available skills (titles) and only reads the full playbook when it decides that skill is needed. This is called **progressive disclosure** — it keeps the AI focused and avoids context overload.

Skills are plain Markdown. You don't need to be a developer to create or customize one. Anyone on the team — architects, leads, QA, DBAs — can write delivery rules in natural language.

### Pack

A pack is a pre-configured set of steering files, agents, hooks, and state templates for a specific stack or domain. Examples: `java-legacy`, `spring-boot`, `postgres`.

When you run `bootstrap.py --pack java-legacy`, the pack determines which files are copied into your `.kiro/` directory.

### Steering

Steering files live in `.kiro/steering/` and tell Kiro how to behave in your project. SpecRail provides opinionated steering templates for:

- **product.md** — what the product is, who it's for, key constraints
- **tech.md** — stack, versions, infrastructure, deployment
- **structure.md** — project layout, module boundaries, naming conventions
- **coding-standards.md** — code style, patterns, anti-patterns
- **testing.md** — test strategy, coverage expectations, test types
- **security.md** — auth, secrets, input validation, OWASP basics
- **Pack-specific** — e.g., `brownfield-java.md`, `postgres.md`

### State files

State files are SpecRail's operational memory. They persist across sessions:

- **STATE.md** — current status, active spec, blockers, next steps
- **DECISIONS.md** — architectural and technical decisions with context and date
- **RISKS.md** — known risks, mitigation status, owner
- **CHANGELOG_AI.md** — log of AI-assisted changes with rationale

### Quality gates

Quality gates are checkpoints enforced by hooks and agents:

- **Pre-task** — are preconditions met? Are risks flagged?
- **Post-task** — did the right files change? Do tests pass? Is state updated?
- **Spec creation** — is the spec complete? Are sections missing?
- **File save** — does the change respect coding standards?

### Agents

SpecRail agents are Kiro custom agents with specific delivery roles. Each agent is a skill — a Markdown playbook that Kiro loads on demand, not a separate bot:

- **Planner** — breaks an idea into scope, risks, tasks, dependencies, done criteria
- **Verifier** — checks delivery against criteria, tests, regressions, state
- **Bugfix investigator** — enforces reproduce → root cause → describe → fix flow

### Skills + MCP

SpecRail skills are designed to work alongside MCP (Model Context Protocol) servers:

- **MCP is the hand** — connects Kiro to external tools and data (APIs, databases, CI pipelines)
- **Skills are the experience** — tell Kiro what to do with the data and tools MCP provides

When MCP integration arrives, SpecRail skills will orchestrate MCP tools with delivery discipline built in.

### Hooks

Hooks are Kiro event-driven automations. SpecRail provides hooks for:

- Spec creation events
- Pre/post task execution
- File save events on critical paths

### Bootstrap

The bootstrap script (`scripts/bootstrap.py`) is the entry point. It copies the right files from SpecRail into your project's `.kiro/` directory based on the selected pack.

### Codebase map

Before planning in a brownfield project, the codebase-mapper agent scans the existing code and produces a `CODEBASE.md` file in `.kiro/state/`. This map documents the stack, architecture, patterns, entry points, and concerns — giving the planner and other agents the context they need to make safe changes.

### Clarify phase

The planner agent includes a clarify phase before breaking work into tasks. It asks structured questions to eliminate ambiguity and records the answers in a `CONTEXT.md` file inside the spec folder. This prevents the AI from guessing and ensures the plan matches what the user actually wants.

### Quick change

Not every change needs the full planner → verifier flow. The quick-change agent handles small, well-understood changes (≤ 3 files, low risk, no migrations) with a lightweight 6-step process. If the change grows beyond scope, it suggests switching to the full planner.

### Atomic commits

Each task in a spec maps to exactly one git commit. The commit message follows the format `type(scope): description`. This keeps history clean, enables `git bisect`, and makes each change independently revertable.

### Spec archive

Completed specs are moved from `.kiro/specs/<name>/` to `.kiro/specs/archive/<date>-<name>/`. This keeps the active specs folder clean while preserving all decisions, context, and design rationale for future reference.
