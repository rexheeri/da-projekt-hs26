# Concept presentation: Tue 17.11.2026, 11:00, SW301

10 minutes, on site, attendance mandatory for all three. Slides as PDF, upload
to Moodle afterwards. Criteria: [grading.md](grading.md#1-concept-presentation-20-).

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
- [ ] Slides done by Thu 12.11.
- [ ] Review with `presentation-coach` agent
- [ ] Dry run with stopwatch on Sun 15.11., all three, ≤ 10:00
- [ ] Time off work on Tue 17.11. morning (all three)
- [ ] Laptop/adapter/PDF on USB stick as backup
- [ ] After the presentation: upload PDF to Moodle, write feedback into `project-state.md`
