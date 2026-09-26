# Eval harness kit — prove a domain skill, don't promise it

A reusable, keyless kit for running the **paired-run eval protocol**: every case runs twice —
once with the skill loaded, once against a clean general-agent baseline — and both answers are
graded against the same structural assertions. The delta between the two runs is the proof that
the skill knows its domain.

This is the method behind `../evals` (the `base-tokenizedstocks` skill's domain suites, which
live in this repo as the living reference implementation — see `examples/`). The kit itself is a
developer tool: installable, stdlib-only, no API keys, no network at grading time.

## Quickstart

Have a domain skill with a `SKILL.md` and some grounding files? Point the kit at your suite.

```bash
# 1. Write (or copy) an evals.json for your skill:
#    one case per capability, assertions structural, never frozen values.
#    See examples/toy-evals.json for the smallest valid suite.

# 2. Validate it — JSON, required fields, sequential ids, referenced files exist.
python3 harness/scripts/validate.py -e my-skill/evals.json -r .

# 3. Expand into a task pack + blank grading worksheet.
python3 harness/scripts/prepare.py -e my-skill/evals.json -o work/

# 4. Run each case twice (human or grading agent, your judgment):
#      work/out/00-foo.without.md   — the prompt, clean baseline, no skill context
#      work/out/00-foo.with.md      — the prompt + grounding files + skill run rules
#    Mark each assertion pass/fail for each run in work/worksheet.json.

# 5. Render the delta table for a dated archive.
python3 harness/scripts/report.py -w work/worksheet.json -e my-skill/evals.json -o delta.md
```

## Scripts (stdlib python3, no dependencies)

| script | does |
|---|---|
| `scripts/validate.py` | Checks an evals.json against the schema's structural rules: well-formed JSON, required fields per case, unique sequential ids, non-empty assertions, referenced `files` existing on disk. Exit 0 = valid, 1 = problems listed. |
| `scripts/prepare.py` | Expands a suite into a runnable task pack — per case a `.with.md` (grounding files + skill run rules) and a `.without.md` (raw prompt, no skill context) — plus a blank grading worksheet serialized as `worksheet.json`. `-n` dry-runs the layout. |
| `scripts/report.py` | Turns a completed grading worksheet + the suite into the markdown delta table (`Q \| Assertions \| With skill \| Baseline \| Baseline's failure` + totals row), ready to paste into a dated sample output. |

Grading itself is deliberate: it stays human/agent judgment, never a script. The worksheet is a
checklist that forces the grader to look, not a scoring formula.

## Read next

- `guide/PROTOCOL.md` — **the transferable method.** What is being proven, case design around
  load-bearing dated negatives, structural assertion design, the paired run, grading-as-judgment,
  dated archiving, capability gating, fairness caveats. Point skill authors here, or vendor the
  method into the skill's own `evals/`.
- `examples/` — a self-contained 2-case toy suite for smoke-testing the scripts standalone, plus
  a pointer to the full reference implementation (24 cases) in `../evals`.
- `../evals/sample-output-*.md` — dated archives of real, graded runs in the exact shape the kit
  produces.