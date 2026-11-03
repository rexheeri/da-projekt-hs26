"""Train stops in the study area and their nearest weather station.

Source: service point directory (atlas) on opentransportdata.swiss,
dataset 'service-point-v2', file 'full-swiss-service-point.csv'.
The 'full' file contains all versions of each stop (validFrom / validTo), so it
also covers stops that existed in past winters but not today.

Key for the join with the Ist-Daten: the column 'number' (7 digits, e.g. 8503000
= Zuerich HB) equals the Ist-Daten column BPUIC for train stops (verified on real data).

Each stop gets two weather stations (decided by ER on 2026-11-03):
- precipitation: nearest station of SMN + precipitation network (ogd-smn-precip)
- temperature:   nearest SMN station (the precipitation network has no thermometer)

Usage (from the repo root):
    python -m src.stops        # download, filter, assign stations, write tables to the DB
"""
import geopandas as gpd
import pandas as pd

from src.db import write_table
from src.download import download_file
from src.paths import RAW_DIR
from src.weather import EXCLUDED_STATIONS, STATIONS, read_stations

SERVICE_POINTS_URL = (
    "https://data.opentransportdata.swiss/dataset/39e5f264-257a-4f3f-bccc-5322c37058c5/"
    "resource/ddc99526-e43f-438b-8072-7ade37d86ad9/download/full-swiss-service-point.csv"
)
SERVICE_POINTS_FILE = RAW_DIR / "stops" / "full-swiss-service-point.csv"

# LV95 = Swiss national coordinate system, units in metres -> distances in metres are exact
CRS_LV95 = "EPSG:2056"


def download_service_points():
    """Download the full service point directory (about 67 MB, skipped if present)."""
    # The portal can be slow to answer (seen: timeouts, 502), hence the long timeout
    return download_file(SERVICE_POINTS_URL, SERVICE_POINTS_FILE, timeout=180)


def load_train_stops(canton="ZH", start="2023-11-01", end="2026-03-31"):
    """Return one row per train stop in `canton` that was valid at any time between start and end.

    Columns: bpuic (string, 7 digits), stop_name, canton, lv95_east, lv95_north, height_masl.
    """
    df = pd.read_csv(SERVICE_POINTS_FILE, sep=";", dtype=str, encoding="utf-8-sig")

    # Swiss stops served by trains ('TRAIN' can be combined, e.g. 'BUS|TRAIN')
    df = df[(df["uicCountryCode"] == "85")
            & df["meansOfTransport"].fillna("").str.contains("TRAIN")
            & (df["cantonAbbreviation"] == canton)]

    # Keep versions whose validity overlaps the study period (ISO dates compare as text)
    df = df[(df["validFrom"] <= end) & (df["validTo"] >= start)]

    # Several versions per stop -> keep the most recent one (coordinates do not change, checked)
    df = df.sort_values("validFrom").drop_duplicates("number", keep="last")

    out = pd.DataFrame({
        "bpuic": df["number"],
        "stop_name": df["designationOfficial"],
        "canton": df["cantonAbbreviation"],
        "lv95_east": df["lv95East"].astype(float),
        "lv95_north": df["lv95North"].astype(float),
        "height_masl": df["height"].astype(float),
    })
    return out.reset_index(drop=True)


def nearest_station(stops, stations):
    """Assign each stop its nearest weather station (straight-line distance in LV95).

    Returns stops plus: station_abbr, distance_km, station_height_masl, height_diff_m.
    """
    # Turn both tables into point layers in the same projected CRS
    g_stops = gpd.GeoDataFrame(stops, geometry=gpd.points_from_xy(stops.lv95_east, stops.lv95_north), crs=CRS_LV95)
    st = stations.rename(columns={"height_masl": "station_height_masl"})
    g_st = gpd.GeoDataFrame(st[["station_abbr", "station_height_masl"]],
                            geometry=gpd.points_from_xy(st.lv95_east, st.lv95_north), crs=CRS_LV95)

    # sjoin_nearest: for every stop, find the closest station; distance_col in metres
    joined = gpd.sjoin_nearest(g_stops, g_st, how="left", distance_col="distance_m")
    # Two stations at exactly the same distance would give two rows -> keep the first
    joined = joined[~joined.index.duplicated(keep="first")]
    joined["distance_km"] = (joined["distance_m"] / 1000).round(2)
    joined["height_diff_m"] = (joined["station_height_masl"] - joined["height_masl"]).round(0)
    cols = list(stops.columns) + ["station_abbr", "distance_km", "station_height_masl", "height_diff_m"]
    return pd.DataFrame(joined[cols])


def weather_stations():
    """All candidate stations of both networks (SMN without excluded summit stations + precipitation network)."""
    smn = read_stations("smn")
    smn = smn[smn.station_abbr.isin(STATIONS) & ~smn.station_abbr.isin(EXCLUDED_STATIONS)]
    precip = read_stations("precip")
    return pd.concat([smn, precip], ignore_index=True)


def stop_station_table(stops, stations):
    """One row per stop with its precipitation station and its temperature station.

    Columns: bpuic, precip_station, precip_distance_km, precip_height_diff_m,
             temp_station, temp_distance_km, temp_height_diff_m
    """
    pre = nearest_station(stops, stations)                                # both networks
    tmp = nearest_station(stops, stations[stations.network == "smn"])     # thermometers: SMN only
    out = pd.DataFrame({
        "bpuic": pre["bpuic"].values,
        "precip_station": pre["station_abbr"].values,
        "precip_distance_km": pre["distance_km"].values,
        "precip_height_diff_m": pre["height_diff_m"].values,
        "temp_station": tmp["station_abbr"].values,
        "temp_distance_km": tmp["distance_km"].values,
        "temp_height_diff_m": tmp["height_diff_m"].values,
    })
    return out


if __name__ == "__main__":
    download_service_points()
    stops = load_train_stops()
    stations = weather_stations()
    stop_station = stop_station_table(stops, stations)

    # Only the stations that are actually used go into the DB
    used = set(stop_station.precip_station) | set(stop_station.temp_station)
    write_table(stops, "stops")
    write_table(stations[stations.station_abbr.isin(used)], "weather_stations")
    write_table(stop_station, "stop_station")

    print(f"{len(stops)} train stops in ZH, {len(used)} weather stations used")
    for kind in ["precip", "temp"]:
        d = stop_station[f"{kind}_distance_km"]
        print(f"{kind:6s}: median {d.median():.1f} km, max {d.max():.1f} km, > 10 km: {(d > 10).sum()}, "
              f"unmatched: {stop_station[f'{kind}_station'].isna().sum()}")
