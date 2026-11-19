#!/usr/bin/env python3
"""Review and check the item entries exported by the GM spawn menu."""

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys


def key(row):
    return row["id"], row["variant"], row["name"]


def read_decisions(path):
    with path.open(encoding="utf-8-sig", newline="") as file:
        rows = csv.DictReader(file)
        columns = {"id", "variant", "name", "decision"}
        if not columns <= set(rows.fieldnames or []):
            raise ValueError("Review requires id, variant, name and decision")
        decisions = {"keep": Counter(), "remove": Counter()}
        for row in rows:
            decision = (row["decision"] or "").strip()
            if not row["id"] or row["variant"] is None or row["name"] is None:
                raise ValueError(f"Incomplete review at line {rows.line_num}")
            if decision not in ("", "keep", "remove"):
                raise ValueError(f"Unknown decision at line {rows.line_num}")
            if decision:
                decisions[decision][key(row)] += 1
    return decisions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path, help="Engine export as JSON.")
    parser.add_argument("--review", type=Path, help="Review decisions as CSV.")
    args = parser.parse_args(argv)

    try:
        rows = json.loads(args.catalog.read_text(encoding="utf-8"))
        if not isinstance(rows, list) or not rows:
            raise ValueError("Expected a nonempty engine catalog")
        if not args.review:
            output = csv.DictWriter(
                sys.stdout,
                fieldnames=("id", "variant", "name", "decision", "reason"),
                lineterminator="\n",
            )
            output.writeheader()
            output.writerows(rows)
            return 0

        decisions = read_decisions(args.review)
        present_removed = []
        present_unreviewed = []
        kept = decisions["keep"]
        removed = decisions["remove"]
        for row in sorted(rows, key=key):
            item = key(row)
            if kept[item]:
                kept[item] -= 1
            elif removed[item]:
                removed[item] -= 1
                present_removed.append(row)
            else:
                present_unreviewed.append(row)
        missing_kept = [
            {"id": item_id, "variant": variant, "name": name}
            for item_id, variant, name in sorted(kept.elements())
        ]
        report = {
            "entries": len(rows),
            "present_removed": present_removed,
            "present_unreviewed": present_unreviewed,
            "missing_kept": missing_kept,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return int(bool(present_removed or present_unreviewed or missing_kept))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
