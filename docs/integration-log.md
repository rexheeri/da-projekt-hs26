# Data integration log

Required for grading: document how the sources were combined – keys, joins, inconsistencies, records lost or gained.

## Sources

| Source | File / endpoint | Period | Rows (raw) | Retrieved on | By |
|---|---|---|---|---|---|
| Ist-Daten v2 (portal) | `data.opentransportdata.swiss/dataset/ist-daten-v2`, file list from the DCAT catalogue `dataset_series/2091d9b2-….jsonld`, script `src/istdaten.py` | 21.10.2026 (prototype day) | 2,583,004 (655.7 MB CSV, 22 columns, `;`, UTF-8) | 2026-11-03 | ER (Claude Code) |
| Ist-Daten v1 (archive), exploration only | `archive.opentransportdata.swiss/istdaten/2026/ist-daten-2026-01.zip` and `-03.zip`, single days read via HTTP Range | 08.01.2026, 21.03.2026, 28.03.2026 | 2,563,219 (08.01.2026) | 2026-11-03 | ER (Claude Code) |
| Service points (atlas) | `data.opentransportdata.swiss/dataset/service-point-v2`, `full-swiss-service-point.csv` (all versions), script `src/stops.py` | all versions | 157,877 rows, 73,201 stop numbers, 56 columns | 2026-11-03 | ER (Claude Code) |
| MeteoSwiss SMN, hourly | STAC `ch.meteoschweiz.ogd-smn`, 18 stations, `h_historical_2020-2029` + `h_recent`, script `src/weather.py` | 01.01.2020 – 02.11.2026 (PFA from 08.12.2022) | 59,952 hours per station (PFA 34,214) | 2026-11-03 | ER (Claude Code) |
| MeteoSwiss precipitation network, hourly | STAC `ch.meteoschweiz.ogd-smn-precip`, 16 stations used, `h_historical_2020-2029` + `h_recent`, script `src/weather.py` | 01.11.2023 – 31.03.2026 used | complete: 24 × days rows per month, 0 missing values (`tests/test_weather_complete.py`) | 2026-11-03 | ER (Claude Code) |
| Ist-Daten v1 (archive) | `archive.opentransportdata.swiss/istdaten/2026/ist-daten-2026-01.zip` (1.37 GB), entry page `archive.opentransportdata.swiss/actual_data_archive.htm`, script `src/istdaten.py` | prototype week 05.–11.01.2026 | 16,662,533 (7 days) | 2026-11-03 | ER (Claude Code) |
| Ist-Daten v1 (archive), full study period | 15 monthly ZIPs `ist-daten-YYYY-MM.zip`, Nov–Mar 2023/24–2025/26, 16 GB on disk (kept until after submission) | 454 days, 450 loaded | 1,005,650,252 | 2026-11-04 | ER (Claude Code) |
| MeteoSwiss manual stations (validation only) | STAC `ch.meteoschweiz.ogd-nime`, daily fresh snow `hns000d0`, 7 stations co-located with SMN | study period | – | 2026-11-04 | ER (Claude Code) |
| MeteoSwiss SMN, metadata | `ogd-smn_meta_stations.csv` (159 stations), `_meta_parameters.csv` (181 parameters), `_meta_datainventory.csv` | – | – | 2026-11-03 | ER (Claude Code) |

## Cleaning and filter steps

| Step | Table | Rule | Rows before | Rows after | Lost | Reason |
|---|---|---|---|---|---|---|
| F1 | service points | Swiss (`uicCountryCode` 85), `meansOfTransport` contains TRAIN, canton ZH, valid at any time 01.11.2023–31.03.2026, latest version per stop | 157,877 | 182 stops | 157,695 | study area = canton ZH, trains only; several versions per stop collapsed (coordinates identical across versions, checked) |
| F3 | Ist-Daten week 05.–11.01.2026 (`src/arrivals.py`, counts in `data/processed/build_log.csv`) | trains only, then all stops of trips that touch ZH (`whole_trips=True`, needed for the previous stop) | 16,662,533 | 287,497 trip rows | – | other modes and trips that never touch ZH |
| F3a | same | stop in ZH | 287,497 | 174,703 | 112,794 | stops outside ZH (kept only to compute `prev_dep_delay_min`) |
| F3b | same | scheduled arrival exists | 174,703 | 163,044 | 11,659 | first stop of a trip has no arrival |
| F3c | same | no pass-through (`DURCHFAHRT_TF`) | 163,044 | 163,001 | 43 | train does not stop |
| F3d | same | not cancelled (`FAELLT_AUS_TF`) | 163,001 | 161,264 | 1,737 | decision ER: cancellations excluded, count reported |
| F3e | same | `AN_PROGNOSE_STATUS = REAL` | 161,264 | 160,831 | 433 | decision ER: measured times only |
| F3f | same | category S or long-distance list | 160,831 | 158,988 | 1,843 | 1,830 night S-Bahn `SN` (Sat/Sun 00–04 h): excluded, decided by ER 2026-11-03, because no long-distance trains run at that time (night hours would exist for one group only); RJ (3/day) is long-distance since Checkpoint 2; EXT excluded |
| F3g | same | arrival delay between −15 and +300 min | 158,988 | 158,986 | 2 | implausible values (limits = proposal, Checkpoint 2) |
| F3h | same | local → UTC conversion | 158,986 | 158,986 | 0 | no time in the spring-forward gap (`tests/test_dst.py`) |
| F4 | Ist-Daten full study period (450 days, `python -m src.build_db --study-period`, `src/quality_report.py`) | same rules as F3, plus duplicates | 1,005,650,252 raw → 18,746,168 trip rows → 11,599,296 in ZH | 10,104,173 | – | see F4a–F4h |
| F4a | same | scheduled arrival exists | 11,599,296 | 10,811,815 | 787,481 | first stop of a trip |
| F4b | same | no pass-through | 10,811,815 | 10,809,325 | 2,490 | train does not stop |
| F4c | same | not cancelled | 10,809,325 | 10,666,795 | 142,530 | decision ER (count reported) |
| F4d | same | status REAL | 10,666,795 | 10,230,541 | 436,254 | decision ER |
| F4e | same | category S or long-distance (incl. RJ) | 10,230,541 | 10,107,193 | 123,348 | mainly night S-Bahn `SN`, EXT, PE |
| F4f | same | delay −15 … +300 min | 10,107,193 | 10,104,207 | 2,986 | implausible values |
| F4g | same | exact duplicate rows in the source | 10,104,207 | 10,104,173 | 34 | same trip, stop and time twice (6 days) |
| F4h | same | departure delays used as predictors: −15 … +300 min, source departure not after the arrival | 10,104,173 | 10,104,173 | 0 rows, 19 values set to NULL | data errors (e.g. RJX with −116 min) |
| F2 | Ist-Daten 21.10.2026 | `PRODUKT_ID = 'Zug'` and `BPUIC` in the 182 ZH stops, 16 of 23 columns kept | 2,583,004 | 25,549 | 2,557,455 | other modes (bus, tram …) and stops outside ZH. 156 of 182 stops have rows; the 26 missing are mostly Forchbahn S18 stops, which the data codes as `PRODUKT_ID = 'Tram'` with 9-digit BPUIC |

## Joins

| Step | Left | Right | Key(s) | Join type | Rows before | Rows after | Lost / gained | Reason |
|---|---|---|---|---|---|---|---|---|
| J1 (prototype, 2026-11-03) | 182 ZH train stops | 17 SMN stations (HOE excluded) | nearest neighbour in LV95 (EPSG:2056), `geopandas.sjoin_nearest` | left | 182 | 182 | 0 unmatched | every stop gets a station; median distance 7.4 km, max 14.9 km, 36 stops > 10 km (Winterthur area) |
| J2 → table `stop_station` (2026-11-03) | 182 ZH train stops | precipitation: 17 SMN + 142 `ogd-smn-precip` stations; temperature: 17 SMN | nearest neighbour in LV95, `sjoin_nearest`, ties → first station | left | 182 | 182 | 0 unmatched, 0 duplicates | precipitation: median 3.6 km, max 10.3 km, 1 stop > 10 km; temperature: median 7.4 km, max 14.9 km, 36 stops > 10 km. 26 stations used (`weather_stations`) |

| J3 → table `analysis_base` (SQL, `src/analysis_base.sql`) | `arrivals` (week 05.–11.01.2026) | `stops`, `stop_station`, `weather_hourly` (twice: precipitation station, temperature station), `calendar_days` | `bpuic`; (`precip_station`, `weather_hour_utc`) = (`station_abbr`, `time_utc`); (`temp_station`, `weather_hour_utc`); `local_date` | inner (stops, stop_station), left (weather, calendar) | 158,986 | 158,986 | 0 lost; 0 without precipitation, 0 without temperature, 0 without calendar | weather hour = scheduled arrival in UTC floored to the hour = last full hour before arrival. 5 rows checked by hand against the raw CSV and the raw MeteoSwiss files: all match (Checkpoint 2) |

| J4 → `analysis_base` full period | `arrivals` (10,104,173) | as J3 | as J3 | as J3 | 10,104,173 | 10,104,173 | 0 lost; 0 without precipitation, 26 without temperature (sensor gaps, all dry hours, so `precip_cat` is set), 0 without calendar | quality report `data/processed/quality_report.md`; tests `test_dst`, `test_weather_complete`, `test_entry_delay` pass |

## Inconsistencies found

| Date | Description | Affected rows | Decision |
|---|---|---|---|
| 2026-11-03 | Cookbook example shows comma separator and an `_id` column; real portal and archive files use `;` and have no `_id` | all | read with `sep=";"`, checked on real files |
| 2026-11-03 | Time zone not documented in the cookbook | all | verified on data: local time (see research-design, VERIFY) |
| 2026-11-03 | `PRODUKT_ID` has both `Bus` and `BUS` | 71,179 rows on 08.01.2026 (not trains) | irrelevant, we filter on `Zug` |
| 2026-11-03 | Forchbahn S18 coded as `Tram` (operator FB, 9-digit BPUIC) | 26 ZH "train" stops without rows | open: proposal to exclude S18 (tram-like light rail), see Checkpoint 1 |
| 2026-11-03 | Single extreme delays, e.g. −1444 min (08.01.2026, Switzerland-wide); one EC with BETRIEBSTAG 08.01. arriving 09.01. 09:05 | few | to handle in cleaning (Phase 2): plausibility limits |
| 2026-11-03 | Night S-Bahn coded `SN` (not `S`), Railjet `RJ` (not `RJX`) | 1,843 rows in the week | decided by ER: `SN` excluded (night hours only in regional traffic), `RJ` = long-distance |
| 2026-11-03 | No official Christmas school-holiday dates found for 2023/24 and 2024/25 | calendar | derived from the binding canton rule (KW 52 + KW 1), marked as derived in `src/calendar_zh.py` |
| 2026-11-04 | Snow definition vs. measured fresh snow (`ogd-nime`, 7 co-located stations) | 3,161 station-days | hit rate 75 %, precision 65 % → definition kept, limitation named |
| 2026-11-03 | 21.10.2026: 1,169 cancelled rows at ZH stops (4.6 %), 686 of them S10 (SZU) | 1,169 | VERIFY cause (planned construction work?) |
| 2026-11-04 | Archive ZIP 2025-01: the days 28.–31.01.2025 are compressed with **Deflate64** (ZIP method 9), which Python's `zipfile` and Windows `tar` cannot read | 4 of 454 days missing | open: proposal to add the package `zipfile-deflate64` (needs ER's OK); the build logs them as ERROR and loads them on the next run |
| 2026-11-04 | 34 exact duplicate rows in the source (6 days, lines S17, S29, S1, IR35, IR46) | 34 | removed (F4g) |
| 2026-11-04 | Night trains of 31.03.2026 arrive on 01.04. → no calendar day | 523 | calendar extended to 01.04.2026 |
| 2026-11-04 | Departure at the stop before the area scheduled after the area arrival (RJX, 09.03.2024, −116 min); 18 implausible departure delays | 19 values | set to NULL (F4h); test `test_entry_delay` checks it |
