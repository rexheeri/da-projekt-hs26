# Onboarding checklist

Goal: after this list you have the same state as everyone else. Takes about
60–90 min. Tick the boxes in your onboarding issue on GitHub.

## 1. Access
- [ ] Accept the GitHub invitation to `rexheeri/da-projekt-hs26`
- [ ] Tell the group your GitHub name ↔ real name (for `project-state.md`)

## 2. Install (skip what you already have)
- [ ] Git
- [ ] Python 3.10 or newer (3.12 recommended)
- [ ] VS Code with the extensions **Python** and **Jupyter** (VS Code suggests them when you open the repo)
- [ ] Claude Code (VS Code extension or CLI), *optional but recommended*
- [ ] Docker Desktop, *only needed for PostgreSQL, not before the presentation*

## 3. Set up the repo
```bash
git clone https://github.com/rexheeri/da-projekt-hs26.git
cd da-projekt-hs26
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m src.check_setup       # must end with "Setup OK."
```
- [ ] `check_setup` says **Setup OK**
- [ ] VS Code uses the `.venv` interpreter

## 4. Read (in this order, ~30 min)
- [ ] `README.md`: structure and team rules
- [ ] `docs/project-state.md`: current state, decisions, **the lecturer's answers**
- [ ] `docs/grading.md`: what is graded, how many points
- [ ] `docs/research-design.md`: research question, hypotheses, open decisions
- [ ] `docs/workplan.md`: phases, roles, dates
- [ ] `docs/concept-presentation.md`: what we present on 17.11.

## 5. Claude
- [ ] Read `docs/claude/README.md`
- [ ] Create your own `CLAUDE.local.md` (language, your role, your initials)
- [ ] Start Claude Code in the repo and run `/status`
- [ ] *Or* set up a claude.ai Project with `docs/claude/project-instructions.md`

## 6. First contribution (tests the Git workflow)
- [ ] `git pull`
- [ ] Fill in your row in `docs/project-state.md` (name, GitHub, initials, role)
- [ ] Commit (`Add <initials> to project state`) and `git push`

## 7. Dates in your calendar
- [ ] **Tue 17.11.2026, 11:00–12:45, SW301 Winterthur:** concept presentation,
  **attendance mandatory**. Take the morning off work now.
- [ ] **Mon 16.11.:** dry run (time to be agreed)
- [ ] **10.01.2027, 23:59:** final submission
- [ ] Weekly 15-min sync (day/time to be agreed)

## 8. Pick your first issue
- [ ] Assign yourself to the issues of your role in milestone **M1**

## 9. Data handover (from ER, Phase 3)

You do **not** need to download the raw data. ER shares the team export.

1. **Where:** OneDrive/Teams, in the folder ER announces in the team chat
   (suggested name `DA_team_export`; size and date are in `manifest.csv`).
   It is never on GitHub. Size: 78 MB; loading takes about 3 minutes and
   creates a database of about 2.4 GB (10.1 million arrivals).
2. **Load it:** copy the folder to `data/export/team/` in your repo, then
   `python -m src.load_shared data/export/team`. It replaces the tables in your
   database (SQLite by default, PostgreSQL if `DATABASE_URL` is set).
3. **Use it:** `from src.db import query` and
   `df = query("SELECT * FROM analysis_base WHERE winter = :w", {"w": "2025/26"})`.

What is in `analysis_base` (one row = one train arrival at a stop in canton ZH):

| Column | Meaning |
|---|---|
| `service_date`, `trip_id`, `line`, `category` | operating day, trip, line (S8, IC1 …), category (S, IC, IR, RE …) |
| `traffic_type` | `regional` (S-Bahn) or `long_distance` (IC, IR, RE, EC, ICE, TGV, RJX, RJ, NJ) |
| `bpuic`, `stop_name` | stop |
| `sched_arr_utc` | scheduled arrival, UTC (text `YYYY-MM-DD HH:MM:SS`) |
| `arr_delay_min`, **`delayed`** | arrival delay in minutes; **target**: 1 if ≥ 3 min |
| `prev_dep_delay_min`, `entry_delay_min` | delay known **before** the arrival (previous stop; last stop before canton ZH, NULL if the trip starts inside) → allowed as features |
| `delay_gain_min` | delay gained since the previous stop → **outcome, never a feature** (leakage) |
| `precip_station`, `temp_station`, `*_distance_km` | weather stations used and their distance |
| `precip_mm`, `temp_c` | weather in the last full hour **before the scheduled arrival** |
| `precip_cat`, `precip_any` | dry / rain / snow; precipitation yes/no (main comparison) |
| `hour`, `weekday`, `rush_hour`, `local_date` | Swiss local time; rush hour = Mon–Fri 06–09 and 16–19 h |
| `holiday`, `public_holiday`, `school_holiday`, `winter`, `month` | calendar controls |

Unlocked issues once the data is loaded: Complete EDA (#18), map (#19),
hypothesis tests (#20), classification (#21), k-means (#22).
