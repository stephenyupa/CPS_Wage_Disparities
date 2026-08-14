-- 03_null_counts.sql
-- Null count in every column of the final analysis table. All should be
-- zero given 01_filter_valid_rows.sql already drops incomplete rows;
-- this re-checks it downstream, after the recode step, in case a bad
-- recode (e.g. LN() of a value it shouldn't have received) introduced a
-- NULL that wasn't there in the filtered table.

SELECT
    SUM(CASE WHEN year     IS NULL THEN 1 ELSE 0 END) AS null_year,
    SUM(CASE WHEN ahe      IS NULL THEN 1 ELSE 0 END) AS null_ahe,
    SUM(CASE WHEN ln_ahe   IS NULL THEN 1 ELSE 0 END) AS null_ln_ahe,
    SUM(CASE WHEN age      IS NULL THEN 1 ELSE 0 END) AS null_age,
    SUM(CASE WHEN age2     IS NULL THEN 1 ELSE 0 END) AS null_age2,
    SUM(CASE WHEN ln_age   IS NULL THEN 1 ELSE 0 END) AS null_ln_age,
    SUM(CASE WHEN bachelor IS NULL THEN 1 ELSE 0 END) AS null_bachelor,
    SUM(CASE WHEN female   IS NULL THEN 1 ELSE 0 END) AS null_female,
    COUNT(*) AS total_rows
FROM cps_2015_analysis;
