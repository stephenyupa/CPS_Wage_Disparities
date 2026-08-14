#!/usr/bin/env python3
"""
run_pipeline.py - executes sql/pipeline/*.sql, in numbered order, against
db/cps_wages.db. Registers a Python LN() fallback so this works
identically regardless of whether the local SQLite build was compiled
with math functions enabled.
"""
import math
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "db" / "cps_wages.db"
PIPELINE_DIR = REPO_ROOT / "sql" / "pipeline"


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"{DB_PATH} not found. Run scripts/build_db.py first.")

    con = sqlite3.connect(DB_PATH)
    con.create_function("LN", 1, lambda x: math.log(x) if x is not None else None)
    try:
        for sql_file in sorted(PIPELINE_DIR.glob("*.sql")):
            print(f"Running {sql_file.relative_to(REPO_ROOT)} ...")
            con.executescript(sql_file.read_text())
        con.commit()

        for table in ("cps_2015_filtered", "cps_2015_analysis"):
            n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {n} rows")
    finally:
        con.close()


if __name__ == "__main__":
    main()
