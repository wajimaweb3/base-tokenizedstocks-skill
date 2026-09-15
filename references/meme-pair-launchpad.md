# Meme pairs and launchpads: the stock-adjacent launch layer

A live, Base-native genre since the B20 launch week: memecoins that launch in pools paired with a real tokenized stock, typically on a launchpad, then graduate to their own stablecoin pools. Enumerated 2026-09-07 by querying pools for each registered B20 token address (re-enumerate per session — the pool set moves with every launch): roughly thirty meme pools across NVDAc (~12), SPCXc (~11), and AAPLc (~14), volumes running from ~$800k/day down to triple digits. This file is the read rubric for that layer: how a launch is structured, how to verify the legs, how to size the amplification, and what makes this genre different from an ordinary memecoin.

## The three layers of a launch

Every "launched on a launchpad" pool is three things stacked, and each layer has its own controller:

1. **The venue** — the AMM where the pool actually lives: Uniswap v3/v4 or Aerodrome Slipstream. The venue's contracts execute; they are the best-audited layer in the stack.
2. **The factory/launchpad** — o1-launchpad dominates this genre on Base, bankr secondary. Both are named as supporting trading venues in Base's official B20 ecosystem announcement (2026-08-24): the dex id `o1-launchpad` in pool data is **o1 Exchange** (o1.exchange, docs.o1.exchange), bankr is bankr.bot, and Flaunch (flaunch.gg) is the third launchpad named there — homepages and docs verified 2026-09-07 (manifest row base-launchpads). A fourth, **BaseStonk** (basestonk.io, docs.basestonk.io), is *not* in the official announcement — found later by a user (2026-09-07), proof the official list is non-exhaustive — and breaks the genre's default lifecycle: every launch is a live Uniswap v4 pool from block one, no bonding curve, no graduation, no migration, the launcher must end holding nothing, and no admin key sits over any pool. A fifth, **vvveity** (stock.vvveity.com, docs at stock.vvveity.com/docs), surfaced in a 2026-09-08 claude.ai test run via web search — it markets itself specifically as a stock-paired launchpad and is not in the official announcement either; no registry-address enumeration on it has landed yet, so treat its claims as unverified until a pool-level read confirms a name and a contract. The launchpad deploys the initial pool, usually as a Uniswap v4-style pool with its own hook, controls initial liquidity parameters, and often holds dev/creator allocations. Who controls the hook controls fees, whether adds/removes can be blocked, and sometimes a settlement take.
3. **The storefront** — the social or agent surface where the token is pitched (an X account, a chat bot, a launch page). Marketing, not infrastructure.

The load-bearing question at the factory layer is hook permissions: read (or demand) the pool's hook address and its permission mask before believing any claim about who can LP, whether liquidity can be locked, or what the fee can become. On o1 pools this is a v4-style pool id (64 hex); the permission read is not optional homework — it is the difference between a fair launch and a rug with branding.

## Verify the stock leg against the registry, never the name

The single best property of this genre on Base: the stock leg can be verified by construction. Enumerate pools **by token address** — every pool listed under the registry address of NVDAc (`0xb200…8108C`) necessarily pairs the real Coinbase token. The `meme-stock-pools` route does exactly this. Name-based search does not:

- Display names drift: the genuine AAPLc often renders as plain "AAPL" in screeners, indistinguishable by eye from anything else calling itself AAPL.
- Name search returns cross-chain noise: "AAPLCAT/AAPL" pairs exist on Robinhood Chain (where the AAPL leg is Robinhood's own tokenized Apple — a real third-issuer product, off-Base evidence) and on BSC ("AAPLB", a Backed bAAPL-style leg). None of those are Base venues.
- The vanity-squat print (verified 2026-09-07): the BLUECHIP memecoin grinds the address `0xb200000000000000000000cfbdf64a8706a94a01` — squatting the `0xb200…` prefix shared by every genuine registry-verified B20 token (the count derives from the registry per session). Anything pattern-matching "starts with 0xb200 = Coinbase" misreads a memecoin as an official contract. The registry list is the only name that matters; the prefix is cosmetics.

## The wrapper surface: wt-prefixed stock legs

Registry enumeration has a verified blind spot (found in the 2026-09-07 degen dogfood, costing the skill a question): a second surface pairs memes against **wrapped** stock tokens — the ST0x family on Base, a set of 1:1-backed equities and ETFs with their own DEX liquidity (examples as of the 2026-09-07 enumeration: wtCOIN, wtNVDA, wtMSTR, wtSPCX, plus wtSGOV/wtSKHY/wtSPYM/wtDRAM/wtQQQM/wtIAU/wtCEG — the family set is a session fact, re-enumerate per session as in the enumeration note below). On the exact day the registry token COINc showed zero pools of any kind, meme pairs against wtCOIN were trading a quarter-million dollars a day (BALD/wtCOIN). Both facts were true; either answer alone was wrong.

So a "paired with COIN" (or NVDA, or SPY) question must first ask *which* token: the native B20 registry token, or a wrapped variant. A wt-leg is neither fake nor the registry token — it is a **separate claim stack**: a wrapper issuer's 1:1-backed claim with its own custody chain and its own unknown-tier corporate-action behavior (what a B20 multiplier update does at the wrapper layer is undocumented until exercised). Walk the wrapper's stack before treating it as the share, and cover both surfaces when enumerating: registry-address enumeration for native legs, wrapped-symbol search or the launchpad's own API (route: `basestonk-launches`) for wrapped ones. BaseStonk's docs (manifest row basestonk-launchpad) are currently the cleanest map of which surface a launchpad actually uses — including their note that most B20 tokens had no on-chain market at the time (2026-09-08; the count is session-derived now, route `token-price`), which is *why* the wrapper family exists.

Also from the same dogfood: pool-count censuses through the dex endpoint do paginate with an explicit `?page=` even when the response's next-link is null — trust page walking over the link field.

## Amplification arithmetic: reserves, not the FDV sticker

A screener FDV is a price times a full supply, and most of that supply is not in the pool. Worse, on this genre the field is not even stable: BLUECHIP's pool FDV read ~$16.7M on the morning of 2026-09-07 and ~$2.97M hours later, while every meme pool in the NVDAc list reported a near-identical FDV tracking the stock side — the FDV field is unusable for the meme leg. The reliable depth number is the pool's reserve in USD (verified populated on o1 hook pools 2026-09-07; an earlier "null reserves" reading was a wrong-key error — the attribute is `reserve_in_usd`, not `reserve_usd`): BLUECHIP carried ~$509k of committed reserves against that $16.7M sticker, a ~33x gap between advertised cap and exit liquidity. That gap is where launch-day "market cap" goes to zero without a single sell. Compute any size impact from the reserves (onchain reads remain the gold standard); treat the FDV as advertising.

## Screening the genre: ranking what is "trending"

The question this genre actually gets asked — "which memes paired with NVDA are trending right now" — is a screen, and the naive answer (sort by 24h volume) is wrong in three separate ways. The route returns the full pool list for a registered stock token in one call; what makes the ranking honest is what happens to that list (all field names below verified in a live 2026-09-07 pull):

1. **Split the two families first.** Pools whose other leg is USDC or WETH are the stock's own books — the depth anchor where the stock leg's price actually forms — never candidates. The meme pairs are everything else. A "trending memes" table that leaves the stock's own ~$3M/day USDC book mixed into the ranking is comparing different assets.
2. **Trending decomposes into four fields, not one.**
   - *Momentum*: 24h volume as the primary sort, with the 6h share as the acceleration check — a uniform day puts ~25% of volume in the last quarter of it; a pool under ~10% is fading whatever its headline says (2026-09-07 NVDAc read: one $68k/day pool at 0.2% six-hour share — flatline), and a pool far above it is where the day's attention actually is.
   - *Flow skew*: buys vs sells (the `transactions` attribute). A young pool with near-all-buys is a launchpad lobby, not a market; a two-sided book with sells winning (BLUECHIP 672 buys / 916 sells, 2026-09-07) is distribution in progress.
   - *Depth*: reserve, never the FDV sticker (see the amplification section — the field swings multiples within a day and mirrors the stock side across all meme pools). Size any interest against reserves before ranking it anywhere.
   - *Age and stage*: pool creation date against the swarm window (≤72h from the stock's listing), and the graduation check — a meme that has opened its own USDC or WETH pool has moved its main book, and the stock-paired pool being ranked may be the abandoned one.
3. **Read meme prints against the stock's own print.** On the 2026-09-07 pull every NVDAc meme pair was down 5–8% on the day while the stock's main USDC book moved 0.08% — genre bleed, not an NVDA repricing. A screen that reports meme price action without the stock leg's own move misattributes the move.
4. **The screen surfaces; the checklist judges.** Rank the table, date it, then run the top rows through the pre-touch checklist below. A screen answers where attention is, never whether the pool is buyable — and "trending" is a statement about the past 24 hours, not the next one.

## The claim-stack twist

This is the part an ordinary memecoin analysis misses: a meme/stock pair embeds a stock claim stack inside a memecoin trade. The meme leg runs on a minutes clock; the stock leg runs on market sessions, depegs on weekends when its underlying does not print, carries an issuer whose dividend pipe is terms-only (all B20 multipliers 1.0 as of the 2026-09-07 sweep), and can be halted by issuer policy. The LP in a meme/stock pool is short options on the pair spread of *those two specific legs* — not "a memecoin with extra steps" but a position whose safe asset is only relatively safe. Weekend gap is the amplifier: the meme leg trades Saturday night against a stock leg whose last confirmed print was Friday's close.

## The lifecycle and the swarm

Two dated patterns from the 2026-09-07 enumeration:

- **Launch → graduate.** A meme launches on the launchpad paired with the stock token, then within days opens its own USDC/WETH pools: BLUECHIP launched on o1 against NVDAc on 2026-08-20, had its own Uniswap v4 USDC pool by 2026-08-23, and an Aerodrome pool by 2026-08-26. Graduation means the stock-paired pool is no longer the meme's main book — depth, and therefore your exit, moves.
- **New-listing swarm.** When a new B20 stock lists, themed memes swarm within days: SPCXc's main pool was created 2026-09-03 and by 2026-09-07 it already carried ~10 meme pairs (MOONBASE at ~$642k/day leading, then CumRocket, MARSCOIN, HolyCow, DOGE-1 and peers). The B20 listing calendar is effectively the launchpad's content calendar — a monitorable pattern, and also a warning that pools born in a swarm are competing for the same attention and die on the same schedule. Most launch pools in this genre are under two weeks old; treat age as a first-class field.

## The pre-touch checklist

Before any position in this layer, in order:

1. Stock leg verified by registry address (route: `meme-stock-pools`), not by name or prefix.
2. Pool's dex and creation date read; age and venue named.
3. Hook permissions read or demanded — who can change fees, block liquidity, or take at settlement.
4. Reserves read onchain; amplification computed from reserves; FDV labeled as sticker only.
5. The stock token's own depth located (its USDC pool on Aerodrome Slipstream) — that book, not the meme pool, is where the stock leg's price actually forms.
6. Weekend exposure stated if holding past Friday's close.

This is research, not financial advice; the skill is read-only and constructs no transaction. The genre's base rate — launch pools under two weeks old, thin reserves, hook powers unaudited — is itself the headline risk, and no framing here turns a meme pair into an investment thesis.
