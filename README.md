# Wage Determinants via Robust Regression – U.S. CPS 2015 Analysis

This repository demonstrates *modern, robust econometric modeling* using U.S. labor data for portfolio and professional review.

The workflow covers all key steps: data cleaning, exploratory analysis, rich regression modeling (incl. nonlinearities and interactions), and results/output professionalization—ready for reproducibility and hiring assessment.

---

## Overview / Skills Demonstrated
- Linear and log-linear regression modeling
- Semi-log and nonlinear effects (age^2, log(age), and margins)
- Interaction effects (gender, education, their cross-effects)
- Robust and reproducible estimation + code
- Automated export of tables and graphs for inclusion in business/deck
- Clear, commented Stata code structure for employer code review

## Data
- **CPS2015.dta** (included): U.S. Current Population Survey, March 2015, full-time full-year workers, age 25–34, with high school or bachelor’s degree
- This data file is included for educational, demonstration, and portfolio reproducibility purposes only. Source: US Bureau of Labor Statistics (public use microdata excerpt).
- Place your copy in: `data/raw/CPS2015.dta` if running locally.

## Repository Structure
```
├── data/
│   └── raw/
│        └── CPS2015.dta
├── do/
│   ├── 01_dataprep.do
│   ├── 02_eda.do
│   ├── 03_regression.do
│   └── age_earnings_CPS2015.do   # advanced modeling (showcase)
├── output/
│   ├── tables/
│   └── graphs/
├── logs/
├── .gitignore
└── README.md
```

## How to Run
1. Place your `CPS2015.dta` in `data/raw/`.
2. Open Stata and set your working directory to the main repo folder.
3. Run analysis, e.g.:
    ```
    do do/age_earnings_CPS2015.do
    ```
4. All outputs are written to `output/tables/` and `output/graphs/` automatically, logs to `logs/`.

## Key Results & Business Insight

- **Wage Determinants:** Econometric modeling demonstrates statistically and economically significant wage premiums for older workers and those with a bachelor’s degree, after controlling for gender and experience.
- **Demographic Disparities:** Gender wage gaps persist, but the degree premium is evident for both men and women. Advanced interaction modeling confirms differences in returns by group.
- **Nonlinear Age Profile:** A quadratic age specification reveals wage growth is positive but slows near the upper end of this cohort’s age range (25–34), consistent with human capital theory.
- **Robustness and Diagnostics:** All models utilize robust (White) standard errors, with formal heteroskedasticity and multicollinearity testing (Breusch-Pagan, White’s test, VIF). These ensure reliable inference for business decisions.
- **Actionable Analytics:** Margins and predictive plots quantify expected wage increases for business/HR benchmarking and highlight target demographics for policy or intervention.
- **Professional Practices:** All code is fully reproducible, well-documented, and outputs reports/plots ready for stakeholder or code review.

_This workflow demonstrates advanced quantitative and econometric competencies suitable for data analyst, economics, or quant roles._

## Why this matters
This project structure, modeling approach, and interpretive output mirror best practices leading employers expect from modern economics/data science analysts. Deliverables here (code, diagnostics, and interpretations) are ready for direct use in consulting, policy, or business analytics review.

## Requirements
- Stata 14 or newer
- SSC add-on (for tables): `ssc install estout`

## Example Interpretation
> This codebase showcases the quantification of wage determinants (age, gender, education) using multiple model specifications. Outputs include predicted wage differences by profile and a variety of effect visualizations. Example: In a quadratic specification, an additional year of age increases predicted earnings more for college graduates than high school grads; interaction terms quantify gender-education differences. All results are fully reproducible.

## Citation/Contact
Feel free to reuse or adapt the code structure for your own empirical portfolio. For questions, reach out at [stepheny042405@gmail.com].

---
**Note:** No data has been included or distributed. All analysis can be replicated by following setup/running instructions with your own legally obtained CPS2015.dta file.
