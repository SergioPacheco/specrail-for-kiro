# 🛤️ KiroRails

**The Tech Lead your AI agent needs.**

KiroRails is a delivery kit for [Kiro](https://kiro.dev) that turns AI-assisted coding into a repeatable, verified process. It installs guardrails, verification loops, and work management into your project's `.kiro/` directory — so your AI writes production code, not prototypes.

Built specifically for **brownfield projects** where the risk of AI breaking existing code is high.

```bash
pip install kirorails
kirorails init
```

> *"GSD builds. BMAD organizes. KiroRails guarantees."*

---

## What is KiroRails?

KiroRails is a Python CLI that installs structured markdown files and bash scripts into your project's `.kiro/` folder. These files tell Kiro how to behave: what standards to follow, how to plan work, how to verify results, and when to stop.

It does NOT write application code. It provides the structure and verification for AI to do so safely.

The system is built on five pillars:

```
┌─────────────────────────────────────────────────────────────────────┐
│                          KiroRails                                  │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │   GUARDRAILS │  │   PERSONAS   │  │       TRUTH LOOP         │  │
│  │              │  │              │  │                          │  │
│  │  steering/   │  │  agents/     │  │  pre-task.sh → implement │  │
│  │  product.md  │  │  planner.md  │  │  → post-task.sh → verify │  │
│  │  tech.md     │  │  verifier.md │  │  → commit or fix & retry │  │
│  │  coding-*.md │  │  mapper.md   │  │                          │  │
│  │  blueprints  │  │  bugfix.md   │  │  Nothing committed       │  │
│  │              │  │              │  │  without green loops.     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────┐  ┌────────────────────────────────┐  │
│  │     EXECUTABLE HOOKS     │  │      SPRINT MANAGEMENT         │  │
│  │                          │  │                                │  │
│  │  kirorails.conf          │  │  backlog.md → sprints → tasks  │  │
│  │  compile=./mvnw compile  │  │  quick tasks (no planning)    │  │
│  │  test=./mvnw test        │  │  progress dashboard           │  │
│  │  lint=./mvnw checkstyle  │  │  status tracking via emoji    │  │
│  │                          │  │                                │  │
│  │  Works with any build    │  │  Markdown is the database.    │  │
│  │  tool. No lock-in.       │  │  No external dependencies.    │  │
│  └──────────────────────────┘  └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

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

## The Five Pillars

### 1. Expert Guardrails

Steering files in `.kiro/steering/` that Kiro loads automatically as context. They define what the AI can and cannot do:

| Guardrail | Loaded | Purpose |
|-----------|--------|---------|
| product.md, tech.md, structure.md | always | Core project context |
| coding-standards.md | auto | Feedback loops, commit rules, quality |
| testing.md, security.md | auto (full) | Test and security standards |
| Stack blueprints (brownfield-java.md, etc.) | auto | Stack-specific rules and patterns |
| compliance.md, regulatory.md | manual | SOX/HIPAA/PCI-DSS/GDPR awareness |

These are templates with sensible defaults. You customize them for your project.

### 2. Specialist Personas

AI agents in `.kiro/agents/` with specific expertise:

| Persona | Mode | What it does |
|---------|------|-------------|
| **Clarifier** | lite | Pre-planning clarification — eliminates ambiguity, produces `CLARIFICATIONS.md` |
| **Planner** | lite | Breaks features into risk-scored atomic tasks (1-5 risk scale), orders risk-first, defines done criteria per task |
| **Analyzer** | lite | Pre-implementation consistency check — validates coverage, ordering, feasibility, produces `ANALYSIS.md` |
| **Verifier** | lite | Runs the Truth Loop — checks done criteria, feedback loops, regressions, phantom completions. Produces `VERIFICATION.md` |
| **Bug Hunter** | full | Reproduce → root cause → fix. Never skips steps |
| **Codebase Mapper** | full | Analyzes brownfield architecture before planning changes |
| **Quick Change** | full | Small changes without full planning flow |
| **Report Generator** | full | Delivery summaries from state files |

### 3. Truth Loop

The verification engine. After every task:

```
Task completed
  → Run feedback loops (compile, test, lint)
  → Check done criteria
  → Check for regressions
  → Verify state files updated
  → Check steering compliance
  → Produce VERIFICATION.md
  → Verdict: ✅ PASS | ⚠️ PASS WITH NOTES | ❌ FAIL
```

Here's what it looks like in practice:

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

### 4. Executable Hooks

Real bash scripts that run your actual build tools. Not documentation — automation.

```bash
# .kiro/kirorails.conf — edit for your project
compile=./mvnw compile -q
test=./mvnw test -q
lint=./mvnw checkstyle:check -q
security=
```

```bash
.kiro/hooks-exec/pre-task.sh    # check clean tree + compile
.kiro/hooks-exec/post-task.sh   # compile + test + lint gate
```

The hooks read `kirorails.conf` so they work with any build tool — Maven, Gradle, npm, cargo, whatever.

### 5. Sprint & Backlog Management

For projects with many requirements, KiroRails organizes work into sprints using markdown files as the database:

```bash
kirorails sprint init                     # creates backlog.md
kirorails sprint new sprint-1-foundation  # creates sprint dir with tasks.md
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

Quick tasks skip the full planning flow:

```bash
kirorails quick "Add CRUD for Product entity"           # standalone quick task
kirorails quick "Fix date format" --sprint sprint-2     # add to existing sprint
```

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

## Progress Dashboard

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

## Execution Modes

| Mode | How | Best for |
|------|-----|----------|
| **HITL** (Human-in-the-loop) | Run one task, review, intervene | Risky tasks, architectural decisions |
| **AFK** (Autonomous) | Truth Loop runs tasks automatically | Well-defined, low-risk tasks |

Start with HITL. Move to AFK once you trust the guardrails.

### Ralph Loop (experimental)

Autonomous execution via `kiro-cli chat --no-interactive`:

```bash
./scripts/kirorails-ralph.sh order-email-notification 5
```

Every iteration: health check → pick task → implement → test → commit → update state. ⚠️ Experimental — test with HITL first.

---

## Core Principles

Built on [Ralph methodology](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum):

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

- **Small steps** — one task = one commit. Never outrun your feedback loops.
- **Risk-first** — hard problems first, easy wins last. Risk scored 1-5 per task.
- **Feedback loops** — tests, types, lint after every task. Nothing committed if they fail.
- **The codebase wins** — existing patterns are respected. AI adapts to your code, not the other way around.

The key insight: AI code quality degrades as context grows (context rot). By keeping each task small and verified, you get consistently high-quality output instead of a slow decline into hallucinations.

---

## CLI Reference

```
kirorails init [--pack NAME] [--mode lite|full|add]   Install KiroRails
kirorails doctor                                       Validate installation health
kirorails clarify [feature]                            Pre-planning clarification
kirorails plan [feature]                               Trigger planner
kirorails analyze [feature]                            Pre-implementation consistency check
kirorails verify                                       Trigger Truth Loop
kirorails map                                          Trigger codebase mapping
kirorails sprint init                                  Create backlog.md
kirorails sprint new <name>                            Create sprint directory
kirorails sprint list                                  Show sprint progress
kirorails quick "<description>" [--sprint NAME]        Quick task (no planning)
kirorails status                                       Progress dashboard
```

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
