# Research design

Status: **decided by ER on 2026-11-03, team to confirm.** The decisions and the
VERIFY results (checked on real data) are in section 2.

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
| `delayed` (target) | arrival delay ≥ 3:00 min (actual `AN_PROGNOSE` − scheduled `ANKUNFTSZEIT`) | binary 0/1 | Ist-Daten |
| `traffic_type` (group) | regional vs. long-distance, from `VERKEHRSMITTEL_TEXT` | binary | Ist-Daten |
| `precip_cat` | dry / rain / snow in the last full hour before the **scheduled** arrival, nearest precipitation station | nominal (3) | MeteoSwiss |
| `precip_any` | rain or snow vs. dry (main comparison) | binary | MeteoSwiss |
| `precip_mm` | precipitation sum in that hour | metric | MeteoSwiss |
| `temp_c` | air temperature 2 m, hourly mean, nearest SMN station | metric | MeteoSwiss |
| `hour`, `weekday`, `rush_hour` | from the scheduled arrival in Swiss local time; rush hour = Mon–Fri 06:00–08:59 and 16:00–18:59 | nominal / binary | derived |
| `holiday` | legal public holiday (ZH) or Christmas school holidays | binary | derived |
| `winter`, `month` | winter half-year (2023/24, 2024/25, 2025/26) and calendar month | nominal | derived |
| `prev_dep_delay_min` | departure delay at the previous stop of the same trip (known before the arrival) | metric | Ist-Daten |
| `entry_delay_min` | departure delay at the **last stop before the study area**; NULL if the trip starts inside the area (known before every arrival in the area, tested in `tests/test_entry_delay.py`). **NULL for 60.3 % of regional and 18.9 % of long-distance arrivals** (57.9 % overall): most S-Bahn trips start inside canton ZH. Usable as a control **for long-distance traffic only** (ER, 2026-11-04; open point in #20) | metric | Ist-Daten |
| `delay_gain_min` | arrival delay here − departure delay at the previous stop. **Alternative outcome, never a model feature** (it contains the arrival delay) | metric | Ist-Daten |

### Decisions (decided by ER on 2026-11-03, team to confirm)

| Item | Decision | Reason / source |
|---|---|---|
| Threshold | arrival delay **≥ 3:00 min** = delayed | SBB: "A train counts as on time if it reaches stations with less than 3 minutes' delay." (reporting.sbb.ch/punctuality, accessed 2026-11-03) |
| Traffic type | **regional = S**; **long-distance = IC, IR, RE, EC, ICE, TGV, RJX, NJ**; plus RJ (Railjet, same family as RJX); excluded: night S-Bahn `SN`, EXT and Forchbahn S18 (coded as `Tram` in the data) | SBB counts EC, ICE, RJX, TGV, IC, IR and RE as long-distance (same source). In the canton of Zurich, "regional traffic" is in practice the **S-Bahn**: category R does not occur at ZH stops (21.10.2026: S 23,765 rows, all long-distance categories together ~1,780) |
| Precipitation categories | dry = 0.0 mm; rain = ≥ 0.1 mm and > 0 °C; snow = ≥ 0.1 mm and ≤ 0 °C (definition 1) | snow-depth increase (definition 2) is too noisy: TAE reports increases on 17 days in Mar/Apr 2024 without a single snow hour |
| Weather hour | last full hour **before the scheduled arrival** (scheduled time, not actual time) | using the actual time would let the delay itself choose the weather hour (leakage). MeteoSwiss hourly timestamp = end of interval, so: scheduled arrival in UTC, floored to the hour → MeteoSwiss value with that timestamp |
| Time zone | stored in **UTC** internally; `hour` and `rush_hour` from Swiss local time | Ist-Daten are local time, MeteoSwiss is UTC (both verified) |
| Cancellations | excluded, count reported; robustness check with cancellations counted as delayed | SBB counts short-notice cancellations as not on time |
| Measured times only | arrivals with `AN_PROGNOSE_STATUS = REAL` only | 95.3 % of ZH arrivals on 21.10.2026 |
| Effect measure | **absolute** risk difference in percentage points (primary), risk ratio as robustness check | intuitive for passengers; baseline rates similar (7–9 %) |
| Weather stations | precipitation: nearest station of SMN **plus** the precipitation network `ogd-smn-precip`; temperature: nearest SMN station; summit station HOE (1133 m) excluded | median stop–station distance 7.4 km → 3.6 km, stops > 10 km: 36 → 1 |
| Main comparison | **precipitation (rain + snow) vs. dry**; snow as a sub-analysis | snow is rare: about 93 snow hours in the whole study period (mean over 6 ZH stations). The research question stays unchanged |
| Controls | `winter`, `month`, `holiday` (public holidays + Christmas school holidays), `hour`, `weekday`, `rush_hour` | three winters = three timetables and different construction work |
| Night S-Bahn `SN` | excluded (decided 2026-11-03, Checkpoint 2) | runs only on weekend nights 00–04 h, when no long-distance trains run: night hours would exist for one group only and bias the comparison (915 rows per weekend day) |
| Plausibility | arrival delays outside −15 … +300 min removed | data errors (e.g. −1444 min); 2 rows in the prototype week |
| Entry delay | departure delay at the last stop before the study area, NULL if the trip starts inside | must be known before the arrival; on 08.01.2026 NULL for 59 % of regional and 18 % of long-distance arrivals |
| Study period | **winter half-year (Nov–Mar)** of 2023/24, 2024/25, 2025/26 (15 months, 454 days) | see below |

### Study period: winter half-year (Nov–Mar) 2023/24 – 2025/26

Mean hours per station (SMA, REH, KLO, WAE, TAE, PFA), Swiss local time, `src.weather.winter_summary()`:

| Winter | dry | rain | snow |
|---|---|---|---|
| 2023/24 | 2,887 | 719 | 41.8 |
| 2024/25 | 3,231 | 364 | 28.5 |
| 2025/26 | 3,168 | 432 | 22.9 |
| **Total** | **9,286** | **1,515** | **93.2** |

Size: 15 monthly ZIPs from the Ist-Daten archive, **17.05 GB** (HEAD requests 2026-11-03).
The switch to summer time (31.03.2024, 30.03.2025, 29.03.2026) lies inside the
period: the local → UTC conversion must handle the missing hour 02:00–02:59.

**Holidays (decided 2026-11-03):** `holiday` = legal public holidays of canton ZH
(Neujahr, Karfreitag, Weihnachtstag, Stephanstag in Nov–Mar) + Christmas school
holidays. Christmas 2025/26 is sourced (Volksschulamt); 2023/24 and 2024/25 are
**derived from the binding canton rule** "Woche 52 und 1" (25.12.2023–06.01.2024,
23.12.2024–04.01.2025); the rule reproduces the sourced 2025/26 dates exactly.

### Validation of the snow definition (2026-11-04)

Snow definition (1) checked against manually measured fresh snow (`ogd-nime`,
`hns000d0`, 06–06 UTC) at the 7 stations where the manual and the automatic
station are at the same place (SMA, PFA, HLL, BUS, MOA, SAG, EIN), all days of the
study period with a reading (`src/snow_validation.py`):

| | days | hits | false alarms | misses | hit rate | precision |
|---|---|---|---|---|---|---|
| all 7 stations | 3,161 | 144 | 78 | 48 | **75.0 %** | **64.9 %** |
| SMA (Zurich / Fluntern) | 454 | 19 | 7 | 5 | 79.2 % | 73.1 % |

Hit rate = share of measured snow days that our definition finds; precision =
share of our snow days with measured fresh snow. Misses are mostly small (median
1 cm). False alarms are plausibly sleet or snow that melted near 0 °C. Good enough
for a sub-analysis; named as a limitation.

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
  Decided (ER, 2026-11-03): absolute (percentage points) is primary, because
  it is more intuitive for passengers; the risk ratio is the robustness check.

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
- **Nearest weather station ≠ weather on the line.** Median distance 3.6 km,
  maximum 10.3 km (precipitation stations incl. `ogd-smn-precip`).
- **Sports holidays (Sportferien) not modelled:** each municipality sets its own
  two weeks in February; `month` absorbs part of it.
- **Snow definition:** finds 75 % of measured snow days, 35 % of its snow days had
  no measurable fresh snow (validation above).
- **Snow is rare** (about 93 snow hours in 15 months, on few days). Snow
  results get wide confidence intervals, especially for long-distance traffic.
- **Rain/snow split by temperature** is a simplification (sleet near 0 °C).
- **Incoming delay only for long-distance traffic:** `entry_delay_min` is NULL
  for 60.3 % of regional arrivals (trip starts inside canton ZH), so it cannot
  control for delays brought in from outside in the regional model. Using it in
  both models would compare a controlled with an uncontrolled effect.
- **Class imbalance:** delayed arrivals are the minority, so accuracy alone is
  misleading.
- **Study period:** a few winter months in one region do not generalize to
  all of Switzerland or to summer thunderstorms.
