#!/usr/bin/env python3
"""Validate an eval suite against the harness schema and the protocol's structural rules.

Usage:
  python3 validate.py -e evals/evals.json            # default repo root = walk up to the SKILL.md dir
  python3 validate.py -e evals/evals.json -r .       # explicit repo root for the `files` check
  python3 validate.py -e harness/examples/toy-evals.json -r .

Exits 0 if the suite is valid, 1 otherwise. Prints a summary of what was checked
and every failure found. stdlib only — no dependencies.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="Validate an evals.json suite for a domain skill.")
    p.add_argument("-e", "--evals", required=True, help="path to evals.json")
    p.add_argument(
        "-r",
        "--repo",
        default=None,
        help="repo root against which the cases' `files` entries are resolved. "
        "Defaults to the parent of the evals directory.",
    )
    return p.parse_args()


def default_repo_root(evals_path):
    """Walk up from the evals file to the directory that holds the skill (SKILL.md).
    Falls back to the evals dir's parent — the old default — if no SKILL.md is found,
    so suites that live next to their skill files still resolve without -r.
    """
    start = os.path.abspath(evals_path)
    for d in [os.path.dirname(start)] + list(_upwards(start)):
        if os.path.exists(os.path.join(d, "SKILL.md")):
            return d
    return os.path.dirname(os.path.abspath(evals_path))


def _upwards(non_dir):
    # generator of ancestor directories above the (non-directory) evals path
    parent = os.path.dirname(non_dir)
    while True:
        yield parent
        above = os.path.dirname(parent)
        if above == parent:
            break
        parent = above


REQUIRED_CASE_FIELDS = ["id", "name", "prompt", "expected_output", "assertions", "files"]
NAME_RE = re.compile(r"^[a-z0-9-]+$")


def validate_suite(data, repo_root, errors):
    if not isinstance(data, dict):
        errors.append("top level is not an object")
        return
    if "skill_name" not in data:
        errors.append('missing required top-level field "skill_name"')
    if "evals" not in data:
        errors.append('missing required top-level field "evals"')
        return
    evals = data["evals"]
    if not isinstance(evals, list) or len(evals) == 0:
        errors.append('"evals" must be a non-empty array')
        return

    seen_ids = set()
    for i, case in enumerate(evals):
        loc = f"case[{i}]"
        if not isinstance(case, dict):
            errors.append(f"{loc}: not an object")
            continue
        for field in REQUIRED_CASE_FIELDS:
            if field not in case:
                errors.append(f"{loc}: missing required field '{field}'")
        if "id" in case:
            cid = case["id"]
            if not isinstance(cid, int) or isinstance(cid, bool) or cid < 0:
                errors.append(f"{loc}: 'id' must be a non-negative integer")
            else:
                if cid in seen_ids:
                    errors.append(f"duplicate case id: {cid}")
                seen_ids.add(cid)
        if "name" in case and (not isinstance(case["name"], str) or not NAME_RE.match(case["name"])):
            errors.append(f"{loc}: 'name' must be a lowercase kebab-case slug (got {case.get('name')!r})")
        for text_field in ("prompt", "expected_output"):
            if text_field in case and (not isinstance(case[text_field], str) or not case[text_field].strip()):
                errors.append(f"{loc}: '{text_field}' must be a non-empty string")
        if "assertions" in case:
            if not isinstance(case["assertions"], list) or len(case["assertions"]) == 0:
                errors.append(f"{loc}: 'assertions' must be a non-empty array")
            else:
                for j, a in enumerate(case["assertions"]):
                    if not isinstance(a, str) or not a.strip():
                        errors.append(f"{loc}.assertions[{j}]: each assertion must be a non-empty string")
        if "files" in case:
            if not isinstance(case["files"], list) or len(case["files"]) == 0:
                errors.append(f"{loc}: 'files' must be a non-empty array")
            else:
                for j, f in enumerate(case["files"]):
                    if not isinstance(f, str) or not f.strip():
                        errors.append(f"{loc}.files[{j}]: each file entry must be a non-empty string")
                        continue
                    if repo_root:
                        full = os.path.join(repo_root, f)
                        if not os.path.exists(full):
                            errors.append(f"{loc}.files[{j}]: referenced file does not exist under repo root: {f}")
        if "should_trigger" in case and not isinstance(case["should_trigger"], bool):
            errors.append(f"{loc}: 'should_trigger' must be a boolean")

    # Sequence check: ids should be unique and (per protocol) gate new capabilities as they land.
    if seen_ids:
        expected = set(range(len(evals))) if max(seen_ids) == len(evals) - 1 else None
        if expected is not None and seen_ids != expected:
            missing = sorted(expected - seen_ids)
            errors.append(f"case ids are not contiguous 0..{len(evals)-1}; missing: {missing}")


def main():
    args = parse_args()
    evals_path = os.path.abspath(args.evals)
    if not os.path.exists(evals_path):
        print(f"error: {args.evals} not found")
        sys.exit(1)

    repo_root = os.path.abspath(args.repo) if args.repo else default_repo_root(evals_path)

    try:
        with open(evals_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"error: {args.evals} is not valid JSON: {e}")
        sys.exit(1)

    errors = []
    validate_suite(data, repo_root, errors)

    n = len(data.get("evals", [])) if isinstance(data, dict) else 0
    if errors:
        print(f"FAIL — {args.evals} ({n} cases, {len(errors)} problem(s))")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"PASS — {args.evals} ({n} cases, all structural + protocol checks clean)")
        sys.exit(0)


if __name__ == "__main__":
    main()