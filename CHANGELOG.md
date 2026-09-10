# Changelog

All notable changes to this skill pack are documented here. The format follows the project's versioning scheme `v[major].[feature].[audit]` (see MAINTENANCE.md § Versioning). Pre-v1.0.0 history is preserved in RESEARCH.md's `Output v0.x.y` markers; this changelog begins at the first stable baseline.

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
