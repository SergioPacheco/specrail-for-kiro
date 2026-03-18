# specrail-for-kiro

Delivery kit for [Kiro](https://kiro.dev): opinionated steering, subagents, and hooks for structured software delivery.

> Steering tells Kiro your standards. Subagents teach it delivery workflows. Hooks enforce quality gates. SpecRail bundles all three.

---

## What it is

SpecRail is a community toolkit that adds delivery discipline to Kiro projects. It provides:

- **Steering files** — project standards (tech stack, coding rules, testing strategy, security) with Kiro inclusion modes (`always`, `auto`, `manual`)
- **Subagents** — Markdown playbooks with YAML frontmatter that Kiro loads on demand (planner, verifier, bugfix investigator, etc.)
- **Hooks** — automated quality gates on spec creation, task execution, and file saves
- **Spec templates** — structured requirements, design, and task breakdowns
- **Pack overlays** — stack-specific opinions (Java legacy, Spring Boot, PostgreSQL, FastAPI, compliance)

Built on [Ralph principles](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum): small steps, feedback loops, progress tracking, risk-first execution.

## Quick start

```bash
git clone https://github.com/SergioPacheco/specrail-for-kiro.git

cd your-project
python path/to/specrail-for-kiro/scripts/bootstrap.py --pack java-legacy
```

This installs 7 files (lite mode):

```
.kiro/
├── steering/
│   ├── product.md            ← your product context (always included)
│   ├── tech.md               ← your tech stack (always included)
│   ├── structure.md          ← your project layout (always included)
│   └── brownfield-java.md    ← Java legacy overlay (auto)
├── agents/
│   ├── planner.md            ← plan features into small tasks
│   └── verifier.md           ← verify delivery meets criteria
└── specs/
    └── feature/
        └── tasks.template.md ← task breakdown template
```

Then tell Kiro: *"Plan the order email notification feature"* — the planner subagent takes over.

## Install modes

| Mode | What you get | Files | Command |
|------|-------------|-------|---------|
| **lite** (default) | 3 core steering + pack overlay + 2 agents + tasks template | ~7 | `--pack java-legacy` |
| **full** | 6 steering + shared (mcp, team) + pack overlay + 6 agents + hooks + state + specs | ~35 | `--pack java-legacy --mode full` |
| **add** | Add a pack overlay to existing install | +1-2 | `--pack postgres --mode add` |

Combine packs: `--pack spring-boot,postgres,compliance --mode full`

List available packs: `bootstrap.py --list`

## How it works

```
1. Bootstrap          → steering + agents into .kiro/
2. Customize steering → fill in your product, tech, structure
3. Plan a feature     → planner subagent creates tasks.md
4. Execute tasks      → one task at a time, feedback loops after each
5. Verify             → verifier checks criteria, saves VERIFICATION.md
6. Archive            → move completed spec to specs/archive/
```

### Execution modes

| Mode | How | Best for |
|------|-----|----------|
| **HITL** | Run one task, watch, intervene | Risky tasks, learning, architectural decisions |
| **AFK** | Ralph loop runs tasks autonomously | Well-defined tasks, bulk implementation |

### Ralph loop (experimental)

```bash
./scripts/specrail-ralph.sh order-email-notification 5
```

⚠️ Experimental. Uses `kiro-cli chat --no-interactive`. Test with HITL first.

## Subagents

All subagents have YAML frontmatter (`name`, `description`, `tools`, `model`) compatible with Kiro custom subagents.

| Agent | Mode | Purpose |
|-------|------|---------|
| **planner** | lite | Break features into small, risk-scored tasks with done criteria |
| **verifier** | lite | Check delivery against criteria, save VERIFICATION.md |
| **bugfix-investigator** | full | Reproduce → root cause → fix (never skip steps) |
| **codebase-mapper** | full | Analyze brownfield codebase, produce structural map |
| **quick-change** | full | Small changes without full planner flow |
| **report-generator** | full | Delivery summaries from state files |

## Hooks

| Hook | Trigger | Mode |
|------|---------|------|
| **on-spec-created** | Spec creation | full |
| **pre-task-quality** | Before task | full |
| **post-task-verification** | After task | full |
| **on-file-save-guardrails** | File save | full |
| **session-summary** | End of session | full |
| **decision-tracker** | After decisions | full |

## Packs

| Pack | Overlay file | Focus |
|------|-------------|-------|
| `java-legacy` | `brownfield-java.md` | Safe refactoring, migration rules, legacy patterns |
| `spring-boot` | `spring-boot.md` | Spring Boot 3.x conventions, sliced tests, security config |
| `postgres` | `postgres.md` | Zero-downtime migrations, query optimization, operational rules |
| `python-fastapi` | `fastapi.md` | Pydantic v2, async patterns, typed config |
| `compliance` | `compliance.md` + `regulatory.md` | Audit trails, SOX/HIPAA/PCI-DSS/GDPR awareness |

Packs are composable. Use `spring-boot,postgres` for a Spring Boot app with heavy database work, or add `compliance` for enterprise audit requirements.

## Steering inclusion modes

SpecRail uses Kiro's inclusion modes to control context consumption:

| File | Mode | When loaded |
|------|------|-------------|
| product.md, tech.md, structure.md | `always` | Every interaction |
| coding-standards.md, testing.md, security.md | `auto` | When Kiro determines relevance |
| Pack overlays (brownfield-java.md, etc.) | `auto` | When working with that stack |
| mcp.md, team.md | `manual` | Only when explicitly requested |
| compliance.md, regulatory.md | `manual` | Only for regulated projects |

## What is tested vs conceptual

| Component | Status |
|-----------|--------|
| Bootstrap script (lite, full, add, pack composition) | ✅ Tested |
| Steering files (content, frontmatter, inclusion modes) | ✅ Tested |
| Subagent frontmatter (name, description, tools, model) | ✅ Tested |
| Planner and verifier workflows | 🔶 Tested in Kiro chat, not automated |
| Ralph loop (`specrail-ralph.sh`) | ⚠️ Experimental — CLI flags may change |
| Hooks | 🔶 Format validated, not tested in live Kiro hooks system |
| MCP integration | 📋 Conceptual — steering guide only |

## Core principles

Adapted from [Ralph Wiggum methodology](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum):

- **Small steps** — one task = one commit. Never outrun your feedback loops.
- **Feedback loops** — tests, types, lint after every task. Nothing committed if they fail.
- **Progress tracking** — PROGRESS.md per spec, STATE.md across sessions.
- **Risk-first** — hard problems first, easy wins last. Planner scores risk 1-5 per task.
- **Explicit quality** — steering tells the AI this is production code. The codebase wins.
- **HITL → AFK** — start supervised, go autonomous once you trust the prompt.

## Example

See [docs/examples/java-legacy.md](docs/examples/java-legacy.md) for a complete walkthrough.

## Roadmap

### v0.1 — Foundation ✅
Core steering, subagents, hooks, spec templates, Ralph loop, health checks, example walkthrough.

### v0.2 — Automation ✅
Session summary hook, decision tracker, Spring Boot/PostgreSQL/FastAPI packs, release checklist, verification reports.

### v0.3 — Team & Integration ✅
MCP integration, report generator, team mode, compliance pack, risk scoring, pack composition.

### Next
- [ ] Test all subagents in live Kiro environment
- [ ] Validate hooks in Kiro hooks system
- [ ] Validate Ralph loop with current kiro-cli release
- [ ] First tagged release with compatibility declaration
- [ ] Explore Kiro Powers format (POWER.md + dynamic activation)

## Contributing

Contributions welcome. Please open an issue first to discuss what you'd like to add.

## License

MIT — see [LICENSE](LICENSE).
