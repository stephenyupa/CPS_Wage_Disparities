#!/usr/bin/env python3
"""
build_db.py - reproducible ingestion step.

Reads data/raw/CPS2015.dta and loads it, unmodified, into a fresh SQLite
database at db/cps_wages.db, into the table defined by
sql/schema/01_schema.sql. This is the only step in the pipeline that
touches the .dta file -- every step after this is plain SQL against
db/cps_wages.db.

No manual loading: running this script is the entire ingestion step.
"""
import sqlite3
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DTA = REPO_ROOT / "data" / "raw" / "CPS2015.dta"
SCHEMA_SQL = REPO_ROOT / "sql" / "schema" / "01_schema.sql"
DB_PATH = REPO_ROOT / "db" / "cps_wages.db"


def main():
    if not RAW_DTA.exists():
        sys.exit(f"Raw source file not found: {RAW_DTA}")

    df = pd.read_stata(RAW_DTA)
    expected_cols = ["year", "ahe", "bachelor", "female", "age"]
    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        sys.exit(
            f"Raw file is missing expected column(s) {missing}. "
            f"Found columns: {list(df.columns)}. Schema/pipeline assume "
            f"exactly {expected_cols}; update sql/schema/01_schema.sql "
            f"before proceeding if the source file's structure changed."
        )

    DB_PATH.parent.mkdir(exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()  # rebuild from scratch every run

    con = sqlite3.connect(DB_PATH)
    try:
        con.executescript(SCHEMA_SQL.read_text())

        rows = [
            (
                row_id,
                int(rec["year"]),
                float(rec["ahe"]),
                int(rec["bachelor"]),
                int(rec["female"]),
                int(rec["age"]),
            )
            for row_id, rec in enumerate(df.to_dict(orient="records"), start=1)
        ]
        con.executemany(
            """
            INSERT INTO cps_2015_raw (row_id, year, ahe, bachelor, female, age)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
        con.commit()

        n = con.execute("SELECT COUNT(*) FROM cps_2015_raw").fetchone()[0]
        print(f"Loaded {n} rows from {RAW_DTA.relative_to(REPO_ROOT)} "
              f"into {DB_PATH.relative_to(REPO_ROOT)}:cps_2015_raw")
    finally:
        con.close()


if __name__ == "__main__":
    main()
