# Reconciliation: SQL analysis table vs. Stata-equivalent (raw .dta)

No Stata license was available to run do/age_earnings_CPS2015.do directly. The 'Stata-equivalent' column below is computed in pandas straight from data/raw/CPS2015.dta using the same formulas that do-file uses (log(ahe), sample N-1 std dev), independently of the SQL pipeline. The 'SQL' column is read from db/cps_wages.db:cps_2015_analysis via sql/reconciliation/01_sql_summary_stats.sql.

| statistic | Stata-equivalent | SQL | difference | match (tol 1e-6) |
|---|---|---|---|---|
| n | 7098.000000 | 7098.000000 | 0.00e+00 | yes |
| mean_ahe | 21.237438 | 21.237438 | 0.00e+00 | yes |
| sd_ahe | 12.124505 | 12.124505 | 3.55e-15 | yes |
| mean_ln_ahe | 2.912822 | 2.912822 | 0.00e+00 | yes |
| sd_ln_ahe | 0.536494 | 0.536494 | 1.11e-16 | yes |
| mean_age | 29.630459 | 29.630459 | 0.00e+00 | yes |
| sd_age | 2.876728 | 2.876728 | 3.55e-15 | yes |
| bachelor_rate | 0.525923 | 0.525923 | 0.00e+00 | yes |
| female_rate | 0.416878 | 0.416878 | 0.00e+00 | yes |

**Overall: MATCH**
