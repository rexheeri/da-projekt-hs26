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
| Ist-Daten and service points, opentransportdata.swiss | "General Terms and Conditions of Use", no licence name. https://opentransportdata.swiss/en/terms-of-use/ (the German version is binding: https://opentransportdata.swiss/de/terms-of-use/). The dataset pages `ist-daten-v2` and `service-point-v2` link there. | **allowed**. § 1: "The data obtained can be processed, analysed and published, including incorporating additional data." | § 5.1: "The URL opentransportdata.swiss must be cited as the source for raw data in publications and analyses that make use of ODMCH data." | § 5.3: "Processed data and analyses must be published under the name of the data user" (us, not SBB). § 5.2 requires data to be "updated regularly and at the same frequency as the underlying raw data"; our release is a fixed snapshot of **historical archive data** (Nov–Mar 2023/24–2025/26), which does not change. **VERIFY**: the terms don't say how § 5.2 applies to snapshots. |
| MeteoSwiss Open Data (`ogd-smn`, `ogd-smn-precip`, `ogd-nime`) | **CC BY 4.0**. https://opendatadocs.meteoswiss.ch/general/terms-of-use; STAC collection field `"license": "CC-BY"` | **allowed**: "copy and redistribute the data in any format or medium for any purpose, even commercially" | "Source: MeteoSwiss" | must not look as if MeteoSwiss endorses our work; no excessive downloading. The FSDI terms also apply: https://www.geo.admin.ch/en/general-terms-of-use-fsdi |

Not checked: the per-dataset legal notes on geocat.ch (linked from the STAC
collections) and the full CC BY 4.0 legal text. Neither changes the result
above as far as the pages read say.

## data-v1 (draft, not published yet)

Release notes text, filled in once the 4 missing days are loaded:

> **Team data export data-v1**
>
> Prepared tables of the ZHAW Data Analytics group project HS 2026, group 3
> (members: see README). Processed and published by group 3.
>
> - **Period:** winter half-year (Nov–Mar) 2023/24, 2024/25, 2025/26 (454 days),
>   canton of Zurich, train arrivals
> - **Rows:** analysis_base …, weather_hourly …, calendar_days …, stops 182,
>   stop_station 182, weather_stations 26
> - **Created:** … · **Pipeline commit:** … (`python -m src.build_db --study-period`, `python -m src.export_shared`)
> - **Load:** `python -m src.load_shared --release data-v1`
> - **Sources (mandatory citation):** Ist-Daten and service points: source
>   of raw data **opentransportdata.swiss**. Weather: **Source: MeteoSwiss**
>   (CC BY 4.0). MeteoSwiss does not endorse this work.
> - **Licence of this export:** DECIDE (proposal: CC BY 4.0, same citations required)
> - Fixed snapshot of historical data; it is not updated. Not an official SBB
>   or MeteoSwiss product.
