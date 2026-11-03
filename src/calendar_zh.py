"""Calendar of the study period: weekday, public holidays, school holidays (canton of Zurich).

Why: holidays change who travels (fewer commuters) and therefore delays. Without
this control the model could mistake "Christmas week" for "weather effect".

Sources (accessed 2026-11-03):
- Legal public holidays canton ZH (nine, equal to Sundays):
  https://www.zh.ch/de/wirtschaft-arbeit/arbeitsbedingungen/arbeitsssicherheit-gesundheitsschutz/arbeits-ruhezeiten/feiertage.html
  In Nov-Mar: Neujahrstag (1.1.), Karfreitag (Good Friday), Weihnachtstag (25.12.),
  Stephanstag (26.12.). Berchtoldstag (2.1.) is NOT a legal holiday there.
  Good Friday is computed from Easter Sunday (dateutil.easter, Gregorian calendar).
- School holidays: in the canton only the Christmas holidays are binding and
  uniform ("Nur der Schulbeginn und die Weihnachtsferien sind verbindlich",
  zh.ch/de/bildung/bildungssystem/schulferien.html). Sports holidays are set by
  each municipality -> see OPEN below.
  Christmas 2025/26: Mon 22.12.2025 - Sat 03.01.2026 (Volksschulamt, "Feriendaten
  Festlegungen und Empfehlungen bis SJ 2032/2033", 26.06.2023).

  Christmas 2023/24 and 2024/25: no official date list found online. They are
  DERIVED FROM THE BINDING CANTON RULE "Woche 52 und 1 (verbindlich)"
  (zh.ch Planungshilfe), i.e. Monday of ISO week 52 to Saturday of ISO week 1.
  Check: the rule gives exactly the sourced 2025/26 dates (22.12.2025 - 03.01.2026).
  Decided by ER on 2026-11-03.
- Sports holidays (Sportferien) are NOT modelled: each municipality sets its own
  two weeks (limitation, see docs/research-design.md).
"""
import datetime as dt

import pandas as pd
from dateutil.easter import easter

# Christmas school holidays (first day, last day) per winter.
CHRISTMAS_SCHOOL_HOLIDAYS = {
    "2023/24": (dt.date(2023, 12, 25), dt.date(2024, 1, 6)),   # derived from the canton rule (KW52 + KW1)
    "2024/25": (dt.date(2024, 12, 23), dt.date(2025, 1, 4)),   # derived from the canton rule (KW52 + KW1)
    "2025/26": (dt.date(2025, 12, 22), dt.date(2026, 1, 3)),   # sourced: Volksschulamt, Feriendaten bis SJ 2032/33
}


def public_holidays(years):
    """Legal public holidays of canton ZH that fall in Nov-Mar, for the given years."""
    days = []
    for y in years:
        days += [dt.date(y, 1, 1), dt.date(y, 12, 25), dt.date(y, 12, 26)]
        days.append(easter(y) - dt.timedelta(days=2))  # Good Friday
    return set(days)


def build_calendar(start="2023-11-01", end="2026-03-31"):
    """One row per local date: weekday, public_holiday, school_holiday, holiday (either)."""
    dates = pd.date_range(start, end, freq="D")
    ph = public_holidays(range(dates.min().year, dates.max().year + 1))
    school = set()
    for first, last in CHRISTMAS_SCHOOL_HOLIDAYS.values():
        school |= {d.date() for d in pd.date_range(first, last, freq="D")}
    cal = pd.DataFrame({"local_date": dates.strftime("%Y-%m-%d"), "weekday": dates.dayofweek})
    cal["public_holiday"] = [int(d.date() in ph) for d in dates]
    cal["school_holiday"] = [int(d.date() in school) for d in dates]
    cal["holiday"] = ((cal.public_holiday == 1) | (cal.school_holiday == 1)).astype(int)
    # Winter half-year label: Nov-Dec belong to the winter that starts that year
    cal["winter"] = [f"{d.year}/{str(d.year + 1)[2:]}" if d.month >= 11 else f"{d.year - 1}/{str(d.year)[2:]}"
                     for d in dates]
    cal["month"] = dates.month
    return cal
