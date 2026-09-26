#!/usr/bin/env python3
"""Expand an eval suite into a runnable task pack and a blank grading worksheet.

Usage:
  python3 prepare.py -e evals/evals.json -o work/          # expand into ./work
  python3 prepare.py -e evals/evals.json -o /tmp/ws -n     # dry-run: print layout only

For each case, writes three artifacts under the workdir:
  out/<id>-<name>.with.md      the prompt as a WITH-skill run (load the grounding files first)
  out/<id>-<name>.without.md   the prompt as a WITHOUT-skill baseline run (no skill context)
  worksheet.json               a blank grid a grader fills in: per-case, per-run assertion verdicts

Grading stays human/agent judgment: a person (or a grading agent) runs each prompt twice and
marks each assertion pass/fail for each run. report.py then turns a completed worksheet into the
delta table that gets archived as a dated sample output.
"""

import argparse
import json
import os
import sys
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Expand an evals.json suite into a task pack + grading worksheet.")
    p.add_argument("-e", "--evals", required=True, help="path to evals.json")
    p.add_argument("-o", "--out", default="./work", help="output workdir (created if missing)")
    p.add_argument("-n", "--dry-run", action="store_true", help="print the layout without writing files")
    return p.parse_args()


def with_prompt(case):
    files = ", ".join(case.get("files", []))
    return (
        f"# Task — {case['name']}\n"
        f"(id {case['id']} — WITH-skill run)\n\n"
        f"Ground on these files first, then answer the prompt below:\n{files}\n\n"
        f"Run rules: follow the skill's operating rules (date every number, pull live state before "
        f"any numeric claim, show the address, stay read-only). Every figure must carry its own as-of "
        f"stamp; a number without a date is folklore.\n\n---\n\n{case['prompt']}\n"
    )


def without_prompt(case):
    return (
        f"# Task — {case['name']}\n"
        f"(id {case['id']} — WITHOUT-skill baseline run)\n\n"
        f"No special skill context is loaded. Answer the prompt as a general agent would.\n\n---\n\n{case['prompt']}\n"
    )


def blank_worksheet(evals):
    return {
        "skill_name": evals.get("skill_name", ""),
        "date": "",
        "run_notes": "",
        "cases": [
            {
                "id": c["id"],
                "name": c["name"],
                "assertions": list(c.get("assertions", [])),
                "with": {"verdicts": [], "notes": ""},
                "baseline": {"verdicts": [], "notes": ""},
                "baseline_failure": "",
            }
            for c in evals.get("evals", [])
        ],
    }


def main():
    args = parse_args()
    with open(args.evals) as f:
        evals = json.load(f)

    out = Path(args.out)
    task_dir = out / "out"
    files_written = [task_dir / f"{c['id']:02d}-{c['name']}.with.md" for c in evals.get("evals", [])]
    files_written += [task_dir / f"{c['id']:02d}-{c['name']}.without.md" for c in evals.get("evals", [])]
    worksheet_path = out / "worksheet.json"

    if args.dry_run:
        print(f"would create {len(files_written)} task files under {task_dir}/")
        print(f"would write blank grading worksheet to {worksheet_path}")
        for c in evals.get("evals", []):
            print(f"  {c['id']:02d}-{c['name']}  ({len(c.get('assertions', []))} assertions)")
        sys.exit(0)

    task_dir.mkdir(parents=True, exist_ok=True)
    for c in evals.get("evals", []):
        (task_dir / f"{c['id']:02d}-{c['name']}.with.md").write_text(with_prompt(c))
        (task_dir / f"{c['id']:02d}-{c['name']}.without.md").write_text(without_prompt(c))

    worksheet_path.write_text(json.dumps(blank_worksheet(evals), indent=2))
    print(f"wrote {len(files_written)} task files to {task_dir}/ and blank worksheet to {worksheet_path}")


if __name__ == "__main__":
    main()