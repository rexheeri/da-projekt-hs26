# Data Analytics – Group Project HS 2026

ZHAW School of Management and Law · BSc Business Information Technology · Module Data Analytics (3DA), HS 2026

> **Status:** Concept phase. Topic and method assessed as suitable by the lecturer; formal approval at the concept presentation on 17.11.2026.

## Research question (draft)

Does the probability of a train delay of 3 minutes or more increase more strongly in regional traffic than in long-distance traffic when it rains or snows?

## Data sources (planned)

| Source | Access | Content |
|---|---|---|
| Ist-Daten (opentransportdata.swiss / opendata.swiss) | daily files via API, downloaded by script | actual vs. scheduled arrival/departure per stop |
| MeteoSwiss Open Data (STAC API) | Web API | precipitation, snow, temperature per weather station |
| Service point directory (Dienststellen) | download | stop coordinates for the spatial join |

Raw data is **not** committed (too large). Every script under `src/` must be able to rebuild `data/` from scratch.

## Repository structure

```
.claude/        shared Claude Code setup (agents, slash commands, permissions)
data/
  raw/          downloaded source files (git-ignored)
  processed/    cleaned / joined data, SQLite database (git-ignored)
docs/
  project-state.md     shared project state: roles, decisions, open questions, timeline
  grading.md           all grading criteria (presentation, final project, submission)
  research-design.md   research question, variables, hypotheses, tests, limitations
  workplan.md          roles, phases, dates, how we work
  concept-presentation.md  slide plan for 17.11.
  onboarding.md        checklist for new team members
  ai-log.md            log of AI usage (required for grading)
  integration-log.md   keys, joins, inconsistencies, records lost/gained (required for grading)
  claude/              how to use Claude in this project, prompts
notebooks/      Jupyter notebooks, one owner per notebook
tools/          create_issues.py: creates labels, milestones and issues on GitHub
src/            reusable Python code
  paths.py      project paths
  db.py         database access, SQLite or PostgreSQL (query, write_table, list_tables)
  check_setup.py
.env.example    template for .env (database URL, credentials)
docker-compose.yml   PostgreSQL (PostGIS) + pgAdmin
CLAUDE.md       rules for Claude (grading criteria, guardrails, repo rules)
```

## Setup

New in the team? Start with **[docs/onboarding.md](docs/onboarding.md)**.

Requires Python 3.10 or newer.

```bash
git clone https://github.com/rexheeri/da-projekt-hs26.git
cd da-projekt-hs26
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
pip install -r requirements.txt
python -m src.check_setup
```

In VS Code: select the interpreter from `.venv` (Ctrl+Shift+P → "Python: Select Interpreter").

### Database

The code works with SQLite and PostgreSQL alike (`src/db.py`, SQLAlchemy). Target for the submission is PostgreSQL.

- **SQLite (default, no setup):** nothing to do. The database is created at `data/processed/project.sqlite`.
- **PostgreSQL:** requires Docker Desktop (or a GitHub Codespace).
  ```bash
  copy .env.example .env        # macOS/Linux: cp .env.example .env
  # in .env: uncomment the DATABASE_URL line for PostgreSQL
  docker compose up -d
  python -m src.check_setup     # should report "Database works: postgresql"
  ```
  pgAdmin runs at http://localhost:5050.

## Working with Claude

The repo contains a shared Claude setup (`CLAUDE.md`, `.claude/`, `docs/claude/`) so that every team member's Claude knows the same rules, grading criteria and project state. Setup and usage: **[docs/claude/README.md](docs/claude/README.md)**.

## How we work together

1. **Pull before you start.** `git pull` every time you open the project.
2. **One notebook, one owner.** Notebooks merge badly in Git. Never edit someone else's notebook. Name them `NN_topic_initials.ipynb`, e.g. `02_eda_weather_er.ipynb`.
3. **Shared code goes into `src/`.** As soon as two notebooks need the same function, move it to `src/` and import it.
4. **Always comment your code.** Every file and function gets a docstring, every non-obvious step a comment saying what happens and why. Every notebook cell is preceded by a short markdown explanation. Uncommented code is not done.
5. **Clear outputs before committing** (Jupyter: "Clear All Outputs"). Keeps diffs small and avoids conflicts.
6. **Small commits with a clear message**, e.g. `Add MeteoSwiss STAC download for Zurich stations`.
7. **Never commit data, the database, `.env` or API keys.** `.gitignore` covers the usual paths – check `git status` before committing.
8. **Log AI usage immediately** in `docs/ai-log.md` – reconstructing it at the end does not work.

## Group

Group 3

| Name | GitHub | Role |
|---|---|---|
| Erion | [@rexheeri](https://github.com/rexheeri) | tbd |
| Lorenzo | [@desalce](https://github.com/desalce) | tbd |
| Levin | [@lvnkhn](https://github.com/lvnkhn) | tbd |

## Deliverables

| What | Due |
|---|---|
| Concept presentation (10 min, on site) | 17.11.2026 |
| Final project: video, materials (zip), presentation (pdf) | 10.01.2027, 23:59 |
