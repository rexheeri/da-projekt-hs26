"""Draw the simple ER diagram of the database for the slide "data structure".

Output: presentation/figures/er_diagram.png
Run from the repo root:  python -m tools.make_er_diagram

Only the key columns are shown (the full schema is in src/schema.sql).
Plain matplotlib boxes and arrows, so no extra package is needed.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from src.paths import ROOT

# Table name -> (x, y of the box centre, list of key columns). PK = primary key, FK = foreign key
TABLES = {
    "arrivals":         (0.18, 0.55, ["trip_id, service_date", "bpuic (FK)", "sched_arr_utc",
                                      "arr_delay_min, delayed", "traffic_type", "weather_hour_utc (FK)",
                                      "local_date (FK)"]),
    "stops":            (0.50, 0.85, ["bpuic (PK)", "stop_name", "lv95_east, lv95_north"]),
    "stop_station":     (0.50, 0.55, ["bpuic (PK, FK)", "precip_station (FK)", "temp_station (FK)",
                                      "distances km"]),
    "weather_stations": (0.83, 0.85, ["station_abbr (PK)", "network smn / precip", "height, LV95"]),
    "weather_hourly":   (0.83, 0.50, ["station_abbr (PK, FK)", "time_utc (PK)", "precip_mm, temp_c"]),
    "calendar_days":    (0.18, 0.15, ["local_date (PK)", "holiday", "winter, month"]),
}
LINKS = [  # (from, to, label)
    ("arrivals", "stops", "bpuic"),
    ("arrivals", "stop_station", "bpuic"),
    ("stop_station", "weather_hourly", "station + hour"),
    ("stop_station", "weather_stations", "station"),
    ("weather_hourly", "weather_stations", "station"),
    ("arrivals", "calendar_days", "local_date"),
]
W, LINE_H = 0.25, 0.032


def box_height(cols):
    """Box height: one title line plus one line per column."""
    return LINE_H * (len(cols) + 1.6)


def edge_points(a, b):
    """Start and end point of an arrow from box a to box b, on the box borders.

    Mostly side by side -> leave from the left/right border; mostly above each
    other -> leave from the top/bottom border. So arrows never cross the text.
    """
    xa, ya, ca = TABLES[a]
    xb, yb, cb = TABLES[b]
    ha, hb = box_height(ca) / 2, box_height(cb) / 2
    if abs(xb - xa) > 0.1:  # boxes in different columns -> horizontal connection
        sign = 1 if xb > xa else -1
        return (xa + sign * W / 2, ya), (xb - sign * W / 2, yb)
    sign = 1 if yb > ya else -1  # same column -> vertical connection
    return (xa, ya + sign * ha), (xb, yb - sign * hb)


def main():
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_axis_off()
    for name, (x, y, cols) in TABLES.items():
        h = box_height(cols)
        ax.add_patch(FancyBboxPatch((x - W / 2, y - h / 2), W, h, boxstyle="round,pad=0.005",
                                    fc="#f4f6f8", ec="#333333", lw=1.2))
        ax.text(x, y + h / 2 - LINE_H * 0.8, name, ha="center", va="center", fontsize=12, weight="bold")
        for i, c in enumerate(cols):
            ax.text(x - W / 2 + 0.01, y + h / 2 - LINE_H * (i + 1.9), c, ha="left", va="center", fontsize=9.5)
    for a, b, label in LINKS:
        (xa, ya), (xb, yb) = edge_points(a, b)
        ax.annotate("", xy=(xb, yb), xytext=(xa, ya),
                    arrowprops=dict(arrowstyle="-|>", color="#1f5fa8", lw=1.3, shrinkA=0, shrinkB=0))
        ax.text((xa + xb) / 2, (ya + yb) / 2 + 0.015, label, ha="center", va="bottom", fontsize=9,
                color="#1f5fa8", bbox=dict(fc="white", ec="none", pad=1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.set_title("Database: one arrival is linked to its stop, its two weather stations, the weather hour and the day",
                 fontsize=12)
    fig.text(0.01, 0.01, "Source: own database (src/schema.sql); key columns only. analysis_base = SQL join of all tables.",
             fontsize=8.5, color="#555555")
    out = ROOT / "presentation" / "figures" / "er_diagram.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"saved {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
