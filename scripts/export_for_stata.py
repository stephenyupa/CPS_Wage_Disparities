#!/usr/bin/env python3
"""
export_for_stata.py - last pipeline step. Exports cps_2015_analysis from
db/cps_wages.db to data/analysis/cps_2015_analysis.dta, the file
do/age_earnings_CPS2015.do actually `use`s. This is the only point where
the SQL pipeline's output re-enters Stata -- everything upstream of this
(ingestion, filtering, recoding) already happened in SQL.
"""
import sqlite3
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "db" / "cps_wages.db"
OUT_PATH = REPO_ROOT / "data" / "analysis" / "cps_2015_analysis.dta"

VARIABLE_LABELS = {
    "row_id": "Surrogate row key (load order in source file, not a person ID)",
    "year": "Survey year",
    "age": "Age in years",
    "age2": "Age squared",
    "ln_age": "Log of age",
    "bachelor": "Bachelor's degree = 1, high school diploma = 0",
    "female": "Female = 1, male = 0",
    "ahe": "Average hourly earnings, $",
    "ln_ahe": "Log of average hourly earnings",
}


def main():
    if not DB_PATH.exists():
        raise SystemExit(f"{DB_PATH} not found. Run scripts/build_db.py and scripts/run_pipeline.py first.")

    con = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql("SELECT * FROM cps_2015_analysis ORDER BY row_id", con)
    finally:
        con.close()

    OUT_PATH.parent.mkdir(exist_ok=True)
    df.to_stata(
        OUT_PATH,
        write_index=False,
        variable_labels=VARIABLE_LABELS,
        data_label="CPS 2015 analysis table, built by the SQL pipeline in sql/",
    )
    print(f"Wrote {len(df)} rows to {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
