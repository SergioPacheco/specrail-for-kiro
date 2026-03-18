# specrail-for-kiro

**Structured delivery toolkit for Kiro.**

Reusable skills, steering, hooks, and workflow packs for brownfield and production-grade software delivery.

> Stop building separate agents. Start documenting expertise as skills that Kiro can learn and apply on demand.

---

## What it is

SpecRail is a community toolkit that adds delivery discipline on top of [Kiro](https://kiro.dev). It's built on [Ralph principles](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum): small steps, feedback loops, progress tracking, explicit quality, and risk-first execution.

It provides:

- **Delivery skills** — Markdown playbooks (agents) that teach Kiro how to plan, verify, and investigate bugs with built-in quality gates
- **Steering packs** — opinionated project/tech/coding standards ready to drop into `.kiro/steering/`
- **Spec templates** — structured requirements, design, and task templates for features and bugfixes
- **Hooks** — automated feedback loops on spec creation, task execution, and file saves
- **State tracking** — persistent operational memory (decisions, risks, progress) across sessions
- **Ralph loop** — autonomous execution script that runs tasks in a loop: pick → implement → test → commit → repeat
- **Domain packs** — pre-configured setups for Java legacy, Spring Boot, PostgreSQL, FastAPI, and more

Every piece is plain Markdown. No code required to create or customize. Anyone on the team — developers, architects, leads, QA — can write and adjust delivery rules.

## Why skills, not more agents?

The industry keeps building separate bots for each function. That doesn't scale — it fragments context and creates maintenance overhead.

SpecRail takes a different approach: **document expertise as skills** (Markdown playbooks) that a single AI loads on demand. Kiro sees a list of available skills and only reads the full playbook when it's needed. This progressive disclosure keeps the AI focused and avoids context overload.

## Skills + MCP

SpecRail skills are designed to work alongside [MCP](https://modelcontextprotocol.io/) servers:

- **MCP is the hand** — connects Kiro to external tools and data (APIs, databases, CI pipelines)
- **Skills are the experience** — tell Kiro what to do with the data and tools MCP provides

When you combine SpecRail skills with MCP integrations, Kiro can autonomously execute complex delivery workflows with discipline built in.

## Install

```bash
# Clone the repo
git clone https://github.com/<your-org>/specrail-for-kiro.git

# Bootstrap into your Kiro project
cd your-project
python path/to/specrail-for-kiro/scripts/bootstrap.py --pack java-legacy
```

The bootstrap script copies the selected steering files, spec templates, agents, hooks, and state files into your project's `.kiro/` directory.

## How it works

SpecRail follows the Ralph loop: define scope → execute in small steps → feedback loops validate each step → progress is tracked → repeat until done.

```
1. Install the kit           → bootstrap.py copies templates into .kiro/
2. Choose a pack             → java-legacy, spring-boot, postgres, etc.
3. Map the codebase          → codebase-mapper analyzes existing code
4. Steering is set           → .kiro/steering/ has your standards
5. Create or refine a spec   → use the spec templates
6. Call the planner agent    → clarify, scope, risks, tasks, done criteria
7. Execute task by task      → hooks validate, one commit per task
8. Verifier closes delivery  → checks tests, docs, state
9. Archive the spec          → move to specs/archive/
10. State persists           → STATE.md, DECISIONS.md, RISKS.md updated
```

### Two modes of execution

| Mode | How it works | Best for |
|------|-------------|----------|
| **HITL** (human-in-the-loop) | Run one task at a time, watch, intervene | Learning, risky tasks, architectural decisions |
| **AFK** (away from keyboard) | Ralph loop runs tasks autonomously | Bulk work, well-defined tasks, low-risk implementation |

Start with HITL — watch the first few iterations. Once you trust the prompt, go AFK.

### The Ralph loop

```bash
# Execute all tasks from a spec, max 10 iterations
./scripts/specrail-ralph.sh order-email-notification

# Limit to 5 iterations
./scripts/specrail-ralph.sh order-email-notification 5
```

Each iteration:
1. Reads `tasks.md` to find the next uncompleted task
2. Implements that one task
3. Runs feedback loops (tests, types, lint)
4. Commits atomically
5. Updates `PROGRESS.md` and `CHANGELOG_AI.md`
6. Stops when all tasks are done or max iterations reached

## Core principles

SpecRail is built on these principles, adapted from [Ralph Wiggum methodology](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum):

**Small steps** — Each task is one atomic commit. Never outrun your feedback loops. If a task feels too large, the planner breaks it into subtasks. Quality over speed.

**Feedback loops** — Tests, types, and linting run after every task. Hooks validate before and after execution. Nothing gets committed if feedback loops fail. The more loops you give the AI, the higher quality code it produces.

**Progress tracking** — `PROGRESS.md` tracks what's done per spec. `STATE.md` persists across sessions. The AI reads these before each iteration to skip exploration and jump straight into the next task.

**Risk-first execution** — The planner prioritizes risky tasks first: architectural decisions, integration points, unknown unknowns. Easy wins come last. Fail fast on hard problems.

**Explicit quality** — The steering files tell the AI what kind of codebase this is. Production code with audit trails, not a prototype. The AI follows the codebase patterns it sees — so keep your codebase clean before letting it loose.

**HITL → AFK** — Start supervised, go autonomous once you trust the prompt. Use HITL for risky tasks and architectural decisions. Use AFK for well-defined implementation work.

## Kiro folder layout after bootstrap

```
your-project/
└── .kiro/
    ├── steering/
    │   ├── product.md
    │   ├── tech.md
    │   ├── structure.md
    │   ├── coding-standards.md
    │   ├── testing.md
    │   ├── security.md
    │   └── <pack-specific>.md
    ├── specs/
    │   └── <your-specs>/
    ├── agents/
    │   ├── planner.md
    │   ├── verifier.md
    │   ├── bugfix-investigator.md
    │   ├── codebase-mapper.md
    │   └── quick-change.md
    ├── hooks/
    │   ├── pre-task-quality.md
    │   ├── post-task-verification.md
    │   ├── on-spec-created.md
    │   └── on-file-save-guardrails.md
    └── state/
        ├── STATE.md
        ├── DECISIONS.md
        ├── RISKS.md
        └── CHANGELOG_AI.md
```

## Agents included

| Agent | Purpose |
|-------|---------|
| **planner** | Transforms an idea into scope, risks, small tasks, dependencies, and done criteria |
| **verifier** | Checks if delivery matches criteria, tests exist, no obvious regression, state updated |
| **bugfix-investigator** | Forces reproduce → isolate root cause → describe current/expected → only then fix |
| **codebase-mapper** | Analyzes existing codebase and produces a structural map for brownfield planning |
| **quick-change** | Handles small, well-understood changes without the full planner flow |

## Hooks included

| Hook | Trigger | What it does |
|------|---------|--------------|
| **on-spec-created** | Spec creation | Validates completeness, suggests missing sections |
| **pre-task-quality** | Before task execution | Checks preconditions, flags risks |
| **post-task-verification** | After task execution | Verifies expected files changed, tests pass, state updated |
| **on-file-save-guardrails** | File save | Checks critical file changes against coding standards |

## Available packs

| Pack | Stack | Focus |
|------|-------|-------|
| `java-legacy` | Java 11+, layered architecture | Safe refactoring, migration, legacy patterns |
| `spring-boot` | Spring Boot | REST APIs, configuration, testing |
| `postgres` | PostgreSQL | Migrations with rollback, query review, schema safety |
| `python-fastapi` | Python + FastAPI | API design, async patterns, typing |

## Example walkthrough

See [docs/examples/java-legacy.md](docs/examples/java-legacy.md) for a complete walkthrough: bootstrapping a Java 17 / JSF / PostgreSQL project, mapping the codebase, planning a feature (email notifications with 4 tasks), and fixing a bug (discount rounding with regression test first).

## Recommended conventions

- Every bugfix starts with a reproduction step
- Every migration includes a rollback strategy
- Every task has explicit done criteria
- State files are updated at the end of each session
- Decisions are recorded with context and date
- Skills are plain Markdown — anyone on the team can create or adjust them
- One task = one atomic commit with a descriptive message
- Completed specs are archived to `specs/archive/` for future reference

## Roadmap

### v0.1 — Foundation
- [x] Bootstrap script
- [x] Core steering pack (product, tech, structure, coding-standards, testing, security)
- [x] Java legacy pack + PostgreSQL pack
- [x] Planner, verifier, and bugfix-investigator agents
- [x] Codebase-mapper and quick-change agents
- [x] 4 core hooks
- [x] Spec templates (feature + bugfix)
- [x] State templates
- [x] Ralph loop script (`specrail-ralph.sh`)
- [x] Health checks before each iteration
- [x] init.sh environment setup template
- [x] Clean state rule and markdown tampering protection
- [x] Example walkthrough (Java legacy)

### v0.2 — Automation
- [ ] Auto-generation of STATE.md summaries
- [ ] Auto-update of DECISIONS.md
- [ ] Spring Boot, FastAPI, and React packs
- [ ] Release checklist templates
- [ ] Verification reports

### v0.3 — Team & Integration
- [ ] MCP integration
- [ ] Report generation
- [ ] Team mode
- [ ] Corporate packs
- [ ] Risk score per task

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to add.

## License

MIT — see [LICENSE](LICENSE).
