#!/usr/bin/env python3
"""
regress_baseline.py - fits the baseline log-wage regression from
do/age_earnings_CPS2015.do (`regress ln_ahe age i.female i.bachelor,
robust`) directly against data/analysis/cps_2015_analysis.dta, using
statsmodels with HC1 heteroskedasticity-robust standard errors (the same
estimator Stata's `, robust` option uses for OLS).

This exists so the headline coefficients quoted in README.md can be
reproduced by anyone, including without a Stata license.
"""
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "analysis" / "cps_2015_analysis.dta"


def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"{DATA_PATH} not found. Run ./scripts/run_all.sh first.")

    df = pd.read_stata(DATA_PATH)
    model = smf.ols("ln_ahe ~ age + female + bachelor", data=df).fit(cov_type="HC1")
    print(model.summary())


if __name__ == "__main__":
    main()
