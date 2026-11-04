"""Test: entry_delay_min never comes from the arrival it is used for (no leakage).

Definition (decided by ER on 2026-11-03): entry_delay_min = departure delay at the
LAST stop BEFORE the study area. Trips that start inside the area -> NULL.
If this value were taken from the arrival in the same row, it would be the
target variable itself and every model would look perfect for the wrong reason.

Checks:
1. Synthetic trips with known answers (incl. a trip that starts inside the area).
2. Real data in the database, for every row with a value:
   - the source stop lies OUTSIDE the study area,
   - the source stop is not the stop of this row,
   - its scheduled departure is BEFORE this row's scheduled arrival.
3. Share of NULL (overall and per traffic type).

Run from the repo root:  python -m tests.test_entry_delay
"""
import pandas as pd

from src.arrivals import prepare_arrivals
from src.db import query


def raw_row(trip, bpuic, arr=None, arr_act=None, dep=None, dep_act=None, cat="S"):
    """One raw Ist-Daten row with status REAL (helper for the synthetic test)."""
    return {
        "FAHRT_BEZEICHNER": trip, "BETRIEBSTAG": "08.01.2026", "BETREIBER_ABK": "SBB",
        "LINIEN_TEXT": cat, "VERKEHRSMITTEL_TEXT": cat, "ZUSATZFAHRT_TF": "false",
        "FAELLT_AUS_TF": "false", "BPUIC": bpuic, "HALTESTELLEN_NAME": bpuic,
        "ANKUNFTSZEIT": arr, "AN_PROGNOSE": arr_act, "AN_PROGNOSE_STATUS": "REAL" if arr else None,
        "ABFAHRTSZEIT": dep, "AB_PROGNOSE": dep_act, "AB_PROGNOSE_STATUS": "REAL" if dep else None,
        "DURCHFAHRT_TF": "false",
    }


def check_synthetic():
    """Trip A enters the area from outside, trip B starts inside."""
    d = "08.01.2026 "
    raw = pd.DataFrame([
        # Trip A: OUT1 -> OUT2 (dep 2 min late) -> IN1 (arr 5 min late) -> IN2
        raw_row("A", "OUT1", dep=d + "08:00", dep_act=d + "08:00:00"),
        raw_row("A", "OUT2", d + "08:10", d + "08:12:00", d + "08:11", d + "08:13:00"),
        raw_row("A", "IN1", d + "08:20", d + "08:25:00", d + "08:21", d + "08:26:00"),
        raw_row("A", "IN2", d + "08:30", d + "08:33:00"),
        # Trip B starts inside the area
        raw_row("B", "IN1", dep=d + "09:00", dep_act=d + "09:01:00"),
        raw_row("B", "IN2", d + "09:10", d + "09:14:00"),
    ])
    out, _ = prepare_arrivals(raw, {"IN1", "IN2"})
    a = out[out.trip_id == "A"].set_index("bpuic")
    # First stop in the area: entry = 2.0 (departure OUT2), NOT 5.0 (its own arrival delay)
    assert a.loc["IN1", "entry_delay_min"] == 2.0 and a.loc["IN1", "arr_delay_min"] == 5.0
    assert a.loc["IN2", "entry_delay_min"] == 2.0
    assert (a.entry_from_bpuic == "OUT2").all()
    b = out[out.trip_id == "B"]
    assert b.entry_delay_min.isna().all(), "trip starting inside the area must have NULL"
    print("OK synthetic: first area stop gets the departure delay of the stop before the area "
          "(2.0 min), not its own arrival delay (5.0 min); trip starting inside -> NULL")


def check_database():
    """Structural checks on every row of the arrivals table."""
    bad_inside = query("""
        SELECT COUNT(*) AS n FROM arrivals a JOIN stops s ON s.bpuic = a.entry_from_bpuic
        WHERE a.entry_delay_min IS NOT NULL""")["n"][0]
    bad_same = query("""
        SELECT COUNT(*) AS n FROM arrivals
        WHERE entry_delay_min IS NOT NULL AND entry_from_bpuic = bpuic""")["n"][0]
    # Times are 'YYYY-MM-DD HH:MM:SS' text in UTC, so text comparison = time comparison.
    # Equal minute is allowed: scheduled times are rounded to minutes, and two stops can
    # be one minute apart; the departure there still happens before the arrival here.
    bad_time = query("""
        SELECT COUNT(*) AS n FROM arrivals
        WHERE entry_delay_min IS NOT NULL AND NOT (entry_from_time_utc <= sched_arr_utc)""")["n"][0]
    same_minute = query("""
        SELECT COUNT(*) AS n FROM arrivals
        WHERE entry_delay_min IS NOT NULL AND entry_from_time_utc = sched_arr_utc""")["n"][0]
    print(f"info: {same_minute} rows where the source departure and this arrival have the same scheduled minute")
    total = query("SELECT COUNT(*) AS n, SUM(CASE WHEN entry_delay_min IS NOT NULL THEN 1 ELSE 0 END) AS with_value FROM arrivals")
    assert bad_inside == 0, f"{bad_inside} rows take entry_delay from a stop inside the area"
    assert bad_same == 0, f"{bad_same} rows take entry_delay from their own stop"
    assert bad_time == 0, f"{bad_time} rows take entry_delay from a departure not before the arrival"
    print(f"OK database: {int(total.with_value[0]):,} of {int(total.n[0]):,} rows with a value; all from a stop "
          "outside the area, never the own stop, departed before or in the same scheduled minute as the arrival")

    nulls = query("""
        SELECT traffic_type, COUNT(*) AS arrivals,
               ROUND(100.0 * SUM(CASE WHEN entry_delay_min IS NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS null_pct
        FROM arrivals GROUP BY traffic_type
        UNION ALL
        SELECT 'all', COUNT(*),
               ROUND(100.0 * SUM(CASE WHEN entry_delay_min IS NULL THEN 1 ELSE 0 END) / COUNT(*), 1)
        FROM arrivals""")
    print("Share of NULL entry_delay_min (trip starts inside the area, or no measured departure before it):")
    print(nulls.to_string(index=False))


if __name__ == "__main__":
    check_synthetic()
    check_database()
    print("all entry_delay checks passed")
