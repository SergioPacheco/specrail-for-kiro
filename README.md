# 🛤️ KiroRails

**The Tech Lead your AI agent needs.**

KiroRails is a delivery kit for [Kiro](https://kiro.dev) that turns AI-assisted coding into a repeatable, verified process. It installs guardrails, verification loops, and work management into your project's `.kiro/` directory — so your AI writes production code, not prototypes.

Built specifically for **brownfield projects** where the risk of AI breaking existing code is high.

> *"GSD builds. BMAD organizes. KiroRails guarantees."*

---

## Quick Start

### Option 1: curl (no dependencies)

```bash
# Install core files
curl -fsSL https://raw.githubusercontent.com/SergioPacheco/KiroRails/main/install.sh | bash

# With a stack blueprint
curl -fsSL https://raw.githubusercontent.com/SergioPacheco/KiroRails/main/install.sh | bash -s -- --pack java-legacy

# Multiple blueprints
curl -fsSL https://raw.githubusercontent.com/SergioPacheco/KiroRails/main/install.sh | bash -s -- --pack spring-boot,postgres
```

Installs all steering files, agents, hooks, templates, and state files directly from GitHub. No Python, no Node.js required.

> For the full CLI (`check-phantom`, sprint management, skill learning), also run `pip install kirorails`.

### Option 2: pip (full CLI)

```bash
pip install kirorails
cd your-project
kirorails init --pack java-legacy
kirorails doctor    # verify installation health
```

### Option 3: Kiro Power (one-click in Kiro IDE)

1. Open Kiro → Powers panel → **Add power from GitHub**
2. Enter: `https://github.com/SergioPacheco/KiroRails`
3. Done — activates automatically when you mention delivery, planning, or brownfield keywords

---

## What is KiroRails?

KiroRails is a Python CLI that installs structured markdown files and bash scripts into your project's `.kiro/` folder. These files tell Kiro how to behave: what standards to follow, how to plan work, how to verify results, and when to stop.

It does NOT write application code. It provides the structure and verification for AI to do so safely.

The system is built on six pillars:

```
┌─────────────────────────────────────────────────────────────────────┐
│                          KiroRails                                  │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │   GUARDRAILS │  │   PERSONAS   │  │       TRUTH LOOP         │  │
│  │              │  │              │  │                          │  │
│  │  steering/   │  │  agents/     │  │  pre-task.sh → implement │  │
│  │  product.md  │  │  clarifier   │  │  → post-task.sh → verify │  │
│  │  tech.md     │  │  analyzer    │  │  → check-phantom         │  │
│  │  coding-*.md │  │  verifier    │  │  → commit or fix & retry │  │
│  │  skills.md   │  │  learner     │  │                          │  │
│  │  blueprints  │  │  bugfix      │  │  Nothing committed       │  │
│  │              │  │              │  │  without green loops.    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────┐  ┌────────────────────────────────┐  │
│  │    CUSTOM SKILLS         │  │      SPRINT MANAGEMENT         │  │
│  │                          │  │                                │  │
│  │  .kiro/skills/           │  │  backlog.md → sprints → tasks  │  │
│  │  Agent Skills standard   │  │  quick tasks (no planning)    │  │
│  │  auto-inject on match    │  │  progress dashboard           │  │
│  │  learn from past specs   │  │  status tracking via emoji    │  │
│  │                          │  │                                │  │
│  │  Team knowledge that     │  │  Markdown is the database.    │  │
│  │  compounds over time.    │  │  No external dependencies.    │  │
│  └──────────────────────────┘  └────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Why KiroRails?

| Problem | KiroRails Solution |
|---------|-------------------|
| AI ignores your coding standards | **Expert Guardrails** enforce your rules on every interaction |
| AI breaks existing code | **Stack Blueprints** teach it your legacy patterns before it touches anything |
| No way to know if AI work is correct | **Truth Loop** verifies every task — including phantom completion detection |
| Requirements are vague | **Deep Interview** uses Socratic questioning with clarity scoring before planning |
| Complex features become a mess | **Specialist Personas** break work into atomic, verified micro-tasks |
| Same patterns reimplemented every time | **Custom Skills** auto-inject learned patterns when triggers match |
| Project has dozens of requirements | **Sprint/Backlog** tracking organizes work into iterations |
| CRUDs don't need full planning | **Quick Tasks** skip requirements→design, go straight to tasks |

---

## The Delivery Workflow

```
clarify → analyze → implement → check-phantom → verify → learn
```

| Step | Command | What happens |
|------|---------|-------------|
| 1. Clarify | `kirorails clarify "feature"` | Deep Interview — Socratic questioning, clarity score, hidden assumptions |
| 2. Analyze | `kirorails analyze "feature"` | Pre-implementation consistency check — coverage, ordering, feasibility |
| 3. Implement | Ralph Loop or manual | AI implements one task at a time, guided by steering + skills |
| 4. Check | `kirorails check-phantom` | Deterministic phantom detection — git diff vs tasks.md |
| 5. Verify | `kirorails verify` | Truth Loop — feedback loops, steering compliance, VERIFICATION.md |
| 6. Learn | `kirorails learn` | Extract reusable patterns from verified specs into skills |

---

## The Six Pillars

### 1. Expert Guardrails

Steering files in `.kiro/steering/` that Kiro loads automatically as context. Uses Kiro's native inclusion modes:

| Guardrail | Inclusion Mode | Purpose |
|-----------|---------------|---------|
| product.md, tech.md, structure.md | `always` | Core project context |
| coding-standards.md | `auto` | Feedback loops, commit rules, quality |
| skills.md | `always` | Custom skills system — auto-injection rules |
| testing.md, security.md | `auto` | Test and security standards |
| Stack blueprints (brownfield-java.md, etc.) | `fileMatch` | Stack-specific rules — loads only for matching files |
| compliance.md, regulatory.md | `manual` | SOX/HIPAA/PCI-DSS/GDPR awareness |

Stack blueprints use `fileMatch` so they only load when you're working on relevant files:
- `brownfield-java.md` → activates for `**/*.java`, `**/pom.xml`
- `postgres.md` → activates for `**/*.sql`, `**/migration*/**`
- `spring-boot.md` → activates for `**/*.java`, `**/application*.yml`
- `fastapi.md` → activates for `**/*.py`, `**/pyproject.toml`

### 2. Specialist Personas

AI agents in `.kiro/agents/` with specific expertise:

| Persona | What it does |
|---------|-------------|
| **Clarifier** | Deep Interview — Socratic clarification with clarity scoring (0-100), hidden assumption exposure |
| **Analyzer** | Pre-implementation consistency check — validates coverage, ordering, feasibility, produces `ANALYSIS.md` |
| **Verifier** | Runs the Truth Loop — checks done criteria, feedback loops, regressions, steering compliance. Produces `VERIFICATION.md` |
| **Learner** | Extracts reusable patterns from verified specs into portable skill files |
| **Bug Hunter** | Reproduce → root cause → fix. Never skips steps |

### 3. Truth Loop

The verification engine. After every task:

```
Task completed
  → Run feedback loops (compile, test, lint)
  → kirorails check-phantom (deterministic git diff check)
  → Check done criteria
  → Check for regressions
  → Verify state files updated
  → Check steering compliance
  → Produce VERIFICATION.md
  → Verdict: ✅ PASS | ⚠️ PASS WITH NOTES | ❌ FAIL
```

**Phantom completion detection** is now deterministic — it runs `git diff` and compares against tasks.md:

```
$ kirorails check-phantom

👻 KiroRails Phantom Detection
────────────────────────────────────────

📋 user-auth
  ✅  Task 1: Add login endpoint
  ⚠️   Task 2: Add password reset
      → Files changed (UserService.java) but no test changes found
  👻  Task 3: Add OAuth integration
      → No matching changes found for: OAuthService.java, OAuthConfig.java

────────────────────────────────────────
  ✅ 1 real  ⚠️  1 suspicious  👻 1 phantom

  ❌ 1 phantom task(s) detected — these need investigation.
```

| Verdict | Meaning |
|---------|---------|
| ✅ Real | Files changed, tests present |
| ⚠️ Suspicious | Files changed but no tests, or no files listed |
| 👻 Phantom | Marked done but no matching code changes found |

A single 👻 Phantom = exit code 1. The post-task hook blocks the commit automatically.

### 4. Custom Skills

Skills follow the open [Agent Skills](https://agentskills.io) standard. They are folders containing a `SKILL.md` file that Kiro activates when relevant to your task.

```
.kiro/skills/our-api-error-pattern/
└── SKILL.md
    ---
    name: our-api-error-pattern
    description: Standard error response format for all REST endpoints. Use when creating or modifying API controllers.
    ---

    All API errors must return: { "error": { "code": "...", "message": "..." } }
    Use @ControllerAdvice for global exception handling...
```

| Scope | Path | Priority |
|-------|------|----------|
| Project | `.kiro/skills/` | Higher (overrides user) — version-controlled with team |
| User | `~/.kiro/skills/` | Lower (fallback) — personal, across all projects |

**Manage skills:**
```bash
kirorails skill list                    # list all skills (project + user)
kirorails skill add "fix-auth"          # create new skill from template
kirorails skill search "migration"      # find skills matching keyword
```

**Auto-learn from completed work:**
```bash
kirorails learn                         # extract patterns from all verified specs
kirorails learn "user-auth"             # learn from specific spec
```

The learner agent analyzes specs with VERIFICATION PASS and extracts patterns that appeared in 2+ tasks. Quality gate ensures only actionable, specific patterns become skills.

Skills also appear as slash commands — type `/` in Kiro chat to see and activate them.

### 5. Executable Hooks

KiroRails installs both Kiro-native JSON hooks and bash scripts:

**Kiro-native hooks** (`.kiro/hooks/*.json`) — trigger automatically:

| Hook | Trigger | Action |
|------|---------|--------|
| Pre-Task Health Check | Pre Task Execution | Shell: `pre-task.sh` |
| Post-Task Verification | Post Task Execution | Shell: `post-task.sh && kirorails check-phantom` |
| Security Guardrails | File Save (migration, auth, model, config) | Ask Kiro |
| Spec Validator | File Save (.kiro/specs/**/*.md) | Ask Kiro |

**Bash scripts** (`.kiro/hooks-exec/`) — the actual build tool commands:

```bash
# .kiro/kirorails.conf — edit for your project
compile=./mvnw compile -q
test=./mvnw test -q
lint=./mvnw checkstyle:check -q
security=
```

The hooks read `kirorails.conf` so they work with any build tool — Maven, Gradle, npm, cargo, whatever.

### 6. Sprint & Backlog Management

For projects with many requirements, KiroRails organizes work into sprints using markdown files as the database:

```bash
kirorails sprint init                     # creates backlog.md
kirorails sprint new sprint-1-foundation  # creates sprint dir with tasks.md
kirorails sprint list                     # show all sprints + progress
```

Quick tasks skip the full planning flow:

```bash
kirorails quick "Add CRUD for Product entity"           # standalone quick task
kirorails quick "Fix date format" --sprint sprint-2     # add to existing sprint
```

---

## Deep Interview (Clarifier)

The clarifier uses Socratic questioning to eliminate ambiguity before planning. It scores clarity across weighted dimensions:

```
📊 Clarity Score: 45/100 (threshold: 70)
  Functional:      35/100 ████░░░░░░ ← needs work
  Technical:       60/100 ██████░░░░
  User Experience: 20/100 ██░░░░░░░░ ← needs work
  Data & State:    55/100 █████░░░░░
  Non-functional:  80/100 ████████░░ ✓
```

**Socratic techniques used:**
- **Assumption exposure** — "You said X, but this implies Y — is that correct?"
- **Edge case probing** — "What happens when [normal flow] fails?"
- **Contradiction surfacing** — "You want A and B, but they conflict when..."
- **Scale questioning** — "This works for 10 users. What changes at 10,000?"

Planning cannot begin until clarity reaches 70/100 (or user explicitly accepts defaults).

```bash
kirorails clarify "user authentication"
```

---

## Stack Blueprints

Pre-configured opinions for your stack. Composable — use multiple. Each uses Kiro's `fileMatch` inclusion so it only loads when you're working on relevant files:

| Blueprint | Focus | Activates for |
|-----------|-------|---------------|
| `java-legacy` | Safe refactoring, migration rules, legacy patterns | `*.java`, `pom.xml`, `build.gradle` |
| `spring-boot` | Spring Boot 3.x conventions, sliced tests, security config | `*.java`, `application*.yml` |
| `postgres` | Zero-downtime migrations, query optimization | `*.sql`, `migration*/**` |
| `python-fastapi` | Pydantic v2, async patterns, typed config | `*.py`, `pyproject.toml` |
| `compliance` | Audit trails, SOX/HIPAA/PCI-DSS/GDPR awareness | Manual inclusion |

```bash
kirorails init --pack spring-boot,postgres,compliance
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

## Installation Health Check

```bash
kirorails doctor
```

```
🩺 KiroRails Doctor

  ✅ .kiro/ directory exists
  ✅ kirorails.conf exists
  ✅ kirorails.conf has compile command
  ✅ kirorails.conf has test command
  ✅ agents/verifier.md
  ✅ agents/clarifier.md
  ✅ agents/analyzer.md
  ✅ agents/learner.md
  ✅ hooks-exec/pre-task.sh exists
  ✅ hooks-exec/pre-task.sh is executable
  ...

────────────────────────────────────────
  ✅ 20 passed  ⚠️  0 warnings  ❌ 0 failed
  🎉 Installation is healthy!
```

---

## What Gets Installed

```
.kiro/
├── steering/                    ← Expert Guardrails
│   ├── product.md               (always loaded)
│   ├── tech.md                  (always loaded)
│   ├── structure.md             (always loaded)
│   ├── coding-standards.md      (auto — feedback loops rule)
│   ├── testing.md               (auto — test standards)
│   ├── security.md              (auto — security rules)
│   ├── skills.md                (always — custom skills system)
│   └── brownfield-java.md       (fileMatch — your stack blueprint)
├── agents/                      ← Specialist Personas
│   ├── clarifier.md             Deep Interview — Socratic clarification
│   ├── analyzer.md              pre-implementation consistency check
│   ├── verifier.md              Truth Loop — verify everything
│   ├── learner.md               extract patterns into skills
│   └── bugfix-investigator.md   reproduce → root cause → fix
├── hooks/                       ← Kiro-Native Hooks (JSON)
│   ├── pre-task-health-check.json    Pre Task Execution → shell
│   ├── post-task-verification.json   Post Task Execution → shell + check-phantom
│   ├── security-guardrails.json      File Save → Ask Kiro
│   └── spec-validator.json           File Save → Ask Kiro
├── hooks-exec/                  ← Bash Scripts (called by hooks)
│   ├── pre-task.sh              check clean tree + compile
│   └── post-task.sh             compile + test + lint gate
├── skills/                      ← Custom Skills (Agent Skills standard)
│   └── _template/SKILL.md       skill template
├── state/                       ← Agent State (append-only)
│   ├── STATE.md                 session summaries
│   ├── CHANGELOG_AI.md          what changed and why
│   ├── DECISIONS.md             architectural decisions
│   └── RISKS.md                 known risks
├── kirorails.conf               ← hook config (edit for your build tool)
└── specs/
    └── feature/
        └── tasks.template.md    task breakdown template
```

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

Every iteration: health check → pick task → implement → test → commit → update state.

Features:
- **Rate limit detection** with exponential backoff (60s → 120s → 240s, max 600s)
- **Auto-retry** up to 5 consecutive rate limits before stopping
- **Skills loading** — matching skills auto-inject into each iteration
- **Progress tracking** via PROGRESS.md

⚠️ Experimental — test with HITL first.

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
│  3. IMPLEMENT      follow steering + skills  │
│     AI writes code guided by guardrails      │
│                    ↓                         │
│  4. VERIFY         post-task.sh              │
│     compile → test → lint → check-phantom    │
│                    ↓                         │
│  5. COMMIT         atomic, or fix and retry  │
│     Only if ALL checks pass                  │
└─────────────────────────────────────────────┘
```

- **Small steps** — one task = one commit. Never outrun your feedback loops.
- **Risk-first** — hard problems first, easy wins last. Risk scored 1-5 per task.
- **Feedback loops** — tests, types, lint after every task. Nothing committed if they fail.
- **The codebase wins** — existing patterns are respected. AI adapts to your code, not the other way around.
- **Learn and reuse** — patterns extracted from verified work become skills for future tasks.

The key insight: AI code quality degrades as context grows (context rot). By keeping each task small and verified, you get consistently high-quality output instead of a slow decline into hallucinations.

---

## CLI Reference

```
kirorails init [--pack NAME]                           Install KiroRails
kirorails doctor                                       Validate installation health
kirorails clarify [feature]                            Deep Interview — Socratic clarification
kirorails analyze [feature]                            Pre-implementation consistency check
kirorails verify                                       Trigger Truth Loop
kirorails check-phantom [spec] [--commits N]           Detect phantom completions (git diff)
kirorails learn [feature]                              Extract patterns into skills
kirorails skill list                                   List all skills (project + user)
kirorails skill add "<name>" [--user]                  Create new skill from template
kirorails skill search "<keyword>"                     Find skills matching keyword
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
| curl/bash installer | ✅ Tested |
| Expert Guardrails (steering files) | ✅ Tested |
| Custom Skills (auto-injection) | ✅ Tested |
| Sprint/Backlog management | ✅ Tested |
| Quick Tasks | ✅ Tested |
| Progress Dashboard | ✅ Tested |
| Installation Health Check (doctor) | ✅ Tested |
| Executable Hooks (bash) | ✅ Tested |
| Phantom Detection (`check-phantom`) | ✅ Tested |
| Specialist Personas (5 agents) | ✅ Tested |
| Deep Interview (Socratic clarifier) | 🔶 Tested in Kiro chat |
| Pre-implementation Analyzer | 🔶 Tested in Kiro chat |
| Truth Loop (verifier) | 🔶 Tested in Kiro chat |
| Skill Learning (pattern extraction) | 🔶 Tested in Kiro chat |
| Kiro-Native Hooks (JSON) | 🔶 Format validated |
| KiroRails Power | 🔶 Format validated |
| Ralph Loop (with rate limit handling) | ⚠️ Experimental |

---

## Roadmap

- [ ] Test all specialist personas in live Kiro environment
- [ ] Validate Kiro-native hooks in Kiro IDE
- [ ] Validate Ralph Loop with current kiro-cli release
- [ ] `kirorails scan` — auto-detect stack and configure steering files
- [ ] `kirorails sprint close` — close sprint, archive, generate retrospective
- [ ] First tagged release with compatibility declaration
- [ ] Notification callbacks (Telegram/Discord/Slack) for AFK mode
- [ ] Publish KiroRails Power to Kiro marketplace

---

## Contributing

Contributions welcome. Please open an issue first to discuss what you'd like to add.

## License

MIT — see [LICENSE](LICENSE).
