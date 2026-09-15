# The build surface: what can be built on Base tokenized stocks

This file answers the developer question the rest of the skill does not: "what can I build here?" The other rubrics judge positions; this one maps the surface a builder stands on. It is organized as three layers — **rails** (the contract-level primitives that already exist and that any build sits on), **integration points** (live venues a build plugs into or extends), and **whitespace** (the dated negatives: primitives that do not exist yet, each named with the rail it would sit on). The map inherits every operating rule from SKILL.md, and two matter most here: date every negative (whitespace flips on a single launch), and name the rail by address, not ticker.

## Layer 1 — Rails: what already exists to build on

### The B20 standard — the dividend and eligibility rail

The B20 token standard carries the dividend mechanism itself, not just plumbing. A builder who treats one B20 token as permanently equal to one share is wrong the day the first dividend lands:

- `multiplier()` — WAD-scaled factor, selector `0x1b3ed722`. Cash dividends convert to shares via a multiplier update, never a cash distribution.
- `scaledBalanceOf(address)` — selector `0x1da24f3e` — raw balance × multiplier; `toScaledBalance` / `toRawBalance` apply the current multiplier to any conversion.
- `MultiplierUpdated` events — the onchain history; `updateUIMultiplier` — scheduled changes with advance onchain notice.
- Policy scopes — allowlist/blocklist transfer control, pausing, seizure, supply caps. This is the eligibility-enforcement layer at the contract, and it is the rail any permissioned build (lending recovery, index gates) must respect.

All tokens in the current B20 registry read multiplier exactly 1.0 as of 2026-09-07 (13 then; re-run the sweep per session — the set and the read are session facts, route `b20-multiplier`) — the mechanism is documented but never exercised. The consequence for builders: any contract that assumes token == share (an index weight, a lending LTV, a strip split) must read the multiplier or it misprices the position the day the pipe fires. The read is one `eth_call` (route: `b20-multiplier`).

### The registry and the custody chain

- Onchain registry `0x3f3E8cf41cdd3b1D118c16471aB0113DfDDd5CaD` — the only name that matters for "is this the real token". Token addresses resolve from the docs.base.org tokenized-stocks registry; the `0xb200…` prefix is cosmetics, not identity (a memecoin already squats it).
- Custody chain: Authorized Participants buy the shares → Alpaca (regulated broker and custodian) → bankruptcy-remote structure supervised by ADGM. Once minted, the token is standard B20 — no whitelisted wallets, no platform lock-in.
- The claim-stack consequence: a build that treats the token as the share (a "stock oracle", a "share-backed" product) is a layer-3 statement about a layer-1 object. The token is a claim against the issuer, not against the company.

### The documentation home

docs.base.org is the canonical source for what Base provides to a builder — the B20 specification, the tokenized-stocks issuance guide, and the registry. The rails facts above are sourced there (manifest rows `b20-standard`, `coinbase-stocks`):

- `https://docs.base.org/specifications/b20/specification-overview` — the B20 standard (multiplier, policy scopes).
- `https://docs.base.org/base-chain/asset-issuance/tokenized-stocks-on-base` — issuance, custody, and eligibility.
- `https://base.org/stocks` — the registry, per-token addresses, and the ADGM prospectus links.

A "what can I build" answer that does not open docs.base.org first is guessing. The ecosystem announcement (blog.base.org/tokenized-stocks) is the tagline surface, not the spec — it names partners, docs.base.org names the contracts.

### The data rails

- **Coinbase B20 Events SQL API** (docs.cdp.coinbase.com/data/sql-api/b20-events) — mints, transfers, policy actions. The candidate source for custody-chain verification and verified-print evidence; auth needs checking per session.
- **Chainlink stock price feeds** — with a documented 96h staleness refusal ("24h would fail every Saturday"). A builder wiring a price feed must handle the two-clock problem: the stock leg quotes the last close on weekends and holidays while the onchain leg trades 24/7.
- **Keyless market data**: GeckoTerminal (token price, pools — routes `token-price`, `meme-stock-pools`), CoinGecko (dShare reference price — route `dshare-price`), Beefy (`stock-yield-vaults`), BaseStonk (`basestonk-launches`), stockanalysis.com (underlying and dividends).

## Layer 2 — Integration points: what is live to plug into

| Venue | What it is | The read a builder must do |
|---|---|---|
| Aerodrome Slipstream stock/USDC pools | Where the stock leg's price actually forms. Which B20 trade live is session-derived — enumerate the registry, then check each token's books (route `token-price`); the 2026-09-08 snapshot read 4 of 13 (NVDAc, GOOGLc, AAPLc, METAc), and the set changed since — never assume it | Pool by both legs' contracts; fee tier; the weekend-gap exposure |
| Beefy auto-compounding vaults | The one live yield layer, on the Aerodrome pools | Vault fee take; quoted APY is trailing, not forward |
| Launchpads — o1, bankr, Flaunch | Named in Base's official B20 announcement | Hook address and permission mask before any fairness claim |
| BaseStonk | Not in the official list; AdvancedLauncherV6 + AdvancedFeeHookV6, AdvancedLauncherB20V6, source-verified; keyless API | Per-launch hook and generation from the API |
| ST0x wrappers (wtCOIN, wtNVDA, …) | 1:1-backed wrapped equities with their own DEX books — a separate claim stack from the registry token | The wrapper's backing and custody, not the native token's |

The load-bearing read at the launchpad layer is hook permissions: who controls the hook controls fees, whether adds/removes can be blocked, and sometimes a settlement take. A launchpad with no documented hook permissions is a hook you are trusting blind.

## Layer 3 — Whitespace: what does not exist yet (the build opportunities)

Each row is a dated negative — re-verified every session, because a single launch flips it.

| Absence (dated) | The rail it would sit on | The consequence for a builder |
|---|---|---|
| No PT/YT strip venue (Pendle verified absent, 2026-09-06) | B20/dShare + the multiplier | The single largest unbuilt primitive; a strip must read the multiplier to split price from dividend correctly |
| No lending market (Morpho/Aave/Euler taglines; no live stock market, 2026-09-07) | B20 policy scopes + a price feed | The hard part is the eligibility-gated recovery path (future-yield-lending.md) |
| No index/basket product (no verified product on Base) | Registry + multiplier + a composition layer | Manual portfolios are analyzable today; the automated product is unbuilt |
| B20 tokens without an onchain market (derive per session via registry + `token-price`; 9 of 13 on 2026-09-08 — the set flips as pools launch) | A DEX pool + a price feed | Liquidity provisioning is itself a build opportunity, not just a gap |
| Dinari's Base dividend pipe is staging (DividendDistribution `0x7978c49C4861e43692702FD74b12B620eE47601e`; production on Plume) | The distribution contract | The Base dividend rail is unexercised — a build that pays out dividends is building on staging |
| No merger endpoint on Dinari (manual triage) | A reconciliation/oracle watch | A disappearing position is the only programmatic signal today |

## The build-read discipline

1. **Verify venue before treating a tagline as live.** base.org/stocks markets dozens of partner integrations; a same-day Morpho check found no live stock market. Announced support is a claim, not a market.
2. **Date every negative; re-verify per session.** Whitespace is the volatile layer of this map. "No strip venue" was true on 2026-09-06 and is a one-launch fact.
3. **Name the rail by address, not ticker** (rule 8). The registry is the only name that matters; the prefix is cosmetics.
4. **Read-only, always.** This file maps the surface; it does not scaffold, deploy, or sign. Recommendations describe what to check, not what to click.
5. **What any build inherits** — the physics no design escapes: the weekend gap (two clocks), the terms-only dividend (multiplier 1.0), eligibility gating (policy scopes), and issuer risk (a claim stack, not a share). A build that ignores one of these is a build that breaks on the first weekend, the first ex-date, or the first policy action.
6. **State the anchor, derive the count** (rule 9). The registry address is stated; the token set, the live-pool set, the vault set are session facts. Any count in this file is a dated snapshot to sanity-check against, never a number to reproduce in an answer.
