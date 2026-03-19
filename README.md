# 🛤️ KiroRails for Kiro

**The only Kiro kit designed for complex brownfield projects.**

KiroRails is the "Tech Lead" your AI agent needs. It wraps [Kiro](https://kiro.dev) with structured planning, expert guardrails, and automated verification loops — so your AI writes production code, not prototypes.

> *"GSD builds. BMAD organizes. KiroRails guarantees."*

---

## Why KiroRails?

| Problem | KiroRails Solution |
|---------|-------------------|
| AI ignores your coding standards | **Expert Guardrails** enforce your rules on every interaction |
| AI breaks existing code | **Stack Blueprints** teach it your legacy patterns before it touches anything |
| No way to know if AI work is correct | **Truth Loop** verifies every task against done criteria + feedback loops |
| Complex features become a mess | **Specialist Personas** break work into atomic, verified micro-tasks |
| Project has dozens of requirements | **Sprint/Backlog** tracking organizes work into iterations |
| CRUDs don't need full planning | **Quick Tasks** skip requirements→design, go straight to tasks |

### Safe for Brownfield

Specialized blueprints for Java Legacy, Spring Boot, PostgreSQL, and compliance-heavy codebases. KiroRails maps your existing architecture before planning any changes.

### Truth Loop

Automated verification that prevents hallucinations. Every task runs through: tests → types → lint → done criteria → verification report. Nothing gets committed without passing.

### Atomic Execution

Break complex features into verified micro-tasks. Each task = one context window = one commit. Small steps, feedback loops, risk-first ordering.

---

## Quick Start

```bash
pip install kirorails

cd your-project
kirorails init
```

The interactive setup asks for your stack and installs everything:

```
🛤️  KiroRails Setup

Available stack blueprints:
  1. java-legacy          Java 11+, layered architecture, safe refactoring
  2. spring-boot          Spring Boot 3.x, REST APIs, sliced tests
  3. postgres             PostgreSQL migrations, query review, schema safety
  4. python-fastapi       Python + FastAPI, async patterns, Pydantic v2
  5. compliance           Audit trails, SOX/HIPAA/PCI-DSS/GDPR

Which blueprint(s)? 1,2
Install mode [lite]: full
```

Or skip the prompts:

```bash
kirorails init --pack java-legacy,spring-boot --mode full
```

Then set up your project:

```bash
kirorails sprint init                    # create backlog for requirements
kirorails sprint new sprint-1-foundation # create first sprint
kirorails quick "Add CRUD for Product"   # quick task, no planning overhead
kirorails status                         # see progress dashboard
```

---

## See It In Action

Here's what happens when KiroRails catches a problem before it reaches production:

```
$ .kiro/hooks-exec/post-task.sh

🛤️  KiroRails post-task verification
─────────────────────────────────────
  Compile... ✓
  Tests  ... ✓
  Lint   ... ✗ FAILED
─────────────────────────────────────
✗ 1 check(s) failed — do NOT commit.
```

The AI wrote code that passed tests but violated your checkstyle rules. Without KiroRails, that commit goes through. With KiroRails, it's blocked — the AI must fix the lint issue before proceeding.

After the fix:

```
$ .kiro/hooks-exec/post-task.sh

🛤️  KiroRails post-task verification
─────────────────────────────────────
  Compile... ✓
  Tests  ... ✓
  Lint   ... ✓
─────────────────────────────────────
✓ All checks passed — safe to commit.
```

That's the Truth Loop in action: **no commit without green feedback loops.**

---

## Sprint & Backlog Management

For projects with many requirements, KiroRails organizes work into sprints:

```bash
kirorails sprint init                     # creates backlog.md
kirorails sprint new sprint-1-foundation  # creates sprint dir with tasks.md
kirorails sprint new sprint-2-crud        # another sprint
kirorails sprint list                     # show all sprints + progress
```

**backlog.md** tracks all requirements:
```markdown
| ID  | Requirement              | Sprint    | Status        |
|-----|--------------------------|-----------|---------------|
| R01 | User authentication      | sprint-1  | ✅ Done       |
| R02 | Product CRUD             | sprint-2  | 🔄 In Progress|
| R03 | Order management         | sprint-3  | 🔲 Todo       |
| R04 | Payment integration      | —         | ❌ Blocked    |
```

Each sprint gets its own `tasks.md` — no rigid requirements→design→tasks flow unless you want it.

### Quick Tasks

Not everything needs full planning. CRUDs, config changes, simple fixes:

```bash
kirorails quick "Add CRUD for Product entity"           # standalone quick task
kirorails quick "Fix date format" --sprint sprint-2     # add to existing sprint
```

Generates just a `tasks.md` — straight to work.

---

## Magic Commands

Process becomes command. Use these in Kiro chat or from your terminal:

| Command | What it does |
|---------|-------------|
| `kirorails:map` | Triggers the codebase mapper → generates `CODEBASE.md` |
| `kirorails:plan` | Triggers the planner → generates risk-scored `TASKS.md` |
| `kirorails:verify` | Triggers the Truth Loop → produces `VERIFICATION.md` |

From terminal:
```bash
kirorails map        # check prerequisites, get the Kiro prompt
kirorails plan       # same for planning
kirorails verify     # same for verification
```

---

## Progress Dashboard

See everything at a glance:

```bash
kirorails status
```

```
🛤️  KiroRails Status Dashboard
═══════════════════════════════════════

📋 Backlog: 63 requirements
   ✅ 24 done  🔄 5 in progress  🔲 31 todo  ❌ 3 blocked

🏃 Sprints: 8 total, 29/63 tasks done

   ✅ sprint-1-foundation            ███████████████ 8/8
   ✅ sprint-2-crud                  ███████████████ 7/7
   🔄 sprint-3-orders               ████████░░░░░░░ 5/9
   🔲 sprint-4-payments             ░░░░░░░░░░░░░░░ 0/6
   ...

🔧 Hooks: configured (.kiro/kirorails.conf)

═══════════════════════════════════════
```

---

## Executable Hooks

Real automation, not just documentation. KiroRails installs bash scripts that run your actual build tools:
```bash
# .kiro/kirorails.conf — edit for your project
compile=./mvnw compile -q
test=./mvnw test -q
lint=./mvnw checkstyle:check -q
security=
```

```bash
# Before starting a task
.kiro/hooks-exec/pre-task.sh
# ✓ Working tree clean
# ✓ Compiling... ✓

# After completing a task
.kiro/hooks-exec/post-task.sh
# ✓ Compile ✓
# ✓ Tests   ✓
# ✓ Lint    ✓
# ✓ All checks passed — safe to commit.
```

The hooks read `kirorails.conf` so they work with any build tool — Maven, Gradle, npm, cargo, whatever.

---

## What Gets Installed

### Lite mode (default) — ~11 files

```
.kiro/
├── steering/                    ← Expert Guardrails
│   ├── product.md               (always loaded)
│   ├── tech.md                  (always loaded)
│   ├── structure.md             (always loaded)
│   ├── coding-standards.md      (auto — feedback loops rule)
│   └── brownfield-java.md       (auto — your stack blueprint)
├── agents/                      ← Specialist Personas
│   ├── planner.md               plan features into verified micro-tasks
│   └── verifier.md              Truth Loop — verify everything
├── hooks-exec/                  ← Real Automation
│   ├── pre-task.sh              check clean tree + compile
│   └── post-task.sh             compile + test + lint gate
├── kirorails.conf                ← hook config (edit for your build tool)
└── specs/
    └── feature/
        └── tasks.template.md    task breakdown template
```

### Full mode — ~24 files

Everything in lite, plus:
- 2 additional guardrails (testing, security)
- 4 additional personas (bug hunter, codebase mapper, quick-change, report generator)
- 6 markdown hooks (for when Kiro supports them natively)
- 1 additional template (design.template.md)

---

## Expert Guardrails

Steering files that keep your AI on the rails. Loaded automatically based on context:

| Guardrail | Mode | Purpose |
|-----------|------|---------|
| product.md, tech.md, structure.md | `always` | Core project context |
| coding-standards.md, testing.md, security.md | `auto` | Quality standards |
| Stack blueprints (brownfield-java.md, etc.) | `auto` | Stack-specific rules |
| mcp.md, team.md | `manual` | On-demand context |
| compliance.md, regulatory.md | `manual` | Regulated projects |

---

## Specialist Personas

AI agents with specific expertise, loaded on demand:

| Persona | Mode | Specialty |
|---------|------|-----------|
| **Planner** | lite | Break features into risk-scored, atomic tasks |
| **Verifier** | lite | Truth Loop — verify work against criteria |
| **Bug Hunter** | full | Reproduce → root cause → fix (never skip steps) |
| **Codebase Mapper** | full | Analyze brownfield architecture before planning |
| **Quick Change** | full | Small changes without full planning flow |
| **Report Generator** | full | Delivery summaries from state files |

---

## Stack Blueprints

Pre-configured opinions for your stack. Composable — use multiple:

| Blueprint | Focus |
|-----------|-------|
| `java-legacy` | Safe refactoring, migration rules, legacy patterns |
| `spring-boot` | Spring Boot 3.x conventions, sliced tests, security config |
| `postgres` | Zero-downtime migrations, query optimization |
| `python-fastapi` | Pydantic v2, async patterns, typed config |
| `compliance` | Audit trails, SOX/HIPAA/PCI-DSS/GDPR awareness |

```bash
kirorails init --pack spring-boot,postgres,compliance --mode full
```

---

## Truth Loop — How Verification Works

The Truth Loop is what makes KiroRails different. Every task goes through:

```
Task completed
  → Run feedback loops (tests, types, lint)
  → Check done criteria
  → Check for regressions
  → Verify state files updated
  → Check steering compliance
  → Produce VERIFICATION.md
  → Verdict: ✅ PASS | ⚠️ PASS WITH NOTES | ❌ FAIL
```

The verifier catches what code review misses: missing tests, broken imports, state drift, steering violations. It creates a permanent audit trail in `VERIFICATION.md`.

---

## Execution Modes

| Mode | How | Best for |
|------|-----|----------|
| **HITL** (Human-in-the-loop) | Run one task, review, intervene | Risky tasks, architectural decisions |
| **AFK** (Autonomous) | Truth Loop runs tasks automatically | Well-defined, low-risk tasks |

Start with HITL. Move to AFK once you trust the guardrails.

### Ralph Loop (experimental)

```bash
./scripts/kirorails-ralph.sh order-email-notification 5
```

⚠️ Experimental. Uses `kiro-cli chat --no-interactive`. Test with HITL first.

---

## CLI Reference

```
kirorails init [--pack NAME] [--mode lite|full|add]   Install KiroRails
kirorails sprint init                                  Create backlog.md
kirorails sprint new <name>                            Create sprint directory
kirorails sprint list                                  Show sprint progress
kirorails quick "<description>" [--sprint NAME]        Quick task (no planning)
kirorails status                                       Progress dashboard
kirorails map                                          Trigger codebase mapping
kirorails plan [feature]                               Trigger planner
kirorails verify                                       Trigger Truth Loop
```

---

## Core Principles

Built on [Ralph methodology](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum):

- **Small steps** — one task = one commit. Never outrun your feedback loops.
- **Risk-first** — hard problems first, easy wins last. Risk scored 1-5 per task.
- **Feedback loops** — tests, types, lint after every task. Nothing committed if they fail.
- **Progress tracking** — dashboards per sprint and across the project.
- **The codebase wins** — existing patterns are respected. AI adapts to your code, not the other way around.

### The Ralph Loop in Practice

Every task follows this cycle:

```
┌─────────────────────────────────────────────┐
│  1. HEALTH CHECK   pre-task.sh              │
│     Is the build green? Working tree clean?  │
│                    ↓                         │
│  2. PICK TASK      highest risk first        │
│     One task, one context window, one commit │
│                    ↓                         │
│  3. IMPLEMENT      follow steering rules     │
│     AI writes code guided by guardrails      │
│                    ↓                         │
│  4. VERIFY         post-task.sh              │
│     compile → test → lint → done criteria    │
│                    ↓                         │
│  5. COMMIT         atomic, or fix and retry  │
│     Only if ALL checks pass                  │
└─────────────────────────────────────────────┘
```

The key insight: AI code quality degrades as context grows (context rot). By keeping each task small and verified, you get consistently high-quality output instead of a slow decline into hallucinations.

---

## Maturity

| Component | Status |
|-----------|--------|
| CLI install (`pip install kirorails`) | ✅ Tested |
| Expert Guardrails (steering files) | ✅ Tested |
| Sprint/Backlog management | ✅ Tested |
| Quick Tasks | ✅ Tested |
| Progress Dashboard | ✅ Tested |
| Executable Hooks (bash) | ✅ Tested |
| Specialist Personas (agent frontmatter) | ✅ Tested |
| Planner and Verifier workflows | 🔶 Tested in Kiro chat |
| Truth Loop (automated verification) | 🔶 Tested in Kiro chat |
| Quality Hooks (markdown) | 🔶 Format validated |
| Ralph Loop | ⚠️ Experimental |

---

## Roadmap

- [ ] Test all specialist personas in live Kiro environment
- [ ] Validate quality hooks in Kiro hooks system
- [ ] Validate Ralph Loop with current kiro-cli release
- [ ] First tagged release with compatibility declaration
- [ ] Explore Kiro Powers format (POWER.md + dynamic activation)

---

## Contributing

Contributions welcome. Please open an issue first to discuss what you'd like to add.

## License

MIT — see [LICENSE](LICENSE).
