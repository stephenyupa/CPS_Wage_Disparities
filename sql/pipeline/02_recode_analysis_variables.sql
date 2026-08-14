-- 02_recode_analysis_variables.sql
-- Purpose: add the derived variables used by the regression specs in
-- do/age_earnings_CPS2015.do, so Stata can `use` this table directly and
-- run its `regress` commands with no further data work.
--
-- Recodes:
--   ln_ahe = log(ahe)   -- outcome variable in every model in that do-file
--   age2   = age^2      -- quadratic age term (spec: ols_quad_inter)
--   ln_age = log(age)   -- log-log spec (spec: ols_loglog)
--
-- bachelor and female are already clean 0/1 indicators in the source
-- file, so Stata's `i.bachelor`, `i.female`, and `i.female#i.bachelor`
-- factor-variable notation can consume them as-is -- no manual dummy or
-- interaction column is materialized here, since none is needed by the
-- do-file this table feeds.

DROP TABLE IF EXISTS cps_2015_analysis;

CREATE TABLE cps_2015_analysis AS
SELECT
    row_id,
    year,
    age,
    age * age AS age2,
    LN(age)   AS ln_age,
    bachelor,
    female,
    ahe,
    LN(ahe)   AS ln_ahe
FROM cps_2015_filtered;
