# ETL STTM Toolkit

Source-to-Target Mapping (STTM) templates and a validator for the mapping
reviews I run as a data / business analyst on ETL projects (Informatica
PowerCenter / IICS / IDMC, AWS Glue). A good STTM is the contract between
the business rules and the ETL build — this toolkit keeps that contract
complete, consistent, and reviewable.

## What's here

| File | Purpose |
|---|---|
| `templates/sttm_template.csv` | The blank mapping template: source system/table/column, target table/column, data types, transformation rule, null handling, default, business definition, owner, sign-off |
| `examples/customer_dim_sttm.csv` | A completed example — customer dimension load from an operational source |
| `examples/flawed_sttm.csv` | The same mapping with planted defects, so the validator has findings to report |
| `src/validate_sttm.py` | Validator: duplicate targets, unmapped sources, missing transformation rules, type mismatches, missing business definitions |
| `docs/mapping_review_checklist.md` | The review checklist used in mapping walk-throughs with business and ETL teams |

## Run the validator

```bash
python src/validate_sttm.py examples/customer_dim_sttm.csv   # clean: 0 errors
python src/validate_sttm.py examples/flawed_sttm.csv        # finds the planted defects
```

Exit code is 1 when ERROR-level findings exist, so it can gate a
mapping sign-off in a build pipeline.

## The checks

- **DUPLICATE_TARGET** — two sources mapping to the same target column
  without a stated merge rule
- **MISSING_RULE** — target column with no transformation rule
- **TYPE_MISMATCH** — source and target types that cannot convert
  implicitly (e.g. VARCHAR → DATE with no format stated)
- **MISSING_DEFINITION** — no business definition; the column will be
  built to a guess
- **UNMAPPED_SOURCE** (warning) — source column carried in the extract
  but mapped nowhere; confirm it is intentionally dropped

## License

MIT
