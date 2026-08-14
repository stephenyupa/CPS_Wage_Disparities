#!/usr/bin/env python3
"""
run_validation.py - executes each query in sql/validation/*.sql against
db/cps_wages.db and prints labeled results. Each file is exactly one SQL
statement, so this is a thin runner, not a query engine: the SQL is the
source of truth, this just executes and formats it.
"""
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "db" / "cps_wages.db"
VALIDATION_DIR = REPO_ROOT / "sql" / "validation"

MAX_ROWS_TO_PRINT = 20


def print_results(cur):
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print("  " + " | ".join(cols))
    for row in rows[:MAX_ROWS_TO_PRINT]:
        print("  " + " | ".join(str(v) for v in row))
    if len(rows) > MAX_ROWS_TO_PRINT:
        print(f"  ... ({len(rows) - MAX_ROWS_TO_PRINT} more rows not shown)")
    if not rows:
        print("  (no rows)")
    return rows


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"{DB_PATH} not found. Run scripts/build_db.py first.")

    con = sqlite3.connect(DB_PATH)
    try:
        for sql_file in sorted(VALIDATION_DIR.glob("*.sql")):
            print(f"\n=== {sql_file.relative_to(REPO_ROOT)} ===")
            cur = con.execute(sql_file.read_text())
            print_results(cur)
    finally:
        con.close()


if __name__ == "__main__":
    main()
