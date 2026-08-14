#!/usr/bin/env bash
# run_all.sh - single reproducible entrypoint for the whole SQL data prep
# layer: build the database from the raw .dta, run the filter/recode
# pipeline, run validation, run the reconciliation check.
#
# Usage: ./scripts/run_all.sh   (from the repo root, or anywhere)
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/build_db.py
python3 scripts/run_pipeline.py
python3 scripts/run_validation.py
python3 scripts/reconcile.py
python3 scripts/export_for_stata.py
