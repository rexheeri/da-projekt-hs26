# Concept presentation: Tue 17.11.2026, 11:00, SW301

10 minutes, on site, attendance mandatory for all three. Slides as PDF, upload
to Moodle afterwards. Criteria: [grading.md](grading.md#1-concept-presentation-20-).

- Checklist and grading grid: [concept-presentation-checklist.md](concept-presentation-checklist.md)
- Slide skeleton (concept per slide in the speaker notes): [presentation/concept_presentation_group_03.pptx](../presentation/concept_presentation_group_03.pptx)

**Editing the slides:** presentation/*.pptx is a binary file and cannot be
merged. Only one person edits it at a time: announce it in issue #13, git pull
before, commit and push right after, then release it in the issue. Export a
PDF next to it at each milestone.

## What we present

The **plan**, not results. But the plan must be backed by real data, otherwise
criterion 4 ("structure of the data explained") can't be fulfilled.

## Slide plan (~10 min)

| # | Slide | Content | Criterion | Time | Speaker |
|---|---|---|---|---|---|
| 1 | Title | Title as a question or claim, **names of all three**, module, date | 1 | 0:15 | A |
| 2 | Outline | 5–6 points, followed exactly | 1 | 0:15 | A |
| 3 | Background | Why punctuality matters (passengers, SBB's 3-min definition), Zurich as a node, weather as a known disruption factor | 2 | 0:50 | A |
| 4 | Problem | Gap: is regional traffic more weather-sensitive than long-distance? Why that matters (timetable buffers, information to passengers) | 2 | 0:40 | A |
| 5 | Objective & research question | RQ word for word, objective in one sentence, scope (region, period) | 3 | 0:40 | B |
| 6 | Hypotheses | H1–H3 as H0/H1, α = 0.05 | 3, 5 | 0:50 | B |
| 7 | Data sources | 3 sources with logo/URL, access (API, script), period, volume | 4 | 0:45 | B |
| 8 | **Data structure** | Real sample: key columns with types, row counts, how the sources connect (stop → nearest station → hour), simple ER diagram | 4 | 1:15 | B |
| 9 | Methods | Pipeline diagram: API → database → EDA → Chi²/z-test/correlation → classification (with/without weather). One line *why* for each method | 5 | 1:20 | C |
| 10 | First look *(preliminary)* | One chart: delay rate per traffic type × dry/rain/snow from the sample, clearly labelled "preliminary, n = …" | 4, 6 | 0:45 | C |
| 11 | Expected results | Per hypothesis: what we expect and why, linked back to the RQ; one limitation | 6 | 0:55 | C |
| 12 | Next steps | Timeline to 10.01., GitHub URL (bonus point) | 1 | 0:20 | C |
| | **Total** | | | **~9:50** | ~3:15 each |

Plan for 9:30–9:50. On the day it always takes longer.

## Draft: slides 7 and 8 "Data" (LK, role B, 2026-11-09)

Draft text only, not yet in the .pptx (editing rule above). Numbers from release
`data-v1` and `notebooks/02_eda_lk.ipynb`. Keywords on the slide, the sentences
are for speaking freely. Target ~2:00 for both slides.

### Slide 7: Three sources, one analysis table (0:45)

| Source | Content | Access | Period / volume | Citation on the slide |
|---|---|---|---|---|
| Ist-Daten (SBB, opentransportdata.swiss) | scheduled vs. actual arrival per train and stop | script, portal + archive (API), monthly ZIPs | Nov–Mar 2023/24–2025/26, 17 GB raw, ~1.0 billion rows | opentransportdata.swiss |
| MeteoSwiss Open Data (STAC API) | hourly precipitation and temperature | script, STAC API (`ogd-smn`, `ogd-smn-precip`) | 26 stations, 548,955 station-hours | Source: MeteoSwiss |
| Service point directory (opentransportdata.swiss) | stop coordinates | script download (`service-point-v2`) | 182 train stops in canton ZH | opentransportdata.swiss |

Message (slide title): **"We collect the data ourselves by script: 10.1 million arrivals plus hourly weather."**
Say: ZH only, winter half-year, three winters; everything downloaded by script, nothing from a ready-made dataset.

### Slide 8: Data structure (1:15)

Unit of observation: **one train arrival at one stop** (table `analysis_base`, 10,104,173 rows, 32 columns).

| Column (examples) | Type | Meaning |
|---|---|---|
| `service_date`, `sched_arr_utc` | text (date / UTC timestamp) | operating day, scheduled arrival |
| `traffic_type` | category | regional (S) vs. long-distance (IC, IR, RE, EC, ICE, TGV, RJX, RJ, NJ) |
| `arr_delay_min` | float | actual minus scheduled arrival, in minutes |
| `delayed` | binary 0/1 | **target:** delay >= 3 min (SBB definition) |
| `precip_mm`, `temp_c` | float | weather in the last full hour **before** the scheduled arrival |
| `precip_cat`, `precip_any` | category / binary | dry / rain / snow; precipitation yes/no |
| `hour`, `weekday`, `rush_hour`, `holiday`, `winter`, `month` | int / binary | controls (confounders) |

**How the sources connect (diagram, left to right):**
`stop (BPUIC, coordinates)` → nearest weather station (`stop_station`, median 3.6 km) → `weather_hourly` (station + hour).
Join key: stop → station by distance, arrival → weather by **station + full hour before the scheduled arrival** (no leakage).
Done in SQL (`analysis_base` is built by a `JOIN`), no row lost in the join.

Numbers worth one sentence: regional 9.51 M arrivals (94.2 %), long-distance 0.59 M; 8.0 % of long-distance and 4.8 % of regional
arrivals are delayed, so **delays are the minority class** (accuracy alone would mislead).

**Known gap (say it, don't hide it):** 450 of 454 days; 28.–31.01.2025 could not be read (Deflate64 ZIP), follows in `data-v2`.

Possible questions: why only canton ZH? (size, one weather region, 182 stops) · why the hour *before* the scheduled arrival?
(the actual time would let the delay choose the weather) · what if a station is far away? (median 3.6 km, max 10.3 km, named as limitation).

### Slide 10 candidate: first look (0:45, with C)

Chart `notebooks/02_eda_lk.ipynb`, section 3 (bar chart delay rate by `precip_cat` and traffic type), labelled
"preliminary, n = 10,104,173, no controls". Finding: delay rate rises with precipitation in both groups
(regional 4.1 % → 9.2 %, long-distance 7.1 % → 13.4 %). The absolute effect is larger for long-distance (+6.3 pp vs. +5.1 pp),
the relative one for regional (ratio 2.24 vs. 1.88). Do **not** claim "regional is more sensitive": it is open (H2) and
depends on the effect measure, which was fixed before the data was seen (absolute = primary).

## Draft: timetable data and database (ER, role A, 2026-11-11)

Draft text only, **not** in the .pptx (editing rule above). It covers the same ground as
slides 7–8 above, from the pipeline side. **Open for the team:** slide 2 of the deck
currently gives ER slides 9–12 and LK slides 5–8. If ER presents the data part, the
speaker split on slide 2 and in the table above has to change (decide at the dry run 16.11.).
All numbers: `docs/integration-log.md` (F4, J4), `analysis_base` on 2026-11-11.

Target **3:00**. If the team keeps the data part at 2:00 (slide plan), drop the
blocks marked *(cut)*.

### Block 1: Source (0:25), slide 7

- **Ist-Daten**, opentransportdata.swiss: one file per operating day, every public
  transport stop event in Switzerland, scheduled vs. actual time.
- 22 columns, `;`-separated. The ones we need: `BPUIC` (stop), `VERKEHRSMITTEL_TEXT`
  (S, IC, IR …), `ANKUNFTSZEIT` (scheduled), `AN_PROGNOSE` (actual), `AN_PROGNOSE_STATUS`,
  `FAELLT_AUS_TF` (cancelled).

Speaking notes:
- one file per day · whole of Switzerland · scheduled vs. actual
- we only need 6 of 22 columns

### Block 2: Collection by script (0:30), slide 7 *(cut to one sentence)*

- `src/istdaten.py`: recent days through the portal (DCAT catalogue), older months
  through the archive (monthly ZIPs). Downloaded by script, no manual files.
- 15 monthly ZIPs, 17 GB, **1,005,650,252 raw rows** for Nov–Mar 2023/24–2025/26.
- Read day by day, only trips that touch the canton of Zurich are kept.

Speaking notes:
- portal = last ~30 days · archive = monthly ZIPs since 2016
- 15 ZIPs · 17 GB · 1 billion rows · read day by day, never all in memory
- lecturer confirmed: scripted download = own data collection

### Block 3: Cleaning (0:40), slide 8 or backup slide *(cut to the first and last number)*

From 11,599,296 rows at ZH stops to **10,104,173 arrivals** (−12.9 %):

| Step | Rows removed | Why |
|---|---|---|
| no scheduled arrival | 787,481 | first stop of a trip, there is no arrival |
| status not REAL | 436,254 | only measured times, no forecasts |
| cancelled | 142,530 | excluded, count reported, robustness check planned |
| other categories | 123,348 | mainly night S-Bahn `SN`, EXT |
| pass-through, delay outside −15 … +300 min, duplicates | 5,510 | train does not stop, data errors |

Speaking notes:
- 11.6 M → 10.1 M · each step logged with rows before/after (integration log)
- biggest loss: first stop has no arrival · second: not measured
- cancellations out, but counted · robustness check later

### Block 4: Database and join (0:40), slide 8

- SQLite now, PostgreSQL from 18.11., same code through `src/db.py` (SQLAlchemy).
- Tables: `arrivals` (10.1 M, 22 columns), `stops` (182), `stop_station` (182),
  `weather_hourly` (548,955), `weather_stations` (26), `calendar_days` (883).
- `analysis_base` (32 columns) is built **in SQL** (`src/analysis_base.sql`): arrival →
  stop (`bpuic`) → nearest station → weather of the **last full hour before the scheduled
  arrival** → calendar day.
- Join result: **0 rows lost**, 0 without precipitation, 26 without temperature (sensor gaps).

Speaking notes:
- one row = one train arrival at one stop
- join in SQL, not pandas · 0 rows lost
- scheduled hour, not actual: otherwise the delay picks the weather (leakage)
- UTC inside, local time only for hour and rush hour

### Block 5: Key figures (0:20), slide 8

- 10,104,173 arrivals: regional 9,513,938 (94.2 %), long-distance 590,235 (5.8 %).
- Delayed (≥ 3 min): regional 4.8 %, long-distance 8.0 % → delays are the minority class.

Speaking notes:
- 94 % regional · long-distance small but 590,000 is still a lot
- 5 % and 8 % delayed → accuracy alone would mislead

### Block 6: Gap and limitations (0:25), slide 8

- **Gap:** 450 of 454 days. 28.–31.01.2025 are packed with Deflate64, which Python's
  `zipfile` cannot read. A fix is tested (`inflate64`), the 4 days follow in `data-v2`.
- **Imported delay:** `entry_delay_min` (delay when the train enters canton ZH) is NULL
  for 60.3 % of regional arrivals, because most S-Bahn trips start inside ZH. So it can
  only be a control for long-distance traffic.
- **Little snow:** 84,564 arrivals in snow hours, only 4,729 of them long-distance.
  Snow is a sub-analysis with wide confidence intervals; the main comparison is
  precipitation (rain + snow) vs. dry.

Speaking notes:
- 4 days missing · reason known · fix tested · say it, don't hide it
- entry delay: works for long-distance only, named as limitation
- snow: rare · sub-analysis only · main comparison = precipitation vs. dry

Likely questions: why the scheduled and not the actual hour? (leakage) · why REAL only?
(forecasts are not measurements) · why not keep cancellations? (no arrival time; SBB
counts them as late, so a robustness check counts them as delayed) · how do you know the
join is right? (5 rows checked by hand against raw files, tests for time zones and entry delay).

## Scientific standards for slides (criterion 8)

- Every chart: title stating the finding, labelled axes with units, source and
  n below the chart.
- Every number/fact from outside has a source on the slide (short form, full list on last slide).
- One message per slide, as the slide title.
- No full sentences to read out. Keywords, charts, diagrams.
- Consistent colours: regional and long-distance always the same colour.
- Slide numbers, readable font size (≥ 18 pt).

## Freely spoken (criterion 7)

- No reading from slides or paper. Cue cards with keywords at most.
- Everyone rehearses their part **out loud** at least 3 times.
- Clean handovers: "… which brings me to the data. [Name]?"
- Prepare for questions: why 3 min? why these traffic types? why classification?
  how big is the data? what if there is not enough snow?

## Before 17.11.

- [ ] Real sample data loaded and structure known (columns, types, rows)
- [ ] DECIDE items in `research-design.md` resolved
- [ ] Slides done by Thu 12.11. (draft: LS and LK, ER is away 07.–15.11.)
- [ ] Review with `presentation-coach` agent
- [ ] Dry run with stopwatch on Mon 16.11., all three, ≤ 10:00
- [ ] Time off work on Tue 17.11. morning (all three)
- [ ] Laptop/adapter/PDF on USB stick as backup
- [ ] After the presentation: upload PDF to Moodle, write feedback into `project-state.md`
