#!/usr/bin/env python3
"""
export_figures.py - reproduces two of the figures from
do/age_earnings_CPS2015.do (specs 5 and 11) in matplotlib, against
data/analysis/cps_2015_analysis.dta, for cases where a Stata license
isn't available to run the do-file's own `graph export` step.

Figure 1: marginal effect of age on predicted ln(ahe), computed from
the quadratic model `ln_ahe ~ age + age2 + female + bachelor +
female:bachelor` (robust SE), evaluated at age = 25..34. Mirrors the
do-file's `margins i.bachelor i.female, at(age=(25(1)34)) dydx(age)`
+ marginsplot.

Figure 2: distribution of ahe by education and gender. Mirrors the
do-file's `graph box ahe, over(bachelor) over(female) asyvars`.

Output: docs/figures/figure1_margins_age_profile.png,
        docs/figures/figure2_box_ahe_edu_gender.png
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
OUT_DIR = REPO_ROOT / "docs" / "figures"


def make_figure1(df: pd.DataFrame) -> None:
    model = smf.ols(
        "ln_ahe ~ age + age2 + female + bachelor + female:bachelor", data=df
    ).fit(cov_type="HC1")

    ages = np.arange(25, 35)
    # dy/dx wrt age for ln_ahe = b0 + b1*age + b2*age^2 + ... is b1 + 2*b2*age.
    # Does not vary by female/bachelor in this specification (no age
    # interaction terms), matching the do-file's model.
    b1 = model.params["age"]
    b2 = model.params["age2"]
    dydx = b1 + 2 * b2 * ages

    # Delta-method SE for a linear combination of two coefficients.
    cov = model.cov_params()
    var_b1 = cov.loc["age", "age"]
    var_b2 = cov.loc["age2", "age2"]
    cov_b1b2 = cov.loc["age", "age2"]
    se = np.sqrt(var_b1 + (2 * ages) ** 2 * var_b2 + 2 * (2 * ages) * cov_b1b2)
    ci_lo, ci_hi = dydx - 1.96 * se, dydx + 1.96 * se

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ages, dydx, marker="o", color="#2c5f8a", label="Marginal effect of age")
    ax.fill_between(ages, ci_lo, ci_hi, color="#2c5f8a", alpha=0.2, label="95% CI")
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xlabel("Age")
    ax.set_ylabel("dy/dx: marginal effect of age on ln(AHE)")
    ax.set_title("Marginal Effect of Age on Predicted Wage")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "figure1_margins_age_profile.png", dpi=200)
    plt.close(fig)


def make_figure2(df: pd.DataFrame) -> None:
    groups = [
        ("HS, Male", (df["bachelor"] == 0) & (df["female"] == 0)),
        ("HS, Female", (df["bachelor"] == 0) & (df["female"] == 1)),
        ("Bachelor's, Male", (df["bachelor"] == 1) & (df["female"] == 0)),
        ("Bachelor's, Female", (df["bachelor"] == 1) & (df["female"] == 1)),
    ]
    data = [df.loc[mask, "ahe"] for _, mask in groups]
    labels = [label for label, _ in groups]
    colors = ["#8aa9c2", "#8aa9c2", "#2c5f8a", "#2c5f8a"]

    fig, ax = plt.subplots(figsize=(7, 5))
    bp = ax.boxplot(data, tick_labels=labels, patch_artist=True, showfliers=False)
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
    ax.set_ylabel("Average hourly earnings ($)")
    ax.set_title("AHE by Education and Gender")
    plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "figure2_box_ahe_edu_gender.png", dpi=200)
    plt.close(fig)


def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"{DATA_PATH} not found. Run ./scripts/run_all.sh first.")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_stata(DATA_PATH)
    make_figure1(df)
    make_figure2(df)
    print(f"Wrote {OUT_DIR / 'figure1_margins_age_profile.png'}")
    print(f"Wrote {OUT_DIR / 'figure2_box_ahe_edu_gender.png'}")


if __name__ == "__main__":
    main()
