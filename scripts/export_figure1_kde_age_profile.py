#!/usr/bin/env python3
"""
Figure 1 for the "College Wage Premium Arrives Early" write-up.

Left panel: overlaid kernel density of AHE, high school vs bachelor's.
Right panel: fitted wage by age for each degree group, from the
baseline specification (ln_ahe ~ age + female + bachelor, robust SE),
ages 25-34. Fitted values are average predictive margins: for each
(age, bachelor) pair, predict ln_ahe for every worker in the sample
using their own actual `female`, holding age/bachelor fixed at the
target values, average the linear (log) predictions, then
exponentiate -- i.e. Stata's default `margins bachelor, at(age=(25/34))`
behavior on the linear predictor, naively back-transformed (same
convention the write-up itself uses for the 0.4615 -> 58.6% headline
number, with the same caveat about retransformation bias).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import gaussian_kde

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "analysis" / "cps_2015_analysis.dta"
OUT_PATH = REPO_ROOT / "docs" / "figures" / "figure1_kde_and_age_profile.png"

BACHELOR_COLOR = "#2c5f8a"
HS_COLOR = "#8aa9c2"


def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"{DATA_PATH} not found. Run ./scripts/run_all.sh first.")
    df = pd.read_stata(DATA_PATH)
    model = smf.ols("ln_ahe ~ age + female + bachelor", data=df).fit(cov_type="HC1")

    fig, (ax_kde, ax_age) = plt.subplots(1, 2, figsize=(11, 4.5))

    # --- Left: overlaid KDE of AHE by degree status ---
    grid = np.linspace(0, df["ahe"].quantile(0.99), 400)
    for bachelor_val, label, color in [(0, "High school", HS_COLOR), (1, "Bachelor's", BACHELOR_COLOR)]:
        vals = df.loc[df["bachelor"] == bachelor_val, "ahe"]
        kde = gaussian_kde(vals)
        ax_kde.plot(grid, kde(grid), color=color, label=label, linewidth=2)
        ax_kde.fill_between(grid, kde(grid), color=color, alpha=0.15)
    ax_kde.set_xlabel("Average hourly earnings ($)")
    ax_kde.set_ylabel("Density")
    ax_kde.set_title("Hourly earnings by degree status")
    ax_kde.legend(frameon=False)

    # --- Right: fitted wage by age, by degree group (avg. over actual female) ---
    ages = np.arange(25, 35)
    for bachelor_val, label, color in [(0, "High school", HS_COLOR), (1, "Bachelor's", BACHELOR_COLOR)]:
        fitted = []
        for a in ages:
            tmp = df.copy()
            tmp["age"] = a
            tmp["bachelor"] = bachelor_val
            pred_ln = model.predict(tmp)
            fitted.append(np.exp(pred_ln.mean()))
        ax_age.plot(ages, fitted, marker="o", color=color, label=label, linewidth=2)
    ax_age.set_xlabel("Age")
    ax_age.set_ylabel("Fitted wage ($/hour)")
    ax_age.set_title("Fitted wage by age and degree status")
    ax_age.legend(frameon=False)

    fig.suptitle("Figure 1. Hourly earnings by degree status, ages 25 to 34", fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
