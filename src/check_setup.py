"""Check that the local setup works. Run from the repo root:

    python -m src.check_setup
"""
import importlib
import sys

PACKAGES = [
    "numpy", "pandas", "requests", "dotenv", "matplotlib", "seaborn",
    "scipy", "statsmodels", "sklearn", "geopandas", "folium",
    "pystac_client", "bs4",
]


def main():
    ok = True
    print(f"Python {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("  [MISSING] Python 3.10 or newer required")
        ok = False

    for name in PACKAGES:
        try:
            module = importlib.import_module(name)
            print(f"  [OK] {name} {getattr(module, '__version__', '')}")
        except ImportError:
            print(f"  [MISSING] {name} -> pip install -r requirements.txt")
            ok = False

    if ok:
        from src.db import execute, list_tables
        execute("CREATE TABLE IF NOT EXISTS _setup_check (id INTEGER)")
        execute("DROP TABLE _setup_check")
        print(f"  [OK] SQLite works ({len(list_tables())} tables in project database)")

    print("\nSetup OK." if ok else "\nSetup incomplete, see [MISSING] above.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
