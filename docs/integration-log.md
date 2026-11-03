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
| F3f | same | category S or long-distance list | 160,831 | 158,988 | 1,843 | 1,830 night S-Bahn `SN` (Sat/Sun 00–04 h), RJ, EXT → decision pending (Checkpoint 2) |
| F3g | same | arrival delay between −15 and +300 min | 158,988 | 158,986 | 2 | implausible values (limits = proposal, Checkpoint 2) |
| F3h | same | local → UTC conversion | 158,986 | 158,986 | 0 | no time in the spring-forward gap (`tests/test_dst.py`) |
| F2 | Ist-Daten 21.10.2026 | `PRODUKT_ID = 'Zug'` and `BPUIC` in the 182 ZH stops, 16 of 23 columns kept | 2,583,004 | 25,549 | 2,557,455 | other modes (bus, tram …) and stops outside ZH. 156 of 182 stops have rows; the 26 missing are mostly Forchbahn S18 stops, which the data codes as `PRODUKT_ID = 'Tram'` with 9-digit BPUIC |

## Joins

| Step | Left | Right | Key(s) | Join type | Rows before | Rows after | Lost / gained | Reason |
|---|---|---|---|---|---|---|---|---|
| J1 (prototype, 2026-11-03) | 182 ZH train stops | 17 SMN stations (HOE excluded) | nearest neighbour in LV95 (EPSG:2056), `geopandas.sjoin_nearest` | left | 182 | 182 | 0 unmatched | every stop gets a station; median distance 7.4 km, max 14.9 km, 36 stops > 10 km (Winterthur area) |
| J2 → table `stop_station` (2026-11-03) | 182 ZH train stops | precipitation: 17 SMN + 142 `ogd-smn-precip` stations; temperature: 17 SMN | nearest neighbour in LV95, `sjoin_nearest`, ties → first station | left | 182 | 182 | 0 unmatched, 0 duplicates | precipitation: median 3.6 km, max 10.3 km, 1 stop > 10 km; temperature: median 7.4 km, max 14.9 km, 36 stops > 10 km. 26 stations used (`weather_stations`) |

| J3 → table `analysis_base` (SQL, `src/analysis_base.sql`) | `arrivals` (week 05.–11.01.2026) | `stops`, `stop_station`, `weather_hourly` (twice: precipitation station, temperature station), `calendar_days` | `bpuic`; (`precip_station`, `weather_hour_utc`) = (`station_abbr`, `time_utc`); (`temp_station`, `weather_hour_utc`); `local_date` | inner (stops, stop_station), left (weather, calendar) | 158,986 | 158,986 | 0 lost; 0 without precipitation, 0 without temperature, 0 without calendar | weather hour = scheduled arrival in UTC floored to the hour = last full hour before arrival. 5 rows checked by hand against the raw CSV and the raw MeteoSwiss files: all match (Checkpoint 2) |

## Inconsistencies found

| Date | Description | Affected rows | Decision |
|---|---|---|---|
| 2026-11-03 | Cookbook example shows comma separator and an `_id` column; real portal and archive files use `;` and have no `_id` | all | read with `sep=";"`, checked on real files |
| 2026-11-03 | Time zone not documented in the cookbook | all | verified on data: local time (see research-design, VERIFY) |
| 2026-11-03 | `PRODUKT_ID` has both `Bus` and `BUS` | 71,179 rows on 08.01.2026 (not trains) | irrelevant, we filter on `Zug` |
| 2026-11-03 | Forchbahn S18 coded as `Tram` (operator FB, 9-digit BPUIC) | 26 ZH "train" stops without rows | open: proposal to exclude S18 (tram-like light rail), see Checkpoint 1 |
| 2026-11-03 | Single extreme delays, e.g. −1444 min (08.01.2026, Switzerland-wide); one EC with BETRIEBSTAG 08.01. arriving 09.01. 09:05 | few | to handle in cleaning (Phase 2): plausibility limits |
| 2026-11-03 | Night S-Bahn coded `SN` (not `S`), Railjet `RJ` (not `RJX`) | 1,843 rows in the week | excluded for now, decision at Checkpoint 2 |
| 2026-11-03 | 21.10.2026: 1,169 cancelled rows at ZH stops (4.6 %), 686 of them S10 (SZU) | 1,169 | VERIFY cause (planned construction work?) |
