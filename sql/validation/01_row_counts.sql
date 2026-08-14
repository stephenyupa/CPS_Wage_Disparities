-- 01_row_counts.sql
-- Row counts at every stage of the pipeline, so a shrinking or growing
-- count is visible immediately rather than discovered downstream in
-- Stata. On the current raw file, all three counts should be equal
-- (7,098) since none of the filters in 01_filter_valid_rows.sql actually
-- remove any rows -- see the reconciliation report for why.

SELECT 'cps_2015_raw'      AS table_name, COUNT(*) AS row_count FROM cps_2015_raw
UNION ALL
SELECT 'cps_2015_filtered', COUNT(*) FROM cps_2015_filtered
UNION ALL
SELECT 'cps_2015_analysis', COUNT(*) FROM cps_2015_analysis;
