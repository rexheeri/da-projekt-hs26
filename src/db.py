"""SQLite helpers. Every database access in the project goes through this module.

Usage in a notebook:
    import sys; sys.path.append("..")
    from src.db import get_connection, query, write_table

    write_table(df, "stops")                       # DataFrame -> table
    df = query("SELECT * FROM stops WHERE canton = ?", ("ZH",))
"""
import sqlite3

import pandas as pd

from src.paths import DB_PATH


def get_connection(db_path=DB_PATH):
    """Open a connection to the project database (created if missing)."""
    return sqlite3.connect(db_path)


def query(sql, params=(), db_path=DB_PATH):
    """Run a SELECT statement and return the result as a DataFrame."""
    with get_connection(db_path) as conn:
        return pd.read_sql_query(sql, conn, params=params)


def execute(sql, params=(), db_path=DB_PATH):
    """Run a statement without result (CREATE, INSERT, UPDATE, DELETE)."""
    with get_connection(db_path) as conn:
        conn.execute(sql, params)
        conn.commit()


def write_table(df, table, if_exists="replace", db_path=DB_PATH):
    """Write a DataFrame to a table. if_exists: 'replace', 'append' or 'fail'."""
    with get_connection(db_path) as conn:
        df.to_sql(table, conn, if_exists=if_exists, index=False)


def list_tables(db_path=DB_PATH):
    """Return all table names with their row counts."""
    tables = query("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name", db_path=db_path)
    counts = [query(f'SELECT COUNT(*) AS n FROM "{t}"', db_path=db_path)["n"][0] for t in tables["name"]]
    return tables.assign(rows=counts)
