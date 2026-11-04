"""Build the project database from the sources: stops, weather, calendar, arrivals, analysis_base.

Usage (from the repo root):
    python -m src.build_db --reset --days 2026-01-08                # prototype: one day
    python -m src.build_db --days 2026-01-05 2026-01-11             # a range (first and last day)
    python -m src.build_db --study-period > data/processed/build_run.log 2>&1
                                    # whole study period (Nov-Mar 2023/24-2025/26), resumable

What happens:
1. Create the tables from src/schema.sql (--reset drops them first).
2. Stops and their weather stations (src/stops.py) -> stops, weather_stations, stop_station.
3. Hourly weather of the used stations (src/weather.py) -> weather_hourly (study period only).
4. Calendar (src/calendar_zh.py) -> calendar_days.
5. For each day: read it directly from the monthly archive ZIP (downloaded if
   missing), prepare it (src/arrivals.py), save it as a small Parquet file in
   data/processed/arrivals/ and replace that day in 'arrivals'.
   Resumable: a day whose Parquet file exists and whose rows are already in the
   database is skipped; if only the Parquet exists, it is loaded from there.
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

STUDY_MONTHS = ["2023-11", "2023-12", "2024-01", "2024-02", "2024-03",
                "2024-11", "2024-12", "2025-01", "2025-02", "2025-03",
                "2025-11", "2025-12", "2026-01", "2026-02", "2026-03"]  # winter half-year (Nov-Mar)
DAY_DIR = PROCESSED_DIR / "arrivals"
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
    # Source files needed before anything else (skipped if present; found missing in
    # the fresh-clone test, where nothing had been downloaded before)
    st.download_service_points()
    wx.download_meta("smn")
    wx.download_meta("precip")
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
    log(f"static tables: {len(stops)} stops, {len(used)} stations, {len(hourly)} weather hours")


def log(msg):
    """Print one progress line with a time stamp (goes to the log file when redirected)."""
    print(f"{pd.Timestamp.now():%Y-%m-%d %H:%M:%S} {msg}", flush=True)


def study_days():
    """All days of the study period (Nov-Mar of three winters) as 'YYYY-MM-DD'."""
    days = pd.date_range("2023-11-01", "2026-03-31", freq="D")
    return [d.strftime("%Y-%m-%d") for d in days if d.strftime("%Y-%m") in STUDY_MONTHS]


def build_day(day, stop_ids):
    """Step 5 for one day 'YYYY-MM-DD': read from the monthly ZIP, prepare, save, load into arrivals."""
    t0 = time.time()
    parquet = DAY_DIR / f"{day}.parquet"
    in_db = query("SELECT COUNT(*) AS n FROM arrivals WHERE service_date = :d", {"d": day})["n"][0]
    if parquet.exists() and in_db > 0:
        log(f"{day}: skip (already processed, {in_db} arrivals)")
        return None
    if parquet.exists():
        df = pd.read_parquet(parquet)       # prepared earlier, only the DB load is missing
        counts = {"arrivals": len(df), "from_parquet": 1}
    else:
        zip_path = download_archive_month(int(day[:4]), int(day[5:7]))
        raw, n_raw = read_day_from_zip(zip_path, day, stop_ids, whole_trips=True)
        df, counts = arr.prepare_arrivals(raw, stop_ids)
        counts = {"raw_rows": n_raw, **counts}
        DAY_DIR.mkdir(parents=True, exist_ok=True)
        df.to_parquet(parquet, index=False)
    execute("DELETE FROM arrivals WHERE service_date = :d", {"d": day})
    write_table(df, "arrivals", if_exists="append")
    counts["seconds"] = round(time.time() - t0)
    log_counts(day, counts)
    log(f"{day}: {counts.get('raw_rows', '-')} raw -> {len(df)} arrivals ({counts['seconds']} s)")
    return counts


def build_analysis_base():
    """Step 6: join arrivals, stations, weather and calendar in SQL."""
    execute('DROP TABLE IF EXISTS "analysis_base"')
    run_sql_file("analysis_base.sql")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--reset", action="store_true", help="drop all project tables first")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--days", nargs="+", help="one day, or first and last day")
    group.add_argument("--study-period", action="store_true", help="all days Nov-Mar 2023/24-2025/26")
    args = parser.parse_args()
    t_start = time.time()

    if args.reset:
        # Rebuild from scratch: drop the tables and the prepared day files
        # (the downloaded raw ZIPs stay, they never change)
        for t in TABLES:
            execute(f'DROP TABLE IF EXISTS "{t}"')
        for f in DAY_DIR.glob("*.parquet"):
            f.unlink()
    run_sql_file("schema.sql")
    build_static()

    stop_ids = set(query("SELECT bpuic FROM stops")["bpuic"])
    if args.study_period:
        days = study_days()
    else:
        days = list(pd.date_range(args.days[0], args.days[-1], freq="D").strftime("%Y-%m-%d"))
    log(f"start: {len(days)} days")
    for i, day in enumerate(days, 1):
        try:
            build_day(day, stop_ids)
        except Exception as e:  # one broken day must not stop the whole run; it is retried next run
            log(f"{day}: ERROR {type(e).__name__}: {e}")
            log_counts(day, {"error": 1})
        if i % 10 == 0:
            log(f"progress: {i}/{len(days)} days, {(time.time() - t_start) / 60:.0f} min")
    log("building analysis_base (SQL join) ...")
    build_analysis_base()
    log(f"done in {(time.time() - t_start) / 60:.0f} min")
    print(list_tables().to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
