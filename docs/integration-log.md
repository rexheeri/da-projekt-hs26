# Data integration log

Required for grading: document how the sources were combined – keys, joins, inconsistencies, records lost or gained.

## Sources

| Source | File / endpoint | Period | Rows (raw) | Retrieved on | By |
|---|---|---|---|---|---|
| Ist-Daten v2 (portal) | `data.opentransportdata.swiss/dataset/ist-daten-v2`, file list from the DCAT catalogue `dataset_series/2091d9b2-….jsonld`, script `src/istdaten.py` | 21.10.2026 (prototype day) | 2,583,004 (655.7 MB CSV, 22 columns, `;`, UTF-8) | 2026-11-03 | ER (Claude Code) |
| Ist-Daten v1 (archive), exploration only | `archive.opentransportdata.swiss/istdaten/2026/ist-daten-2026-01.zip` and `-03.zip`, single days read via HTTP Range | 08.01.2026, 21.03.2026, 28.03.2026 | 2,563,219 (08.01.2026) | 2026-11-03 | ER (Claude Code) |
| Service points (atlas) | `data.opentransportdata.swiss/dataset/service-point-v2`, `full-swiss-service-point.csv` (all versions), script `src/stops.py` | all versions | 157,877 rows, 73,201 stop numbers, 56 columns | 2026-11-03 | ER (Claude Code) |
| MeteoSwiss SMN, hourly | STAC `ch.meteoschweiz.ogd-smn`, 18 stations, `h_historical_2020-2029` + `h_recent`, script `src/weather.py` | 01.01.2020 – 02.11.2026 (PFA from 08.12.2022) | 59,952 hours per station (PFA 34,214) | 2026-11-03 | ER (Claude Code) |
| MeteoSwiss SMN, metadata | `ogd-smn_meta_stations.csv` (159 stations), `_meta_parameters.csv` (181 parameters), `_meta_datainventory.csv` | – | – | 2026-11-03 | ER (Claude Code) |

## Cleaning and filter steps

| Step | Table | Rule | Rows before | Rows after | Lost | Reason |
|---|---|---|---|---|---|---|
| F1 | service points | Swiss (`uicCountryCode` 85), `meansOfTransport` contains TRAIN, canton ZH, valid at any time 01.11.2023–31.03.2026, latest version per stop | 157,877 | 182 stops | 157,695 | study area = canton ZH, trains only; several versions per stop collapsed (coordinates identical across versions, checked) |
| F2 | Ist-Daten 21.10.2026 | `PRODUKT_ID = 'Zug'` and `BPUIC` in the 182 ZH stops, 16 of 23 columns kept | 2,583,004 | 25,549 | 2,557,455 | other modes (bus, tram …) and stops outside ZH. 156 of 182 stops have rows; the 26 missing are mostly Forchbahn S18 stops, which the data codes as `PRODUKT_ID = 'Tram'` with 9-digit BPUIC |

## Joins

| Step | Left | Right | Key(s) | Join type | Rows before | Rows after | Lost / gained | Reason |
|---|---|---|---|---|---|---|---|---|
| J1 (prototype, not yet in DB) | 182 ZH train stops | 17 SMN stations (HOE excluded) | nearest neighbour in LV95 (EPSG:2056), `geopandas.sjoin_nearest` | left | 182 | 182 | 0 unmatched | every stop gets a station; median distance 7.4 km, max 14.9 km, 36 stops > 10 km (Winterthur area) |

## Inconsistencies found

| Date | Description | Affected rows | Decision |
|---|---|---|---|
| 2026-11-03 | Cookbook example shows comma separator and an `_id` column; real portal and archive files use `;` and have no `_id` | all | read with `sep=";"`, checked on real files |
| 2026-11-03 | Time zone not documented in the cookbook | all | verified on data: local time (see research-design, VERIFY) |
| 2026-11-03 | `PRODUKT_ID` has both `Bus` and `BUS` | 71,179 rows on 08.01.2026 (not trains) | irrelevant, we filter on `Zug` |
| 2026-11-03 | Forchbahn S18 coded as `Tram` (operator FB, 9-digit BPUIC) | 26 ZH "train" stops without rows | open: proposal to exclude S18 (tram-like light rail), see Checkpoint 1 |
| 2026-11-03 | Single extreme delays, e.g. −1444 min (08.01.2026, Switzerland-wide); one EC with BETRIEBSTAG 08.01. arriving 09.01. 09:05 | few | to handle in cleaning (Phase 2): plausibility limits |
| 2026-11-03 | 21.10.2026: 1,169 cancelled rows at ZH stops (4.6 %), 686 of them S10 (SZU) | 1,169 | VERIFY cause (planned construction work?) |
