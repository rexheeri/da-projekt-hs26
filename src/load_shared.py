"""Load the team export (Parquet files from src/export_shared.py) into your own database.

For Lorenzo and Levin: you do not need to download the 17 GB of raw data.
1. Copy the export folder from OneDrive/Teams to your computer, e.g. data/export/team/
2. From the repo root:  python -m src.load_shared data/export/team
3. Check:               python -m src.check_setup   (lists the tables)

Works with SQLite (default) and PostgreSQL (if DATABASE_URL is set in .env).
The tables are replaced, so you can run it again with a newer export.
"""
import sys
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from src.db import execute, list_tables, write_table

TABLES = ["stops", "weather_stations", "stop_station", "weather_hourly", "calendar_days", "analysis_base"]


def load_table(path, table):
    """Replace `table` with the content of the Parquet file, read in batches (low memory)."""
    execute(f'DROP TABLE IF EXISTS "{table}"')
    rows = 0
    for batch in pq.ParquetFile(path).iter_batches(batch_size=200_000):
        write_table(batch.to_pandas(), table, if_exists="append")
        rows += batch.num_rows
    return rows


def main(folder):
    folder = Path(folder)
    manifest = pd.read_csv(folder / "manifest.csv").set_index("table")
    for t in TABLES:
        n = load_table(folder / f"{t}.parquet", t)
        expected = manifest.loc[t, "rows"]
        status = "OK" if n == expected else f"MISMATCH (expected {expected})"
        print(f"{t}: {n:,} rows {status}", flush=True)
    print(list_tables().to_string(index=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python -m src.load_shared <export folder>")
    main(sys.argv[1])
