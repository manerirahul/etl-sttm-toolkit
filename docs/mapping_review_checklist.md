# STTM Review Checklist

Used in mapping walk-throughs before ETL build sign-off.

## Completeness
- [ ] Every target column has exactly one mapping row (or a stated merge rule)
- [ ] Every source column in the extract is mapped or explicitly dropped
- [ ] Keys are identified, with duplicate-handling stated
- [ ] Reference/lookup tables named, with their owner and refresh cadence

## Rules quality
- [ ] Each transformation rule is executable as written (no "clean the data")
- [ ] Null handling stated per column: reject, default, or set null
- [ ] Defaults are business-approved values, not developer conveniences
- [ ] Type conversions state format/pattern (dates, amounts, codes)

## Business meaning
- [ ] Every column has a one-sentence business definition
- [ ] Definitions reviewed by the business owner, not only the ETL team
- [ ] Regulatory/PII columns flagged with their handling rule

## Sign-off
- [ ] Validator run is clean at ERROR level
- [ ] Open items logged with owners and dates
- [ ] Business and ETL leads have signed the mapping version being built
