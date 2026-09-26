# The paired-run eval protocol

A transferable method for proving that an agent with a domain skill knows the domain —
and noticing the instant it stops knowing it.

The claim this protocol makes: **fluency should be proven, not promised.** A skill author
says "my agent is fluent in X". This protocol is the machine that makes that claim testable:
each case runs twice — once with the skill loaded, once against a clean baseline — and both
answers are graded against the same structural assertions. The skill earns its keep only if it
beats the baseline on its own assertions. The delta is the proof.

Worked reference implementation: `../evals/evals.json` (24 cases) and the dated archives
`../evals/sample-output-2026-09-07.md`, `-analyst-2026-09-08.md`, `-degen-2026-09-07.md` in this
repo. This file is the generalized method; those files are the method in action.

## 1. What is being proven

A domain skill's value is **anti-hallucination in a narrow vertical**, not raw knowledge.
A general agent already knows *about* most domains; what it does not know is the domain's
load-bearing facts, its dated negatives, its honest scope, and how to decompose before judging.

So the baseline is not a strawman and not "the wrong answer". The baseline is a strong general
agent with web access. The question the protocol answers is narrow: *what does the skill add
that the general agent gets wrong, goes fuzzy on, or states with confidence but cannot date?*

## 2. Case design

Write cases as a real user would type them — lowercase, loose grammar, no skill vocabulary.
Idealized prompts test nothing; they prime the answer.

- **One case per capability.** A screen-mode case, a track-mode case, a refusal case, a
  build-mode case. When a new capability lands, it ships with a case: the case is the gate.
- **Carry the load-bearing facts, especially the dated negatives.** "No strip venue exists",
  "the dividend pipe has never fired", "no lending market is verified live" — each is a fact a
  single event flips. Cases that test a dated negative are the cases whose assertions survive
  the flip and catch the rot.
- **Name the `files` that ground the case.** Asserting which references the with-skill run is
  supposed to load makes the run reproducible and keeps the case honest about what it gates.

## 3. Assertion design (the heart)

Assertions grade **structure and discipline, never specific values.** Live data drifts, and a
skill's load-bearing facts are session facts — so an assertion that demands "the price is X"
fails tomorrow for a reason unrelated to the skill's health. The correct demand is:

- **A dated check.** "States paid/not-paid only with a dated trace or an explicit unresolved
  flag." The number may be anything; it must carry its own timestamp.
- **A named evidence tier.** "Classifies the tier explicitly: mechanism documented, never
  exercised." Verified-print vs terms-only vs unknown is a discipline, not a value.
- **A named procedure.** "Walks the Mints-and-redeems row before any liquidity claim."
- **A refusal where the premise is fabricated.** "Never states or implies the token 'is' the
  share." A skill's most load-bearing assertion is often negative.

Rule of thumb: an assertion should still be markable pass/fail the day after the domain's
biggest event ever happens. If a real-world event could make the assertion un-answerable, it is
testing the wrong thing.

## 4. The paired run

For each case, produce **two** answers:

1. **WITH** — the skill is loaded; the grounding files are read; live state is pulled before
   any numeric claim.
2. **WITHOUT** — a clean baseline: a general-purpose agent, no skill context, project directory
   off-limits, web search allowed. A strong baseline, not a strawman.

Same prompts, same assertions, blind grading: the grader marks the two answers independently,
ideally without knowing which is which.

## 5. Grading is judgment, not a script

No auto-scorer. A human or a grading agent reads both outputs and marks each assertion
pass/fail, arguing each mark. The protocol is a *checklist that forces the grader to look*,
not a scoring formula. That is deliberate: the moment grading becomes scripting, it grades the
script, not the skill.

Record verdicts per assertion per run (the `worksheet.json` from `prepare.py` is the blank grid;
`report.py` renders the delta table). A case that no longer separates the skill from the
baseline is a signal — either the baseline learned, or the assertion rotted. Both are findings.

## 6. Dated archiving

Every real graded run is archived as a dated sample output next to the suite
(`sample-output-{date}.md`) containing:

- the questions and both answers (or faithful excerpts),
- the delta table,
- a verdict paragraph saying plainly whether the gate passed,
- **fairness caveats**, recorded honestly:
  - whether the grader authored both the assertions and the skill-side run (and that a second,
    independent grader should re-score before this counts as canonical),
  - tooling asymmetry (baseline with web search vs skill with keyless routes — roughly
    comparable, not identical),
  - anything the run flagged as unverified that needs a post-hoc check,
- a **post-run verification note**: what was pulled live this session, what remains unresolved,
  and which prior archived claim (if any) flipped.

## 7. Capability gating

A new capability lands only with a new case. The suite is the changelog of trust: if there is
no case that proves today's new claim, the claim has no test, and the skill does not ship the
claim. Backfilling a rule without its case is a recorded violation, not a quiet exception.

## 8. Fairness caveats (recap — these are load-bearing)

1. **Grader bias** — prefer a blind, independent grading pass for anything presented as the
   suite's canonical pass.
2. **Tooling asymmetry** — name it when the baseline gets web search and the skill gets its own
   keyless routes. Roughly comparable, never identical.
3. **The baseline is not a strawman** — when the baseline gets things right, say so. The skill's
   edge is discipline, not raw knowledge; an archive that hides the baseline's wins is lying to
   the reader about what the skill is worth.

---

This file is meant to be copied. Point any skill author here, or vendor the method into the
skill's own `evals/` — the schema, scripts, and toy example in this directory make the copy
mechanical.