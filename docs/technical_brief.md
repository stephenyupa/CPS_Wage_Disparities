TECHNICAL BRIEF

WAGE DETERMINANTS AMONG U.S. WORKERS AGES 25–34: EVIDENCE FROM CPS, MARCH 2015

Prepared by: Stephen Yupa
Prepared for: Portfolio / professional review (writing sample)
Date: August 18, 2026

*Note on form: This brief is formatted using the numbered-paragraph, exhibit-referenced convention common to expert reports submitted as litigation exhibits (e.g., in wage-and-hour or employment-discrimination matters). No litigation, client, or engagement is associated with this document — it is a writing sample demonstrating that format, applied to the analysis in this repository. See [README.md](../README.md) for the underlying code and reproduction steps.*

---

I. PURPOSE AND SCOPE

1. This brief summarizes an econometric analysis of hourly wage determinants among full-time, full-year U.S. workers ages 25–34, using public-use microdata from the Current Population Survey (CPS), March 2015 supplement.

2. The analysis addresses three questions: (a) how average hourly earnings (AHE) relate to age, gender, and educational attainment; (b) whether the age–earnings relationship is linear or exhibits diminishing returns; and (c) whether the return to a bachelor's degree differs by gender.

3. The sample is restricted to workers with a high school diploma or a bachelor's degree, ages 25–34, consistent with the scope stated in [README.md](../README.md). The estimation sample comprises 7,098 observations (Exhibit 1, columns 1–4).

II. DATA AND METHODOLOGY

4. Data source: CPS March 2015, public-use microdata excerpt, U.S. Bureau of Labor Statistics. The raw file (`data/raw/CPS2015.dta`) is included in this repository for reproducibility. Filtering and variable construction are implemented as an auditable SQL pipeline (`sql/pipeline/`, `sql/validation/`) rather than in the statistical package itself; see [README.md](../README.md) for the full pipeline and a reconciliation step confirming the SQL output matches statistics computed independently from the raw file.

5. Dependent variable: the natural log of average hourly earnings, `ln_ahe`, used to interpret coefficients as approximate percentage effects.

6. Specifications estimated (`do/age_earnings_CPS2015.do`, replicated in Exhibit 1):
   a. Baseline OLS: `ln_ahe` on age, female, bachelor's degree (conventional SEs).
   b. Same specification with heteroskedasticity-robust (White) standard errors.
   c. Expanded model adding a quadratic age term (`age²`) and a female × bachelor's interaction, robust SEs.
   d. Log-log specification (`ln_age`) as a semi-elasticity check.

7. Diagnostic testing: Breusch-Pagan/Cook-Weisberg and White's tests for heteroskedasticity; variance inflation factors (VIF) for multicollinearity. The baseline coefficients in Section III are independently cross-checked outside Stata in `scripts/regress_baseline.py` (statsmodels OLS, HC1 robust SEs); the full specification suite and diagnostics below were run in Stata against the identical pipeline output and are reproducible via `do/age_earnings_CPS2015.do` (estimation log generated locally, not committed — see `.gitignore`).

III. FINDINGS

8. Age. In the baseline specification, each additional year of age is associated with a 2.42% increase in hourly earnings (coefficient 0.0242, SE 0.0020, p<0.001; Exhibit 1, column 1–2). This effect is stable across the robust-SE specification.

9. Gender. Holding age and education constant, women earn approximately 17.8% less than men (coefficient −0.178, SE 0.012, p<0.001; Exhibit 1, columns 1–4). The gap is estimated at −0.190 (SE 0.016) in the interaction specification and is materially unchanged by the addition of a quadratic age term.

10. Education. Holding a bachelor's degree is associated with 46.2% higher earnings relative to a high school diploma (coefficient 0.462, SE 0.012, p<0.001; Exhibit 1, columns 1–2), the largest single effect in the model.

11. Nonlinearity in age. Adding a quadratic term (Exhibit 1, column 3) yields a positive linear age coefficient (0.135, SE 0.046, p=0.003) and a negative, statistically significant quadratic term (−0.00187, SE 0.00077, p=0.016). This indicates earnings rise with age within this 25–34 cohort but at a diminishing rate, consistent with a concave human-capital accumulation profile rather than a constant-return age effect.

12. Gender × education interaction. The female × bachelor's interaction coefficient is 0.0235 (SE 0.0229) and is not statistically distinguishable from zero at conventional levels. The data therefore do not support a claim that the bachelor's-degree wage premium differs by gender within this sample; the degree premium and the gender gap appear approximately additive rather than interactive.

13. Functional form check. The log-log specification (Exhibit 1, column 4) produces an age semi-elasticity of 0.715 (SE 0.059), consistent in direction and significance with the linear-age results and offering no evidence that the semi-log functional form materially misrepresents the age relationship.

IV. ROBUSTNESS, DIAGNOSTICS, AND LIMITATIONS

14. Heteroskedasticity. Both the Breusch-Pagan test (χ²(1) = 39.35, p<0.001) and White's test (χ²(7) = 41.45, p<0.001) reject the null of constant error variance. Accordingly, all reported inference relies on heteroskedasticity-robust (White) standard errors rather than the conventional-SE baseline; this is a data-driven choice, not a default.

15. Multicollinearity. Variance inflation factors in the quadratic specification are elevated for `age` and `age²` (VIF ≈ 541 each; Exhibit 1 diagnostics, `logs/age_earnings_CPS2015.log`). This is the expected mechanical consequence of including a variable and its square and does not indicate a specification error; it does, however, mean the individual linear- and quadratic-age coefficients should not be interpreted in isolation from one another — the marginal effect of age (Section III, ¶11; see `margins`/`marginsplot` output) is the more reliable quantity for interpretation. VIFs for the gender, education, and interaction terms are low (1.7–3.2) and unremarkable.

16. External validity. The sample is limited to full-time, full-year workers ages 25–34 with a high school diploma or bachelor's degree in a single survey month (March 2015). Findings should not be extrapolated to other age ranges, educational categories (e.g., graduate degrees, some college), part-time workers, or later periods without re-estimation on appropriate data.

17. Causal interpretation. This is a cross-sectional, observational analysis. Coefficients on gender and education are conditional associations, not causal effects; unobserved factors correlated with these variables (e.g., occupation, industry, hours composition, unmeasured experience) are not controlled for and could account for part of the estimated gaps.

V. CONCLUSION

18. Within this sample, age, gender, and educational attainment are all statistically significant, economically meaningful predictors of log hourly earnings. The estimated gender gap (≈17–19%) persists after controlling for age and education and does not vary detectably with education. The bachelor's-degree premium (≈46%) is the largest single factor examined. The age-earnings relationship is positive but concave over this age range. All reported estimates use heteroskedasticity-robust inference, consistent with the diagnostic evidence in Section IV.

EXHIBIT LIST

Exhibits 1–5 are pipeline outputs (`output/`, `logs/`) rather than files shipped in the repository — both directories are gitignored by design (see [README.md](../README.md)). They are regenerated by running `./scripts/run_all.sh` followed by `do do/age_earnings_CPS2015.do`, per the reproduction steps in the README.

- Exhibit 1 — Model comparison table (all four specifications): `output/tables/model_comparison.txt`
- Exhibit 2 — Marginal effect of age on predicted wage, by education and gender: `output/graphs/margins_lnAHE_age_profile.gph`
- Exhibit 3 — AHE distribution by education and gender: `output/graphs/box_ahe_edu_gender.gph`
- Exhibit 4 — Wage-age scatter with linear fit: `output/graphs/scatter_ahe_age_linearfit.gph`
- Exhibit 5 — Full estimation log (regressions, diagnostics, margins): `logs/age_earnings_CPS2015.log`

---

Prepared by Stephen Yupa. Code and full reproduction instructions: [README.md](../README.md). Contact: stepheny042405@gmail.com.
