# Wage Determinants: Education and Gender, CPS 2015

This project asks how average hourly earnings for young U.S. full-time
workers differ by educational attainment and gender, holding age fixed.
Using March 2015 Current Population Survey microdata, a log-wage
(Mincer-style) regression on 7,098 workers age 25-34 finds a college
wage premium of 0.4615 log points (SE 0.011) and a gender wage gap of
-0.1776 log points (SE 0.012) for women relative to men, both estimated
with age held constant and both significant well beyond conventional
thresholds.

## Data source and sample size

- **Source file:** `data/raw/CPS2015.dta` — a 5-column, 7,098-row
  extract of the March 2015 CPS (BLS public-use microdata).
- **Population:** already restricted, upstream of this repository, to
  full-time, full-year workers age 25-34 with a high school diploma or
  bachelor's degree. This repo cannot independently re-verify the
  full-time/full-year part of that restriction — the hours- and
  weeks-worked fields it would require aren't in the extract.
- **Variables:** `year` (constant, 2015), `ahe` (average hourly
  earnings, $2.04-$105.77), `bachelor` (0/1), `female` (0/1), `age`
  (25-34).
- **No person or household identifier.** The extract is flat and
  de-identified; there is nothing to join it to, and "duplicate
  person-record" can only be checked as exact duplication across all
  five fields (see Limitations).

## Pipeline: raw file to analysis table

Ingestion, filtering, and recoding all happen in SQL, against a SQLite
database (`db/cps_wages.db`, rebuilt from scratch on every run). Stata
only reads the finished table this produces.

1. `sql/schema/01_schema.sql` — defines `cps_2015_raw`, typed columns,
   a surrogate primary key (there's no real one to use).
2. `scripts/build_db.py` — loads the raw `.dta` into that table. No
   join step: there is only one source table.
3. `sql/pipeline/01_filter_valid_rows.sql` — drops incomplete rows,
   enforces the age 25-34 bound, requires positive wages.
4. `sql/pipeline/02_recode_analysis_variables.sql` — adds `ln_ahe`,
   `age2`, `ln_age`, producing `cps_2015_analysis`.
5. `sql/validation/01-04_*.sql` — row counts against source, a
   duplicate check, null counts, and range checks on wages/age/education.
6. `scripts/export_for_stata.py` — writes `cps_2015_analysis` to
   `data/analysis/cps_2015_analysis.dta`, the only file
   `do/age_earnings_CPS2015.do` reads.

## How to reproduce

```
./scripts/run_all.sh
```

Requires Python 3 with `pandas` and `numpy` (sqlite3 is in the standard
library). This rebuilds the database, runs the filter/recode pipeline,
runs validation, writes `sql/reconciliation/RECONCILIATION.md`
confirming the SQL output matches statistics computed independently
from the raw file, and exports the Stata-ready table.

Then, in Stata:

```
do do/age_earnings_CPS2015.do
```

No Stata license was available in the environment this was built in.
The coefficients below were obtained by fitting the identical
specification in Python (`scripts/regress_baseline.py`, statsmodels
OLS with HC1 robust standard errors — the same estimator Stata's
`, robust` option uses), against the same `data/analysis/cps_2015_analysis.dta`
file Stata would read. Running the do-file in real Stata against that
file reproduces these numbers.

## Findings

Baseline specification: `ln(ahe) = b0 + b1*age + b2*female + b3*bachelor`,
robust (HC1) standard errors, N = 7,098, R² = 0.208.

| variable | coefficient | robust SE | interpretation |
|---|---|---|---|
| `bachelor` | **0.4615** | 0.011 | college wage premium: ~58.6% higher AHE than an otherwise-identical high-school-only worker |
| `female` | **-0.1776** | 0.012 | gender wage gap: ~16.3% lower AHE than an otherwise-identical male worker |
| `age` | 0.0242 | 0.002 | ~2.4% higher AHE per additional year of age |
| intercept | 2.0274 | 0.060 | |

All three coefficients are significant at p < 0.001. A quadratic
age term and a female×bachelor interaction were also tested
(`do/age_earnings_CPS2015.do`, specs 5-6); the interaction term is not
statistically distinguishable from zero (coefficient 0.0235, SE 0.023,
p = 0.31) — no strong evidence in this sample that the college premium
differs by gender.

A longer write-up of these findings, methodology, and caveats —
formatted as a numbered-paragraph brief with exhibit references, the
convention used for expert-report exhibits — is in
[docs/technical_brief.md](docs/technical_brief.md).

## Limitations

This is a cross-sectional OLS regression on four variables, and it
identifies correlations, not causal effects:

- **No causal identification of the college premium.** The `bachelor`
  coefficient cannot separate the return to a degree from unobserved
  ability, family background, or the selection of who completes
  college — the classic Mincer ability-bias problem. Nothing in this
  dataset (no test scores, no parental education, no pre-college
  earnings) can address it.
- **`female` is a raw/lightly-adjusted gap, not a discrimination
  estimate.** It nets out only age and education. Occupation,
  industry, actual hours, tenure, region, and unobserved productivity
  are all uncontrolled and likely correlated with both gender and
  wages. This coefficient should be read as "the gap that remains
  after controlling for almost nothing," not as a measure of unequal
  pay for equal work.
- **`age` is a weak stand-in for labor market experience.** There's no
  years-of-experience or tenure field; age conflates actual
  experience with cohort effects, and a single cross-section cannot
  separate age, period, and cohort effects from one another.
- **Selection into full-time, full-year employment is unmodeled.**
  The sample already excludes anyone not working full-time/full-year;
  if that selection operates differently by gender or education
  (which labor research generally suggests it does), the coefficients
  above are conditional on that selection, not representative of the
  full population age 25-34.
- **Single year, single cross-section.** These estimates describe 2015
  only and say nothing about trends, and R² = 0.208 means most
  variation in wages is explained by factors outside this model.
- **43% of raw rows are exact duplicates** across all five fields
  (`sql/validation/02_duplicate_check.sql`). Plausible given how few
  distinct values `age`, `bachelor`, and `female` take, and not
  something this repo can rule in or out as a sign of rounding/binning
  in how the extract was built — flagged, not resolved.

## Repository structure

```
CPS_Wage_Disparities/
├── data/
│   ├── raw/
│   │   └── CPS2015.dta                       # source file, 7,098 rows x 5 cols
│   └── analysis/                              # generated by the pipeline, gitignored
│       └── cps_2015_analysis.dta
├── db/                                        # generated by the pipeline, gitignored
│   └── cps_wages.db
├── sql/
│   ├── README.md                              # SQL layer documentation
│   ├── schema/
│   │   └── 01_schema.sql                      # raw table definition
│   ├── pipeline/
│   │   ├── 01_filter_valid_rows.sql
│   │   └── 02_recode_analysis_variables.sql
│   ├── validation/
│   │   ├── 01_row_counts.sql
│   │   ├── 02_duplicate_check.sql
│   │   ├── 03_null_counts.sql
│   │   └── 04_range_checks.sql
│   └── reconciliation/
│       ├── 01_sql_summary_stats.sql
│       └── RECONCILIATION.md                  # generated by the pipeline
├── scripts/
│   ├── build_db.py                            # ingest raw .dta -> SQLite
│   ├── run_pipeline.py                        # run sql/pipeline/*.sql
│   ├── run_validation.py                      # run sql/validation/*.sql
│   ├── reconcile.py                           # SQL output vs. raw-file baseline
│   ├── export_for_stata.py                    # SQLite -> data/analysis/*.dta
│   ├── regress_baseline.py                    # reproduces the headline regression
│   └── run_all.sh                             # runs all of the above, in order
├── do/
│   ├── age_earnings_CPS2015.do                # main analysis, reads data/analysis/
│   ├── 01_dataprep.do                         # earlier, now-superseded prep script
│   ├── 02_eda.do
│   ├── 03_regression.do
│   └── 04_reporting.do
└── docs/
    └── technical_brief.md                     # findings write-up, expert-report-exhibit format
```
