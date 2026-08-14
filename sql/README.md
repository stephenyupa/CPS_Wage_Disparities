# SQL data preparation layer

Ingestion, filtering, and recoding for the CPS 2015 wage data now happen
here, in SQL, against a SQLite database. Stata (`do/age_earnings_CPS2015.do`)
only reads the finished table this produces.

## Why there's no "join" script

The source data is a single file, `data/raw/CPS2015.dta` (5 columns:
`year`, `ahe`, `bachelor`, `female`, `age`), with no person or household
ID. There is nothing to join it to. The pipeline goes raw table -> filter
-> recode, with no join step. See `sql/schema/01_schema.sql` for the full
explanation of why there's no real key, and what `row_id` is instead
(a surrogate, load-order key, not a person identifier).

## Run it

```
./scripts/run_all.sh
```

This rebuilds `db/cps_wages.db` from scratch, runs the pipeline, runs
validation, and writes `sql/reconciliation/RECONCILIATION.md`. It's the
only command you need; nothing is loaded by hand.

Individual steps, if you want to run or read them one at a time:

| step | file(s) | what it does |
|---|---|---|
| 1 | `scripts/build_db.py` | Reads the raw `.dta`, creates `db/cps_wages.db` from `sql/schema/01_schema.sql`, loads `cps_2015_raw`. |
| 2 | `sql/pipeline/01_filter_valid_rows.sql` | Drops incomplete rows, enforces the age 25-34 population bound, requires positive wages. Produces `cps_2015_filtered`. |
| 3 | `sql/pipeline/02_recode_analysis_variables.sql` | Adds `ln_ahe`, `age2`, `ln_age`. Produces `cps_2015_analysis` -- the table Stata should `use`. |
| 4 | `sql/validation/01-04_*.sql` | Row counts vs. source, duplicate-record check, null counts, out-of-range flags. Run via `scripts/run_validation.py`. |
| 5 | `sql/reconciliation/01_sql_summary_stats.sql` | Key summary stats from the SQL table, compared against the same stats computed independently from the raw `.dta` in `scripts/reconcile.py`. |

## Known limitations (read before trusting the validation output)

- **Duplicate check is not a real person-level check.** No ID column
  exists in the source file, so `sql/validation/02_duplicate_check.sql`
  can only flag exact duplication across all five observable fields. On
  the current data that's 3,029 of 7,098 rows -- expected given how few
  distinct values `age`, `bachelor`, and `female` take, not evidence of
  a data bug.
- **The "full-time, full-year worker" population filter mentioned in the
  main README cannot be independently re-verified here.** This extract
  doesn't carry the hours/weeks-worked fields that filter would need;
  only the age bound is checkable in SQL, and it is checked.
- **Every filter in `01_filter_valid_rows.sql` currently removes 0
  rows.** The raw file is already clean and already within the age
  bound. The filters are there to make the population definition
  explicit and enforced, not because they currently do any filtering --
  see `sql/reconciliation/RECONCILIATION.md` for the row counts that
  confirm this.
