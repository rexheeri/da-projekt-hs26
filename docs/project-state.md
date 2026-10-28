# Project state

Shared team memory. Keep it short and current. Claude reads this file in every
session. Anything not written here is unknown in the next session.

**Last updated:** 2026-10-28 (ER)

## Group

| GitHub | Initials | Main responsibility |
|---|---|---|
| rexheeri | ER | tbd |
| desalce | tbd | tbd |
| lvnkhn | tbd | tbd |

Planned split of responsibilities (not yet assigned to people):
1. Timetable data (Ist-Daten) + database (SQLite / PostgreSQL)
2. Weather data + geodata + EDA
3. Models + statistical tests

Cross-cutting, each person takes a share: GitHub, AI log, slides, video.

## Topic (draft – not yet approved)

- **Working title:** Public transport delays and weather
- **Research question:** Does the probability of a delay ≥ 3 min increase more
  strongly in regional traffic than in long-distance traffic when it rains or
  snows?
- **Scope:** Greater Zurich area, several winter months (snow days needed).
  Exact months depend on how far back the archives go.
- **Approval:** formally at the concept presentation. Email with the topic sent
  to Gellrich on 2026-10-13. Reply: **open, please fill in**.

## Data (plan)

| Source | Access | Status |
|---|---|---|
| opentransportdata.swiss – Ist-Daten (daily files) | download by script | not started / tbd |
| MeteoSwiss Open Data – STAC API | Web API | not started / tbd |
| Service point directory (stop coordinates) | download | not started / tbd |

Join: stop → nearest weather station (coordinates) + timestamp. Storage in
SQLite, queries via SQL from Python.

## Methods (plan)

EDA · Chi² per traffic type · effect comparison (delay rate with vs. without
precipitation per traffic type) · Classification Tree + Random Forest per
traffic type · Confusion Matrix, Recall, ROC-AUC · map (geodata) · k-means on
stops.

Bonus points: aim for all six. PostgreSQL is the first to drop if time runs short.

## Timeline

Fixed: **17.11.2026** concept presentation · **10.01.2027, 23:59** submission.
Everything else is a planned value.

| By | What | Done |
|---|---|---|
| 06.11. | Pipeline: first real data in SQLite, join tested | ☐ |
| 08.11. | First EDA | ☐ |
| 15.11. | Slides done, dry run with stopwatch | ☐ |
| 17.11. | **Concept presentation**, upload PDF to Moodle afterwards | ☐ |
| 13.12. | Model, tests, map | ☐ |
| 14.–27.12. | Buffer (other module deadlines, holidays) | – |
| 28.12.–08.01. | Report PDF, self-assessment appendix, video | ☐ |
| 10.01. | **Submission** with buffer | ☐ |

## Open questions for the lecturer

| Question | Asked | Answer |
|---|---|---|
| Does downloading the Ist-Daten daily files count as own data collection? | 13.10. | open |
| Does PostgreSQL replace the SQLite requirement or come on top? | 13.10. | open |
| Is the maximum 16 or 22 points, and how are points converted to a grade? | 13.10. | open |

## Decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-10-28 | Repo public from day one | bonus point; raw data and keys are never committed |
| 2026-10-28 | One notebook = one owner; shared code in `src/` | notebooks cannot be merged reliably |
| 2026-10-28 | Code, docs and deliverables in English | language of instruction and assessment |

## Change log

- 2026-10-28 ER: repo, Claude configuration and team rules created
