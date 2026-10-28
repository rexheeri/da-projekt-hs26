# Using Claude in this project

Everything Claude needs is in the repo. Every team member gets the same rules,
the same project state and the same tools, whether you use **Claude Code** or a
**claude.ai Project**.

| File | Purpose |
|---|---|
| `CLAUDE.md` | Rules: grading criteria, methodological guardrails, repo rules. Loaded automatically by Claude Code. |
| `docs/project-state.md` | Shared memory: roles, decisions, open questions, timeline. **Update it** (`/session-end`). |
| `.claude/agents/` | Specialised sub-agents (grading check, stats review, data pipeline, presentation coach) |
| `.claude/commands/` | Slash commands (`/status`, `/ai-log`, `/explain`, …) |
| `.claude/settings.json` | Shared permissions (e.g. never read `.env`, no force push) |
| `docs/claude/project-instructions.md` | Copy-paste instructions for a claude.ai Project |
| `docs/claude/prompts.md` | Prompt library for recurring tasks |
| `CLAUDE.local.md` | *Your* personal preferences (git-ignored, create it yourself) |

## Option A — Claude Code (recommended)

1. Clone the repo and open the folder in VS Code.
2. Install the **Claude Code** extension (or use `claude` in the terminal).
3. Start Claude Code **in the repo root**. `CLAUDE.md` and
   `docs/project-state.md` are loaded automatically, agents and commands are
   available.
4. Try: `/status`

Agents are called by Claude when they fit, or explicitly: *"Use the
stats-reviewer agent on notebooks/04_model_ab.ipynb"*.

## Option B — claude.ai Project

1. Create a new Project on claude.ai, e.g. "DA Project HS26".
2. Paste the content of `docs/claude/project-instructions.md` into the project
   instructions.
3. Upload these files to the project knowledge: `CLAUDE.md`,
   `docs/project-state.md`, `docs/ai-log.md`, `docs/integration-log.md`.
4. **Important:** The project knowledge is a copy. After each `git pull`,
   re-upload `docs/project-state.md`, otherwise Claude works with an outdated state.
5. Prompts from `docs/claude/prompts.md` replace the slash commands.

## Your own preferences

Create `CLAUDE.local.md` in the repo root (it is git-ignored), for example:

```markdown
- Answer me in German, Swiss spelling.
- I am responsible for the weather data and EDA. My initials are AB.
- I am new to geopandas, explain more there.
```

## Team rules for Claude use

- **Log AI usage right away** (`/ai-log`). It is graded, and it can't be reconstructed at the end.
- **Only commit what you understand.** You must explain your part freely in the video.
- **Update `docs/project-state.md`** when something was decided or changed (`/session-end`). If it isn't written there, your teammates' Claude doesn't know it.
