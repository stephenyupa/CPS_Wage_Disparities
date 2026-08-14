-- 02_duplicate_check.sql
-- Duplicate check on the join key.
--
-- IMPORTANT CAVEAT: CPS2015.dta has no person or household identifier
-- (see sql/schema/01_schema.sql). There is no real join key to check
-- duplicates against. What this query actually does is group on every
-- observable field (year, ahe, bachelor, female, age) and flag exact
-- full-record duplicates -- the closest available proxy.
--
-- On the current raw data this returns a large number of duplicate
-- groups (3,029 of 7,098 rows, ~43%). That is expected, not a data
-- quality defect: with only ~10 distinct ages, 2 education levels, 2
-- genders, and a wage variable that itself repeats common rounded hourly
-- rates, two unrelated respondents landing on identical values across
-- all five fields is unsurprising in a sample this size. Without an ID
-- column this query cannot distinguish "same person twice" from
-- "two different people who happen to share every recorded
-- characteristic" -- treat its output as informational, not as a
-- pass/fail gate.

SELECT
    year,
    ahe,
    bachelor,
    female,
    age,
    COUNT(*) AS n_duplicate_rows
FROM cps_2015_raw
GROUP BY year, ahe, bachelor, female, age
HAVING COUNT(*) > 1
ORDER BY n_duplicate_rows DESC, ahe;
