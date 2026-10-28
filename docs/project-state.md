# Project state

Shared team memory. Keep it short and current. Claude reads this file in every
session. Anything not written here is unknown in the next session.

**Last updated:** 2026-10-28 (ER)

## Group

| Name | GitHub | Initials | Main responsibility |
|---|---|---|---|
| Erion | rexheeri | ER | tbd |
| Lorenzo | tbd | tbd | tbd |
| Levin | tbd | tbd | tbd |

GitHub invitations sent to `desalce` and `lvnkhn`. Please fill in your own row.

Planned split of responsibilities (not yet assigned to people):
1. Timetable data (Ist-Daten via API) + database (PostgreSQL)
2. Weather data + geodata + EDA
3. Models + statistical tests

Cross-cutting, each person takes a share: GitHub, AI log, slides, video.

## Topic

- **Working title:** Weather and punctuality in Swiss public transport
- **Research question:** Does the probability of a delay ≥ 3 min increase more
  strongly in regional traffic than in long-distance traffic when it rains or
  snows?
- **Scope:** Greater Zurich area, several winter months (snow days needed).
  Exact months depend on how far back the archives go.
- **Lecturer feedback (Gellrich, reply to email of 2026-10-13):** topic and
  data "exciting and suitable", classification "suitable". Formal approval
  follows at the concept presentation on 17.11.

## Data (plan)

| Source | Access | Status |
|---|---|---|
| Ist-Daten (daily files) | **API, by script** (confirmed as own data collection) | not started |
| MeteoSwiss Open Data – STAC API | Web API | not started |
| Service point directory (stop coordinates) | download / API | not started |

Join: stop → nearest weather station (coordinates) + timestamp. Storage in
PostgreSQL (SQLite as fallback, same code via `src/db.py`).

## Methods (plan)

EDA · Chi² per traffic type · effect comparison (delay rate with vs. without
precipitation per traffic type) · Classification Tree + Random Forest per
traffic type · Confusion Matrix, Recall, ROC-AUC · map (geodata) · k-means on
stops.

Bonus points: aim for all six.

## Timeline

Fixed: **17.11.2026** concept presentation · **10.01.2027, 23:59** submission.
Everything else is a planned value.

| By | What | Done |
|---|---|---|
| 06.11. | Pipeline: first real data in the database, join tested | ☐ |
| 08.11. | First EDA | ☐ |
| 15.11. | Slides done, dry run with stopwatch | ☐ |
| 17.11. | **Concept presentation**, upload PDF to Moodle afterwards | ☐ |
| 13.12. | Model, tests, map | ☐ |
| 14.–27.12. | Buffer (other module deadlines, holidays) | – |
| 28.12.–08.01. | Report PDF, self-assessment appendix, video | ☐ |
| 10.01. | **Submission** with buffer | ☐ |

## Questions for the lecturer

| Question | Answer (Gellrich) |
|---|---|
| Does downloading the Ist-Daten daily files by script count as own data collection? | **Yes**, it's an API. |
| Does PostgreSQL replace the SQLite requirement? | **Yes**, PostgreSQL replaces SQLite (and earns the bonus point). |
| Max. 16 or 22 points? Conversion to grade? | **22 points** (9 + 6 + 7). Grade conversion after all projects are assessed, i.e. relative. |
| Where did we see "16 points"? | He asks us to tell him. **Open, ER replies.** |

## Decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-10-28 | Repo public from day one | bonus point; raw data and keys are never committed |
| 2026-10-28 | One notebook = one owner; shared code in `src/` | notebooks cannot be merged reliably |
| 2026-10-28 | Code, docs and deliverables in English | language of instruction and assessment |
| 2026-10-28 | Target database PostgreSQL (PostGIS image), SQLite as fallback, same code via SQLAlchemy | PostgreSQL replaces SQLite and earns a bonus point; fallback keeps us working if Docker causes trouble before 17.11. |
| 2026-10-28 | Ist-Daten only via scripted API download | condition for counting as own data collection |

## Change log

- 2026-10-28 ER: repo, Claude configuration and team rules created
- 2026-10-28 ER: lecturer's answers added; database layer switched to SQLAlchemy (SQLite/PostgreSQL), docker-compose added
