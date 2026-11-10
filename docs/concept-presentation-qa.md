# Concept presentation: why we run the tests, and questions to expect

For the group's preparation of the concept presentation (Tue 17.11.2026). Everyone has to be able to
explain this freely (criterion 7). Numbers come from release `data-v1` and from
`notebooks/02_eda_lk.ipynb` / `03_slide_figures_lk.ipynb`. Rules and facts: [research-design.md](research-design.md),
[project-state.md](project-state.md). A shorter list of critical questions is in
[concept-presentation-checklist.md](concept-presentation-checklist.md#critical-questions-with-answer-keywords).

Status marks: **decided** = in `research-design.md` / `project-state.md`; **open** = not decided by the team yet;
**not checked** = we have not verified it.

---

## Part A. The tests: why we run them and what a result does

### A0. The idea in one paragraph

The research question compares two groups (regional vs. long-distance). A table of delay rates shows a difference, but it
does not say how sure we can be about it, and whether the two groups differ from *each other*. The tests give us that.
We use three of them, each for one job, plus a classification model as a second method. Significance level
**α = 0.05, fixed in advance** (so we cannot choose it after seeing results).

| | Question it answers | Test | H0 (nothing going on) | If H0 is rejected, we may say | What it is used for |
|---|---|---|---|---|---|
| **H1** | Are delay and weather related at all? | Chi² test of independence on delayed × dry/rain/snow, per traffic type; effect size Cramér's V | delay is independent of weather | the delay rate differs between dry, rain and snow | Entry ticket: without a relation, comparing the two groups is pointless |
| **H2** | Is the weather effect **larger in regional traffic**? (the research question) | one-sided z-test on the difference of the two effects; 95 % confidence intervals | effect regional ≤ effect long-distance | regional traffic reacts more strongly (in percentage points) | **Core**: answers the research question |
| **H3** | Do more precipitation and more delay go together (dose-response)? | Pearson correlation on daily values, per traffic type | ρ = 0 | days with more precipitation have a higher delay rate | Supports that the weather effect is real, avoids counting the same hour millions of times |
| Model | Does weather add predictive information beyond hour, weekday, holiday? | Classification tree and random forest per traffic type, with vs. without weather features | – (not a hypothesis test) | – | Second method for the same question, tells how much weather matters in practice |

### A1. H1, Chi² test (relation between delay and weather)

- **What it does.** Counts delayed and on-time arrivals in each weather class (dry, rain, snow) and compares them with what we
  would see if weather made no difference. Done separately for regional and long-distance traffic.
- **Result and meaning.** A small p-value (< 0.05) means: a relation as strong as the one we see would be very unlikely if
  delay and weather were unrelated. It does **not** mean the relation is large or causal.
- **Why also Cramér's V.** With millions of rows the p-value will be practically 0 for any difference. V (0 to 1) says how
  strong the relation is. A V around 0.1 is a small relation.
- **Why we need it.** If H1 is not rejected for a traffic type, there is no weather effect to compare there.
- **Illustration with the first-look numbers** (not the official run, no controls): regional chi² ≈ 86,000, long-distance
  ≈ 5,400, both with p practically 0 and Cramér's V ≈ 0.095. So H1 would be rejected for both. Because of dependence between
  arrivals (A5), the exact p-values are too optimistic, but the direction is not in doubt.

### A2. H2, z-test on the difference of the two effects (the core)

- **Effect per traffic type.** RD = P(delayed | precipitation) − P(delayed | dry), in percentage points (pp).
  Rain and snow pooled (`precip_any`). This absolute measure is **primary** (decided 03.11., before the data was seen);
  the risk ratio is the robustness check.
- **What the test does.** It takes the difference RD_regional − RD_long-distance and divides it by its standard error (z).
  It works because regional and long-distance arrivals are different rows. It is **one-sided**: it only asks whether the
  regional effect is *larger*.
- **Result and meaning.**

| Outcome | What we say about the research question |
|---|---|
| Difference clearly above 0 (confidence interval entirely above 0), H0 rejected | Regional traffic is hit harder, in percentage points. Then check the risk ratio |
| Confidence interval contains 0, H0 not rejected | We cannot tell the two traffic types apart. **Not** "they are equal" |
| Confidence interval entirely below 0 | The long-distance effect is larger. A one-sided test cannot reject in this direction, so the interval carries the message |
| Percentage points and risk ratio point in opposite directions | The answer depends on the measure: regional traffic starts from a lower base, so the relative rise can be larger even if the absolute rise is smaller. We report both and name the primary one |

- **A test never proves H2.** It can reject H0 or fail to reject it. Say "tested", not "proved".
- **Illustration with the first-look numbers** (rain + snow vs. dry, no controls, naive standard errors that ignore dependence):

| | P(delayed), precipitation | P(delayed), dry | RD | 95 % interval | risk ratio |
|---|---|---|---|---|---|
| regional | 9.15 % | 4.09 % | **+5.06 pp** | 5.01 to 5.11 | 2.24 |
| long-distance | 13.44 % | 7.14 % | **+6.30 pp** | 6.06 to 6.54 | 1.88 |

  The difference regional − long-distance is **−1.24 pp** (interval −1.49 to −1.00), z ≈ −9.9. A one-sided test for
  "regional larger" would **not** reject H0. With these numbers the data point the other way in percentage points, and in
  the same direction as H2 only for the risk ratio. This is a first look, not the official test (it comes in issue #20),
  and it can change with controls (hour, weekday, holiday), with the stop mix (A5) and with proper standard errors. It
  must not be presented as a result. The honest line for the slide is: "H2 is open".
- **Open (team decision, #20).** The test was fixed as one-sided before the data was seen. Switching to a two-sided test now
  because of what we saw would be choosing the test by the result. The clean way: keep the one-sided test and report the
  interval of the difference, which also shows an opposite direction.

### A3. H3, Pearson correlation (dose-response)

- **What it does.** One point per day and traffic type: x = daily precipitation, y = share of delayed arrivals that day. The
  correlation r runs from −1 to +1. Test: ρ > 0 (one-sided).
- **Result and meaning.** A clearly positive r with p < 0.05 means: on days with more precipitation the delay rate is higher,
  "the more rain, the more delay". That fits a real effect better than a mere on/off difference.
- **Why we need it.** It looks at the same question with a different data structure: about 450 independent days instead of
  10 million dependent arrivals. This reduces the problem that all trains in one hour share the same weather.
- **Weak points.** Only a straight-line relation. Days also differ in weekday, holiday and season, which affect delays too.
  **Open:** how the daily precipitation is formed from several stations (e.g. mean over stations) is not decided yet.

### A4. Classification (decision tree, random forest)

- **What it does.** Predicts the target `delayed` per traffic type once with the control variables only (hour, weekday,
  rush hour, holiday, winter, month) and once with the weather variables added. Evaluated on a test set that is split off
  **before** any fitting.
- **Result and meaning.** The **gain in ROC-AUC** from adding weather says how much weather improves the prediction beyond
  timetable effects. A larger gain for regional than for long-distance traffic would agree with H2 from a second angle.
  A tiny gain in both means: even if the tests are significant, weather explains little compared with hour and weekday.
- **Why we need it.** (1) It is a course requirement and the lecturer confirmed that classification suits the topic.
  (2) It shows practical size, which p-values do not. (3) Feature importance shows which weather variable matters.
- **Why recall, precision, ROC-AUC.** Delays are the minority (4.8 % regional, 8.0 % long-distance); accuracy alone
  would be high for a model that always says "on time".
- **Leakage rule.** No variable that is only known after the departure. `delay_gain_min` is the outcome, never a feature;
  `entry_delay_min` only for long-distance traffic (60.3 % missing for regional).

### A5. Why p-values are not enough here

- **Dependence.** Arrivals of the same train and all trains in the same hour share the same weather. Row-level p-values are
  too optimistic. With 10 million rows almost anything is "significant". So we lean on **effect sizes and confidence
  intervals**, and on H3 at day level.
- **Different stops.** Long-distance trains stop at 35 stops, regional trains at 157. The two groups are measured in
  partly different places and hours. **Open:** robustness check on the stops served by both (comment in #3).
- **Confounding.** Rush hour has more delays also when it is dry. Hour, weekday and holidays must be controlled.
  Planned: effect per hour group or a model, not only the pooled difference.
- **Correlation ≠ causation.** Weather goes with season, holidays and construction work.
- **Several tests.** We run H1 twice (per traffic type), H2 and H3, each at 0.05, without correction. We say so if asked.

---

## Part B. Questions to expect, per slide

Short answers. "→" points to where the proof is.

### Slide 1, Title
- *Is your topic approved?* Mario Gellrich called topic and data "exciting and suitable" and classification "suitable"; formal approval is at this presentation (→ project-state.md).
- *Why this title?* It is the research question in short form.

### Slide 2, Outline
- *Why this order?* It follows one thread: problem → question → data → methods → first look → expectations → next steps, and the eight grading criteria of the concept presentation.

### Slide 3, Background
- *Where does 94.1 % come from, what does it count?* SBB's annual result 2025 as reported by swissinfo.ch: share of punctual passenger trains, all of Switzerland. Our study covers only the canton of Zurich. SBB defines on time as less than 3 min late (reporting.sbb.ch/punctuality).
- *Why exactly 3 minutes?* It is SBB's own definition, and it gives us a clear binary target.
- *Is "3,000 trains per weekday" reliable?* It is a figure from the SRF documentary on Zürich HB, not an SBB statistic (**not checked** against an SBB source). We use it only to give context.
- *Do you have evidence that weather causes delays?* Only the general argument (dwell times, adhesion, boarding). The project tests the relation; correlation does not prove cause.

### Slide 4, Problem
- *Why do you think regional trains react more?* These are hypotheses: many stops and tight timetables give weather more places to add delay. We do not claim them as facts.
- *Long-distance trains bring delays from outside. Doesn't that bias the result?* Yes, it is our biggest weakness. For long-distance traffic we control for the departure delay at the last stop before the area (`entry_delay_min`). For regional traffic this is mostly NULL (60.3 %, trips start inside Zurich), so it cannot be used there. The asymmetry is a limitation.
- *Is "regional" really the S-Bahn?* In the canton of Zurich, yes: category R does not occur at Zurich stops. RE counts as long-distance (SBB list).
- *Why does it matter?* Timetable buffers and passenger information in bad weather.

### Slide 5, Objective and research question
- *What does "stronger" mean?* The absolute difference in percentage points between the delay rate with precipitation and when dry, decided before we saw the data. The risk ratio is the robustness check.
- *You analyse long-distance trains, but only Zurich?* We count train arrivals at stops in the canton of Zurich for both traffic types. Long-distance trains appear only where they stop there (35 of 182 stops, regional trains at 157). The weather is the weather in Zurich.
- *Why only Zurich and only winter?* Size and one weather region: already 10.1 million arrivals. Winter half-year (Nov–Mar) because rain and snow are common then; three winters, three timetables.
- *Why exclude cancellations?* A cancelled train has no arrival time. SBB counts them as not on time, so we report their count and plan a robustness check (cancellations as delayed). **Open:** the check is not yet done.
- *Summer, thunderstorms, hail?* Not covered. Limitation (hail is not in our data).

### Slide 6, Hypotheses
- *Why these tests?* → Part A. H1 relation, H2 comparison (core), H3 dose-response.
- *Why one-sided?* The question is directional ("more strongly in regional traffic"), fixed before the data. We add the interval of the difference.
- *Why α = 0.05, no correction?* Convention, fixed in advance. We run few tests and say that we do not correct.
- *With millions of rows everything is significant.* Yes. Hence effect sizes and confidence intervals, and H3 at day level.
- *Are the observations independent?* No (same weather, same trains). p-values are optimistic; this is a stated limitation.
- *Why not regression?* Classification and the tests are in the plan. A logistic regression with controls would give an adjusted effect directly. **Open:** not planned yet, worth a decision before #20.

### Slide 7, Data sources
- *Is the scripted download your own data collection?* Yes, the lecturer confirmed it for the Ist-Daten (API).
- *May you use and publish the data?* Both sources allow processing and publishing with citation: opentransportdata.swiss and "Source: MeteoSwiss" (→ docs/data-releases.md). One clause on regular updates is unclear for snapshots: risk accepted, see that file.
- *How good are the Ist-Daten?* We use measured times only (status REAL). On the sample day this was 95.3 % of arrivals (not the whole period).
- *Why 26 weather stations?* Nearest precipitation or temperature station per stop; the set comes from that assignment. Median distance 3.6 km.
- *Where is it stored?* SQLite now (fallback), PostgreSQL planned; the lecturer confirmed PostgreSQL may replace the SQLite requirement.

### Slide 8, Data structure
- *How do you join the sources?* Stop ID `bpuic` joins arrivals and stops; each stop gets its nearest station; station plus hour gives the weather. In SQL, the join lost 0 rows.
- *Why the hour before the scheduled arrival?* With the actual time the delay itself would choose the weather hour (leakage).
- *Time zones?* Ist-Daten are Swiss local time, MeteoSwiss is UTC; stored in UTC, `hour` and `rush_hour` in local time; tested around the summer-time switch.
- *Missing values and errors?* 34 duplicate rows removed; delays outside −15 … +300 min removed; `precip_mm` has no NULLs; 26 rows without temperature (sensor gaps, all dry); `entry_delay_min` NULL for 60.3 % of regional arrivals.
- *Four days missing?* 28–31.01.2025 could not be read (a compression format the tool does not support). 450 of 454 days; planned in `data-v2`.
- *How do you tell rain from snow?* ≥ 0.1 mm at ≤ 0 °C is snow. Checked against measured fresh snow: finds 75 % of measured snow days, 65 % of our snow days had measured fresh snow. Sleet is a limitation.

### Slide 9, Methods
- *Why classification when you want a comparison?* The tests give the answer; the model shows how much weather adds in practice (AUC gain per traffic type).
- *Why tree and forest?* The tree is easy to read, the forest is more accurate and gives feature importance.
- *Class imbalance?* Delays are 4.8 % (regional) and 8.0 % (long-distance): recall, precision, ROC-AUC, baseline = majority class.
- *Data leakage?* Train/test split before fitting; no variable known only after departure; `delay_gain_min` is the outcome.
- *How do you avoid overfitting?* Test set and cross-validation (→ research-design.md). Time-based split if asked.
- *Isn't this just rush hour?* Hour, weekday, holiday as controls.
- *What are map and k-means for?* Bonus: map of stops and stations; k-means groups stops by their delay behaviour. **Open:** variables not fixed.

### Slide 10, First look
- *Is this a result?* No: preliminary, no controls, no test, n = 10.1 million.
- *Why is the snow rate so high?* Few arrivals (79,835 regional, 4,729 long-distance), possibly sleet or melting near 0 °C. Wide uncertainty.
- *Why are the base rates different (4.1 % vs 7.1 %)?* Different stops, hours and timetables. This is also why the effect measure matters.
- *Did you choose the effect measure after the data?* No: absolute primary, risk ratio robustness, decided on 03.11., before we saw the data.
- *So is regional more sensitive?* Not decided. In percentage points the pooled effect is larger for long-distance (+6.3 vs +5.1), as a ratio for regional (2.24 vs 1.88). The test (H2) and controls are still to come.
- *Isn't it just rush hour?* Delays peak at 7–9 h and 17–19 h also when dry. That is why we control for hour.

### Slide 11, Expected results
- *Why do you expect a larger regional effect?* More stops per km and less buffer give weather more places to add delay. It is a hypothesis.
- *Your first look points the other way in percentage points. Do you still expect it?* We keep H2 as the hypothesis and let the test decide. We say openly that it is open.
- *What if H2 is not supported?* Then the answer is "no evidence that regional traffic is hit harder" or "long-distance is hit harder", a valid result (→ A2).
- *What else could explain the result?* Rush hour, holidays, season, construction, different stops (35 vs 157), imported delays.
- *Which limitations?* Correlation ≠ causation; nearest station ≠ weather on the line (median 3.6 km, maximum 10.3 km); one region, three winters; snow is rare; dependent observations.
- *Practical value?* Where timetable buffers and passenger information in bad weather matter most.

### Slide 12, Next steps
- *Is the timeline realistic?* Only 10.01.2027 is a fixed deadline; the rest is our plan. The pipeline and data exist already.
- *What do you aim for besides the minimum?* All bonus points: creativity, PostgreSQL with SQL joins and aggregations, geodata, Chi², k-means, public GitHub repo (URL on the slide).
- *How did you use AI?* Claude Code for pipeline code, notebooks, texts and slides. Documented in `docs/ai-log.md`, including mistakes (for example a draft release that did not exist, a rain-only rate presented as the precipitation rate, text and layout we had to correct). Every number comes from a script on the data; we check the results.
- *Can each of you explain every part?* Yes, that is the team rule: code and slides are kept simple enough for everyone to explain.

### Slide 13, Sources (appendix)
- *Where does number X come from?* Use this slide: opentransportdata.swiss (Ist-Daten, service points), MeteoSwiss Open Data and STAC API, SBB (reporting.sbb.ch, result via swissinfo.ch), SRF DOK. Access dates: SBB definition 03.11.2026; swissinfo.ch and SRF 10.11.2026.

---

## Open points found while writing this (for the team, not decided here)

1. H2 as a one-sided test cannot show the opposite direction: keep the test, report the interval of the difference (#20).
2. Add a logistic regression with controls? It gives an adjusted effect (#20/#21).
3. How to form the daily precipitation for H3 (#20).
4. Robustness checks: only the 35 stops served by both traffic types; without `RE`; cancellations as delayed; effect per hour group.
5. The checklist says we also measure the delay increase *within* the area; the current plan only has `entry_delay_min` (long-distance) and `delay_gain_min`. Check that the wording matches what we will do.
