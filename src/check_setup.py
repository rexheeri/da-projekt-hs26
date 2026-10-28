"""Check that the local setup works. Run from the repo root:

    python -m src.check_setup

Checks the Python version, all required packages and the database connection.
Exit code 0 = everything OK, 1 = something is missing (useful for scripts).
"""
import importlib
import sys

# Import names of the packages from requirements.txt
# (import name differs from pip name for some: dotenv = python-dotenv, sklearn = scikit-learn, bs4 = beautifulsoup4)
PACKAGES = [
    "numpy", "pandas", "requests", "dotenv", "sqlalchemy", "psycopg2",
    "matplotlib", "seaborn",
    "scipy", "statsmodels", "sklearn", "geopandas", "folium",
    "pystac_client", "bs4",
]


def main():
    """Run all checks and print one line per check."""
    ok = True

    # 1. Python version
    print(f"Python {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("  [MISSING] Python 3.10 or newer required")
        ok = False

    # 2. Packages: try to import each one and show its version
    for name in PACKAGES:
        try:
            module = importlib.import_module(name)
            print(f"  [OK] {name} {getattr(module, '__version__', '')}")
        except ImportError:
            print(f"  [MISSING] {name} -> pip install -r requirements.txt")
            ok = False

    # 3. Database: only if the packages are there (src.db needs pandas and sqlalchemy)
    if ok:
        from src.db import backend, execute, list_tables
        try:
            # Create and drop a dummy table = proves we can connect and write
            execute("CREATE TABLE IF NOT EXISTS _setup_check (id INTEGER)")
            execute("DROP TABLE _setup_check")
            print(f"  [OK] Database works: {backend()} ({len(list_tables())} tables)")
        except Exception as exc:  # e.g. PostgreSQL container not running
            print(f"  [MISSING] Database {backend()} not reachable: {exc.__class__.__name__}")
            print("            PostgreSQL: is `docker compose up -d` running? Otherwise remove DATABASE_URL from .env")
            ok = False

    print("\nSetup OK." if ok else "\nSetup incomplete, see [MISSING] above.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
