"""Ist-Daten (actual arrival/departure times per stop and day) from opentransportdata.swiss.

Two ways to get the daily files, both by script:
1. Data portal (dataset 'ist-daten-v2'): the last ~30 days as one CSV per day.
   The list of files is read from the portal's machine-readable DCAT catalogue
   (JSON-LD). Note: the CKAN action API (/api/3/action/...) answers 403, so we
   use the catalogue instead.
2. Archive (archive.opentransportdata.swiss): one ZIP per month with one CSV per
   day, from 2016 until the last full month. Needed for past winters.

Facts verified on real files (see docs/research-design.md, VERIFY results):
- Semicolon-separated, UTF-8, 22 columns (BETRIEBSTAG ... DURCHFAHRT_TF, SLOID).
- Times are Swiss local time (Europe/Zurich): in the night of the switch to
  summer time (29.03.2026) there is not a single arrival between 02:00 and 02:59.
- ANKUNFTSZEIT = scheduled arrival (minutes), AN_PROGNOSE = actual/forecast
  arrival (seconds), AN_PROGNOSE_STATUS = REAL / PROGNOSE / UNBEKANNT / empty.

Usage (from the repo root):
    python -m src.istdaten 2026-11-02       # download one day from the portal and filter it
"""
import json
import sys
import zipfile

import pandas as pd
import requests

from src.download import HEADERS, download_file
from src.paths import PROCESSED_DIR, RAW_DIR

PORTAL_CATALOG = ("https://data.opentransportdata.swiss/dataset_series/"
                  "2091d9b2-8012-4d70-bf90-214ee6a9b458.jsonld")
ARCHIVE_URL = "https://archive.opentransportdata.swiss/istdaten/{year}/ist-daten-{year}-{month:02d}.zip"
IST_DIR = RAW_DIR / "istdaten"

# Columns we keep. Departure columns stay because the departure delay at the
# previous stop is known before the next arrival (needed for delay_gain).
KEEP_COLS = [
    "BETRIEBSTAG", "FAHRT_BEZEICHNER", "BETREIBER_ABK", "LINIEN_TEXT", "VERKEHRSMITTEL_TEXT",
    "ZUSATZFAHRT_TF", "FAELLT_AUS_TF", "BPUIC", "HALTESTELLEN_NAME",
    "ANKUNFTSZEIT", "AN_PROGNOSE", "AN_PROGNOSE_STATUS",
    "ABFAHRTSZEIT", "AB_PROGNOSE", "AB_PROGNOSE_STATUS", "DURCHFAHRT_TF",
]


def portal_days():
    """Return {'YYYY-MM-DD': download URL} for all daily files currently on the portal."""
    r = requests.get(PORTAL_CATALOG, headers=HEADERS, timeout=120)
    r.raise_for_status()
    graph = r.json()["@graph"]
    days = {}
    for node in graph:
        # Each daily file is a DCAT 'Distribution' with a downloadURL
        if node.get("@type") == "dcat:Distribution":
            url = node["dcat:downloadURL"]["@id"]
            day = url.rsplit("/", 1)[1][:10]  # file name starts with the date, e.g. 2026-11-02_istdaten.csv
            days[day] = url
    return dict(sorted(days.items()))


def download_portal_day(day):
    """Download one day (format 'YYYY-MM-DD') from the portal into data/raw/istdaten/portal/."""
    days = portal_days()
    if day not in days:
        raise ValueError(f"{day} is not on the portal. Available: {min(days)} to {max(days)}")
    return download_file(days[day], IST_DIR / "portal" / f"{day}_istdaten.csv", timeout=180)


def download_archive_month(year, month):
    """Download one monthly ZIP from the archive (about 1.0-1.4 GB) into data/raw/istdaten/archive/."""
    url = ARCHIVE_URL.format(year=year, month=month)
    return download_file(url, IST_DIR / "archive" / url.rsplit("/", 1)[1], timeout=180)


def zip_members(zip_path):
    """List the daily CSV files inside a monthly ZIP as {'YYYY-MM-DD': member name}."""
    with zipfile.ZipFile(zip_path) as z:
        return {name[:10]: name for name in z.namelist() if name.lower().endswith(".csv")}


def read_day(source, stop_ids, whole_trips=False, chunksize=500_000):
    """Read one daily file and keep only train rows at the given stops.

    source:      path to a CSV, or an open file object (e.g. from zipfile, no unpacking needed)
    stop_ids:    set of BPUIC strings (7 digits) of the study area
    whole_trips: False -> only rows at the study-area stops.
                 True  -> all stops of every train trip that touches the study
                 area (needed to know the stop BEFORE the first stop in the area).
    Returns (filtered DataFrame, number of raw rows).

    The file is read in chunks of 500k rows, so memory stays low even for 650 MB files.
    """
    parts, n_raw = [], 0
    reader = pd.read_csv(source, sep=";", dtype=str, encoding="utf-8",
                         usecols=KEEP_COLS + ["PRODUKT_ID"], chunksize=chunksize)
    for chunk in reader:
        n_raw += len(chunk)
        # Filter early: trains only (and, unless whole trips are needed, only study-area stops)
        mask = chunk["PRODUKT_ID"] == "Zug"
        if not whole_trips:
            mask &= chunk["BPUIC"].isin(stop_ids)
        parts.append(chunk.loc[mask, KEEP_COLS])
    df = pd.concat(parts, ignore_index=True)
    if whole_trips:
        # Keep the trips with at least one stop in the study area
        trips = set(df.loc[df["BPUIC"].isin(stop_ids), "FAHRT_BEZEICHNER"])
        df = df[df["FAHRT_BEZEICHNER"].isin(trips)].reset_index(drop=True)
    return df, n_raw


def read_day_from_zip(zip_path, day, stop_ids, whole_trips=False):
    """Read one day directly from a monthly ZIP (no unpacking to disk)."""
    member = zip_members(zip_path)[day]
    with zipfile.ZipFile(zip_path) as z, z.open(member) as f:
        return read_day(f, stop_ids, whole_trips=whole_trips)


if __name__ == "__main__":
    from src.stops import load_train_stops

    day = sys.argv[1] if len(sys.argv) > 1 else max(portal_days())
    path = download_portal_day(day)
    stops = set(load_train_stops()["bpuic"])
    df, n_raw = read_day(path, stops)
    out = PROCESSED_DIR / "istdaten" / f"{day}_zh_trains.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"{day}: {n_raw} raw rows -> {len(df)} train rows at {len(stops)} ZH stops -> {out.name}")
    print(json.dumps({"columns": list(df.columns)}, indent=1))
