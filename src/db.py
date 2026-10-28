"""Database helpers. Every database access in the project goes through this module.

The database is chosen by DATABASE_URL in the file .env (see .env.example):
- not set   -> SQLite file data/processed/project.sqlite (works without setup)
- set       -> e.g. PostgreSQL in Docker (docker-compose.yml), same code

Write standard SQL so that queries run on both. Use named parameters (:name).

Usage in a notebook:
    import sys; sys.path.append("..")
    from src.db import query, write_table, execute, list_tables

    write_table(df, "stops")
    df = query("SELECT * FROM stops WHERE canton = :canton", {"canton": "ZH"})
"""
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, make_url, text

from src.paths import DB_PATH, ROOT

load_dotenv(ROOT / ".env")
DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{DB_PATH.as_posix()}"

# SQLAlchemy >= 2.1 maps "postgresql://" to the psycopg 3 driver, the course
# uses psycopg2. Pin the driver so the URL works with every SQLAlchemy version.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

_engine = None


def get_engine():
    """Return the SQLAlchemy engine (created once per session)."""
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL)
    return _engine


def backend():
    """Name of the database in use: 'sqlite' or 'postgresql'."""
    return make_url(DATABASE_URL).get_backend_name()


def query(sql, params=None):
    """Run a SELECT statement and return the result as a DataFrame."""
    with get_engine().connect() as conn:
        return pd.read_sql_query(text(sql), conn, params=params)


def execute(sql, params=None):
    """Run a statement without result (CREATE, INSERT, UPDATE, DELETE)."""
    with get_engine().begin() as conn:
        conn.execute(text(sql), params or {})


def write_table(df, table, if_exists="replace", chunksize=10_000):
    """Write a DataFrame to a table. if_exists: 'replace', 'append' or 'fail'."""
    df.to_sql(table, get_engine(), if_exists=if_exists, index=False, chunksize=chunksize)


def list_tables():
    """Return all table names with their row counts."""
    names = sorted(inspect(get_engine()).get_table_names())
    rows = [query(f'SELECT COUNT(*) AS n FROM "{t}"')["n"][0] for t in names]
    return pd.DataFrame({"name": names, "rows": rows})
