"""Validate the snow definition (1) against measured fresh snow.

Our definition (decided by ER on 2026-11-03): an hour is a "snow hour" if
precipitation >= 0.1 mm and air temperature <= 0 degC (automatic SMN station).
Check: on days with at least one snow hour, did the observer at the same place
measure fresh snow (manual network ogd-nime, parameter hns000d0)?

Only stations where the manual and the automatic station are at the SAME place
(distance 0 km in the metadata) are used, so location differences do not blur
the comparison. Both day definitions match the MeteoSwiss rule for snow:
06:00 UTC to 06:00 UTC of the next day.

Usage (from the repo root):  python -m src.snow_validation
Output: table printed and saved to data/processed/snow_validation.csv
"""
import pandas as pd

from src import weather as wx
from src.paths import PROCESSED_DIR

# Manual snow stations at the same place as an SMN station (same abbreviation, 0 km)
COLOCATED = ["SMA", "PFA", "HLL", "BUS", "MOA", "SAG", "EIN"]
STUDY_MONTHS = (11, 12, 1, 2, 3)
STUDY_START, STUDY_END = "2023-11-01", "2026-03-31"


def snow_hours_per_day(hourly):
    """Count snow hours per station and 'snow day' (06:00 UTC to 06:00 UTC).

    Hourly timestamps mark the END of the hour, so the hours ending 07:00 on day d
    up to 06:00 on day d+1 belong to day d: subtract 6 h 1 min and take the date.
    """
    h = hourly.copy()
    h["date"] = (h["time_utc"] - pd.Timedelta(hours=6, minutes=1)).dt.strftime("%Y-%m-%d")
    # Missing measurements give <NA>; count them as "not a snow hour"
    h["snow_hour"] = (wx.precip_category(h["precip_mm"], h["temp_c"]) == "snow").fillna(False).astype(int)
    return h.groupby(["station_abbr", "date"], as_index=False)["snow_hour"].sum().rename(
        columns={"snow_hour": "snow_hours"})


def validate(stations=COLOCATED):
    """Return one row per station: agreement between snow hours and measured fresh snow."""
    wx.download_daily(stations, "nime")
    days = snow_hours_per_day(wx.read_hourly(stations, "smn"))
    snow = wx.read_fresh_snow(stations, "nime")
    df = days.merge(snow, on=["station_abbr", "date"], how="inner")
    d = pd.to_datetime(df["date"])
    df = df[(df["date"] >= STUDY_START) & (df["date"] <= STUDY_END) & d.dt.month.isin(STUDY_MONTHS)]
    df = df[df["fresh_snow_cm"].notna()]  # only days with a manual reading

    ours = df["snow_hours"] >= 1          # our definition says: snow fell that day
    measured = df["fresh_snow_cm"] > 0    # the observer measured fresh snow
    df = df.assign(hit=ours & measured, false_alarm=ours & ~measured,
                   miss=~ours & measured, both_no=~ours & ~measured)
    out = df.groupby("station_abbr")[["hit", "false_alarm", "miss", "both_no"]].sum()
    out.loc["ALL"] = out.sum()
    out["days"] = out.sum(axis=1)
    # Share of measured snow days that our definition also finds, and share of our snow days that were real
    out["hit_rate_pct"] = (100 * out.hit / (out.hit + out.miss)).round(1)
    out["precision_pct"] = (100 * out.hit / (out.hit + out.false_alarm)).round(1)
    out["agreement_pct"] = (100 * (out.hit + out.both_no) / out.days).round(1)
    return out.reset_index(), df


if __name__ == "__main__":
    table, detail = validate()
    table.to_csv(PROCESSED_DIR / "snow_validation.csv", index=False)
    print(table.to_string(index=False))
    miss = detail[detail.miss]
    print("\nMeasured fresh snow but no snow hour (misses), fresh snow cm:",
          miss.fresh_snow_cm.describe().round(1).to_dict())
