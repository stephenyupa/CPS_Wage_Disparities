-- 01_sql_summary_stats.sql
-- Key summary statistics on the final analysis table, computed to match
-- what Stata's `summarize` would report (sample standard deviation, i.e.
-- N-1 denominator -- SQLite has no built-in STDEV, so it's computed by
-- hand from sums). Compared against the same statistics computed
-- directly from the raw .dta in scripts/reconcile.py.
--
-- NOTE on the `* 1.0`: `age` is stored as INTEGER, so SUM(age)*SUM(age)
-- and COUNT(*) are both integers, and SQLite's `/` between two integers
-- truncates (integer division), which silently corrupts the variance.
-- `ahe` and `ln_ahe` are REAL already so this isn't needed for them, but
-- the `* 1.0` is applied everywhere for consistency and to guard against
-- the same bug if a future column is added as INTEGER.

SELECT
    COUNT(*)                                                                AS n,
    AVG(ahe)                                                                AS mean_ahe,
    SQRT((SUM(ahe * ahe) - SUM(ahe) * SUM(ahe) * 1.0 / COUNT(*))
         / (COUNT(*) - 1))                                                  AS sd_ahe,
    AVG(ln_ahe)                                                             AS mean_ln_ahe,
    SQRT((SUM(ln_ahe * ln_ahe) - SUM(ln_ahe) * SUM(ln_ahe) * 1.0 / COUNT(*))
         / (COUNT(*) - 1))                                                  AS sd_ln_ahe,
    AVG(age)                                                                AS mean_age,
    SQRT((SUM(age * age) - SUM(age) * SUM(age) * 1.0 / COUNT(*))
         / (COUNT(*) - 1))                                                  AS sd_age,
    AVG(bachelor)                                                           AS bachelor_rate,
    AVG(female)                                                             AS female_rate
FROM cps_2015_analysis;
