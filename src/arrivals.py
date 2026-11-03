"""Turn the raw Ist-Daten rows of one day into the 'arrivals' table.

One output row = one train arrival at one stop in the study area (canton ZH).

Steps (each step's row count is returned, for docs/integration-log.md):
1. Parse the times. Ist-Daten are Swiss local time -> convert to UTC.
   Around the switch to summer time (last Sunday in March) the local hour
   02:00-02:59 does not exist; such a time would become NaT (counted, expected 0).
2. Delays in minutes: actual (AN_PROGNOSE, seconds) - scheduled (ANKUNFTSZEIT, minutes).
3. Per trip, in stop order: departure delay at the previous stop and delay at
   the first stop in the study area (both known BEFORE the arrival -> no leakage).
4. Filters decided by ER on 2026-11-03: study-area stop, a scheduled arrival
   exists, no pass-through, not cancelled, status REAL, traffic type S or long-distance.
5. Derived columns: delayed (>= 3 min), traffic_type, local hour, weekday,
   rush hour, and the weather hour (scheduled arrival in UTC, floored to the hour).

All times are stored as text 'YYYY-MM-DD HH:MM:SS' in UTC, so that the same
SQL works on SQLite and PostgreSQL (no database-specific date functions).
"""
import pandas as pd

TZ_LOCAL = "Europe/Zurich"
DELAY_THRESHOLD_MIN = 3.0  # SBB: on time = less than 3 minutes late

# Traffic type by VERKEHRSMITTEL_TEXT (decided by ER on 2026-11-03).
# Long-distance list = SBB's definition (reporting.sbb.ch/punctuality).
TRAFFIC_TYPE = {
    "S": "regional",
    "IC": "long_distance", "IR": "long_distance", "RE": "long_distance",
    "EC": "long_distance", "ICE": "long_distance", "TGV": "long_distance",
    "RJX": "long_distance", "NJ": "long_distance",
}

# Plausibility limits for the arrival delay in minutes. Values outside are
# data errors (seen: -1444 min). PROPOSAL, to be confirmed at Checkpoint 2.
DELAY_MIN_LIMIT, DELAY_MAX_LIMIT = -15.0, 300.0

# Rush hour = Monday-Friday, 06:00-08:59 and 16:00-18:59 local time. PROPOSAL.
RUSH_HOURS = set(range(6, 9)) | set(range(16, 19))


def local_to_utc(text, fmt):
    """Parse local Swiss time strings and convert them to UTC.

    nonexistent='NaT': a local time inside the spring-forward gap (02:00-02:59)
    cannot be real -> NaT instead of a silently shifted time.
    ambiguous='NaT':   a local time in the doubled autumn hour cannot be placed
    -> NaT (not in our Nov-Mar period, but safe).
    """
    local = pd.to_datetime(text, format=fmt)
    return local.dt.tz_localize(TZ_LOCAL, nonexistent="NaT", ambiguous="NaT").dt.tz_convert("UTC")


def utc_text(ts):
    """UTC timestamps -> text 'YYYY-MM-DD HH:MM:SS' (portable between SQLite and PostgreSQL)."""
    return ts.dt.strftime("%Y-%m-%d %H:%M:%S")


def prepare_arrivals(raw, stop_ids):
    """Build the arrivals table from the raw rows of one day (all stops of the ZH trips).

    raw:      DataFrame from src.istdaten.read_day(..., whole_trips=True)
    stop_ids: set of BPUIC of the study area
    Returns (arrivals DataFrame, dict with row counts per step).
    """
    df = raw.copy()
    counts = {"raw_trip_rows": len(df)}

    # 1. Times: scheduled (minutes) and actual (seconds), local -> UTC
    df["sched_arr_utc"] = local_to_utc(df["ANKUNFTSZEIT"], "%d.%m.%Y %H:%M")
    df["act_arr_utc"] = local_to_utc(df["AN_PROGNOSE"], "%d.%m.%Y %H:%M:%S")
    df["sched_dep_utc"] = local_to_utc(df["ABFAHRTSZEIT"], "%d.%m.%Y %H:%M")
    df["act_dep_utc"] = local_to_utc(df["AB_PROGNOSE"], "%d.%m.%Y %H:%M:%S")
    counts["times_not_convertible"] = int((df["ANKUNFTSZEIT"].notna() & df["sched_arr_utc"].isna()).sum())

    # 2. Delays in minutes (only meaningful if the status is REAL, checked below)
    df["arr_delay_min"] = (df["act_arr_utc"] - df["sched_arr_utc"]).dt.total_seconds() / 60
    df["dep_delay_min"] = (df["act_dep_utc"] - df["sched_dep_utc"]).dt.total_seconds() / 60
    dep_real = df["AB_PROGNOSE_STATUS"] == "REAL"
    df.loc[~dep_real, "dep_delay_min"] = float("nan")

    # 3. Per trip, in stop order (scheduled time; the first stop has only a departure)
    df["stop_time_utc"] = df["sched_arr_utc"].fillna(df["sched_dep_utc"])
    df = df.sort_values(["FAHRT_BEZEICHNER", "stop_time_utc"]).reset_index(drop=True)
    trip = df.groupby("FAHRT_BEZEICHNER", sort=False)
    # Departure delay at the previous stop: the train left there before it arrives here
    df["prev_dep_delay_min"] = trip["dep_delay_min"].shift(1)
    df["prev_bpuic"] = trip["BPUIC"].shift(1)

    # Delay at the first study-area stop of the trip (its departure delay there),
    # given to all LATER study-area stops; at that first stop itself it is unknown (NaN)
    in_area = df["BPUIC"].isin(stop_ids)
    df["area_stop_no"] = in_area.astype(int).groupby(df["FAHRT_BEZEICHNER"]).cumsum()
    first = df[in_area & (df["area_stop_no"] == 1)].set_index("FAHRT_BEZEICHNER")["dep_delay_min"]
    df["entry_delay_min"] = df["FAHRT_BEZEICHNER"].map(first)
    df.loc[df["area_stop_no"] <= 1, "entry_delay_min"] = float("nan")

    # Delay gain since the previous stop. ATTENTION: contains this arrival's delay,
    # so it is an alternative OUTCOME, never a model feature (leakage).
    df["delay_gain_min"] = df["arr_delay_min"] - df["prev_dep_delay_min"]

    # 4. Filters (decided by ER on 2026-11-03), counting what each step removes
    def step(name, keep):
        nonlocal df
        counts[name] = int((~keep).sum())
        df = df[keep]

    step("removed_outside_area", df["BPUIC"].isin(stop_ids))
    counts["area_rows"] = len(df)
    step("removed_no_scheduled_arrival", df["ANKUNFTSZEIT"].notna())   # first stop of a trip
    step("removed_pass_through", df["DURCHFAHRT_TF"] != "true")
    step("removed_cancelled", df["FAELLT_AUS_TF"] != "true")
    step("removed_not_real", df["AN_PROGNOSE_STATUS"] == "REAL")
    step("removed_other_category", df["VERKEHRSMITTEL_TEXT"].isin(TRAFFIC_TYPE))
    step("removed_implausible_delay", df["arr_delay_min"].between(DELAY_MIN_LIMIT, DELAY_MAX_LIMIT))
    counts["arrivals"] = len(df)

    # 5. Derived columns
    local = df["sched_arr_utc"].dt.tz_convert(TZ_LOCAL)
    out = pd.DataFrame({
        "service_date": pd.to_datetime(df["BETRIEBSTAG"], format="%d.%m.%Y").dt.strftime("%Y-%m-%d"),
        "trip_id": df["FAHRT_BEZEICHNER"],
        "operator": df["BETREIBER_ABK"],
        "line": df["LINIEN_TEXT"],
        "category": df["VERKEHRSMITTEL_TEXT"],
        "traffic_type": df["VERKEHRSMITTEL_TEXT"].map(TRAFFIC_TYPE),
        "extra_trip": (df["ZUSATZFAHRT_TF"] == "true").astype(int),
        "bpuic": df["BPUIC"],
        "sched_arr_utc": utc_text(df["sched_arr_utc"]),
        "act_arr_utc": utc_text(df["act_arr_utc"]),
        "arr_delay_min": df["arr_delay_min"].round(2),
        "delayed": (df["arr_delay_min"] >= DELAY_THRESHOLD_MIN).astype(int),
        "prev_dep_delay_min": df["prev_dep_delay_min"].round(2),
        "entry_delay_min": df["entry_delay_min"].round(2),
        "delay_gain_min": df["delay_gain_min"].round(2),
        # Weather key: MeteoSwiss hourly value with this (end-of-interval) timestamp
        # covers the last full hour BEFORE the scheduled arrival
        "weather_hour_utc": utc_text(df["sched_arr_utc"].dt.floor("h")),
        "local_date": local.dt.strftime("%Y-%m-%d"),
        "hour": local.dt.hour,
        "weekday": local.dt.dayofweek,  # 0 = Monday
    })
    out["rush_hour"] = ((out["weekday"] < 5) & out["hour"].isin(RUSH_HOURS)).astype(int)
    return out.reset_index(drop=True), counts
