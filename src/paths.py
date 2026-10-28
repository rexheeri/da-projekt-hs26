"""Central project paths. Import these instead of hard-coding paths in notebooks.

Example (in a notebook under notebooks/):
    import sys; sys.path.append("..")
    from src.paths import RAW_DIR, DB_PATH
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DB_PATH = PROCESSED_DIR / "project.sqlite"

for _d in (RAW_DIR, PROCESSED_DIR):
    _d.mkdir(parents=True, exist_ok=True)
