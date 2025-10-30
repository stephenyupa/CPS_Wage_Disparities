// 03_regression.do - Regression Analysis
// Runs models, outputs tables and plots

clear all
set more off

log using "logs/03_regression.log", replace

use "data/CPS_cleaned.dta", clear

// Base model: log_AHE ~ BACHELOR + FEMALE + AGE + i.YEAR
reg log_AHE BACHELOR FEMALE AGE, robust
est store base

// Interaction model: log_AHE ~ BACHELOR*FEMALE + AGE + i.YEAR
reg log_AHE c.BACHELOR##c.FEMALE AGE, robust
est store inter

// Optional: cluster-robust by YEAR (no individual ID available)
reg log_AHE c.BACHELOR##c.FEMALE AGE, vce(cluster AGE)

// Export regression tables
esttab base inter using "output/tables/regression_results.rtf", replace se label star(* 0.10 ** 0.05 *** 0.01) title("Wage Regression Results")

// Coefficient plot
coefplot base inter, drop(_cons) yline(0) saving("output/graphs/coefplot.gph", replace)

// Margins: visualize interaction effects
margins BACHELOR#FEMALE
marginsplot, saving("output/graphs/marginsplot.gph", replace)

log close
