-- 01_schema.sql
-- Defines the raw table(s) loaded directly from source files. One raw
-- table per source file, no transformation. There is exactly one source
-- file in this project (data/raw/CPS2015.dta), so there is exactly one
-- raw table.

DROP TABLE IF EXISTS cps_2015_raw;

CREATE TABLE cps_2015_raw (
    -- CPS2015.dta ships with no person or household identifier -- it is a
    -- flat, already-de-identified extract (5 variables, no ID column).
    -- row_id is a surrogate key equal to 1-based row order in the source
    -- .dta file. It is NOT a CPS person ID and does not assert that two
    -- rows with the same row_id represent anything in particular -- it
    -- exists only so this table has a primary key and later pipeline
    -- steps have a stable handle to carry a row through. See
    -- sql/validation/02_duplicate_check.sql for what "duplicate" can and
    -- can't mean without a real key.
    row_id      INTEGER PRIMARY KEY,

    -- Survey year. Constant at 2015 in this extract; kept as a column
    -- because the source file has it and a future refresh may not be
    -- single-year.
    year        INTEGER NOT NULL,

    -- Average hourly earnings, in dollars. Source variable: ahe.
    ahe         REAL    NOT NULL,

    -- 1 = bachelor's degree, 0 = high school diploma only (per the source
    -- file's variable label). Source variable: bachelor.
    bachelor    INTEGER NOT NULL CHECK (bachelor IN (0, 1)),

    -- 1 = female, 0 = male. Source variable: female.
    female      INTEGER NOT NULL CHECK (female IN (0, 1)),

    -- Age in years. Source file is pre-filtered to full-time, full-year
    -- workers age 25-34 (per the repo README); we do not re-derive that
    -- filter here because the underlying hours/weeks-worked fields that
    -- would let us verify "full-time full-year" are not present in this
    -- extract -- only age is directly checkable, and that check lives in
    -- sql/pipeline/01_filter_valid_rows.sql.
    age         INTEGER NOT NULL
);
