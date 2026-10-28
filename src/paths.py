"""Central project paths. Import these instead of hard-coding paths in notebooks.

Why: absolute paths like C:\\Users\\... only work on one laptop. These paths are
computed relative to the repo, so the same code runs for every team member.

Example (in a notebook under notebooks/):
    import sys; sys.path.append("..")
    from src.paths import RAW_DIR, DB_PATH
"""
from pathlib import Path

# Repo root = the folder above src/ (this file lives in src/paths.py)
ROOT = Path(__file__).resolve().parents[1]

# Data folders (both git-ignored, rebuilt by the scripts in src/)
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"              # downloaded source files, unchanged
PROCESSED_DIR = DATA_DIR / "processed"  # cleaned/joined data, SQLite file

# SQLite database file (used when no DATABASE_URL is set in .env)
DB_PATH = PROCESSED_DIR / "project.sqlite"

# Create the data folders on first import so scripts never fail on a missing folder
for _d in (RAW_DIR, PROCESSED_DIR):
    _d.mkdir(parents=True, exist_ok=True)
