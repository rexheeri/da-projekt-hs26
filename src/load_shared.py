"""Load the team export (Parquet files from src/export_shared.py) into your own database.

For Lorenzo and Levin: you do not need to download the 17 GB of raw data.
The export is attached to a GitHub release of this repo (e.g. tag "data-v1").

    python -m src.load_shared --release data-v1     # download the release, then load it
    python -m src.load_shared data/export/team      # load an export folder you already have
    python -m src.check_setup                       # check: lists the tables

--release downloads the files over plain HTTPS from the public release page
(no GitHub login, no `gh` needed) into data/export/<tag>/. Files already there
are not downloaded again. Every table is checked against the row count in
manifest.csv.

Works with SQLite (default) and PostgreSQL (if DATABASE_URL is set in .env).
The tables are replaced, so you can run it again with a newer export.
"""
import argparse
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from src.db import execute, list_tables, write_table
from src.download import download_file
from src.paths import DATA_DIR

TABLES = ["stops", "weather_stations", "stop_station", "weather_hourly", "calendar_days", "analysis_base"]
# Public repo: release files are at .../releases/download/<tag>/<file name>
RELEASE_URL = "https://github.com/rexheeri/da-projekt-hs26/releases/download/{tag}/{name}"


def download_release(tag):
    """Download manifest.csv and all table files of a release to data/export/<tag>/."""
    folder = DATA_DIR / "export" / tag
    # The manifest comes first: it lists the tables, so we know what to fetch
    download_file(RELEASE_URL.format(tag=tag, name="manifest.csv"), folder / "manifest.csv")
    for t in pd.read_csv(folder / "manifest.csv")["table"]:
        download_file(RELEASE_URL.format(tag=tag, name=f"{t}.parquet"), folder / f"{t}.parquet")
    return folder


def load_table(path, table):
    """Replace `table` with the content of the Parquet file, read in batches (low memory)."""
    execute(f'DROP TABLE IF EXISTS "{table}"')
    rows = 0
    for batch in pq.ParquetFile(path).iter_batches(batch_size=200_000):
        write_table(batch.to_pandas(), table, if_exists="append")
        rows += batch.num_rows
    return rows


def main(folder):
    """Load all tables of an export folder and compare the row counts with manifest.csv."""
    folder = Path(folder)
    manifest = pd.read_csv(folder / "manifest.csv").set_index("table")
    for t in TABLES:
        n = load_table(folder / f"{t}.parquet", t)
        expected = manifest.loc[t, "rows"]
        status = "OK" if n == expected else f"MISMATCH (expected {expected})"
        print(f"{t}: {n:,} rows {status}", flush=True)
    print(list_tables().to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("folder", nargs="?", help="export folder with manifest.csv and *.parquet")
    source.add_argument("--release", metavar="TAG", help="GitHub release tag, e.g. data-v1")
    args = parser.parse_args()
    main(download_release(args.release) if args.release else args.folder)
