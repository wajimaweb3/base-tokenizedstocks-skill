#!/usr/bin/env python3
"""Render the delta table for a dated eval archive from a completed grading worksheet.

Usage:
  python3 report.py -w work/worksheet.json -e evals/evals.json         # print the markdown table
  python3 report.py -w work/worksheet.json -e evals/evals.json -o out.md  # write to a file

The table has one row per case and a totals row, in the archived-delta shape:

| Q | Assertions | With skill | Baseline | Baseline's failure |

A verdict is 'pass' / 'fail' per assertion. `with` is a fraction of assertions passed in the
WITH-skill run, `baseline` in the WITHOUT run. The table renders what a grading agent or human
marked; the surrounding narrative (verdict paragraph, fairness caveats, post-run verification
note) is prose the maintainer writes by hand into the dated sample-output archive.
"""

import argparse
import json
import sys
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Render the paired-run delta table into markdown.")
    p.add_argument("-w", "--worksheet", required=True, help="path to a completed worksheet.json")
    p.add_argument("-e", "--evals", required=True, help="path to the evals.json the case text lives in")
    p.add_argument("-o", "--out", default=None, help="optional output file; defaults to stdout")
    return p.parse_args()


def count(verdicts):
    if not verdicts:
        return None
    return sum(1 for v in verdicts if v == "pass")


def render(worksheet):
    lines = []
    lines.append("| Q | Assertions | With skill | Baseline | Baseline's failure |")
    lines.append("|---|---|---|---|---|")
    t_with = t_base = t_total = 0
    for c in worksheet["cases"]:
        n = len(c["assertions"])
        w = count(c["with"]["verdicts"])
        b = count(c["baseline"]["verdicts"])
        t_total += n
        t_with += w or 0
        t_base += b or 0
        w_str = str(w) if w is not None else "—"
        b_str = str(b) if b is not None else "—"
        failure = c.get("baseline_failure", "").strip()
        lines.append(f"| {c['id']} | {n} | {w_str} | {b_str} | {failure} |")
    lines.append(f"| **Total** | **{t_total}** | **{t_with}** | **{t_base}** | |")
    return "\n".join(lines) + "\n"


def main():
    args = parse_args()
    if not Path(args.worksheet).exists():
        print(f"error: worksheet {args.worksheet} not found", file=sys.stderr)
        sys.exit(1)
    with open(args.worksheet) as f:
        worksheet = json.load(f)

    # Coerce empty verdict lists into explicit pass/fail lists so the table is honest about
    # what was and wasn't graded. An ungraded case renders as "—".
    rendered = render(worksheet)
    if args.out:
        Path(args.out).write_text(rendered)
        print(f"wrote delta table to {args.out}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()