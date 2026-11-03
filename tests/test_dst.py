"""Test: local Swiss time -> UTC is correct around the switch to summer time.

The study period (Nov-Mar) contains the spring-forward nights 31.03.2024,
30.03.2025 and 29.03.2026: local time jumps from 01:59:59 CET to 03:00:00 CEST,
so 02:00-02:59 does not exist. A wrong conversion shifts every arrival after
the switch by one hour and puts it into the wrong weather hour.

Run from the repo root:  python -m tests.test_dst
(no pytest needed; every check prints OK or raises an AssertionError)
"""
import pandas as pd

from src.arrivals import local_to_utc, prepare_arrivals
from src.paths import RAW_DIR

FMT = "%d.%m.%Y %H:%M"


def check_synthetic():
    """Known answers for the three switch nights."""
    for day in ["31.03.2024", "30.03.2025", "29.03.2026"]:
        s = pd.Series([f"{day} 01:55", f"{day} 02:30", f"{day} 03:05"])
        utc = local_to_utc(s, FMT)
        date_iso = pd.to_datetime(day, format="%d.%m.%Y").strftime("%Y-%m-%d")
        # 01:55 CET = UTC+1 -> 00:55 UTC
        assert utc[0] == pd.Timestamp(f"{date_iso} 00:55", tz="UTC"), utc[0]
        # 02:30 local does not exist -> NaT (never silently shifted)
        assert pd.isna(utc[1]), utc[1]
        # 03:05 CEST = UTC+2 -> 01:05 UTC, i.e. only 10 real minutes after 01:55
        assert utc[2] == pd.Timestamp(f"{date_iso} 01:05", tz="UTC"), utc[2]
        print(f"OK synthetic {day}: 01:55 -> {utc[0]:%H:%M} UTC, 02:30 -> NaT, 03:05 -> {utc[2]:%H:%M} UTC")
    # A winter day without switch: CET = UTC+1
    w = local_to_utc(pd.Series(["08.01.2026 07:35"]), FMT)[0]
    assert w == pd.Timestamp("2026-01-08 06:35", tz="UTC")
    print("OK synthetic 08.01.2026 07:35 local -> 06:35 UTC (CET)")


def check_real_night(path=RAW_DIR / "istdaten" / "explore" / "2026-03-28_IstDaten_v1.csv"):
    """Real data of the night 28./29.03.2026: no arrival falls into the gap, and
    trips running through the switch get increasing UTC times."""
    if not path.exists():
        print(f"SKIP real-data check ({path.name} not present)")
        return
    raw = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8")
    raw = raw[raw["PRODUKT_ID"] == "Zug"]
    night = raw["ANKUNFTSZEIT"].fillna("").str.startswith("29.03.2026")
    gap = raw.loc[night, "ANKUNFTSZEIT"].str[11:13] == "02"
    assert gap.sum() == 0, "scheduled arrivals inside the non-existent hour"
    utc = local_to_utc(raw["ANKUNFTSZEIT"], FMT)
    assert (raw["ANKUNFTSZEIT"].notna() & utc.isna()).sum() == 0, "a real time became NaT"

    # Trips with stops before 02:00 and after 03:00 local on 29.03.: UTC must rise
    raw = raw.assign(utc=utc, hhmm=raw["ANKUNFTSZEIT"].str[11:16])
    n = raw[night & (raw.hhmm < "02:00")].FAHRT_BEZEICHNER
    m = raw[night & (raw.hhmm >= "03:00")].FAHRT_BEZEICHNER
    through = set(n) & set(m)
    for trip in list(through)[:3]:
        t = raw[(raw.FAHRT_BEZEICHNER == trip) & raw.utc.notna()].sort_values("utc")
        assert t["utc"].is_monotonic_increasing
        print(f"OK trip {trip}: local {t.hhmm.iloc[0]} ... {t.hhmm.iloc[-1]} -> "
              f"UTC {t.utc.iloc[0]:%H:%M} ... {t.utc.iloc[-1]:%H:%M}")
    print(f"OK real night 28./29.03.2026: 0 arrivals 02:00-02:59, 0 times lost, "
          f"{len(through)} trips run through the switch")


def check_prepare_counts():
    """prepare_arrivals counts times it could not convert (expected 0 on real data)."""
    raw = pd.DataFrame({
        "FAHRT_BEZEICHNER": ["t1", "t1"], "BETRIEBSTAG": ["28.03.2026"] * 2,
        "BETREIBER_ABK": ["SBB"] * 2, "LINIEN_TEXT": ["SN1"] * 2, "VERKEHRSMITTEL_TEXT": ["S"] * 2,
        "ZUSATZFAHRT_TF": ["false"] * 2, "FAELLT_AUS_TF": ["false"] * 2, "BPUIC": ["8503000", "8503006"],
        "HALTESTELLEN_NAME": ["A", "B"], "ANKUNFTSZEIT": [None, "29.03.2026 03:10"],
        "AN_PROGNOSE": [None, "29.03.2026 03:13:00"], "AN_PROGNOSE_STATUS": [None, "REAL"],
        "ABFAHRTSZEIT": ["29.03.2026 01:50", None], "AB_PROGNOSE": ["29.03.2026 01:51:00", None],
        "AB_PROGNOSE_STATUS": ["REAL", None], "DURCHFAHRT_TF": ["false"] * 2,
    })
    out, counts = prepare_arrivals(raw, {"8503000", "8503006"})
    assert counts["times_not_convertible"] == 0
    row = out.iloc[0]
    assert row.sched_arr_utc == "2026-03-29 01:10:00" and row.weather_hour_utc == "2026-03-29 01:00:00"
    assert row.arr_delay_min == 3.0 and row.delayed == 1 and row.hour == 3
    assert row.prev_dep_delay_min == 1.0
    print("OK prepare_arrivals across the switch: 03:10 local -> 01:10 UTC, weather hour 01:00 UTC, "
          "delay 3.0 min -> delayed, local hour 3")


if __name__ == "__main__":
    check_synthetic()
    check_prepare_counts()
    check_real_night()
    print("all DST checks passed")
