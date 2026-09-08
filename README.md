# base-tokenizedstocks

A skill pack that makes an AI agent fluent in **tokenized equity on Base** — real shares issued onchain by two live issuers (Dinari: 700+ dShares; Coinbase: 13 B20 stocks, NVDAc to TSLAc), and the primitives being built on top of them. Base is the skill's only subject: off-Base products enter solely as evidence about the class, never as venues.

Drop it into Claude, ChatGPT/Codex, Grok, Cursor, or any agent harness, and the agent stops answering tokenized-stock questions with generic finance boilerplate and starts answering them the way an equity-native analyst would: claims before tickers, decomposition before verdicts, evidence tiers before promises.

## What it does

The skill exists because a general AI gets tokenized equity wrong in predictable ways: it says a tokenized stock "is" the share, quotes returns without saying which legs they contain, and asserts corporate-action outcomes no live event has tested. base-tokenizedstocks fixes that with three frameworks a general model does not carry:

- **The claim stack** — every tokenized stock is four layers (token → issuer claim → underlying → pass-through rights). Ownership questions are answered by walking the layers, not by trusting the ticker.
- **The gap menu** — for yield strips, the analytical content is the gap between the implied forward dividend and the announced one, explained in ranked order (special dividend → fee leak → stale pricing → market view → true mispricing).
- **Evidence tiers** — every corporate-action claim is tagged verified print, terms-only, or unknown. Nothing gets stated as fact until a real event has exercised it — and corporate actions are read at two layers: on the underlying, and on the issuer itself (the one live issuer-level print: Backed's acquisition by Kraken and pivot to xStocks).
- **The composition read** — an onchain basket is N claim stacks plus a composition layer: weakest-link screens per constituent, weight drift, dollar-accurate dividend composition, rebalance cost at the thinnest exit, and the eligibility intersection that redlines the whole basket.
- **The lending read** — what breaks first when the collateral is a claim stack: an eligibility-gated recovery path, liquidation that never sleeps against a collateral priced on market sessions, dividends landing somewhere mid-term, and an LTV that credits future yield is underwriting the dividend itself.
- **The meme/launchpad read** — memecoins launching in pools paired with real tokenized stocks: verify the stock leg against the registry (never the name or address prefix — one memecoin already squats the B20 vanity pattern), read the launchpad's hook permissions, compute amplification from onchain reserves rather than the FDV sticker (the FDV field proved unstable within a single day), and respect that the position embeds an equity claim stack with a weekend gap. The trending screen ranks the genre on momentum, flow skew, reserve depth, and lifecycle stage — never volume alone.
- **The LP/vault yield read** — the one live yield layer on tokenized stocks (Aerodrome stock/USDC pools, Beefy auto-compounding vaults) judged as four dated legs — fee flow computed from same-day volume, incentives, session-clock impermanent loss (the stock leg gaps on weekends while the pool keeps trading), and vault layer costs — with the honesty flag that it is trading-pair yield, never dividend pass-through.
- **The onchain basis read** — the gap between a tokenized stock's onchain price and the underlying's last print is not an error; it is the live price of the claim-stack friction, read across two clocks (the onchain leg trades 24/7, the equity leg quotes the last close on weekends and holidays). The rubric decomposes it into four ranked entries — session gap, depth and float, arb-access asymmetry, and stacked wrapper legs — and refuses to call a session-stale basis a mispricing.
- **The cross-issuer comparison read** — for one underlying, N claim stacks (three for NVDA as of 2026-09-08: a Dinari dShare, a Coinbase B20, an ST0x wrapper). The comparison is per claim layer — legal claim, custody, mint/redeem access, eligibility, corporate-action tier, where it trades, depth, price fidelity — never a ranking, and the verdict is the weakest link per holder goal.

It serves, in order: people new to tokenized stocks, analysts, traders hunting mispricings — and only last, developers building on the rails.

## How it works

Two layers, loaded on demand:

- **The task layer** (`references/how-work.md`) shapes the answer for the job: understand (teach the primitive), valuate (judge one instrument), screen (sort the universe), track (diff what changed).
- **The domain layer** (`references/claim-stack.md`, `references/corporate-action.md`, `references/yield-strip.md`, `references/index-composition.md`, `references/future-yield-lending.md`, `references/meme-pair-launchpad.md`, `references/lp-vault-yield.md`, `references/onchain-basis.md`, `references/issuer-comparison.md`, `references/concepts.md`) holds the frameworks themselves.

Per question, the agent runs a four-step routine: classify the task and domain, ground on the foundations, pull live state through `api-routes.json` (keyless first, every number dated), then answer with the decomposition visible. `manifest.json` is the address book of verified issuer documentation. The worked shape of a full answer is in `examples/assessment-example.md`.

Read-only, always: the skill analyzes and flags risk; it never constructs or signs a transaction.

## Evals

`evals/evals.json` holds the test suite: 21 cases spanning all four task modes (understand, valuate, screen, track) and every rubric, from a normie asking whether dNVDA is the same as owning NVIDIA to an execution request the skill must refuse. Each case runs twice — once with the skill loaded, once without — and both outputs are graded against the same assertions; the skill earns its keep only if it beats the baseline on its own assertions. Grading is judgment (a model or human reads both outputs), not a script, and assertions demand structure and discipline — a dated check, a named evidence tier — never frozen values, because the skill's load-bearing facts are dated negatives (no strip venue, an unexercised dividend pipe) that a single event will flip. New capabilities gate on a new case before they land, and full real runs are archived as dated sample outputs next to the suite.

## Honest scope (as of 2026-09-07)

- **Two issuers are live on Base**: Dinari dShares (714 assets) and Coinbase's B20 stocks (13 tokens — NVDAc, TSLAc, AAPLc and peers — 1:1 against shares in regulated custody, ex-US only, mint/redeem restricted to KYC'd Authorized Participants; verified 2026-09-07). **Backed bTokens** are a retired line, not a dead issuer: Backed was acquired by Kraken (Dec 2025) and pivoted all-in to xStocks (Mar 2026, Solana — off-Base). bTokens stay redeemable with no new issuance, and the pivot itself is the anchor precedent for issuer-level events — the one live issuer-level print.
- **The class's only verified underlying-level dividend print also lives off-Base**: xStocks' reinvesting multiplier (AAPLx 1.0 → 1.0033 over five quarterly activations, SPYx 1.0 → 1.0057 over four, issuer API cross-checked onchain to full precision, 2026-09-07). On Base itself every dividend remains terms-only — and the question is now swept, not assumed: all 13 B20 multipliers read exactly 1.0, and Dinari's Base distribution contract has served a single reclaimed 0.77 USD+ internal test (both verified 2026-09-07), so the state is a one-call check per issuer, re-run after every ex-date. Off-Base evidence is cited for what a mechanism looks like when it fires — never as a venue.
- **No PT/YT strip venue for tokenized equity exists yet, on any chain.** The yield-strip rubric is deliberately forward-looking: it is the method for pricing strips the moment one launches. Treat any "strip price" an agent quotes today as fabricated.
- **No index, basket, or AI-personalized portfolio product for tokenized equity is verified on Base either — but the single-token yield layer is live and now judgeable**: Aerodrome stock/USDC pools with active Beefy auto-compounding vaults (NVDAc, AAPLc, METAc, GOOGLc; verified 2026-09-07) — the LP/vault rubric decomposes their yield into four dated legs and flags that it is trading-pair yield, not dividend pass-through. Manual multi-dShare portfolios are analyzable today (Part A of the composition rubric); treat any quoted "index product" as fabricated until it names a venue and a contract. The class's first live onchain equity index sits off-Base as evidence (Hood Index hMAG7, Robinhood Chain, live 2026-07-17), and the announced S&P Digital Markets 50 (Dinari × S&P DJI, Oct 2025) is not live.
- **No lending or margin path for tokenized equity is documented by any issuer or verified on any chain** — base.org's partner page markets Aave/Morpho/Euler lending taglines, but a 2026-09-07 Morpho check found no live tokenized-stock market: taglines are not venues. The lending rubric is forward-looking in full — the method for judging a venue the moment one appears, led by what breaks first when the collateral is a claim stack.
- **The onchain basis and the cross-issuer comparison are live-feasible today** — both legs of the basis (token price via GeckoTerminal, underlying via Yahoo) pull keyless, so the basis rubric's worked set is dated and re-pullable, not hypothetical; the cross-issuer comparison runs on three real stacks for NVDA (dNVDA, NVDAc, wtNVDA), and only four of thirteen B20 tokens trade in live pools at all (NVDAc, GOOGLc, AAPLc, METAc; per docs.basestonk.io, 2026-09-08), so an empty pool enumeration for the other nine is a finding about where the market lives, not an absence of product.
- **The meme/launchpad layer is live and Base-native — and its stock legs come in two surfaces** (enumerated 2026-09-07 by registry token address): roughly thirty memecoin pools paired with real B20 stocks (NVDAc ~12, SPCXc ~11, AAPLc ~14), o1-launchpad (01 Exchange, per Base's official B20 ecosystem announcement) dominant with bankr secondary, volumes from ~$800k/day to triple digits. A second surface pairs memes against **wrapped** stock tokens (the ST0x family — wtCOIN, wtNVDA and peers; found 2026-09-07 when the degen dogfood showed COINc-native with zero pools while BALD/wtCOIN traded $247k/day): a "paired with stock X" question must first ask which token, native or wrapped, because registry verification sees only the native leg and a wrapper is a separate claim stack. The genre runs a launch-then-graduate lifecycle, swarms new stock listings (SPCXc listed 2026-09-03 and carried ten meme pairs within days), and its one verified impersonation-adjacent trick is address vanity-squatting — a memecoin grinding the `0xb200…` B20 prefix. BaseStonk (basestonk.io) breaks the lifecycle default — live Uniswap v4 pools from block one, no graduation — and is not in Base's official ecosystem list, which proves that list non-exhaustive. The same pairs exist off-Base under other issuers' tokens (Robinhood Chain, BSC) as evidence, never venues.
- Market data comes from free public endpoints (Yahoo Finance, stockanalysis.com, GeckoTerminal); terms come from issuer docs. Every figure in this pack is a teaching prop until re-pulled live.

## Structure

```
base-tokenizedstocks/
├── SKILL.md                      # entry: triggers, operating rules, runtime routine
├── MAINTENANCE.md                # maintenance protocol: three clocks, negative sweep, automation gradient
├── manifest.json                 # verified issuer + standard documentation
├── api-routes.json               # question → endpoint router (with honesty flags)
├── references/
│   ├── concepts.md               # foundations: the core mental models
│   ├── claim-stack.md            # what a tokenized stock actually gives you
│   ├── corporate-action.md       # who gets what when the underlying — or the issuer — moves
│   ├── yield-strip.md            # separating the price leg from the dividend leg
│   ├── index-composition.md      # a basket is N claim stacks plus a composition layer
│   ├── future-yield-lending.md   # what breaks first when the collateral is a claim stack
│   ├── meme-pair-launchpad.md    # memecoins paired with real stocks: verify, size, survive
│   ├── lp-vault-yield.md         # the live yield layer: four dated legs, no fused APR
│   ├── onchain-basis.md          # the gap between token price and share price, across two clocks
│   ├── issuer-comparison.md      # same underlying, N claim stacks: compare per layer, never rank
│   └── how-work.md               # understand / valuate / screen / track
├── examples/
│   └── assessment-example.md     # the output shape, worked on dNVDA
└── evals/
    └── evals.json                # 21 paired-run cases: assertions on structure, not values
```

## Install

Manual (works now): clone or copy this folder into your agent's skills directory (for Claude Code: `.claude/skills/` in a project, or `~/.claude/skills/` globally). The skill activates on the triggers in `SKILL.md`.

Skills CLI (pending publication): `npx skills add <owner>/base-tokenizedstocks` once the repository is published.

## License

MIT — free, forever.
