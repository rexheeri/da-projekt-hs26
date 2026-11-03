"""Build the project database from the sources: stops, weather, calendar, arrivals, analysis_base.

Usage (from the repo root):
    python -m src.build_db --reset --days 2026-01-08                # prototype: one day
    python -m src.build_db --days 2026-01-05 2026-01-11             # a range (first and last day)

What happens:
1. Create the tables from src/schema.sql (--reset drops them first).
2. Stops and their weather stations (src/stops.py) -> stops, weather_stations, stop_station.
3. Hourly weather of the used stations (src/weather.py) -> weather_hourly (study period only).
4. Calendar (src/calendar_zh.py) -> calendar_days.
5. For each day: read it directly from the monthly archive ZIP (downloaded if
   missing), prepare it (src/arrivals.py) and replace that day in 'arrivals'.
   Re-running a day replaces it, so the build is idempotent.
6. Join everything IN SQL into the table analysis_base (src/analysis_base.sql).

Row counts of every step are written to data/processed/build_log.csv for
docs/integration-log.md.
"""
import argparse
import time

import pandas as pd

from src import arrivals as arr
from src import stops as st
from src import weather as wx
from src.calendar_zh import build_calendar
from src.db import execute, list_tables, query, write_table
from src.istdaten import download_archive_month, read_day_from_zip
from src.paths import PROCESSED_DIR, ROOT

STUDY_START_UTC = "2023-10-31 23:00:00"  # 01.11.2023 00:00 local (CET = UTC+1)
STUDY_END_UTC = "2026-04-01 00:00:00"
TABLES = ["analysis_base", "arrivals", "calendar_days", "weather_hourly", "stop_station",
          "weather_stations", "stops"]  # drop order: dependent tables first
BUILD_LOG = PROCESSED_DIR / "build_log.csv"


def run_sql_file(name):
    """Execute all statements of an SQL file in src/ (split at ';')."""
    sql = (ROOT / "src" / name).read_text(encoding="utf-8")
    # Remove comment lines first, then split into single statements
    lines = [ln for ln in sql.splitlines() if not ln.strip().startswith("--")]
    for statement in "\n".join(lines).split(";"):
        if statement.strip():
            execute(statement)


def replace_rows(df, table):
    """Empty a table and insert df (keeps the table definition from schema.sql)."""
    execute(f'DELETE FROM "{table}"')
    write_table(df, table, if_exists="append")


def log_counts(step, counts):
    """Append row counts of a build step to data/processed/build_log.csv.

    Long format (one line per number: time, step, metric, value), because the
    steps report different metrics.
    """
    now = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    rows = pd.DataFrame([{"time": now, "step": step, "metric": k, "value": v} for k, v in counts.items()])
    rows.to_csv(BUILD_LOG, mode="a", header=not BUILD_LOG.exists(), index=False)


def build_static():
    """Steps 2-4: stops, stations, weather, calendar (small, rebuilt every run)."""
    stops = st.load_train_stops()
    stations = st.weather_stations()
    stop_station = st.stop_station_table(stops, stations)
    used = stations[stations.station_abbr.isin(set(stop_station.precip_station) | set(stop_station.temp_station))]
    replace_rows(stops, "stops")
    replace_rows(used, "weather_stations")
    replace_rows(stop_station, "stop_station")

    # Hourly weather: download the used stations of each network, keep the study period
    frames = []
    for network in ["smn", "precip"]:
        names = list(used.loc[used.network == network, "station_abbr"])
        wx.download_hourly(names, network)
        frames.append(wx.read_hourly(names, network))
    hourly = pd.concat(frames, ignore_index=True)
    hourly["time_utc"] = hourly["time_utc"].dt.strftime("%Y-%m-%d %H:%M:%S")
    hourly = hourly[(hourly.time_utc >= STUDY_START_UTC) & (hourly.time_utc <= STUDY_END_UTC)]
    replace_rows(hourly, "weather_hourly")

    replace_rows(build_calendar(), "calendar_days")
    log_counts("static", {"stops": len(stops), "stations": len(used), "weather_hours": len(hourly)})


def build_day(day, stop_ids):
    """Step 5 for one day 'YYYY-MM-DD': read from the monthly ZIP, prepare, replace in arrivals."""
    t0 = time.time()
    zip_path = download_archive_month(int(day[:4]), int(day[5:7]))
    raw, n_raw = read_day_from_zip(zip_path, day, stop_ids, whole_trips=True)
    df, counts = arr.prepare_arrivals(raw, stop_ids)
    execute("DELETE FROM arrivals WHERE service_date = :d", {"d": day})
    write_table(df, "arrivals", if_exists="append")
    counts = {"raw_rows": n_raw, **counts, "seconds": round(time.time() - t0)}
    log_counts(day, counts)
    print(f"{day}: {n_raw} raw -> {counts['raw_trip_rows']} trip rows -> {len(df)} arrivals ({counts['seconds']} s)")
    return counts


def build_analysis_base():
    """Step 6: join arrivals, stations, weather and calendar in SQL."""
    execute('DROP TABLE IF EXISTS "analysis_base"')
    run_sql_file("analysis_base.sql")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reset", action="store_true", help="drop all project tables first")
    parser.add_argument("--days", nargs="+", required=True, help="one day, or first and last day")
    args = parser.parse_args()

    if args.reset:
        for t in TABLES:
            execute(f'DROP TABLE IF EXISTS "{t}"')
    run_sql_file("schema.sql")
    build_static()

    stop_ids = set(query("SELECT bpuic FROM stops")["bpuic"])
    first, last = args.days[0], args.days[-1]
    for day in pd.date_range(first, last, freq="D").strftime("%Y-%m-%d"):
        build_day(day, stop_ids)
    build_analysis_base()
    print(list_tables().to_string(index=False))


if __name__ == "__main__":
    main()
