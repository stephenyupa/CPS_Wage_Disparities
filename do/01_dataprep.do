// 01_dataprep.do - Data Preparation
// Loads raw data, drops missing values, generates analysis variables, and saves cleaned set
// Author: [Stephen Yupa]
// Date: [10/30/2025]

clear all
set more off

log using "logs/01_dataprep.log", replace

// Load and label the datasets
use "data/raw/CPS2015.dta", clear
// No renaming needed: FEMALE, YEAR, AHE, BACHELOR, AGE already conform to dictionary
append using "../data/raw/CPS2015.dta"

// Drop if missing in critical variables
foreach var in AHE BACHELOR FEMALE AGE {
   drop if missing(`var')
}

// Generate log(AHE)
gen log_AHE = log(AHE)

// Encode YEAR as a factor (for easier regression)
encode string(YEAR), gen(year_cat) // optional: treat YEAR as factor

// Create interaction term
// BACHELOR*FEMALE = 1 if bachelor female, 0 else
gen bachelor_female = BACHELOR * FEMALE

// Save cleaned dataset for use in later steps
save "data/CPS_cleaned.dta", replace

log close
