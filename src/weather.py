"""Weather data from MeteoSwiss Open Data (automatic weather stations, SMN) via the STAC API.

Source: STAC collection 'ch.meteoschweiz.ogd-smn' on https://data.geo.admin.ch/api/stac/v1
Docs:   https://opendatadocs.meteoswiss.ch (Source: MeteoSwiss, licence CC BY 4.0)

What this module does:
1. Ask the STAC API which files exist for each station (one STAC "item" per station).
2. Download the station metadata, the parameter list and the hourly files
   (historical = until 31 Dec of last year, recent = 1 Jan this year until yesterday).
3. Read the hourly files into one tidy table: station, time (UTC), precipitation,
   temperature, snow depth.

Facts verified from the source (see docs/research-design.md, VERIFY results):
- All MeteoSwiss timestamps are UTC.
- Hourly values: the timestamp is the END of the interval
  ("ReferenceTS 16:00 = 15:10 to 16:00"). Example: 07:00 UTC = precipitation 06:10-07:00 UTC.
- Files: semicolon-separated, decimal point, Windows-1252 encoding, missing value = empty field.

Usage (from the repo root):
    python -m src.weather              # downloads metadata + hourly files for STATIONS
"""
import pandas as pd
from pystac_client import Client

from src.download import download_file
from src.paths import RAW_DIR

STAC_URL = "https://data.geo.admin.ch/api/stac/v1"
COLLECTION = "ch.meteoschweiz.ogd-smn"
WEATHER_DIR = RAW_DIR / "weather"

# Parameter codes, taken from ogd-smn_meta_parameters.csv (not guessed):
PARAMS = {
    "rre150h0": "precip_mm",  # Precipitation; hourly total (mm)
    "tre200h0": "temp_c",     # Air temperature 2 m above ground; hourly mean (degC)
    "htoauths": "snow_cm",    # Snow depth (automatic measurement); hourly current value (cm)
}

# Candidate stations in and around the canton of Zurich that measure hourly
# precipitation and temperature (from ogd-smn_meta_datainventory.csv).
# The final list = stations that are the nearest station of at least one stop.
STATIONS = [
    "SMA", "REH", "KLO", "PFA", "WAE", "TAE", "HOE",   # canton ZH
    "CHZ", "PSI", "BEZ", "LAC", "SHA", "HLL", "BUS", "EIN", "MOA", "SAG", "LEI",  # neighbours
]

# Which hourly files we need: historical (2020-2029 decade file, until 31 Dec 2025)
# and recent (1 Jan 2026 until yesterday). Winter 2025/26 needs both.
HOURLY_FILES = ["h_historical_2020-2029", "h_recent"]

META_FILES = ["ogd-smn_meta_stations.csv", "ogd-smn_meta_parameters.csv",
              "ogd-smn_meta_datainventory.csv"]


def station_assets(station):
    """Return {file name: download URL} for one station, read from the STAC API.

    We ask the API instead of building URLs by hand, so the code keeps working
    if MeteoSwiss changes the file layout.
    """
    item = Client.open(STAC_URL).get_collection(COLLECTION).get_item(station.lower())
    return {name: asset.href for name, asset in item.assets.items()}


def download_meta():
    """Download the three metadata files (stations, parameters, data inventory)."""
    collection = Client.open(STAC_URL).get_collection(COLLECTION)
    for name in META_FILES:
        download_file(collection.assets[name].href, WEATHER_DIR / "meta" / name)


def download_hourly(stations=STATIONS):
    """Download the hourly files (historical + recent) for each station.

    Note: 'recent' changes every day. The downloader skips existing files, so
    delete data/raw/weather/hourly/*_h_recent.csv to refresh it.
    """
    for st in stations:
        assets = station_assets(st)
        for kind in HOURLY_FILES:
            name = f"ogd-smn_{st.lower()}_{kind}.csv"
            download_file(assets[name], WEATHER_DIR / "hourly" / name)


def read_stations():
    """Station metadata: abbreviation, name, canton, height (m a.s.l.), LV95 coordinates."""
    df = pd.read_csv(WEATHER_DIR / "meta" / "ogd-smn_meta_stations.csv", sep=";", encoding="cp1252")
    cols = {
        "station_abbr": "station_abbr",
        "station_name": "station_name",
        "station_canton": "station_canton",
        "station_height_masl": "height_masl",
        "station_coordinates_lv95_east": "lv95_east",
        "station_coordinates_lv95_north": "lv95_north",
    }
    return df[list(cols)].rename(columns=cols)


def read_hourly(stations=STATIONS):
    """Read the hourly files of all stations into one table.

    Columns: station_abbr, time_utc (end of the hourly interval, tz-aware UTC),
    precip_mm, temp_c, snow_cm (NaN where the station does not measure it).
    """
    frames = []
    for st in stations:
        for kind in HOURLY_FILES:
            path = WEATHER_DIR / "hourly" / f"ogd-smn_{st.lower()}_{kind}.csv"
            # usecols with a callable: keep only the columns we need, if present
            df = pd.read_csv(path, sep=";", encoding="cp1252",
                             usecols=lambda c: c in ["station_abbr", "reference_timestamp", *PARAMS])
            frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    # Timestamps are UTC (MeteoSwiss docs) -> parse and attach the time zone explicitly
    df["time_utc"] = pd.to_datetime(df["reference_timestamp"], format="%d.%m.%Y %H:%M").dt.tz_localize("UTC")
    df = df.drop(columns="reference_timestamp").rename(columns=PARAMS)

    # A station without a snow sensor has no snow column at all -> add it as empty
    for col in PARAMS.values():
        if col not in df.columns:
            df[col] = float("nan")
    return df[["station_abbr", "time_utc", "precip_mm", "temp_c", "snow_cm"]]


if __name__ == "__main__":
    download_meta()
    download_hourly()
    hourly = read_hourly()
    print(hourly.groupby("station_abbr")["time_utc"].agg(["min", "max", "count"]))
