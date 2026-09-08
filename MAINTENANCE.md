# Maintenance protocol

Maintainer-facing document (repo-level, like README; not loaded at runtime). Everything in this pack is dated, and dates expire. This file is the protocol for expiring gracefully.

What makes this skill rot differently from most: its load-bearing facts are dated negatives. "No strip venue exists", "the B20 dividend mechanism has never fired", "no lending market for tokenized equity" — each of these flips on a single event, and a skill that keeps asserting a flipped negative is worse than no skill at all. Maintenance here is not housekeeping; it is re-checking the negatives before they lie.

## The three clocks

1. **Per session (already enforced at runtime).** SKILL.md and api-routes.json carry the rule: re-verify endpoint liveness on first use in a session, date every number. This clock needs no protocol beyond what ships.
2. **Event-driven (same day).** When a load-bearing negative flips — a B20 dividend actually fires, a strip venue launches, an index product ships on Base, Dinari's dividend pipe moves off staging — the touched files update the same day: the relevant reference, the route notes, the dated claims in README, and any eval sample output that asserts the old state. Eval *assertions* are structural by design ("states the venue status dated") and survive flips; the *prose around them* does not.
3. **Quarterly, and immediately after any market event that touches the class.** The full sweep below.

## Quarterly checklist

1. **Negative sweep — the skill's load-bearing facts, in order:**
   - B20 multipliers: one `eth_call` per live token (selector `0x1b3ed722`, expect exactly 1e18 on all tokens; the curl one-liner is in RESEARCH.md §1.4). Anything above 1e18 means a corporate action has finally fired — update corporate-action.md, claim-stack.md, how-work.md, the b20-multiplier route notes, README's dated claims, and file the print in RESEARCH.md.
   - Dinari DividendDistribution on Base (proxy `0x7978…01e`): lifetime transaction count still 5? A sixth transaction (`createDistribution`/`distribute`) means the pipe has moved off staging — same-day propagation as above.
   - base.org/stocks FAQ: does "How are dividends and splits handled?" now have a published answer? (As of 2026-09-07 the question ships with no answer.)
   - Strip venue: any PT/YT product for tokenized equity on any chain. yield-strip.md stays forward-looking until one names a venue and a contract.
   - Index/basket/AI-portfolio on Base (index-composition.md Part B), and lending markets with tokenized-stock collateral (Aave and Euler remain unverified taglines until checked; Morpho's negative dates from 2026-09-07).
   - Live layer drift: Beefy stock vaults still active, Aerodrome pool volumes re-pulled, new stock/meme pairs noted (BLUECHIP/NVDAc was the first, found 2026-09-07).
2. **Route liveness:** hit every route in api-routes.json once and shape-check the response, not just the status code. The Stooq lesson is the canonical case: verified 2026-09-06, dead by 2026-09-07. Record the check date in the route's notes on every sweep.
3. **Manifest:** fetch each manifest.json source once; fix moved URLs; add new llms.txt endpoints when issuers publish them.
4. **Eval re-run:** the paired protocol — with skill, without skill, same assertions, blind grading. The skill must still beat the baseline on its own assertions; a case that no longer separates them is a signal the baseline learned (or the assertion rotted). Archive each run as `evals/sample-output-{date}.md` with a post-run verification note.
5. **Calibration refresh:** every dated number in references/ re-pulled. Superseded numbers are marked, not silently replaced — the date is part of the claim, and "terms-only as of X, superseded as of Y" is evidence, not clutter.

## Versioning

Scheme: `v[major].[feature].[audit]` — set by the user 2026-09-08.

- **Major (digit 1)** — a structural break: a rewrite of the prime directives (read-only, evidence tiers, Base-exclusive scope), a change to the audience ladder, or a release boundary declared by the user. `v1.0.0` is the first stable baseline: everything accumulated before it is the baseline, and the feature counter starts from zero at this major. Bumping major is a human decision, never automatic.
- **Feature (digit 2)** — a new capability landed: a new rubric file, a new route, a new eval case gating a capability, or a substantive new section in an existing rubric. Bumps the second digit and resets the audit digit to 0. `v1.0.0` → `v1.1.0` when the next feature lands (e.g. Wasabi/perps research, developer-tier features).
- **Audit (digit 3)** — testing, troubleshooting, or polish that does not add a capability: a dogfood re-run, a calibration refresh, a route-liveness fix, a prose pass, a consistency sweep, a verification archive. Bumps only the third digit. `v1.0.0` → `v1.0.1` on the next audit pass.

The changelog of record is `CHANGELOG.md`; `DESIGN.md` §7 holds scope & roadmap. RESEARCH.md's `Output v0.x.y` markers are the historical ledger of when features landed before `v1.0.0` and are left as-is (changing them would falsify the ledger). No change lands without a row in the changelog.

## Self-updating (the automation gradient)

One hard rule: **machines may re-check facts; changing judgment is a human act.**

- **Fully automatic, safe on a schedule:** the negative sweep and route liveness checks are pure keyless reads with deterministic expected values (multiplier == 1e18; tx count == 5; response shape per route). A scheduled job may run them and write a dated report. It never edits references/, evals/, or SKILL.md.
- **Auto-propose, human-merge:** an agent may run the quarterly checklist and draft the updates a flip would require, delivered as a diff or pull request. A human approves before anything lands. On release, a scheduled CI job opening PRs is the right shape; in a private workspace, a recurring task producing a dated change report.
- **Human-only:** the prime directives (read-only, evidence tiers, Base-exclusive scope), rubric content, audience priorities, and assertion wording. Those are the editorial judgment that makes the skill trustworthy.

Why the gate exists: an agent that rewrites its own beliefs from whatever it reads is a prompt-injection target. One adversarial page claiming "dividends now pay cash to all Base holders" must never be able to edit corporate-action.md by itself. Pages propose; the maintainer disposes.

## Where the evidence lives

RESEARCH.md (repo root, not shipped) is the evidence ledger: addresses, tx hashes, selectors, endpoints, negative results, and the exact re-check command for every claim in the sweep above. A maintenance run that cannot reproduce a claim from RESEARCH.md treats the claim as unverified and flags it for re-verification — never silently keeps or drops it.
