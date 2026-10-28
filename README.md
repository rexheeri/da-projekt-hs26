# Data Analytics – Group Project HS 2026

ZHAW School of Management and Law · BSc Business Information Technology · Module Data Analytics (3DA), HS 2026

> **Status:** Concept phase. The topic is not yet approved; approval follows at the concept presentation on 17.11.2026.

## Research question (draft)

Does the probability of a train delay of 3 minutes or more increase more strongly in regional traffic than in long-distance traffic when it rains or snows?

## Data sources (planned)

| Source | Access | Content |
|---|---|---|
| opentransportdata.swiss – Ist-Daten | daily files, downloaded by script | actual vs. scheduled arrival/departure per stop |
| MeteoSwiss Open Data (STAC API) | Web API | precipitation, snow, temperature per weather station |
| Service point directory (Dienststellen) | download | stop coordinates for the spatial join |

Raw data is **not** committed (too large). Every script under `src/` must be able to rebuild `data/` from scratch.

## Repository structure

```
data/
  raw/          downloaded source files (git-ignored)
  processed/    cleaned / joined data, SQLite database (git-ignored)
docs/
  ai-log.md            log of AI usage (required for grading)
  integration-log.md   keys, joins, inconsistencies, records lost/gained (required for grading)
notebooks/      Jupyter notebooks, one owner per notebook
src/            reusable Python code (data loading, database, helpers)
```

## Setup

Requires Python 3.10 or newer.

```bash
git clone https://github.com/<owner>/<repo>.git
cd <repo>
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
pip install -r requirements.txt
```

In VS Code: select the interpreter from `.venv` (Ctrl+Shift+P → "Python: Select Interpreter").

## How we work together

1. **Pull before you start.** `git pull` every time you open the project.
2. **One notebook, one owner.** Notebooks merge badly in Git. Never edit someone else's notebook. Name them `NN_topic_initials.ipynb`, e.g. `02_eda_weather_er.ipynb`.
3. **Shared code goes into `src/`.** As soon as two notebooks need the same function, move it to `src/` and import it.
4. **Clear outputs before committing** (Jupyter: "Clear All Outputs"). Keeps diffs small and avoids conflicts.
5. **Small commits with a clear message**, e.g. `Add MeteoSwiss STAC download for Zurich stations`.
6. **Never commit data, the database, `.env` or API keys.** `.gitignore` covers the usual paths – check `git status` before committing.
7. **Log AI usage immediately** in `docs/ai-log.md` – reconstructing it at the end does not work.

## Group

| Name | Main responsibility |
|---|---|
| Erion Rexhepi | tbd |
| tbd | tbd |
| tbd | tbd |

## Deliverables

| What | Due |
|---|---|
| Concept presentation (10 min, on site) | 17.11.2026 |
| Final project: video, materials (zip), presentation (pdf) | 10.01.2027, 23:59 |
