"""Validate a source-to-target mapping (STTM) CSV.

Usage: python src/validate_sttm.py <mapping.csv>
Exit code 1 when ERROR findings exist (usable as a sign-off gate).
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict

IMPLICIT_OK = {
    ("INT", "INT"), ("INT", "DECIMAL"), ("INT", "VARCHAR"),
    ("VARCHAR", "VARCHAR"), ("DECIMAL", "DECIMAL"), ("DECIMAL", "VARCHAR"),
    ("DATE", "DATE"), ("TIMESTAMP", "TIMESTAMP"), ("TIMESTAMP", "DATE"),
    ("TIMESTAMP", "VARCHAR"), ("DATE", "VARCHAR"),
}


def base_type(t: str) -> str:
    return (t or "").split("(")[0].strip().upper()


def validate(rows: list[dict]) -> list[tuple[str, str, str]]:
    """Return findings as (severity, code, message)."""
    findings: list[tuple[str, str, str]] = []
    targets: dict[str, list[int]] = defaultdict(list)

    for i, row in enumerate(rows, start=2):
        tgt_table = (row.get("target_table") or "").strip()
        tgt_col = (row.get("target_column") or "").strip()
        rule = (row.get("transformation_rule") or "").strip()
        definition = (row.get("business_definition") or "").strip()
        src_type = base_type(row.get("source_type", ""))
        tgt_type = base_type(row.get("target_type", ""))

        if tgt_table and tgt_col:
            targets[f"{tgt_table}.{tgt_col}"].append(i)
            if not rule:
                findings.append(("ERROR", "MISSING_RULE",
                                 f"row {i}: {tgt_table}.{tgt_col} has no transformation rule"))
            if not definition:
                findings.append(("ERROR", "MISSING_DEFINITION",
                                 f"row {i}: {tgt_table}.{tgt_col} has no business definition"))
            if src_type and tgt_type and (src_type, tgt_type) not in IMPLICIT_OK:
                findings.append(("ERROR", "TYPE_MISMATCH",
                                 f"row {i}: {src_type} -> {tgt_type} for "
                                 f"{tgt_table}.{tgt_col} needs an explicit conversion rule"))
        else:
            src = f"{row.get('source_table', '')}.{row.get('source_column', '')}"
            findings.append(("WARN", "UNMAPPED_SOURCE",
                             f"row {i}: source {src} maps to no target "
                             "(confirm it is intentionally dropped)"))

    for target, lines in targets.items():
        if len(lines) > 1:
            findings.append(("ERROR", "DUPLICATE_TARGET",
                             f"{target} is mapped from rows {lines} with no "
                             "single stated merge rule"))
    return findings


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    with open(sys.argv[1], newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    findings = validate(rows)
    errors = [f for f in findings if f[0] == "ERROR"]
    for severity, code, msg in findings:
        print(f"[{severity}] {code}: {msg}")
    print(f"\n{len(rows)} mapping rows checked: "
          f"{len(errors)} errors, {len(findings) - len(errors)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
