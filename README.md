# Dataframe Quality Checker

A Python/pandas validation library and CLI for schema drift, missingness, uniqueness, ranges, categories, regex patterns and statistical outliers. Repository: dataframe-quality-checker.

**History disclosure:** this is an AI-assisted educational project with a reconstructed development history assigned to February 7–24, 2025. Historical Git metadata does not establish when the code was actually written. Review, understand and test it before presenting it as your own work.

## Ubuntu setup

Python 3.10+ is required. Runtime dependencies: pandas >=2.2,<3 and NumPy >=1.26,<3.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e . -r requirements-dev.txt
python -m pytest -q
python -m dataframe_quality_checker examples/clean.csv --schema examples/schema.json
```

If venv support is missing, install python3-venv on Ubuntu. Internet is required for initial dependency installation; no network is used by validation.

## CLI

```bash
mkdir -p reports
python -m dataframe_quality_checker examples/dirty.csv --schema examples/schema.json --output reports/dirty.json
python -m dataframe_quality_checker examples/clean.csv --schema examples/schema.json --format csv --output reports/clean.csv
python -m dataframe_quality_checker examples/dirty.csv --schema examples/schema.json --fail-on-warning
```

The installed command is df-quality. Exit 0: no failing error checks (and no warnings if requested). Exit 1: data-quality failure, expected for dirty.csv. Exit 2: configuration, input or execution failure. JSON report passed depends on error checks; --fail-on-warning affects the process exit status only. Diagnostics go to stderr; report data goes to stdout unless --output is set. --max-rows defaults to 1,000,000 and rejects larger inputs. --verbose enables debug logging; --version prints the version.

The clean fixture has six rows and passes. The dirty fixture contains a duplicate customer ID, a missing age, an out-of-range age, invalid email/country and one extreme spend. Raw cell values are not included in reports; bounded row positions help locate problems. Reports and local environments are ignored by Git.

## Library API

```python
import pandas as pd
from dataframe_quality_checker import Schema, validate
from dataframe_quality_checker.profile import profile

frame = pd.DataFrame({"age": [21, 35, 150, None]})
schema = Schema.from_dict({
    "version": 1,
    "columns": {"age": {"type": "integer", "nullable": False, "min": 0, "max": 120}}
})
result = validate(frame, schema)
print(result["passed"])
print(profile(frame))
```

Use Schema.from_dict or Schema.load to validate configuration. Input frames must have unique nonempty string column names and scalar cells. The library never mutates the frame. All checks are deterministic. Rules/thresholds and zero-IQR behavior are documented in docs/rules.md.

## Schema

The JSON schema root requires version 1 and nonempty columns. Optional allow_extra defaults false; min_rows defaults 1; unique_rows defaults false; sample_limit defaults 5 (0–100). Each column requires type: integer, number, string, boolean or datetime. Optional required defaults true; nullable defaults true. Other rules: max_missing (fraction 0–1), unique, inclusive min/max, allowed scalar values, regex (full match), outlier (method iqr or zscore, positive threshold, min_samples >=2).

Unknown keys, duplicate JSON keys and invalid combinations are rejected. See examples/schema.json for a complete working schema. An optional absent column is skipped. Outlier checks warn rather than fail by default, and fewer than min_samples finite observations cause a documented skip.

## CSV interpretation and limits

The CLI uses pandas CSV type inference/default NA markers; numeric-looking strings can be inferred as numbers. For exact dtypes, leading-zero IDs or literal NA strings, load the DataFrame yourself with explicit pandas options and call validate. There is no automatic cleaning/coercion. Empty or duplicate headers are rejected before pandas can rename them. max_rows bounds rows read, not bytes per field or total memory: this is an in-memory learning library, not a streaming validator. Nested values are unsupported. Use trusted schemas; pathological regexes can be slow.

Numeric outliers are calculated from the current batch, not a fitted baseline. Schema drift here means missing/unexpected columns or incompatible semantic values, not distribution-shift monitoring. Reports materialize check results and bounded row examples. A row can fail multiple rules, so failed_count totals are not a count of distinct invalid rows.

## Synthetic data and performance

```bash
python scripts/generate_data.py --rows 1000 --seed 42 > reports/synthetic.csv
python scripts/generate_data.py --rows 1000 --seed 42 --dirty > reports/synthetic-dirty.csv
python -m dataframe_quality_checker reports/synthetic.csv --schema examples/schema.json
python scripts/benchmark.py --rows 10000
```

Benchmark time and peak allocations depend on your environment. There are no claimed hardware-independent throughput numbers.

## Docker

```bash
docker build -t dataframe-quality-checker:local .
docker run --rm -v "$PWD/examples:/data:ro" dataframe-quality-checker:local /data/clean.csv --schema /data/schema.json
```

The image runs as UID 10001. Mounted inputs must be readable. Redirect stdout on the host to save reports, or use a writable output mount. CI is configured for Python 3.10–3.12 and includes a Docker build; remote execution depends on GitHub Actions.

## Push to GitHub

After generating the repository from project-03.json using the continuation kit, create an empty GitHub repository named dataframe-quality-checker, without README/license initialization. From the generated repository:

```bash
git remote add origin https://github.com/hasanahmeds/dataframe-quality-checker.git
git push -u origin main
```

Do not force-push over existing work. The manifest and engine are external orchestration files, not application dependencies.
