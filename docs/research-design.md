# Research design

Status: **draft for team decision**. Items marked **DECIDE** must be fixed by
the team before the concept presentation. Items marked **VERIFY** are
assumptions that the data prototype must confirm.

## 1. Research question

> Does precipitation (rain or snow) increase the probability of an arrival
> delay of 3 minutes or more **more strongly in regional rail traffic than in
> long-distance rail traffic** in the Greater Zurich area?

This is a **comparison question** (two groups: regional vs. long-distance),
which the grading requires ("beyond a standard prediction").

## 2. Unit of observation and variables

**Observation:** one scheduled train arrival at one stop in the study area
(one row of the Ist-Daten).

| Variable | Definition | Type | Source |
|---|---|---|---|
| `delayed` (target) | arrival delay ≥ 3 min (actual − scheduled arrival) | binary 0/1 | Ist-Daten |
| `traffic_type` (group) | regional vs. long-distance, derived from the train category | binary | Ist-Daten |
| `precip_cat` | dry / rain / snow in the hour before arrival at the nearest weather station | nominal (3) | MeteoSwiss |
| `precip_mm` | precipitation sum in that hour | metric | MeteoSwiss |
| `temp_c` | air temperature | metric | MeteoSwiss |
| `hour`, `weekday`, `rush_hour`, `holiday` | control variables against confounding | nominal / binary | derived |

**DECIDE:**
- **Threshold 3 min.** Proposal: keep it. SBB measures customer punctuality as
  arrival less than 3 min late. **VERIFY** the source before quoting it on a
  slide.
- **Traffic type mapping.** Proposal: regional = S, R, RE · long-distance = IC,
  IR, EC, ICE, TGV, RJX, EN, NJ. IR is the debatable one, so decide and justify it.
- **Precipitation categories.** Proposal: dry = 0.0 mm in the previous hour;
  rain = ≥ 0.1 mm and temperature > 0 °C; snow = ≥ 0.1 mm and temperature ≤ 0 °C.
  The temperature split is a simplification (sleet near 0 °C). Name it as a
  limitation.
- **Cancelled trains** (`FAELLT_AUS_TF`): Proposal: exclude and report the
  count. A cancellation is not a delay.
- **Only measured times.** Proposal: keep rows with arrival status "REAL" only
  and drop estimated or forecast values. **VERIFY** the column name and values.
- **Study period.** Winter months with enough snow days in Zurich. Determine
  it from the weather data first, then download the Ist-Daten for that period.

### VERIFY results (2026-11-03, ER with Claude Code, checked on real files)

| Item | Result | Evidence |
|---|---|---|
| Ist-Daten format | `;`-separated, UTF-8, 22 columns: BETRIEBSTAG, FAHRT_BEZEICHNER, BETREIBER_ID, BETREIBER_ABK, BETREIBER_NAME, PRODUKT_ID, LINIEN_ID, LINIEN_TEXT, UMLAUF_ID, VERKEHRSMITTEL_TEXT, ZUSATZFAHRT_TF, FAELLT_AUS_TF, BPUIC, HALTESTELLEN_NAME, ANKUNFTSZEIT, AN_PROGNOSE, AN_PROGNOSE_STATUS, ABFAHRTSZEIT, AB_PROGNOSE, AB_PROGNOSE_STATUS, DURCHFAHRT_TF, SLOID | portal file 21.10.2026, archive files 2026-01 and 2026-03 (v1 also has SLOID since Oct 2025; 2024 files have 21 columns, without SLOID) |
| Time zone Ist-Daten | **Swiss local time** (CET/CEST) | night of the switch to summer time, 29.03.2026: 0 scheduled arrivals 02:00–02:59 (one week earlier, 22.03.: 14,376) |
| Time formats | ANKUNFTSZEIT `DD.MM.YYYY HH:MM` (scheduled, minutes); AN_PROGNOSE `DD.MM.YYYY HH:MM:SS` (actual) | real files |
| Arrival status column | `AN_PROGNOSE_STATUS`, values REAL / PROGNOSE / UNBEKANNT / empty. ZH trains 21.10.2026 with a scheduled arrival: REAL 22,700 (95.3 %), UNBEKANNT 954, PROGNOSE 175. Empty = first stop of a trip (no arrival) | cookbook + data |
| Cancellation flag | `FAELLT_AUS_TF` (`true`/`false`); cancelled rows have status UNBEKANNT and no actual time | 08.01.2026: 1,165 cancelled train rows CH-wide; 21.10.2026: 1,169 at ZH stops |
| Extra trips | `ZUSATZFAHRT_TF`; 136 rows at ZH stops on 21.10.2026 | data |
| Train category column | `VERKEHRSMITTEL_TEXT` (S, IR, IC, RE, EC, ICE, TGV, NJ, RJX, EXT at ZH stops); `PRODUKT_ID = 'Zug'` selects trains. `LINIEN_TEXT` has the line (S10, IC1 …) | data |
| Stop key | Ist-Daten `BPUIC` (7 digits for trains) = service point `number` | 156 of 182 ZH stops matched on 21.10.2026 |
| 3-min threshold source | SBB: "A train counts as on time if it reaches stations with less than 3 minutes' delay … Trains cancelled at short notice are counted as not on time." SBB counts **RE as long-distance** (EC, ICE, RJX, TGV, IC, IR, RE) | reporting.sbb.ch/punctuality (accessed 2026-11-03) |
| MeteoSwiss time zone | **UTC** | opendatadocs.meteoswiss.ch/general/download: "All reference time stamps at MeteoSwiss are in UTC!" |
| Hourly interval | timestamp = **end** of the hour: "ReferenceTS 16:00 = 15:10 to 16:00" (since 2018) | same page |
| Parameter codes | `rre150h0` precipitation hourly total (mm), `tre200h0` air temperature 2 m hourly mean (°C), `htoauths` snow depth hourly (cm). No fresh-snow parameter in SMN | `ogd-smn_meta_parameters.csv` |
| Weather file format | `;`, decimal point, Windows-1252, missing = empty field | MeteoSwiss docs + files |

## 3. Hypotheses and tests

Significance level **α = 0.05** for all tests, fixed in advance.

### H1: Precipitation and delay are related (per traffic type)
- **H0:** For regional traffic, `delayed` is independent of `precip_cat`.
- **H1:** For regional traffic, `delayed` depends on `precip_cat`.
- Same pair separately for long-distance traffic (H1a regional, H1b long-distance).
- **Test:** Chi² test of independence on the 2×3 contingency table
  (`delayed` × dry/rain/snow), per traffic type. Effect size: Cramér's V.
- Course: week 7. Counts as bonus "Chi² with p-value".

### H2: The effect is stronger in regional traffic (core of the research question)
- Effect per traffic type = **risk difference**
  RD = P(delayed | precipitation) − P(delayed | dry), in percentage points.
- **H0:** RD_regional ≤ RD_long-distance
- **H1:** RD_regional > RD_long-distance
- **Test:** one-sided z-test for the difference of two risk differences
  (z = (RD_reg − RD_ld) / √(Var_reg + Var_ld)), plus a 95 % confidence interval
  for each RD. Easy to compute with numpy/scipy, and easy to explain.
- **Robustness check:** also report the **relative** effect (risk ratio).
  "Stronger" in absolute terms (percentage points) and in relative terms can
  point in different directions if the baseline delay rates differ.
  **DECIDE** which one is primary. Proposal: absolute (percentage points),
  because it is more intuitive for passengers.

### H3: More precipitation, more delays (dose-response)
- Aggregated per day and traffic type: daily precipitation sum vs. daily delay rate.
- **H0:** ρ = 0 (no linear correlation). **H1:** ρ > 0.
- **Test:** Pearson correlation with p-value (course: week 7), per traffic type.
  Daily aggregation also reduces the dependence problem (see 5).

### Model part (classification, required)
Not a hypothesis test, but it answers the same question with a second method:
- Classification tree and random forest **per traffic type**, target `delayed`.
- Two variants each: **without** weather features (controls only) and
  **with** weather features.
- **Comparison measure:** gain in ROC-AUC (and recall) from adding the weather
  features. Prediction: the gain is larger for regional traffic.
- Train/test split (time-based, e.g. last weeks as test set) and
  cross-validation; confusion matrix, precision, recall, ROC-AUC; the baseline
  is the share of the majority class.

### Optional bonus methods
- **k-means** on stops (e.g. delay rate dry, delay rate with precipitation,
  number of trains), then check whether clusters line up with regional and
  long-distance hubs.
- **Map:** stops coloured by the extra delay under precipitation, with the
  weather stations (geodata bonus).

## 4. Expected results (link to the research question)

| Hypothesis | Expected | Reasoning (for the slide) |
|---|---|---|
| H1a/b | Delay rate is higher with precipitation for both traffic types | longer dwell times, lower adhesion, slower boarding |
| H2 | RD_regional > RD_long-distance | more stops per km means more dwell time that precipitation can extend; less buffer in tight S-Bahn timetables |
| H3 | positive correlation, stronger for regional | dose-response supports a real effect |
| Model | larger AUC gain from weather for regional | consistent with H2 |

**Plausible counter-result:** Long-distance trains often bring delays from
outside the study area (weather in Bern or Geneva), which blurs the local
weather effect in both directions. Mention this as a limitation. A stronger
design would measure the **delay increase between two consecutive stops** inside
the study area instead of the absolute delay. That is optional and depends on
the data.

## 5. Limitations (name them, don't hide them)

- **Correlation ≠ causation.** Weather goes together with season, holidays and
  construction work. Controls help but don't solve it.
- **Dependent observations.** Arrivals of the same train run, and all trains in
  the same hour, share the same weather. p-values on row level are too
  optimistic. With millions of rows almost everything is "significant", so
  **effect sizes and confidence intervals matter more than p-values.** H3 on daily
  level partly addresses this.
- **Nearest weather station ≠ weather on the line.**
- **Class imbalance:** delayed arrivals are the minority, so accuracy alone is
  misleading.
- **Study period:** a few winter months in one region do not generalize to
  all of Switzerland or to summer thunderstorms.
