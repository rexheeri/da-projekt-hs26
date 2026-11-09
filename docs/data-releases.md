# Data releases

The prepared tables (team export from `src/export_shared.py`) are attached as
files to GitHub releases of this repo. They are **never committed** to the repo
(`.gitignore` stays). A newer export gets a new tag (`data-v2`, …); old
releases stay, so every result can be traced back to the data it used.

Get and load a release: `python -m src.load_shared --release data-v1`
(details in `onboarding.md` § 9).

## Terms of use of the sources (checked 2026-11-04)

Both sources allow publishing processed data, with a citation.

| Source | Terms | Publishing derived data | Mandatory citation | Other conditions |
|---|---|---|---|---|
| Ist-Daten and service points, opentransportdata.swiss | "General Terms and Conditions of Use", no licence name. https://opentransportdata.swiss/en/terms-of-use/ (the German version is binding: https://opentransportdata.swiss/de/terms-of-use/). The dataset pages `ist-daten-v2` and `service-point-v2` link there. | **allowed**. § 1: "The data obtained can be processed, analysed and published, including incorporating additional data." | § 5.1: "The URL opentransportdata.swiss must be cited as the source for raw data in publications and analyses that make use of ODMCH data." | § 5.3: "Processed data and analyses must be published under the name of the data user" (us, not SBB). § 5.2 requires data to be "updated regularly and at the same frequency as the underlying raw data"; our release is a fixed snapshot of **historical archive data** (Nov–Mar 2023/24–2025/26), which does not change. **VERIFY**: the terms don't say how § 5.2 applies to snapshots (risk accepted, see below). |
| MeteoSwiss Open Data (`ogd-smn`, `ogd-smn-precip`, `ogd-nime`) | **CC BY 4.0**. https://opendatadocs.meteoswiss.ch/general/terms-of-use; STAC collection field `"license": "CC-BY"` | **allowed**: "copy and redistribute the data in any format or medium for any purpose, even commercially" | "Source: MeteoSwiss" | must not look as if MeteoSwiss endorses our work; no excessive downloading. The FSDI terms also apply: https://www.geo.admin.ch/en/general-terms-of-use-fsdi |

Not checked: the per-dataset legal notes on geocat.ch (linked from the STAC
collections) and the full CC BY 4.0 legal text. Neither changes the result
above as far as the pages read say.

**§ 5.2 (regular updates), decided 2026-11-09 (ER):** VERIFY not resolved,
risk **knowingly accepted**. Our releases are fixed snapshots of historical
archive data, labelled as such in every release note. If the provider objects,
we take the release down.

## data-v1 (published 2026-11-09)

https://github.com/rexheeri/da-projekt-hs26/releases/tag/data-v1

- Tag `data-v1` on `main` at `5167de1` (the first commit with
  `load_shared --release`). The data itself was built with pipeline commit
  `c79b133`: the export (2026-11-04 01:18) already contains the entry-delay
  safety rules committed at 01:22, checked on the data (4,258,093 non-null
  `entry_delay_min`, 0 values outside −15 … +300).
- 7 assets: `manifest.csv` + 6 Parquet files (~81 MB). Size and SHA-256 digest
  of every asset checked against the local files before publishing.
- Checked after publishing (2026-11-09): all 7 download URLs answer HTTP 200
  without login, with the right size; `python -m src.load_shared --release data-v1`
  in a fresh clone loads all 6 tables with the manifest row counts
  (8.5 min incl. download, SQLite file 2.36 GB); `gh release download` gives
  identical checksums.
- The tests `tests.test_weather_complete` and `tests.test_entry_delay` need the
  raw weather CSVs and the `arrivals` table, which are not in the release. They
  only run after a full rebuild (README option B); `tests.test_dst` skips its
  real-data check (#45).
- Licence decided: **CC BY 4.0**.
- Known gap: 28.–31.01.2025 missing (Deflate64 extraction) → data-v2.
- `manifest.csv` has no checksums yet → planned from data-v2 (#46).

Release notes (final text, identical on GitHub):

> **Team data export data-v1**
>
> Prepared tables of the ZHAW Data Analytics group project HS 2026, group 3
> (members: see README). Processed and published by group 3.
>
> - **Period:** winter half-year (Nov–Mar) 2023/24, 2024/25, 2025/26, canton of Zurich, train arrivals
> - **Coverage:** 450 of 454 days, 10,104,173 rows in analysis_base. 28.–31.01.2025 missing (Deflate64 extraction), will follow in data-v2.
> - **Rows:** analysis_base 10,104,173 · weather_hourly 548,955 · calendar_days 883 · stops 182 · stop_station 182 · weather_stations 26
> - **Created:** 2026-11-04 (export) · **Published:** 2026-11-09 · **Pipeline commit:** c79b133 (`python -m src.build_db --study-period`, `python -m src.export_shared`)
> - **Load:** `python -m src.load_shared --release data-v1`
> - **Sources (mandatory citation):** Ist-Daten and service points: source of raw data **opentransportdata.swiss**. Weather: **Source: MeteoSwiss** (CC BY 4.0). MeteoSwiss does not endorse this work.
> - **Licence of this export:** CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); the source citations above are required as well.
> - Fixed snapshot of historical archive data; it is not updated. Not an official SBB or MeteoSwiss product.
