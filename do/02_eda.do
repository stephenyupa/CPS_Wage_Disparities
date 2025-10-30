// 02_eda.do - Exploratory Data Analysis
// Summary stats, tables, and descriptive figures

clear all
set more off

log using "logs/02_eda.log", replace

use "data/CPS_cleaned.dta", clear

// Summary statistics
summarize AHE log_AHE AGE

// Table statistics by BACHELOR
tabstat AHE log_AHE AGE, by(BACHELOR) statistics(mean sd min max)

tab BACHELOR
tab FEMALE
tab YEAR

// Boxplot for AHE by Education and Gender
graph box AHE, over(BACHELOR) over(FEMALE) asyvars title("AHE by Education and Gender") saving("output/graphs/box_ahe_education_gender.gph", replace)

// Histogram of log_AHE by BACHELOR and FEMALE
forvalues edu = 0/1 {
  forvalues gen = 0/1 {
    preserve
    keep if BACHELOR == `edu' & FEMALE == `gen'
    histogram log_AHE, bin(25) freq title("log_AHE | Bachelor=`edu', Female=`gen'") saving("output/graphs/hist_logAHE_`edu'_`gen'.gph", replace)
    restore
  }
}

log close
