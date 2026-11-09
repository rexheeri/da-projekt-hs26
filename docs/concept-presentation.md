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
