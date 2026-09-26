# Examples

- **`toy-evals.json`** — a self-contained 2-case suite so you can smoke-test the kit
  standalone without a domain skill. Run `validate.py -e harness/examples/toy-evals.json -r .`
  and `prepare.py -e harness/examples/toy-evals.json -o /tmp/toy`.

- **`../evals`** — the full reference implementation: a 24-case domain suite plus dated archived
  runs (`sample-output-2026-09-07.md`, `-analyst-2026-09-08.md`, `-degen-2026-09-07.md`) in the
  exact shape this kit produces. The suite is the changelog of trust for the
  `base-tokenizedstocks` skill: every capability shipped with a case, and every case runs twice.