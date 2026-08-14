-- 01_filter_valid_rows.sql
-- Purpose: apply the filters that define the analysis population.
--
-- There is only one raw source table (cps_2015_raw) and it carries no
-- person/household identifier, so there is no join step in this
-- pipeline -- we go directly from the raw table to a filtered one.
--
-- Filters applied, and why each one is here:
--
--   1. Completeness on the four analysis variables (ahe, bachelor,
--      female, age). CPS2015.dta currently has zero missing values in
--      these columns, so today this filter removes 0 rows. It mirrors
--      the `drop if missing(...)` guard in the project's do-files and
--      exists so the pipeline fails safe (drops the row, not the run)
--      if a future refresh of the raw extract does have missingness.
--
--   2. Age between 25 and 34, inclusive. The repo README states this
--      extract is restricted to workers age 25-34. We re-assert that
--      bound explicitly here rather than trusting it silently, so the
--      population definition is auditable in code and will visibly
--      remove rows if a future raw file violates it. (Today: removes 0
--      rows -- see the reconciliation report.)
--
--   3. ahe > 0. Step 02 takes log(ahe); log() of a non-positive number
--      is undefined. Today's data has ahe ranging from ~2.04 to ~105.77,
--      so this also removes 0 rows currently.
--
-- Note what this script deliberately does NOT do: it does not attempt to
-- verify "full-time, full-year worker" (a filter the README also
-- claims), because the hours-worked / weeks-worked fields that would let
-- us check that are not present in this 5-column extract. That
-- population restriction was applied upstream of this repository and
-- cannot be independently verified here -- flagged, not silently
-- assumed away.

DROP TABLE IF EXISTS cps_2015_filtered;

CREATE TABLE cps_2015_filtered AS
SELECT
    row_id,
    year,
    ahe,
    bachelor,
    female,
    age
FROM cps_2015_raw
WHERE ahe      IS NOT NULL
  AND bachelor IS NOT NULL
  AND female   IS NOT NULL
  AND age      IS NOT NULL
  AND ahe > 0
  AND age BETWEEN 25 AND 34;
