"""Team export: the database tables as Parquet files, so that the whole team can
work with the same data without running the full download (17 GB) themselves.

The export is never committed to the repo. It is attached as files to a GitHub
release (data-v1, data-v2, ...; see docs/data-releases.md); the others load it
with `python -m src.load_shared --release <tag>`.

Usage (from the repo root):
    python -m src.export_shared                 # -> data/export/team/
Output: one Parquet file per table + manifest.csv (rows, size, export date).
"""
import sys
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import text

from src.db import get_engine
from src.paths import DATA_DIR

TABLES = ["analysis_base", "stops", "weather_stations", "stop_station", "weather_hourly", "calendar_days"]
CHUNK_ROWS = 500_000  # rows per read, keeps memory low for the 10-million-row table


def export_table(table, folder):
    """Copy one table to <folder>/<table>.parquet in chunks. Returns the number of rows."""
    out = Path(folder) / f"{table}.parquet"
    writer, rows, schema = None, 0, None
    with get_engine().connect() as conn:
        for chunk in pd.read_sql_query(text(f'SELECT * FROM "{table}"'), conn, chunksize=CHUNK_ROWS):
            batch = pa.Table.from_pandas(chunk, preserve_index=False)
            if writer is None:
                schema = batch.schema
                writer = pq.ParquetWriter(out, schema, compression="zstd")
            # All chunks must have the same column types as the first one
            writer.write_table(batch.cast(schema))
            rows += len(chunk)
    if writer:
        writer.close()
    return rows


def main(folder=DATA_DIR / "export" / "team"):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    manifest = []
    for t in TABLES:
        n = export_table(t, folder)
        size = (folder / f"{t}.parquet").stat().st_size / 1e6
        manifest.append({"table": t, "rows": n, "mb": round(size, 1)})
        print(f"{t}: {n:,} rows, {size:.1f} MB", flush=True)
    m = pd.DataFrame(manifest)
    m["exported"] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    m.to_csv(folder / "manifest.csv", index=False)
    print(f"total {m.mb.sum():.0f} MB in {folder}")


if __name__ == "__main__":
    main(*sys.argv[1:])
