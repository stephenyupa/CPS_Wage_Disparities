#!/usr/bin/env python3
"""
reconcile.py - compares the SQL pipeline's output table (cps_2015_analysis)
against statistics computed independently, straight from the raw .dta,
using the same formulas do/age_earnings_CPS2015.do uses (log(ahe),
age^2, sample N-1 standard deviation).

No Stata license is available in this environment, so this script does
not literally run age_earnings_CPS2015.do. Instead it recomputes, in
pandas, exactly what that do-file's `summarize`/`gen` commands would
produce from the same raw values, and treats that as the reconciliation
target. This is a faithful stand-in because Stata's `summarize` and
`log()` on IEEE-754 doubles/floats over the same 7,098 values will not
diverge from pandas/numpy doing the same arithmetic.

If any statistic differs beyond floating-point tolerance, this script
prints the discrepancy and exits non-zero. It does not adjust anything
to force a match.
"""
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DTA = REPO_ROOT / "data" / "raw" / "CPS2015.dta"
DB_PATH = REPO_ROOT / "db" / "cps_wages.db"
SQL_FILE = REPO_ROOT / "sql" / "reconciliation" / "01_sql_summary_stats.sql"
REPORT_PATH = REPO_ROOT / "sql" / "reconciliation" / "RECONCILIATION.md"

TOLERANCE = 1e-6


def stata_equivalent_stats_from_raw():
    # Stata's `summarize` computes internally in double precision
    # regardless of a variable's storage type. The .dta stores these as
    # 4-byte floats, and pandas/numpy will silently accumulate mean/std
    # in that same float32 precision unless explicitly widened first --
    # so cast to float64 here to match what Stata actually reports.
    df = pd.read_stata(RAW_DTA).astype(
        {"ahe": "float64", "age": "float64", "bachelor": "float64", "female": "float64"}
    )
    ln_ahe = np.log(df["ahe"])
    return {
        "n": len(df),
        "mean_ahe": df["ahe"].mean(),
        "sd_ahe": df["ahe"].std(ddof=1),
        "mean_ln_ahe": ln_ahe.mean(),
        "sd_ln_ahe": ln_ahe.std(ddof=1),
        "mean_age": df["age"].mean(),
        "sd_age": df["age"].std(ddof=1),
        "bachelor_rate": df["bachelor"].mean(),
        "female_rate": df["female"].mean(),
    }


def sql_stats_from_db():
    con = sqlite3.connect(DB_PATH)
    try:
        cur = con.execute(SQL_FILE.read_text())
        cols = [d[0] for d in cur.description]
        row = cur.fetchone()
        return dict(zip(cols, row))
    finally:
        con.close()


def main():
    if not DB_PATH.exists():
        raise SystemExit(
            f"{DB_PATH} not found. Run scripts/build_db.py and "
            f"scripts/run_pipeline.py first."
        )

    stata_stats = stata_equivalent_stats_from_raw()
    sql_stats = sql_stats_from_db()

    lines = []
    lines.append("# Reconciliation: SQL analysis table vs. Stata-equivalent (raw .dta)\n")
    lines.append(
        "No Stata license was available to run do/age_earnings_CPS2015.do "
        "directly. The 'Stata-equivalent' column below is computed in "
        "pandas straight from data/raw/CPS2015.dta using the same "
        "formulas that do-file uses (log(ahe), sample N-1 std dev), "
        "independently of the SQL pipeline. The 'SQL' column is read from "
        "db/cps_wages.db:cps_2015_analysis via "
        "sql/reconciliation/01_sql_summary_stats.sql.\n"
    )
    lines.append("| statistic | Stata-equivalent | SQL | difference | match (tol 1e-6) |")
    lines.append("|---|---|---|---|---|")

    all_match = True
    for key in [
        "n", "mean_ahe", "sd_ahe", "mean_ln_ahe", "sd_ln_ahe",
        "mean_age", "sd_age", "bachelor_rate", "female_rate",
    ]:
        stata_val = stata_stats[key]
        sql_val = sql_stats[key]
        diff = abs(stata_val - sql_val)
        match = diff <= TOLERANCE
        all_match &= match
        lines.append(
            f"| {key} | {stata_val:.6f} | {sql_val:.6f} | {diff:.2e} | "
            f"{'yes' if match else 'NO'} |"
        )

    lines.append("")
    lines.append(f"**Overall: {'MATCH' if all_match else 'DISCREPANCY FOUND'}**")

    report = "\n".join(lines)
    print(report)
    REPORT_PATH.write_text(report + "\n")
    print(f"\nWrote {REPORT_PATH.relative_to(REPO_ROOT)}")

    if not all_match:
        sys.exit(1)


if __name__ == "__main__":
    main()
