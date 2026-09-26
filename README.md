# base-tokenizedstocks

[![skills.sh](https://skills.sh/b/wajimaweb3/base-tokenizedstocks-skill)](https://skills.sh/wajimaweb3/base-tokenizedstocks-skill)

A skill pack that makes an AI agent fluent in **tokenized stocks on Base** — real shares issued onchain by live issuers (Dinari dShares, Coinbase B20 stocks) and the primitives being built on top of them. Drop it into any agent (Claude Code, ChatGPT/Codex, Grok, Cursor) and the agent stops answering tokenized-stock questions with generic finance boilerplate and answers them like a tokenized-stock analyst would: claims before tickers, decomposition before verdicts.

## Install

Manual (works now): clone or copy this folder into your agent's skills directory — for Claude Code, `.claude/skills/` in a project, or `~/.claude/skills/` globally. The skill activates on the triggers in `SKILL.md`.

Skills CLI: `npx skills add wajimaweb3/base-tokenizedstocks-skill` — the CLI detects your agent (Claude Code, Cursor, Codex, Windsurf, Gemini, and more) and installs into its skills directory. Run `npx skills update` to pull future versions.

## What it does

A general AI gets tokenized stocks wrong in predictable ways: it says a tokenized stock "is" the share, quotes returns without naming which legs they contain, and asserts corporate-action outcomes no live event has tested. base-tokenizedstocks fixes that with ten frameworks:

- **The claim stack** — every tokenized stock is four layers (token → issuer claim → underlying → pass-through rights). Ownership questions are answered by walking the layers, not trusting the ticker.
- **The gap menu** — for yield strips, the analytical content is the gap between the implied forward dividend and the announced one, explained in ranked order (special dividend → fee leak → stale pricing → market view → true mispricing).
- **Evidence tiers** — every corporate-action claim is tagged verified print, terms-only, or unknown, read at two layers: on the underlying, and on the issuer itself.
- **The composition read** — an onchain basket is N claim stacks plus a composition layer: weakest-link screens, weight drift, dollar-accurate dividend composition, rebalance cost, eligibility intersection.
- **The lending read** — what breaks first when the collateral is a claim stack: eligibility-gated recovery, liquidation that never sleeps against a market-session clock, dividends landing mid-term, an LTV that underwrites the dividend itself.
- **The meme/launchpad read** — memecoins paired with real stocks: verify the stock leg against the registry (never the name — one memecoin squats the B20 vanity prefix), read hook permissions, size amplification from onchain reserves.
- **The LP/vault yield read** — the one live yield layer (Aerodrome pools, Beefy auto-compounding vaults) judged as four dated legs, with the honesty flag that it is trading-pair yield, never dividend pass-through.
- **The onchain basis read** — the gap between a token's onchain price and the underlying's last print is the price of claim-stack friction read across two clocks (the onchain leg trades 24/7, the stock leg quotes the last close); never call a session-stale basis a mispricing.
- **The cross-issuer comparison read** — one underlying, N claim stacks (three for NVDA). Compare per claim layer, never rank; the verdict is the weakest link per holder goal.
- **The build-surface read** — for developers: the rails that exist, the integration points that are live, and the whitespace — the dated negatives (no strip venue, no lending market, no index product).

It serves, in order: people new to tokenized stocks, analysts, traders hunting mispricings — and only last, developers building on the rails.

## How it works

Two layers, loaded on demand:

- **Task layer** (`references/how-work.md`) — shapes the answer for the job: understand, valuate, screen, track, build.
- **Domain layer** (`references/concepts.md` plus ten rubrics) — the frameworks themselves.

Per question, the agent runs a four-step routine: classify the task and domain, ground on foundations, pull live state through `api-routes.json` (keyless first, every number dated), then answer with the decomposition visible. `manifest.json` is the address book of verified issuer documentation. The worked shape of a full answer is in `examples/assessment-example.md`.

Read-only, always: the skill analyzes and flags risk; it never constructs or signs a transaction.

## Evals

`evals/evals.json` holds the test suite: 24 cases spanning all five task modes and every rubric. Each case runs twice — once with the skill loaded, once without — and both outputs are graded against the same structural assertions: a dated check, a named evidence tier, never frozen values, because the skill's load-bearing facts are dated negatives (no strip venue, an unexercised dividend pipe) that a single event will flip. New capabilities gate on a new case before they land.

## Honest scope (as of 2026-09-07)

- **Two issuers live on Base**: Dinari dShares (714 assets) and Coinbase's B20 stocks (13 tokens, 1:1 against shares in regulated custody, ex-US only, mint/redeem restricted to KYC'd Authorized Participants). Backed bTokens are a retired line, not a dead issuer: Backed was acquired by Kraken (Dec 2025) and pivoted all-in to xStocks (Mar 2026, Solana — off-Base).
- **No PT/YT strip venue exists yet, on any chain.** The yield-strip rubric is the method for pricing strips the moment one launches; treat any "strip price" an agent quotes today as fabricated.
- **No index product is verified on Base**, but the single-token yield layer is live (Aerodrome pools, Beefy vaults — LP yield, not dividend pass-through). The class's first live onchain stock index sits off-Base as evidence (Hood Index hMAG7); the announced S&P Digital Markets 50 is not live.
- **No lending or margin market is verified** — base.org's partner page markets lending taglines; a 2026-09-07 Morpho check found no live tokenized-stock market.

Off-Base names appear only as evidence about the class, never as venues. Market data comes from free public endpoints (Yahoo Finance, stockanalysis.com, GeckoTerminal); every figure in this pack is a teaching prop until re-pulled live.

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
│   ├── build-surface.md          # what can be built on Base: rails, integration points, whitespace
│   └── how-work.md               # understand / valuate / screen / track / build
├── examples/
│   └── assessment-example.md     # the output shape, worked on dNVDA
└── evals/
    └── evals.json                # 24 paired-run cases: assertions on structure, not values
```

## License

MIT — free, forever.