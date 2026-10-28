# Work plan

What we have to deliver, what we have to work out, and in which order.
Tasks are tracked as **GitHub issues** (milestones M1 and M2). This file
explains the big picture. Dates are planned values except 17.11. and 10.01.

## What is required, in one sentence each

1. **Concept presentation 17.11.** (20 % of the module grade): 10 min on site,
   8 criteria. We present the *plan*, backed by *real sample data*.
2. **Final project 10.01.** (20 %): collect data via API, integrate ≥ 2
   sources in a database, EDA, tests and classification answering our
   comparison question. Delivered as PDF + zip + 15-min video.
3. The **exam** (60 %) is individual. The weekly exercises are exam material.
   Don't let the project eat the exam preparation.

Details: [grading.md](grading.md) · Hypotheses: [research-design.md](research-design.md)
· Presentation: [concept-presentation.md](concept-presentation.md)

## Roles (assign in `project-state.md`)

| Role | Owns | Typical issues |
|---|---|---|
| **A: Timetable data & database** | Ist-Daten download script, DB schema, loading, PostgreSQL | API prototype, pipeline, schema, PostgreSQL |
| **B: Weather, geodata & EDA** | MeteoSwiss STAC script, stop↔station mapping, map, EDA | weather prototype, study period, join, EDA, map |
| **C: Methods & models** | variable definitions, hypothesis tests, classification, k-means | definitions, Chi²/z-test, correlation, models |

Cross-cutting, split evenly: slides, video (5 min each), AI log, README.

## Phase 1: until the concept presentation (M1, 17.11.)

Goal: a convincing concept with **real data structure** and first numbers.

| By | What | Who | Result |
|---|---|---|---|
| Fri 30.10. | Roles assigned, everyone onboarded | all | `project-state.md` filled in, `check_setup` OK for everyone |
| Wed 04.11. | **Data prototypes**: 1 day of Ist-Daten via API, 1 day of weather via STAC, stop list | A, B | sample in `data/raw`, columns and row counts noted in the integration log |
| Wed 04.11. | Study period chosen from weather data (snow days) | B | months fixed in `project-state.md` |
| Wed 04.11. | Variable definitions decided (DECIDE items in research-design) | C + all | `research-design.md` updated |
| Fri 06.11. | Prototype data in the DB, stop→station→hour join works | A, B | tables in DB, join documented in the integration log |
| Sun 08.11. | First EDA: data structure + delay rate per traffic type × weather (1–2 weeks of data) | B, C | figures for the slides |
| Thu 12.11. | Slides draft | all | PDF draft, each person their part |
| Sun 15.11. | **Dry run with stopwatch**, feedback with `presentation-coach` | all | ≤ 10:00, freely spoken |
| **Tue 17.11.** | **Concept presentation** 11:00, SW301 | all | upload PDF to Moodle afterwards |

## Phase 2: until submission (M2, 10.01.)

| By | What | Who |
|---|---|---|
| 22.11. | Feedback from the presentation into `project-state.md`, adjust plan | all |
| 29.11. | Full pipeline for the whole study period; switch to PostgreSQL | A |
| 06.12. | Complete EDA (tables + plots), map with stops and stations | B |
| 06.12. | Hypothesis tests H1–H3 with effect sizes and CIs | C |
| 13.12. | Classification with/without weather per traffic type, measures of fit | C |
| 13.12. | k-means (bonus), stats review with `stats-reviewer` | C, B |
| 14.–27.12. | Buffer: other module deadlines, holidays | – |
| 03.01. | Final PDF: Introduction, Materials & Methods, Results & Discussion, Conclusions, AI reflection, self-assessment appendix | all |
| 06.01. | Video recorded (15 min, 5 min each, no notebook scrolling) | all |
| 08.01. | `/check-grading`, zip, final review | all |
| **10.01.** | **Submission** (one person) | ER |

## How we work

- **Data first, slides second.** Every claim on a slide is backed by a query or a notebook.
- **Issues are the to-do list.** Assign yourself, link commits (`Fixes #12`), close when done.
- **Update `project-state.md` after each session** (`/session-end`). Otherwise
  the next person's Claude works with an outdated state.
- **Integration log and AI log right away**, not in January.
- **Weekly sync** (15 min, e.g. Sunday evening): what's done, what's blocked,
  next week. Decisions go into `project-state.md`.
- **Small steps:** one day of data → one week → full period. Never download
  months of data before a single day works end to end.
