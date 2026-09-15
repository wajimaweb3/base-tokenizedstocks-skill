# Changelog

All notable changes to this skill pack are documented here. The format follows the project's versioning scheme `v[major].[feature].[audit]` (see MAINTENANCE.md § Versioning). Pre-v1.0.0 history is preserved in RESEARCH.md's `Output v0.x.y` markers; this changelog begins at the first stable baseline.

## [1.2.2] — 2026-09-15

Closes the two residual hardcoded counts the v1.2.1 count sweep left in `meme-pair-launchpad.md`. No new rubric, route, or operating rule — an audit pass.

### Changed

- **`meme-pair-launchpad.md` — the surface's last two static counts are gone.** The vanity-squat entry's "shared by all thirteen genuine B20 tokens" now reads "every genuine registry-verified B20 token (the count derives from the registry per session)". The wrapper-surface entry's "eleven 1:1-backed equities and ETFs (wtCOIN, …)" now reads "a set of 1:1-backed equities and ETFs (examples as of the 2026-09-07 enumeration: wtCOIN, wtNVDA, wtMSTR, wtSPCX, + wtSGOV/wtSKHY/wtSPYM/wtDRAM/wtQQQM/wtIAU/wtCEG — the family set is a session fact, re-enumerate per session)". Both now follow rule 9's doctrine (dated snapshot + derive instruction) that already governed the rest of the surface; the ST0x list is a dated example set, and the family count is derived per session, never quoted.
- **Version bumped to 1.2.2** in SKILL.md frontmatter, manifest.json, and package.json (audit digit, per MAINTENANCE.md § Versioning).

## [1.2.1] — 2026-09-14

Audit pass on the build surface: the derive-the-universe schema. No new rubric or route — a discipline change across the skill's surface, driven by the unit test (case 23 `build-surface-dev`) that caught the "4 of 13 in live pools" whitespace negative already stale six days after v1.2.0 shipped (Beefy then read 10 stock-USDC vaults). Supersedes hardcoded static counts with "state the anchor, derive the count."

### Changed

- **Rule 9 added to SKILL.md — "Derive the universe, don't state it."** Token, pool, and vault counts (13 B20 tokens, 4 of 13 in live pools, 9 Beefy vaults, ~30 meme pools) are session facts: the agent pulls the set from the registry and live enumeration (routes `b20-multiplier`, `meme-stock-pools`, `token-price`, `stock-yield-vaults`, `basestonk-launches`) rather than quoting a snapshot. Dated counts in the pack are worked examples for sanity-checking, never assumptions the answer carries.
- **Count sweep across the surface.** Every "N of 13" / "~N pools" / "N vaults" / "N launches" stated in `build-surface.md` (all three layers + the build-read discipline gains a sixth point "state the anchor, derive the count"), `how-work.md` (build-mode step 2), `issuer-comparison.md` ("where it trades" row + "absence is data"), `meme-pair-launchpad.md`, `README.md`, `manifest.json` (dshares + coinbase-stocks rows), and `api-routes.json` (`token-price`, `meme-stock-pools`, `stock-yield-vaults`, `basestonk-launches`, `b20-multiplier`) now reads as *method + dated snapshot*: derive the set per session, keep the snapshot as a sanity-check baseline, never reproduce it as the count.
- **Eval assertions brought in line with the protocol's own rule.** The suite's notes already said "assertions test structure and discipline, never specific values: live data drifts" — but case 20 `issuer-comparison` and case 23 `build-surface-dev` hardcoded "4 of 13" and "9 of 13", which would fail any agent that correctly derived the live count. Reframed to assert the discipline (derive the pool set per session, date every negative) with the snapshot admitted only as a named reference, satisfying the protocol the suite already claimed.
- **Description frontmatter and manifest version bumped** to 1.2.1; description trimmed the volatile "714 dShares / 13 B20" counts (trigger coverage unchanged — the ticker anchors remain).

### Recorded (unit-test finding, 2026-09-14)

- **Whitespace negative "9 of 13 B20 without an onchain market" requires re-verification.** Independent checks today: Beefy API reads **10 active stock-USDC vaults** on Base (AAPLc, AMZNc, GOOGLc, METAc, MSFTc, MSTRc, NVDAc, SNDKc, SPCXc, TSLAc — the v1.2.0 state was 4), implying live Aerodrome books for at least ten B20 tokens, not four. `docs.basestonk.io/stock-pairs.md` still reads "four trade in live pools" but that is the launchpad's pair-gate stance (it refuses Aerodrome pools), not evidence of absence. The skill now handles this exactly as designed: the count is no longer in the pack — the agent derives it per session. Treat "which B20 trade live" as flippable until a full per-token registry enumeration this session settles it.

## [1.2.0] — 2026-09-11

First developer-audience feature: the build surface.

### Added

- **`build-surface.md` rubric.** The map of what can be built on Base tokenized equity, in three layers — rails (the B20 standard with its multiplier and policy-scope reads, the onchain registry, the custody chain, the data rails), integration points (Aerodrome stock/USDC pools, Beefy vaults, the launchpads with their hook-permission read), and whitespace (the dated negatives — no strip venue, no lending market, no index product, 9 of 13 B20 without a pool — each named with the rail it would sit on). Names docs.base.org as the documentation home, distinct from the ecosystem announcement's tagline surface.
- **"build" task mode (fifth) in `how-work.md`.** Classifies the build intent (integrate / extend / fill), maps the three layers, and states what any build inherits (weekend gap, terms-only dividend, eligibility gating, issuer risk).
- **Gating case 23 `build-surface-dev`.** Eval suite is now 24 cases.

## [1.1.0] — 2026-09-10

First feature since the stable baseline: a keyless dShare price route.

### Added

- **`dshare-price` route (CoinGecko, keyless).** dShares have no permissionless DEX book on Base — they trade on Dinari's order sessions — so GeckoTerminal returns empty by design and the issuer's own API is keyed (X-API-Key-Id + X-API-Secret-Key, enterprise-only). CoinGecko lists the major dShares and ETFs with live prices, closing the gap that left `issuer-comparison.md` and `onchain-basis.md` unable to run on dShares. The route labels the price a reference print (order-session aggregate, not a DEX price), stamps `last_updated_at`, and notes the keyed-if-in-env pattern for a CoinGecko demo key.
- **Wired into two rubrics.** `issuer-comparison.md`: the dNVDA float/vol and price-fidelity rows now carry the CoinGecko reference read, and the "absence is data" paragraph records that the keyless route exists while the no-DEX-book absence stands. `onchain-basis.md`: the arb-access entry and the worked-set note now distinguish the dShare's reference basis (order-session aggregate vs underlying) from an onchain basis.
- **Gating case 22 `dshare-price-cross-issuer-basis`.** Eval suite is now 23 cases.

## [1.0.2] — 2026-09-10

Second audit pass. No new rubric, route, or operating rule — a gating-case backfill for rule 8, a canonical-number consistency sweep, and a full route-liveness re-check.

### Changed

- **Rule 8 gating case backfilled.** Rule 8 ("show the address, not just the ticker") landed in v1.0.1 without an eval case, against the skill's own gate rule. Added eval case 21 `contract-address-discipline` (every named token and pool carries its contract address on first mention) and extended case 13's first-mention assertion to demand the contract address. Eval suite is now 22 cases.
- **Canonical-number sweep.** README's "700+ dShares" corrected to 714 (the count every other file already carried); a corrupted arrow in SKILL.md rule 3 repaired. 714 and 13 B20 now read identically across SKILL.md, README, manifest, and api-routes.
- **Route liveness re-check (2026-09-10).** All 13 routes hit and shape-checked; the check date is recorded in each route's notes. Findings: Yahoo query1 still HTTP 429 (the stockanalysis.com fallback remains the working path); BaseStonk's live endpoint now exercised (506 launches returned); everything else HTTP 200 with unchanged response shapes.

## [1.0.1] — 2026-09-09

First audit pass on the stable baseline. No new rubric, route, or eval case — this is spec-compliance, a new output rule, and two recorded findings.

### Changed

- **Description frontmatter trimmed (2860 → 992 chars).** The v1.0.0 description exceeded Anthropic's 1024-char limit, which claude.ai rejects at upload. Trimmed to the issuer identities, the primitive list, one or two trigger examples per category, and the three exclusions. No trigger coverage lost.
- **New operating rule 8 — "Show the address, not just the ticker."** Every token, pool, or contract named in an answer now carries its contract address on first mention (full address when known, otherwise the source and a verify-the-full-address note). A ticker alone is a copycat's opening. Reinforced in the runtime routine's asset-identification step.

### Recorded (RESEARCH.md evidence ledger)

- **vvveity launchpad** (docs at stock.vvveity.com/docs) — a stock-paired launchpad not in Base's official ecosystem list, surfaced via web search in a claude.ai browser test. Added to `meme-pair-launchpad.md` as an unverified-until-enumerated fifth factory-layer entry.
- **claude.ai browser test finding** — keyless routes are partially blocked in the claude.ai sandbox (a docs.base.org curl failed), and the skill falls back to web search; the verify-by-address discipline held even over the uncured surface (it flagged the CoinGecko "Stonks" cross-chain trap). Claude Code remains the venue for validating live numbers.

## [1.0.0] — 2026-09-08

First stable baseline. Everything accumulated before this version is the baseline; the feature counter starts from zero at this major. Bumping major from here is a human decision.

### Shipped

- **10 rubric files** in `references/`: claim-stack, corporate-action, yield-strip, index-composition, future-yield-lending, meme-pair-launchpad, lp-vault-yield, onchain-basis, issuer-comparison, concepts, plus how-work (task modes).
- **13 routes** in `api-routes.json` (all keyless): underlying-price, dividend-calendar, corporate-action-announcements, multiplier-history, b20-multiplier, stock-yield-vaults, constituent-universe, token-price, strip-implied-yield, eligibility-custody, meme-stock-pools, basestonk-launches, onchain-basis.
- **10 manifest rows** in `manifest.json` (issuer docs + B20 standard + ecosystem announcement + launchpad venues).
- **21 eval cases** in `evals/evals.json` spanning all four task modes (understand, valuate, screen, track) and every rubric, from a normie asking whether dNVDA is the same as owning NVIDIA to an execution request the skill must refuse.
- `SKILL.md` (entry, triggers, operating rules, runtime routine), `README.md`, `MAINTENANCE.md` (maintenance protocol + versioning scheme), `LICENSE` (MIT, holder @wajimaa_).
- `examples/assessment-example.md` — the worked output shape on dNVDA.
- Two archived dogfood runs: `evals/sample-output-degen-2026-09-07.md` (degen tier, 3 questions), `evals/sample-output-analyst-2026-09-08.md` (analyst tier, 4 questions across two batches).

### Verified live state (2026-09-08)

- **Two issuers live on Base**: Dinari (714 dShares) and Coinbase (13 B20 stocks — NVDAc, TSLAc, AAPLc, MSFTc, and peers, ex-US).
- **All Base dividend mechanisms terms-only**: 13/13 B20 multipliers read exactly 1.0; Dinari's Base DividendDistribution pipe is staging (one reclaimed 0.77 USD+ internal test, no public payout).
- **xStocks multiplier print verified off-Base** (evidence anchor only — AAPLx 1.0→1.0033 over five quarterly activations, SPYx 1.0→1.0057 over four, 2026-09-07).
- **Beefy auto-compounding vaults live** on Aerodrome stock/USDC pools (NVDAc, AAPLc, METAc, GOOGLc).
- **Meme/launchpad layer live**: ~37 native meme×stock pools + ~60 wrapped wtCOIN pools; o1-launchpad dominant, bankr secondary, BaseStonk not in the official ecosystem list (list non-exhaustive).
- **Onchain basis live-feasible** (GeckoTerminal + Yahoo keyless); 4 of 13 B20 trade in live pools, 9 have no onchain market yet.
- **No strip venue, no index/basket product, no lending market on Base** as of 2026-09-08 — those rubrics are forward-looking, the method for the day one ships.

### Pre-v1.0.0 history

See RESEARCH.md's `Output v0.x.y` markers for the dated ledger of when each feature landed before this baseline (v0.1.0 manifest draft → v0.10.1 analyst-tier amendments). Those markers are left as-is; changing them would falsify the ledger.
