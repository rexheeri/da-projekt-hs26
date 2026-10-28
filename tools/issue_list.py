"""Labels, milestones and issues for the project. Used by tools/create_issues.py.

Edit here, then run the script again. Existing issues (same title) are skipped.
"""

M1 = "M1 Concept presentation (17.11.)"
M2 = "M2 Final submission (10.01.)"

MILESTONES = [
    {"title": M1, "due_on": "2026-11-17T10:00:00Z",
     "description": "Concept presentation, Tue 17.11.2026, 11:00, SW301. See docs/concept-presentation.md"},
    {"title": M2, "due_on": "2027-01-10T22:59:00Z",
     "description": "Final submission on Moodle, 10.01.2027, 23:59. See docs/grading.md"},
]

LABELS = [
    ("setup", "bfd4f2", "Onboarding, tools, environment"),
    ("data", "1d76db", "Data collection and cleaning"),
    ("database", "5319e7", "SQLite / PostgreSQL"),
    ("geo", "0e8a16", "Geodata and maps"),
    ("analysis", "fbca04", "EDA, tests, models"),
    ("presentation", "d93f0b", "Slides, video, report"),
    ("docs", "c5def5", "Documentation, logs"),
    ("admin", "ededed", "Organisation, Moodle, lecturer"),
    ("bonus", "f9d0c4", "Earns bonus points"),
]

ONBOARDING = """Work through [docs/onboarding.md](../blob/main/docs/onboarding.md) and tick here:

- [ ] GitHub invitation accepted, GitHub name ↔ real name told to the group
- [ ] Git, Python ≥ 3.10, VS Code (+ Python/Jupyter extensions) installed
- [ ] Repo cloned, `.venv` created, `pip install -r requirements.txt`
- [ ] `python -m src.check_setup` → **Setup OK**
- [ ] Read: README, project-state, grading, research-design, workplan, concept-presentation
- [ ] `CLAUDE.local.md` created, `/status` tried (or claude.ai Project set up)
- [ ] Own row in `docs/project-state.md` filled in, committed and pushed
- [ ] 17.11. morning taken off work, dry run 15.11. in calendar
- [ ] Assigned to first issues of own role
"""

ISSUES = [
    # ---------------- M1: concept presentation ----------------
    {"title": "Onboarding: Lorenzo", "labels": ["setup"], "milestone": M1, "body": ONBOARDING},
    {"title": "Onboarding: Levin", "labels": ["setup"], "milestone": M1, "body": ONBOARDING},
    {"title": "Assign roles A/B/C and fill in project-state", "labels": ["admin"], "milestone": M1,
     "body": """Roles are described in [docs/workplan.md](../blob/main/docs/workplan.md#roles-assign-in-project-statemd).

- [ ] Role A (timetable data & database): ___
- [ ] Role B (weather, geodata & EDA): ___
- [ ] Role C (methods & models): ___
- [ ] Speaker split for 17.11. agreed (slides 1–4 / 5–8 / 9–12)
- [ ] Weekly sync slot agreed
- [ ] Everything written into `docs/project-state.md`

Target: Fri 30.10."""},
    {"title": "Reply to lecturer: where Moodle shows \"max. 16 points\"", "labels": ["admin"], "milestone": M1,
     "body": """Gellrich asked where we saw "max. 16 points".

- [ ] Find the spot on Moodle, take a screenshot
- [ ] Also mention the submission slot "Due: 11 January 2026" vs. title "10.01.2027"
- [ ] Send reply, note it in `docs/project-state.md`"""},
    {"title": "Weather: find rain/snow days in Zurich and choose the study period", "labels": ["data"], "milestone": M1,
     "body": """Weather first, then the timetable data: we need months with enough snow days.

- [ ] MeteoSwiss Open Data STAC API: find the collection for the automatic weather stations (SMN) and the Zurich-area stations
- [ ] Daily precipitation sum, temperature, fresh snow for candidate winters
- [ ] Count dry / rain / snow days per month
- [ ] Check how far back the Ist-Daten archive goes
- [ ] Propose study period (months) → `docs/project-state.md`
- [ ] Integration log: source entry

Target: Wed 04.11. · Role B"""},
    {"title": "Ist-Daten: API download prototype for one day", "labels": ["data"], "milestone": M1,
     "body": """Must be **scripted via the API** (lecturer: counts as own data collection; manual downloads don't).

- [ ] Find the API endpoint for the daily Ist-Daten files
- [ ] `src/` script: download one day into `data/raw/` (skip if already there)
- [ ] Filter early: Greater Zurich stops, trains only, relevant columns
- [ ] Note real columns, data types, row counts (raw and filtered)
- [ ] VERIFY assumptions in `docs/research-design.md`: arrival status column ("REAL"), cancellation flag, train category column
- [ ] Integration log: source entry · AI log entry

Target: Wed 04.11. · Role A"""},
    {"title": "Weather: STAC API prototype for one day (Zurich stations)", "labels": ["data"], "milestone": M1,
     "body": """- [ ] `src/` script: 10-min (or hourly) precipitation and temperature for the Zurich-area stations, one day
- [ ] Station metadata with coordinates
- [ ] Aggregate to hourly values per station
- [ ] Note columns, units, row counts
- [ ] Integration log: source entry

Target: Wed 04.11. · Role B"""},
    {"title": "Stops: coordinates and nearest weather station", "labels": ["data", "geo"], "milestone": M1,
     "body": """- [ ] Service point directory (stop coordinates) by script
- [ ] Nearest weather station per stop (distance in km, e.g. with geopandas)
- [ ] Check: maximum and median distance, flag stops > 10 km away
- [ ] Table `stop_station` in the DB
- [ ] Integration log: join entry (stops matched / unmatched)

Target: Fri 06.11. · Role B"""},
    {"title": "Decide variable definitions (DECIDE items in research-design)", "labels": ["analysis"], "milestone": M1,
     "body": """Decide as a team, document reasons in `docs/research-design.md` and `project-state.md`.

- [ ] Delay threshold 3 min, with source for the SBB definition
- [ ] Traffic type mapping (where does IR go?)
- [ ] Precipitation categories dry / rain / snow (thresholds)
- [ ] Cancelled trains and non-measured times: exclude?
- [ ] Primary effect measure: absolute (percentage points) or relative
- [ ] Study period (from the weather issue)

Target: Wed 04.11. · Role C + all"""},
    {"title": "Database schema and loading of prototype data", "labels": ["database"], "milestone": M1,
     "body": """- [ ] Tables: `arrivals`, `weather_hourly`, `stops`, `stop_station` (proposal)
- [ ] Load prototype data via `src/db.py` (SQLite for now)
- [ ] Portable SQL only (works on PostgreSQL later)
- [ ] `list_tables()` output for the slide "data structure"
- [ ] Simple ER diagram for the slides

Target: Fri 06.11. · Role A"""},
    {"title": "Join arrivals → stop → nearest station → hour", "labels": ["data", "database"], "milestone": M1,
     "body": """- [ ] SQL join (or pandas + write back) arrivals × stop_station × weather_hourly
- [ ] Rows before/after, lost records and reasons → `docs/integration-log.md`
- [ ] Spot check 5 rows by hand
- [ ] View/table `analysis_base` with all variables from research-design

Target: Fri 06.11. · Role A + B"""},
    {"title": "First EDA for the presentation", "labels": ["analysis"], "milestone": M1,
     "body": """With 1–2 weeks of data, clearly labelled as preliminary.

- [ ] Data structure overview: rows, columns, types, missing values
- [ ] Delay rate per traffic type × dry/rain/snow (table + bar chart)
- [ ] Distribution of arrival delays (histogram, per traffic type)
- [ ] Charts in slide quality (title = finding, axes, n, source)

Target: Sun 08.11. · Role B + C"""},
    {"title": "Concept presentation slides", "labels": ["presentation"], "milestone": M1,
     "body": """Follow [docs/concept-presentation.md](../blob/main/docs/concept-presentation.md).

- [ ] Slides 1–4 (title, outline, background, problem)
- [ ] Slides 5–8 (RQ, hypotheses, data sources, data structure)
- [ ] Slides 9–12 (methods, first look, expected results, next steps + GitHub URL)
- [ ] Sources on slides, consistent colours, slide numbers
- [ ] Review with the `presentation-coach` agent
- [ ] Export PDF

Target: Thu 12.11. · all"""},
    {"title": "Dry run with stopwatch", "labels": ["presentation"], "milestone": M1,
     "body": """- [ ] All three, freely spoken, no reading
- [ ] Total ≤ 10:00 (target 9:30–9:50), time per person noted
- [ ] Practise likely questions (see concept-presentation.md)
- [ ] Fix slides after the dry run

Target: Sun 15.11. · all"""},
    {"title": "After the presentation: upload PDF to Moodle, record feedback", "labels": ["admin"], "milestone": M1,
     "body": """- [ ] Upload slide PDF to Moodle
- [ ] Write lecturer's feedback and questions into `docs/project-state.md`
- [ ] Adjust plan/issues for M2

Target: Tue 17.11."""},

    # ---------------- M2: final submission ----------------
    {"title": "Full pipeline for the whole study period", "labels": ["data", "database"], "milestone": M2,
     "body": """- [ ] Download all days of the study period (idempotent, resumable)
- [ ] Load into the DB, join, `analysis_base`
- [ ] Rebuild from a fresh clone works (`README` instructions)
- [ ] Integration log complete

Target: 29.11. · Role A"""},
    {"title": "Switch to PostgreSQL (bonus)", "labels": ["database", "bonus"], "milestone": M2,
     "body": """Lecturer: PostgreSQL replaces SQLite and earns the bonus point.

- [ ] Docker Desktop installed for whoever runs the pipeline
- [ ] `docker compose up -d`, `DATABASE_URL` in `.env`
- [ ] `python -m src.check_setup` reports postgresql
- [ ] Full pipeline runs on PostgreSQL
- [ ] Screenshot (pgAdmin / query) for the self-assessment appendix

Target: 29.11. · Role A"""},
    {"title": "Complete EDA (tabular and graphical)", "labels": ["analysis"], "milestone": M2,
     "body": """- [ ] Descriptive statistics per traffic type and weather category
- [ ] Delay rate by hour/weekday (confounders visible)
- [ ] Correlation heatmap of numeric variables
- [ ] All charts in report quality

Target: 06.12. · Role B"""},
    {"title": "Map: stops, weather stations and extra delay under precipitation (bonus)", "labels": ["geo", "bonus"], "milestone": M2,
     "body": """- [ ] Map (folium/geopandas) with stops coloured by extra delay (rain/snow vs. dry)
- [ ] Weather stations and stop→station assignment visible
- [ ] Static export for the slides

Target: 06.12. · Role B"""},
    {"title": "Hypothesis tests H1–H3 with effect sizes", "labels": ["analysis", "bonus"], "milestone": M2,
     "body": """See [docs/research-design.md](../blob/main/docs/research-design.md#3-hypotheses-and-tests).

- [ ] H1a/b: Chi² per traffic type + Cramér's V
- [ ] H2: risk differences with 95 % CI, one-sided z-test, risk ratio as robustness check
- [ ] H3: Pearson correlation daily precipitation vs. daily delay rate
- [ ] Interpretation in plain words, limitations (dependence, large n)

Target: 06.12. · Role C"""},
    {"title": "Classification per traffic type, with and without weather features", "labels": ["analysis"], "milestone": M2,
     "body": """- [ ] Time-based train/test split, cross-validation
- [ ] Classification tree + random forest, per traffic type
- [ ] Variant without weather vs. with weather features
- [ ] Confusion matrix, precision, recall, ROC-AUC, baseline
- [ ] Compare AUC gain from weather: regional vs. long-distance
- [ ] Feature importance (not causal!)

Target: 13.12. · Role C"""},
    {"title": "k-means on stops (bonus)", "labels": ["analysis", "bonus"], "milestone": M2,
     "body": """- [ ] Features per stop (e.g. delay rate dry, delay rate with precipitation, trains/day), scaled
- [ ] Choose k with WCSS (elbow) and silhouette
- [ ] Interpret clusters, show on the map

Target: 13.12. · Role C/B"""},
    {"title": "Stats review before results go into the report", "labels": ["analysis"], "milestone": M2,
     "body": """- [ ] Run the `stats-reviewer` agent on all analysis notebooks
- [ ] Fix all 🔴 findings, decide on 🟡
- [ ] Note what was changed in the AI log

Target: 13.12. · all"""},
    {"title": "Final presentation PDF with required structure and self-assessment appendix", "labels": ["presentation", "docs"], "milestone": M2,
     "body": """Required structure (see grading.md):
- [ ] Title and names
- [ ] Introduction
- [ ] Materials & Methods
- [ ] Results & Discussion
- [ ] Conclusions
- [ ] AI reflection (from `docs/ai-log.md`)
- [ ] **Appendix: self-assessment of points incl. screenshots/code** (use `/check-grading`)
- [ ] GitHub URL on a slide

Target: 03.01. · all"""},
    {"title": "Video (15 min, 5 min per person)", "labels": ["presentation"], "milestone": M2,
     "body": """- [ ] Script/outline, 5 min each
- [ ] Freely spoken, no notebook scrolling
- [ ] AI reflection part included
- [ ] Length checked (time keeping is graded)
- [ ] File name `video_recording_group_XX.mp4` (parts if needed)

Target: 06.01. · all"""},
    {"title": "AI reflection summary", "labels": ["docs"], "milestone": M2,
     "body": """- [ ] `docs/ai-log.md` complete
- [ ] Summary: advantages, disadvantages, where it failed (concrete examples)
- [ ] Slide for the PDF and part for the video

Target: 03.01. · all"""},
    {"title": "Submission package on Moodle", "labels": ["admin"], "milestone": M2,
     "body": """- [ ] `/check-grading` run, gaps closed
- [ ] `materials_group_XX.zip` (code, notebooks, scripts; data or rebuild instructions)
- [ ] `presentation_group_XX.pdf`
- [ ] `video_recording_group_XX.mp4`
- [ ] Group number filled in for XX
- [ ] Uploaded by one person, confirmation screenshot

Target: 08.01., deadline **10.01.2027, 23:59** · ER"""},
]
