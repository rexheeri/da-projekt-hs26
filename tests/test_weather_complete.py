"""Test: hourly weather is complete for the whole study period, without gap or duplicate.

MeteoSwiss splits each station into 'historical' (until 31 Dec of last year) and
'recent' (from 1 Jan of this year). Winter 2025/26 needs both files. This test
checks, for every station used in the database:
- number of hourly rows per month = 24 x days of the month (no gap, no duplicate),
- the boundary 31.12.2025 23:00 UTC -> 01.01.2026 00:00 UTC is exactly one hour apart,
- how many hours have no precipitation value (missing measurement).

Run from the repo root:  python -m tests.test_weather_complete
"""
import pandas as pd

from src import weather as wx
from src.db import query

STUDY_MONTHS = ["2023-11", "2023-12", "2024-01", "2024-02", "2024-03",
                "2024-11", "2024-12", "2025-01", "2025-02", "2025-03",
                "2025-11", "2025-12", "2026-01", "2026-02", "2026-03"]


def main():
    used = query("SELECT station_abbr, network FROM weather_stations")
    frames = [wx.read_hourly(list(g.station_abbr), net) for net, g in used.groupby("network")]
    hourly = pd.concat(frames, ignore_index=True)

    # 1. Rows per station and month (UTC months)
    hpm = wx.hours_per_month(hourly)
    hpm = hpm[hpm.month.isin(STUDY_MONTHS)]
    table = hpm.pivot(index="station_abbr", columns="month", values="rows")
    expected = hpm.groupby("month")["expected"].first()
    pd.set_option("display.width", 250, "display.max_columns", 20)
    print("Hourly rows per station and month (expected per month in the last line):")
    print(pd.concat([table, expected.to_frame().T.rename(index={"expected": "EXPECTED"})]).to_string())
    bad = hpm[hpm.rows != hpm.expected]
    assert len(table) == len(used), "a station has no data in the study period"
    assert bad.empty, f"months with gaps or duplicates:\n{bad}"
    print(f"OK {len(used)} stations x {len(STUDY_MONTHS)} months: every month has 24 x days rows")

    # 2. Year boundary historical -> recent
    for st, g in hourly.groupby("station_abbr"):
        t = g.time_utc.sort_values()
        around = t[(t >= pd.Timestamp("2025-12-31 22:00", tz="UTC")) & (t <= pd.Timestamp("2026-01-01 01:00", tz="UTC"))]
        assert len(around) == 4 and around.diff().dropna().eq(pd.Timedelta(hours=1)).all(), st
    print("OK boundary 31.12.2025 22:00 - 01.01.2026 01:00 UTC: 4 consecutive hours for every station, no duplicate")

    # 3. Missing measurements (empty fields) in the study months
    miss = hpm.groupby("station_abbr")["precip_missing"].sum()
    print("Hours without precipitation value in the study months:", miss[miss > 0].to_dict() or "none")


if __name__ == "__main__":
    main()
