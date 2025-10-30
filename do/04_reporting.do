// 04_reporting.do - Export Tables and Figures for Reporting

clear all
set more off

log using "logs/04_reporting.log", replace

use "data/CPS_cleaned.dta", clear

// Export previous regression tables in HTML and Word
esttab using "output/tables/reg_results.html", html replace
esttab using "output/tables/reg_results.docx", rtf replace

// Export graphs as PDF for sharing
foreach graph in coefplot marginsplot box_ahe_education_gender {
  graph use "output/graphs/`graph'.gph"
  graph export "output/graphs/`graph'.pdf", replace
}

// Optional: export all histograms
forvalues edu = 0/1 {
  forvalues gen = 0/1 {
    local hname hist_logAHE_`edu'_`gen'
    capture confirm file output/graphs/`hname'.gph
    if !_rc {
      graph use "output/graphs/`hname'.gph"
      graph export "output/graphs/`hname'.pdf", replace
    }
  }
}

log close
