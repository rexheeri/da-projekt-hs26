"""Weather data from MeteoSwiss Open Data via the STAC API.

Two station networks (decided by ER on 2026-11-03):
- 'smn'    = automatic weather stations, STAC collection 'ch.meteoschweiz.ogd-smn'
             (precipitation, temperature, snow depth)
- 'precip' = automatic precipitation stations, 'ch.meteoschweiz.ogd-smn-precip'
             (precipitation only, but many more stations, e.g. Winterthur)
Each stop gets its precipitation from the nearest station of both networks and
its temperature from the nearest SMN station (see src/stops.py).

Source: https://data.geo.admin.ch/api/stac/v1 (Source: MeteoSwiss, licence CC BY 4.0)
Docs:   https://opendatadocs.meteoswiss.ch/general/download

What this module does:
1. Ask the STAC API which files exist for each station (one STAC "item" per station).
2. Download the station metadata and the hourly files:
   'historical' = start of measurement until 31 Dec of last year (decade file 2020-2029),
   'recent'     = 1 Jan of this year until yesterday (re-checked with ETag on every run).
3. Read the hourly files into one tidy table: station, time (UTC), precipitation,
   temperature, snow depth. historical + recent are joined without gap or duplicate.

Facts verified from the source (see docs/research-design.md, VERIFY results):
- All MeteoSwiss timestamps are UTC, format dd.mm.yyyy HH:MM.
- Hourly values: the timestamp is the END of the interval ("16:00 = 15:10 to 16:00").
- Files: semicolon-separated, decimal point, Windows-1252, missing value = empty field.

Usage (from the repo root):
    python -m src.weather              # metadata + hourly files of the SMN candidate stations
"""
import pandas as pd
from pystac_client import Client

from src.download import download_file
from src.paths import RAW_DIR

STAC_URL = "https://data.geo.admin.ch/api/stac/v1"
COLLECTIONS = {
    "smn": "ch.meteoschweiz.ogd-smn",
    "precip": "ch.meteoschweiz.ogd-smn-precip",
    "nime": "ch.meteoschweiz.ogd-nime",  # manual stations: daily fresh snow, used only to validate the snow definition
}
WEATHER_DIR = RAW_DIR / "weather"

# Parameter codes, taken from the *_meta_parameters.csv files (not guessed):
PARAMS = {
    "rre150h0": "precip_mm",  # Precipitation; hourly total (mm)
    "tre200h0": "temp_c",     # Air temperature 2 m above ground; hourly mean (degC)
    "htoauths": "snow_cm",    # Snow depth (automatic measurement); hourly current value (cm)
}

# SMN stations in and around the canton of Zurich with hourly precipitation and
# temperature (from ogd-smn_meta_datainventory.csv). HOE (Hoernli, 1133 m, summit
# station) is excluded: it would be the nearest station for Toesstal stops that
# lie 380-530 m lower (decided by ER on 2026-11-03).
STATIONS = [
    "SMA", "REH", "KLO", "PFA", "WAE", "TAE",                                      # canton ZH
    "CHZ", "PSI", "BEZ", "LAC", "SHA", "HLL", "BUS", "EIN", "MOA", "SAG", "LEI",  # neighbours
]
EXCLUDED_STATIONS = {"HOE"}

# Which hourly files we need. Winter 2025/26 needs both (historical ends 31.12.2025).
HOURLY_FILES = ["h_historical_2020-2029", "h_recent"]


def collection(network):
    """Return the STAC collection object of a network ('smn' or 'precip')."""
    return Client.open(STAC_URL).get_collection(COLLECTIONS[network])


def station_assets(station, network="smn"):
    """Return {file name: download URL} for one station, read from the STAC API.

    We ask the API instead of building URLs by hand, so the code keeps working
    if MeteoSwiss changes the file layout.
    """
    item = collection(network).get_item(station.lower())
    return {name: asset.href for name, asset in item.assets.items()}


def download_meta(network="smn"):
    """Download the metadata files of a network (stations, parameters, data inventory)."""
    col = collection(network)
    for name, asset in col.assets.items():
        if "_meta_" in name:
            download_file(asset.href, WEATHER_DIR / "meta" / name)


def download_hourly(stations=STATIONS, network="smn"):
    """Download the hourly files (historical + recent) for each station.

    'historical' never changes during the year -> downloaded once.
    'recent' changes every day -> re-checked with the ETag (refresh=True).
    """
    prefix = COLLECTIONS[network].split(".")[-1]  # e.g. 'ogd-smn' or 'ogd-smn-precip'
    for st in stations:
        assets = station_assets(st, network)
        for kind in HOURLY_FILES:
            name = f"{prefix}_{st.lower()}_{kind}.csv"
            download_file(assets[name], WEATHER_DIR / "hourly" / name, refresh=(kind == "h_recent"))


def read_stations(network="smn"):
    """Station metadata: abbreviation, name, canton, height (m a.s.l.), LV95 coordinates, network."""
    prefix = COLLECTIONS[network].split(".")[-1]
    df = pd.read_csv(WEATHER_DIR / "meta" / f"{prefix}_meta_stations.csv", sep=";", encoding="cp1252")
    cols = {
        "station_abbr": "station_abbr",
        "station_name": "station_name",
        "station_canton": "station_canton",
        "station_height_masl": "height_masl",
        "station_coordinates_lv95_east": "lv95_east",
        "station_coordinates_lv95_north": "lv95_north",
    }
    out = df[list(cols)].rename(columns=cols)
    out["network"] = network
    return out


def read_hourly(stations=STATIONS, network="smn"):
    """Read the hourly files of the given stations into one table.

    Columns: station_abbr, time_utc (end of the hourly interval, tz-aware UTC),
    precip_mm, temp_c, snow_cm (NaN where the station does not measure it).
    """
    prefix = COLLECTIONS[network].split(".")[-1]
    frames = []
    for st in stations:
        for kind in HOURLY_FILES:
            path = WEATHER_DIR / "hourly" / f"{prefix}_{st.lower()}_{kind}.csv"
            # usecols with a callable: keep only the columns we need, if present
            df = pd.read_csv(path, sep=";", encoding="cp1252",
                             usecols=lambda c: c in ["station_abbr", "reference_timestamp", *PARAMS])
            frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    # Timestamps are UTC (MeteoSwiss docs) -> parse and attach the time zone explicitly
    df["time_utc"] = pd.to_datetime(df["reference_timestamp"], format="%d.%m.%Y %H:%M").dt.tz_localize("UTC")
    df = df.drop(columns="reference_timestamp").rename(columns=PARAMS)

    # historical ends 31.12. 23:00 and recent starts 01.01. 00:00; should a file ever
    # overlap, keep one row per station and hour (the later file = recent wins)
    df = df.drop_duplicates(["station_abbr", "time_utc"], keep="last")

    # A station without a sensor has no column at all -> add it as empty
    for col in PARAMS.values():
        if col not in df.columns:
            df[col] = float("nan")
    return df[["station_abbr", "time_utc", "precip_mm", "temp_c", "snow_cm"]]


def download_daily(stations, network="nime"):
    """Download the daily files (historical + recent) of a network, e.g. the manual snow stations."""
    prefix = COLLECTIONS[network].split(".")[-1]
    for st in stations:
        assets = station_assets(st, network)
        for kind in ["d_historical", "d_recent"]:
            name = f"{prefix}_{st.lower()}_{kind}.csv"
            download_file(assets[name], WEATHER_DIR / "daily" / name, refresh=(kind == "d_recent"))


def read_fresh_snow(stations, network="nime"):
    """Daily fresh snow 'hns000d0' (cm) per station.

    MeteoSwiss docs: for snow the daily value covers 06:00 UTC of that date until
    06:00 UTC of the next day ("ReferenceTS 22.6.2023 = 22.6.2023 6:10 UTC to 23.6.2023 6:00 UTC").
    Returns columns: station_abbr, date (the reference date), fresh_snow_cm.
    """
    prefix = COLLECTIONS[network].split(".")[-1]
    frames = []
    for st in stations:
        for kind in ["d_historical", "d_recent"]:
            path = WEATHER_DIR / "daily" / f"{prefix}_{st.lower()}_{kind}.csv"
            frames.append(pd.read_csv(path, sep=";", encoding="cp1252",
                                      usecols=["station_abbr", "reference_timestamp", "hns000d0"]))
    df = pd.concat(frames, ignore_index=True)
    df["date"] = pd.to_datetime(df["reference_timestamp"], format="%d.%m.%Y %H:%M").dt.strftime("%Y-%m-%d")
    df = df.drop_duplicates(["station_abbr", "date"], keep="last")
    return df.rename(columns={"hns000d0": "fresh_snow_cm"})[["station_abbr", "date", "fresh_snow_cm"]]


def hours_per_month(hourly, start="2023-11-01", end="2026-04-01"):
    """Completeness check: number of hourly rows and of missing precipitation per station and month (UTC).

    A complete month has 24 x days rows. Used to prove that historical + recent
    fit together without gap or duplicate.
    """
    h = hourly[(hourly.time_utc >= pd.Timestamp(start, tz="UTC")) & (hourly.time_utc < pd.Timestamp(end, tz="UTC"))]
    month = h.time_utc.dt.strftime("%Y-%m")
    out = h.groupby([h.station_abbr, month]).agg(rows=("time_utc", "size"),
                                                 precip_missing=("precip_mm", lambda x: x.isna().sum()))
    out.index.names = ["station_abbr", "month"]
    out["expected"] = [pd.Period(m).days_in_month * 24 for m in out.index.get_level_values("month")]
    return out.reset_index()


def precip_category(precip_mm, temp_c):
    """Classify hourly values into 'dry' / 'rain' / 'snow' (decided by ER on 2026-11-03).

    dry  = 0.0 mm
    rain = >= 0.1 mm and temperature > 0 degC
    snow = >= 0.1 mm and temperature <= 0 degC  (simplification: sleet near 0 degC)
    Anything else (missing precipitation or missing temperature when it rains) -> NaN.
    Works on pandas Series (vectorised).
    """
    cat = pd.Series(pd.NA, index=precip_mm.index, dtype="string")
    cat[precip_mm == 0] = "dry"
    wet = precip_mm >= 0.1
    cat[wet & (temp_c > 0)] = "rain"
    cat[wet & (temp_c <= 0)] = "snow"
    return cat


def winter_summary(stations=("SMA", "REH", "KLO", "WAE", "TAE", "PFA"),
                   months=(11, 12, 1, 2, 3), start="2023-11-01", end="2026-03-31"):
    """Count dry / rain / snow hours per month, averaged over the given stations.

    Used to choose the study period (issue 'find rain/snow days'). Months are
    counted in Swiss local time, because the timetable data are local time.
    Returns one row per month with mean hours per station: dry, rain, snow, missing.
    """
    h = read_hourly(list(stations))
    local = h["time_utc"].dt.tz_convert("Europe/Zurich")
    h = h[(local >= pd.Timestamp(start, tz="Europe/Zurich"))
          & (local < pd.Timestamp(end, tz="Europe/Zurich") + pd.Timedelta(days=1))
          & local.dt.month.isin(months)].copy()
    h["month"] = h["time_utc"].dt.tz_convert("Europe/Zurich").dt.strftime("%Y-%m")
    h["cat"] = precip_category(h["precip_mm"], h["temp_c"]).fillna("missing")

    # Hours per station, month and category -> mean over stations
    counts = h.groupby(["station_abbr", "month", "cat"]).size().unstack(fill_value=0)
    out = counts.groupby("month").mean().round(1)
    return out.reindex(columns=["dry", "rain", "snow", "missing"], fill_value=0)


if __name__ == "__main__":
    download_meta("smn")
    download_meta("precip")
    download_hourly(STATIONS, "smn")
    hourly = read_hourly(STATIONS, "smn")
    print(hourly.groupby("station_abbr")["time_utc"].agg(["min", "max", "count"]))
