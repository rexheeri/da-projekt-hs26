# Concept presentation DA – checklist and grading grid

Status 03.11.2026 · ER. Team version of the checklist, complements `docs/concept-presentation.md`. Slide skeleton: `presentation/concept_presentation_group_03.pptx` (concept per slide in the speaker notes, red = still to be added).

## Key facts

We present the **concept, not results**: 10 minutes, live on site, graded with 8 equally weighted criteria. Two of them (freely spoken, slide quality) are purely about form and together make up 25 % of the presentation grade.

| Item | Status |
| --- | --- |
| Date | Tue 17.11.2026, 11:00, at the beginning of the large class (slot 11:00–12:45) |
| Room | SW301, Winterthur |
| Duration | 10 min per group, 3–4 groups per lecture |
| Attendance | mandatory on site for all three, only on this day |
| Language | English (language of instruction and submission) |
| Content according to the module | background, problem, objectives, research question, data, methods, expected results |
| Slides | upload as PDF to Moodle; the slot states the deadline 10.01.2027, 23:59. We upload right after 17.11. |
| Weight | 20 % of the module grade |
| Grading | 8 criteria, each graded 1–6, average = presentation grade |
| Side effect | Gellrich formally approves the topic here |
| Recording | not required for the concept presentation (the video belongs to the final project) |

Grading scale per criterion: 6 complete and convincing · 5 good, minor weaknesses · 4 fulfilled in its essential aspects · 3 key elements missing or wrong · 2 only fragments · 1 not fulfilled.

## Grading grid: what each criterion needs

Each criterion counts 12.5 %. The column "Moodle checks" is the original wording, the column next to it translates it into concrete slide content for our topic.

| # | Criterion | Moodle checks | Must be on the slides | Slide |
| --- | --- | --- | --- | --- |
| 1 | Structure & outline | Outline shown and followed? Clear thread? Parts balanced? Title clear? Names of all students? | Title as a question or claim, all three names, module, date · outline with 5–6 points that we follow exactly · slide numbers · roughly equal time per part | 1, 2, 12 |
| 2 | Background & problem | Context clear? Problem convincingly motivated? | Why punctuality matters (commuters, SBB definition "< 3 min" with source) · Zurich as a hub · weather as a known disruption factor · the gap: does regional traffic react more strongly than long-distance traffic? · who benefits from the answer (timetable buffers, passenger information) | 3, 4 |
| 3 | Objective & research question | Clearly defined? | Research question word for word · objective in one sentence · scope: region, period, rail only · hypotheses H1–H3 as H0/H1, α = 0.05 | 5, 6 |
| 4 | Data | Source shown? Structure of the data explained? | Three sources with name and URL (Ist-Daten, MeteoSwiss STAC, service point directory) · access by script/API · period and volume · **real sample**: key columns with type, row counts · how the sources connect (stop → nearest station → hour) as an ER sketch · PostgreSQL | 7, 8 |
| 5 | Methods | Appropriate for the research question? Correctly described and justified? | Pipeline diagram API → DB → EDA → tests → classification · one sentence *why* per method: Chi² per traffic type, difference of delay rates (core of the comparison question), classification tree and random forest with and without weather, recall/ROC-AUC because of class imbalance · control variables (hour, weekday) · how we handle the delay that long-distance trains bring into the region | 9 |
| 6 | Expected results | Plausible? Linked back to the research question? | Per hypothesis: what we expect and why · explicit link to the research question · possible counter-result · one or two limitations (correlation ≠ causation, nearest station ≠ weather on the line) | 10, 11 |
| 7 | Language | Freely spoken? | No reading from slides or paper, cue cards at most · clean handovers between speakers · everyone rehearses their part at least 3× out loud | all |
| 8 | Quality of the presentation | Graphics, tables, slides according to scientific standards? | Slide title = finding · every chart with axes, units, n and source · sources on the slide, list at the end · regional and long-distance always in the same colour · font ≥ 18 pt · no full sentences | all |

Criterion 4 is the reason why we need real sample data by 17.11. Without it, "structure of the data explained" remains a claim.

## Slide plan

12 slides, target 9:30–9:50, a good 3:15 per person. Based on `docs/concept-presentation.md`, plus the handling of the long-distance bias on slide 9. Speakers 1–3 are assigned in the team call.

| # | Slide | Content | Criterion | Time | Speaker |
| --- | --- | --- | --- | --- | --- |
| 1 | Title | Title as a question or claim, all three names, module, date | 1 | 0:15 | 1 |
| 2 | Outline | 5–6 points, followed exactly | 1 | 0:15 | 1 |
| 3 | Background | Punctuality, SBB definition 3 min (source), Zurich as a hub, weather as a disruption factor | 2 | 0:50 | 1 |
| 4 | Problem | Gap: is regional traffic more sensitive to weather? Why that matters | 2 | 0:40 | 1 |
| 5 | Objective & RQ | Research question word for word, objective in one sentence, scope | 3 | 0:40 | 2 |
| 6 | Hypotheses | H1–H3 as H0/H1, α = 0.05 | 3, 5 | 0:50 | 2 |
| 7 | Data sources | 3 sources with URL, access by script/API, period, volume | 4 | 0:45 | 2 |
| 8 | Data structure | Real sample: columns, types, rows, ER sketch, join logic | 4 | 1:15 | 2 |
| 9 | Methods | Pipeline diagram, one *why* per method, control variables, handling of the delay brought in | 5 | 1:20 | 3 |
| 10 | First look *(preliminary)* | One chart: delay rate per traffic type × dry/rain/snow, "preliminary, n = …" | 4, 6 | 0:45 | 3 |
| 11 | Expected results | Expectation and reasoning per hypothesis, link to the RQ, limitation | 6 | 0:55 | 3 |
| 12 | Next steps | Timeline to 10.01., GitHub URL | 1 | 0:20 | 3 |
|  | **Total** |  |  | **~9:50** |  |

Slide 10 is optional. If there are no reliable numbers by 12.11., it is dropped and slide 8 gets the time.

## Required elements and formalities

Tick off before the PDF counts as finished.

**Content**

- [ ] Title and **all three names** on slide 1
- [ ] Outline on slide 2, the order of the slides matches it
- [ ] Research question word for word, identical on slide 5 and slide 11
- [ ] All three data sources with name, URL and type of access
- [ ] Real data structure: columns, types, row counts from the sample
- [ ] Join logic visible (stop → nearest weather station → hour)
- [ ] Every method with one sentence of justification
- [ ] Expected results per hypothesis, linked to the research question
- [ ] At least one limitation named
- [ ] GitHub URL on the last slide

**Form**

- [ ] Slide numbers on every slide
- [ ] Slide titles state the finding, not the topic
- [ ] Every chart: title, axes with unit, n, source
- [ ] Every external number with its source on the slide, list of sources at the end
- [ ] Regional and long-distance traffic in the same two colours everywhere
- [ ] Font at least 18 pt, no full sentences
- [ ] English throughout, consistent terms ("regional", "long-distance")
- [ ] PDF exported, file name with group 03

**Talk**

- [ ] Total time in the dry run at most 10:00
- [ ] Everyone speaks freely, cue cards at most
- [ ] Handovers between speakers rehearsed

## What does not belong on the slides

- **Finished results or conclusions.** The concept is graded. Preliminary numbers only as "preliminary" with n.
- **Code and notebooks.** No code screenshot, unless it explains the data structure better than a table.
- **Model names without justification.** "Random forest" alone is not a methods section; the *why* earns the grade.
- **Text slides to read out.** They cost criterion 7 and 8 at the same time.
- **Claims without a source**, e.g. the SBB definition of punctuality.
- **More than 12 slides.** With 10 minutes, every extra slide takes time away from data and methods.

## Critical questions with answer keywords

Gellrich formally approves the topic at the presentation. These questions are the most likely. Everyone knows the answers for their own part.

| Question | Answer keywords |
| --- | --- |
| Why exactly 3 minutes? | SBB definition of customer punctuality (show the source), binary target for the classification |
| Does the archive download count as own data collection? | Gellrich confirmed the scripted download of the daily files as own data collection; the winter data are in the official monthly archive and are also fetched by script. Clarify briefly with him beforehand |
| Long-distance trains bring delays from outside. Doesn't that bias the result? | Yes, that is why we also measure the delay increase within the study area, or control for the delay when entering the region |
| How do you tell rain from snow? | Precipitation at a temperature ≤ 0 °C counts as snow, checked against the increase in snow depth; sleet around 0 °C as a limitation |
| Where does the IR belong? | Team decision with justification (open DECIDE item) |
| Were there enough snow days at all? | The study period was chosen from the weather data, show the number of snow days |
| Why classification if you want a comparison? | The core answer is the effect comparison (difference of delay rates); the model adds the AUC gain from the weather variables per traffic type |
| Accuracy is worthless for rare delays. | That is why recall, precision and ROC-AUC, baseline = share of the majority class |
| With millions of rows everything is significant. | Effect sizes and confidence intervals matter more than p-values; H3 on the daily level |
| Isn't this just rush-hour traffic? | Hour, weekday and holidays as control variables |
| How big are the data? | Rows raw and filtered, storage, period from the pipeline |
| Nearest weather station = weather on the line? | No, show the distances (median, maximum), name it as a limitation |

## Preparation until 17.11.

ER is not available from 07. to 15.11. Therefore the dry run moves to Mon 16.11., and LS and LK carry the slide draft.

- [ ] By Thu 05.11.: team call, roles and speakers 1–3 assigned
- [ ] By Fri 06.11.: sample data in the DB, DECIDE items decided, methods part (slides 6, 9, 11) as a draft
- [ ] By Thu 12.11.: slide draft complete, chart for slide 10 or decision to drop it
- [ ] Sun 15.11.: review with the `presentation-coach` agent
- [ ] Mon 16.11.: dry run with stopwatch, all three, at most 10:00, then correct the slides
- [ ] Morning of 17.11. taken off work (all three)
- [ ] On 17.11.: laptop, adapter, PDF on a USB stick as backup
- [ ] After the presentation: upload the PDF to Moodle, write the feedback into `docs/project-state.md`
