# AI usage log

Required for grading: document AI usage **for the code and for the presentation**
(slides, texts, charts): which tool, for which task, advantages, disadvantages,
and where something did not work. It must also appear in the slides **and** the video.
Add an entry **when it happens**, not at the end of the project.

| Date | Who | Tool | Task | Result | What went wrong / what we had to fix |
|---|---|---|---|---|---|
| 2026-10-28 | ER | Claude | Repository structure, README, .gitignore, SQLite helpers | used | – |
| 2026-10-28 | ER | Claude | Shared Claude setup: CLAUDE.md, agents, slash commands, prompt library | used | Review found that the planned models per traffic type don't answer the comparison question → direct effect comparison added as guardrail |
| 2026-10-28 | ER | Claude | Database layer for SQLite + PostgreSQL, docker-compose from course template | used | URL from course template fails with SQLAlchemy ≥ 2.1 (defaults to psycopg 3) → driver pinned in `src/db.py`; found by testing against a real PostgreSQL server |
| 2026-10-28 | ER | Claude | Draft of grading overview, research design (hypotheses), work plan, slide plan, issue list | partly used | Drafts only; DECIDE items (threshold, traffic type mapping, precipitation categories) still need a team decision; data assumptions marked VERIFY |

| 2026-11-03 | ER | Claude Code | Phase 1 data collection: explore Ist-Daten portal/archive, MeteoSwiss STAC, service points; prototype scripts `src/download.py`, `src/istdaten.py`, `src/weather.py`, `src/stops.py`; VERIFY of columns, time zones, parameter codes | used, numbers checked on real files | Brief assumed a CKAN API for the current month: the action API returns 403, so file lists come from the DCAT catalogue instead. First read of Ist-Daten with the wrong encoding (cp1252 instead of UTF-8) crashed and was fixed. Cookbook example (comma, `_id` column) did not match the real files. Time zone of Ist-Daten not documented; Claude proposed a DST test instead of assuming |
| 2026-11-03 | ER | Claude Code | Phase 2 prototype: precipitation network, `stop_station`, downloader with retries/ETag, schema, `src/arrivals.py`, SQL join to `analysis_base`, DST and weather completeness tests, ER diagram, first EDA notebook and figures | used; 5 rows checked by hand against raw files | Claude claimed the checklist's key-facts table contained Q&A rows; wrong (it had read two concatenated outputs), corrected by ER. Brief asked for `delay_gain` "known before arrival", which is contradictory (it contains the arrival delay) → split into predictors (`prev_dep_delay_min`, `entry_delay_min`) and an outcome (`delay_gain_min`). Build log CSV was malformed (different columns per step) → long format. Wrong date (04.11.) written into the integration log → fixed. First ER diagram had arrows over the text → redrawn. Weekend night S-Bahn (`SN`) silently fell out of the filter → found in the counts, decision pending |
| 2026-11-03 | ER | Claude Code | Research for decisions: SBB 3-min source, MeteoSwiss download docs, MeteoSwiss GitHub, data collections A–D, ZH school holidays | partly used | Official ZH school-holiday dates for 2023/24 and 2024/25 not found online; Sportferien are set per municipality, so the decided "school holidays canton ZH" variable cannot be built as one flag |

## Summary for the final presentation

*Fill in at the end, based on the table above.*

- **Advantages:**
- **Disadvantages:**
- **Where it failed:**
