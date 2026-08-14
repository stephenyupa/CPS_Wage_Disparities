-- 04_range_checks.sql
-- Flags out-of-range values on wages, age, and education in the final
-- analysis table. Bounds and rationale:
--
--   ahe:      must be > 0 (required for LN(ahe) in the recode step) and
--             <= 500/hr, a deliberately generous sanity ceiling (not a
--             statistical outlier rule) -- anything above it is almost
--             certainly a data entry or unit error, not a real wage.
--   age:      must be 25-34, the population definition stated in the
--             repo README and enforced in 01_filter_valid_rows.sql. A
--             row failing this in the analysis table would mean the
--             filter step itself has a bug.
--   bachelor: must be exactly 0 or 1 (enforced by a CHECK constraint at
--             load time already; re-checked here for defense in depth).
--   female:   must be exactly 0 or 1 (same reasoning).
--
-- Expect zero rows back on the current data -- everything here should
-- already be guaranteed by the schema CHECK constraints and the filter
-- step. A non-empty result means one of those upstream guarantees broke.

SELECT row_id, 'ahe_out_of_range' AS flag, ahe AS value
FROM cps_2015_analysis
WHERE ahe <= 0 OR ahe > 500

UNION ALL

SELECT row_id, 'age_out_of_range', age
FROM cps_2015_analysis
WHERE age < 25 OR age > 34

UNION ALL

SELECT row_id, 'bachelor_out_of_range', bachelor
FROM cps_2015_analysis
WHERE bachelor NOT IN (0, 1)

UNION ALL

SELECT row_id, 'female_out_of_range', female
FROM cps_2015_analysis
WHERE female NOT IN (0, 1)

ORDER BY flag, row_id;
