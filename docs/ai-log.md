# AI usage log

Required for grading: document where AI was used, what worked, what didn't and where it failed.
Add an entry **when it happens**, not at the end of the project.

| Date | Who | Tool | Task | Result | What went wrong / what we had to fix |
|---|---|---|---|---|---|
| 2026-10-28 | ER | Claude | Repository structure, README, .gitignore, SQLite helpers | used | – |
| 2026-10-28 | ER | Claude | Shared Claude setup: CLAUDE.md, agents, slash commands, prompt library | used | Review found that the planned models per traffic type don't answer the comparison question → direct effect comparison added as guardrail |
| 2026-10-28 | ER | Claude | Database layer for SQLite + PostgreSQL, docker-compose from course template | used | URL from course template fails with SQLAlchemy ≥ 2.1 (defaults to psycopg 3) → driver pinned in `src/db.py`; found by testing against a real PostgreSQL server |
| 2026-10-28 | ER | Claude | Draft of grading overview, research design (hypotheses), work plan, slide plan, issue list | partly used | Drafts only; DECIDE items (threshold, traffic type mapping, precipitation categories) still need a team decision; data assumptions marked VERIFY |

## Summary for the final presentation

*Fill in at the end, based on the table above.*

- **Advantages:**
- **Disadvantages:**
- **Where it failed:**
