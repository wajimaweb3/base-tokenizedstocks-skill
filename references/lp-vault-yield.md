# LP and vault yield on stock pools: what the yield actually is

The only live yield infrastructure above single tokenized stocks on Base (verified 2026-09-07): Aerodrome Slipstream stock/USDC pools with Beefy auto-compounding vaults on top (NVDAc, AAPLc, METAc, GOOGLc pairs). A degen asking "should I LP into the NVDAc pool and farm the vault" is asking about real, deployed contracts — and the answer is a decomposition, because the headline APR hides four different things stacked on top of each other.

## The decomposition: four legs, each dated separately

LP return = fee yield + incentives − impermanent loss − layer costs. No single leg is "the yield":

1. **Fee yield** is flow, not rate: (pool volume × fee tier) ÷ reserves, per day. It scales with attention and dies with it — a launch-week volume figure annualized is not a forward rate, it is a peak reading. Compute it fresh and date it (worked example below).
2. **Incentives**, where present, are dated emissions — someone's budget decision, usually temporary by design. State who pays and until when, or state that none is verified.
3. **Impermanent loss** is the cost leg — and in a stock pair it is not the textbook symmetric thing (next section).
4. **Layer costs**: at the vault layer, the vault's own performance/withdrawal fees; at the pool layer, gas and any concentrated-range management. Each layer takes its cut before the wallet does.

An APR that fuses these legs is not information. Rebuild the four legs from dated onchain numbers before quoting any yield figure.

## The session-clock twist: IL in a stock pair

Both legs of a stock/USDC pool run on different clocks. The USDC leg never sleeps; the stock leg's underlying prints on market sessions and the token depegs on weekends when the share does not trade (concepts.md, the weekend gap). Consequences an ordinary LP analysis misses:

- **Weekend IL is one-sided.** When the stock gaps at Monday's open, the pool is the first arbitrage venue for that gap — the pool's price has been drifting on crypto-side flow for two days against a stock leg whose last confirmed print was Friday's close. The gap damage lands in the pool before the market opens.
- **Concentrated liquidity amplifies both directions.** Slipstream positions earn fees (and incentive multipliers) only in range — and take the weekend gap at full leverage inside the range. A tight range on a stock pair is a bet that the stock does not gap; stocks gap.
- **Volume regime ≠ yield regime.** Fee yield is highest exactly when the pair is moving hardest — which is also when IL is being realized. The two big legs of the decomposition are correlated against the LP.

## What the yield is NOT: no dividend reaches the pool

This is the honesty flag that separates an equity-native read from a screener read: pool fee yield and vault APY are **trading-pair yield** — fees paid by swappers. NVDA's dividend does not flow through the pool to the LP, and the B20 dividend pipe is terms-only (all thirteen multipliers read exactly 1.0 as of the 2026-09-07 sweep; corporate-action.md). Quoting a vault APR as "yield on tokenized NVDA" fuses two different claim layers. And the forward question is genuinely open-tier: when a B20 multiplier update eventually fires, the pool holds raw token balances while redemption value shifts via the multiplier — what that does to pool pricing and LP positions has never been exercised (unknown tier, not terms-only — the interaction is undocumented).

## The vault layer: what auto-compounding adds and costs

Beefy's vaults (earnedToken `mooCowAerodromeBase*`) reinvest fees into the LP position. What that adds: compounding discipline and gas efficiency no individual can match on a Slipstream range. What it costs and adds in risk: the vault's own fee take (read it from the vault listing and date it), an extra contract in the custody chain, and strategist control over the position. The vault's quoted APY is a trailing measurement of what the four legs did — never a forward rate; date it like any other number and rebuild the legs underneath it.

## The meme-pool case: LP as short options

Providing the stock leg in a meme/stock pool (meme-pair-launchpad.md) is a different trade wearing the same vocabulary. The LP is short options on the meme/stock spread: if the meme runs, the pool relentlessly sells it against the stock reserve and the LP ends up holding more meme and less stock exactly as the chart goes vertical; if the meme dies, the stock leg survives but the pool's volume — its fee yield — dies with the meme. The fee carrot is paid in a coin whose behavior is the risk. Combined with the weekend gap on the stock side, both legs can move against the position on different clocks in the same 48 hours.

## Worked example, dated 2026-09-07 (NVDAc/USDC 0.103%, Aerodrome Slipstream)

First-order fee flow from the same day's pull: volume $2.98M/24h across a $2.52M reserve at a 0.103% fee tier ≈ $3.1k/day of fees ≈ 0.12%/day ≈ low-double-digit to ~40%+ annualized *if volume and reserves both held — they will not*. Volume on these books is launch-week inflated (main pool created 2026-08-12); reserves and volume decay together as attention rotates. That annualization is a ceiling reading with a decay assumption attached, and saying so is the difference between a yield quote and a marketing quote. Rebuild from fresh numbers on any reuse.

## Pre-deposit checklist

1. Pool identified by both legs' contracts (stock leg from the registry; route: `meme-stock-pools` enumerates all of a stock token's pools, including its own books) and dated.
2. Fee flow computed from same-day volume × fee tier ÷ reserves — not from a quoted APR.
3. Incentives verified present or absent, with payer and end date.
4. Weekend plan stated: range width vs the stock's gap history; concentrated leverage acknowledged.
5. Vault layer read: fee take, quoted-APY date, what it compounds.
6. The dividend question answered by name: this is pair yield; the multiplier pipe is terms-only, and its first exercise on an LP position is unknown-tier.
7. Exit sized against reserves, not against the APR.

Research, not financial advice — the skill is read-only and constructs no deposit, range, or harvest transaction. Every leg above decays at a different speed; the yield that survives re-pulling the numbers a week later is the only one that was ever real.
