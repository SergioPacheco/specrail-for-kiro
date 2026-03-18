# Vision

## SpecRail for Kiro

SpecRail is a community-driven delivery toolkit built on top of Kiro's native primitives.

### Problem

AI-assisted development tools are powerful but undisciplined. The industry keeps building separate agents for each function — one for code review, another for testing, another for migrations. This doesn't scale, fragments context, and turns AI into a brilliant generalist that lacks the specific expertise real workflows demand.

In brownfield and enterprise projects, teams face:

- **Context loss** — decisions made in one session are forgotten in the next
- **Drift** — implementation diverges from requirements without anyone noticing
- **Missing gates** — no systematic verification before marking work as done
- **Stack blindness** — generic AI advice that ignores legacy constraints, migration risks, and database safety

### Thesis

The answer isn't more agents. It's better skills.

A skill is a Markdown file that works as a playbook — it teaches the AI exactly how to execute a specific task, which steps to follow, and what to avoid. Instead of building separate bots, you document expertise in files that a universal AI can learn and apply on demand.

Kiro already provides the right building blocks: specs, steering, hooks, and agents. What's missing is an opinionated library of delivery skills that connects these blocks into a disciplined workflow — especially for teams working on real, messy, production systems.

### Approach

SpecRail doesn't replace Kiro. It configures Kiro for structured delivery by providing:

1. **Steering packs** — stack-specific coding standards and project rules (the "context skills")
2. **Spec templates** — structured requirements, design, and task breakdowns
3. **Agents as skills** — planner, verifier, and bugfix investigator with built-in quality gates. Each agent is a Markdown playbook that Kiro loads on demand — not a separate bot
4. **Hooks** — automated checks at key moments in the delivery flow
5. **State files** — persistent operational memory across sessions

The key design: Kiro doesn't load everything at once. It sees a list of available skills and only reads the full playbook when it decides that skill is needed for the current task. This is progressive disclosure — it keeps the AI focused and avoids context overload.

### Skills + MCP

SpecRail skills work alongside MCP (Model Context Protocol) servers:

- **MCP is the hand** — it connects Kiro to external tools and data (APIs, databases, CI pipelines)
- **Skills are the experience** — they tell Kiro what to do with the data and tools MCP provides

When MCP integration arrives (v0.3), SpecRail skills will orchestrate MCP tools with delivery discipline built in.

### No-code by design

You don't need to be a developer to create or customize a skill. Every agent, steering file, and hook in SpecRail is plain Markdown. Team leads, architects, DBAs, or QA engineers can write delivery rules in natural language. The AI reads and follows them.

This makes SpecRail accessible to the whole team, not just the developers.

### Target audience

- Teams working on brownfield / legacy systems
- Enterprise projects with compliance or governance needs
- Developers using Kiro who want more structure without more overhead
- Non-developers (architects, leads, QA) who want to encode team standards into AI behavior

### Design principles

- **Kiro-native** — uses specs, steering, hooks, and agents as they were designed
- **Skills over agents** — document expertise in Markdown, don't build separate bots
- **Opinionated but swappable** — strong defaults, easy to override
- **Brownfield-first** — assumes existing code, existing databases, existing constraints
- **Minimal bootstrap** — one command to install, one pack to choose
- **State over chat** — important decisions persist in files, not in conversation history
- **No-code accessible** — anyone on the team can read, write, and customize skills

### Non-goals

- Building another IDE or editor plugin
- Replacing Kiro's spec engine
- Creating a universal framework for all AI tools
- Building separate agents/bots for each function
- Supporting non-Kiro workflows
