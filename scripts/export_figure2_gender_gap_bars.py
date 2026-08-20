#!/usr/bin/env python3
"""
Figure 2 for the wage-premium write-up: gender wage gap, unadjusted
and adjusted for age and education.

Two bars: (1) the raw log-wage gap by sex (`ln_ahe ~ female`, robust
SE, no controls) and (2) the female coefficient from the baseline
specification (`ln_ahe ~ age + female + bachelor`, robust SE). Both
are transformed to percentages via exp(coef) - 1, with 95% confidence
intervals computed by transforming the log-scale CI bounds the same
way (not by scaling the point estimate's CI width), since the
percentage transform is nonlinear.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "analysis" / "cps_2015_analysis.dta"
OUT_PATH = REPO_ROOT / "docs" / "figures" / "figure2_gender_gap_bars.png"

BAR_COLOR = "#2c5f8a"


def pct_and_ci(coef: float, se: float) -> tuple[float, float, float]:
    lo, hi = coef - 1.96 * se, coef + 1.96 * se
    return (np.exp(coef) - 1) * 100, (np.exp(lo) - 1) * 100, (np.exp(hi) - 1) * 100


def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"{DATA_PATH} not found. Run ./scripts/run_all.sh first.")
    df = pd.read_stata(DATA_PATH)

    unadj = smf.ols("ln_ahe ~ female", data=df).fit(cov_type="HC1")
    adj = smf.ols("ln_ahe ~ age + female + bachelor", data=df).fit(cov_type="HC1")

    pct_u, lo_u, hi_u = pct_and_ci(unadj.params["female"], unadj.bse["female"])
    pct_a, lo_a, hi_a = pct_and_ci(adj.params["female"], adj.bse["female"])

    labels = ["Unadjusted\n(raw wage difference)", "Adjusted\n(age + education)"]
    pcts = [pct_u, pct_a]
    err_lo = [pct_u - lo_u, pct_a - lo_a]
    err_hi = [hi_u - pct_u, hi_a - pct_a]

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.bar(labels, pcts, color=BAR_COLOR, width=0.5,
           yerr=[err_lo, err_hi], capsize=6, ecolor="black")
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_ylabel("Women's wages relative to men's (%)")
    ax.set_title("Figure 2. Gender wage gap, unadjusted and adjusted\nfor age and education")
    for i, (p, hi) in enumerate(zip(pcts, [hi_u, hi_a])):
        ax.annotate(f"{p:.1f}%", (i, hi + 0.6), ha="center", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
    print(f"Wrote {OUT_PATH}")
    print(f"Unadjusted: {pct_u:.1f}% [{lo_u:.1f}%, {hi_u:.1f}%]")
    print(f"Adjusted:   {pct_a:.1f}% [{lo_a:.1f}%, {hi_a:.1f}%]")


if __name__ == "__main__":
    main()
