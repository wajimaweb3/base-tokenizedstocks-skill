# The onchain basis: what the gap between token price and share price means

A tokenized stock trades on two clocks at once. The onchain leg prints continuously — a B20 token on an Aerodrome or Uniswap v4 pool ticks every block. The equity leg prints on sessions, and on weekends and market holidays it quotes the last close until the next open. The **basis** is the percentage gap between those two prices at one instant, read across both clocks. It is not an error term and not a verdict; it is the live price the market charges for everything that sits between the wallet and the share — the claim-stack friction (see `claim-stack.md`).

## Date both legs with their own timestamps

The single rule that makes a basis read honest: stamp each leg with its **own** clock, and name the session state of the equity leg (open / pre-open / closed-holiday / closed-weekend). A basis quoted as "+0.7%" without saying the onchain leg is Tuesday pre-market and the equity leg is Friday's close is folklore. The two-clock problem is real enough that production venues design around it: Chainlink's equity feeds refuse beyond 96 hours of staleness because, in the feed's own words, "24h would fail every Saturday" (docs.basestonk.io/stock-pairs.md, 2026-09-08) — a venue admitting the basis is unmeasurable against a stale anchor.

## The four entries that explain a basis, ranked

Read a basis the way `yield-strip.md` reads a strip gap: rank the entries, do not pick one. Most live bases are explained by the first three; the fourth is where the wrapper surface lives.

1. **Session gap.** Between Friday's equity close and Tuesday's open the onchain leg is the only leg that moves. Any basis read in that window is flow-only information about the onchain book, repricing against a frozen anchor — not information about the share. The 2026-09-08 set below is exactly this case: Monday was Labor Day, the equity leg stamped 2026-09-04T20:00Z, and the onchain leg had been the only market for four days. Never call a session-gap basis a mispricing.
2. **Depth and float.** The onchain float is a rounding error against the share float: 13,731 NVDAc against ~24.4 billion NVDA shares; 280 wtNVDA against the same. A basis wide enough to matter at your size has to be read against the onchain book's reserves, not the share's market cap — compute size impact from `reserve_in_usd` (the method is in `meme-pair-launchpad.md` §3). The 2026-09-08 set shows the onchain leg converging to the stale anchor when flow is balanced: AAPLc and METAc drifted from −0.08% and −0.49% (first pull) to +0.01% and +0.04% (second pull, same morning) against an unchanged Friday print — the onchain book doing the adjusting, the equity leg frozen.
3. **Arb-access asymmetry.** The peg has no retail restoration path. B20 mint and redeem are AP-only (Coinbase); dShare pricing routes through Dinari's KYC order sessions. Whoever could cross the basis is gated, so a basis can persist structurally — the premium or discount is the priced cost of that gate. Cross-check the mint/redeem access row in `issuer-comparison.md` before calling any basis an arbitrage.
4. **Stacked legs.** A wrapped token carries its own basis against its native counterpart, on a book that is often orders of magnitude thinner. wtNVDA traded $231.43 against NVDAc's $232.01 on 2026-09-08 — a −0.25% spread to the native token, on $14k of total reserve where the native book holds $1.58M. Wrapper basis = wrapper friction + native basis; the wrapper's claim stack is walked in `claim-stack.md`'s wrapper section, and its corporate-action tier is unknown (see `issuer-comparison.md`). There is even a live market whose entire subject is that spread: the NVDAc/wtNVDA 0.05% pool on hydrex-integral (created 2026-08-26, $4.1k reserve, $3.0k vol24 on 2026-09-08) — reading its reserves tells you how much capital is actually committed to the peg.

## Worked set — 2026-09-08 (Tuesday pre-market, equity leg = Friday close)

| Token | Price (onchain) | Underlying | Basis | Reserve | Float | Vol24 |
|---|---|---|---|---|---|---|
| NVDAc `0xb200…8108C` | $232.01 | NVDA $230.36 (Fri 2026-09-04 20:00Z) | +0.71% | $1.58M | 13,731 | $6.79M |
| AAPLc `0xb200…cd1fb` | $320.00 | AAPL $319.97 (Fri) | +0.01% | $963k | 6,194 | $5.16M |
| METAc `0xb200…7C` | $617.04 | META $616.77 (Fri) | +0.04% | $667k | 2,229 | $2.56M |
| GOOGLc `0xb200…f58B7` | $340.21 | GOOGL $338.46 (Fri) | +0.52% | $1.18M | 6,114 | $4.49M |
| wtNVDA `0xfb5b…8d6e7` | $231.43 | NVDA $230.36 (Fri) | +0.47% / −0.25% vs NVDAc | $14.0k | 280 | $6.6k |

All onchain legs stamped 2026-09-08 via the GeckoTerminal token endpoint (`price_usd`, `total_reserve_in_usd`, `normalized_total_supply`); relationships live under `top_pools`, not `pools`. Underlying legs via Yahoo v8 chart, `meta.regularMarketPrice` / `regularMarketTime`. AAPLc's display symbol on GeckoTerminal is "AAPL" — verify the token by address, never by symbol.

## Which book is the token price quoting?

A token endpoint's `price_usd` is a blend across the token's books, and the books themselves disagree. NVDAc read ~1.1% of dispersion across its own USDC/WETH books in one instant on 2026-09-08 (USDC 0.103% at ~$231.06 on $2.52M of reserve, WETH 0.017% at ~$232.01, USDC 0.99% at ~$228.97) and ~7% once a thin stale book was included (a $21k KAI pool quoting ~$215). Two disciplines follow: quote the book you would actually trade, sized against that book's reserve — not the blended token price; and treat a far-off thin-book quote as stale or one-sided flow, never as the token "really" trading there. Intra-token dispersion is also the cheapest available sanity check on any screener number: if the deep books cluster and one outlier does not, the outlier is the artifact.

## What the basis is not

It is not the strip premium: that is a different leg of `R_total` (see `concepts.md`), and no PT/YT venue exists on any chain as of 2026-09-08. It is not a dividend signal: basis moves on flow, dividends are a corporate-action evidence question (`corporate-action.md`). And it is not, by itself, mispricing — entries 1 through 3 explain most live reads before any genuine dislocation needs to be invoked.

## Track-mode line

For a held position, the basis is a watch line: the token-vs-underlying spread and, when a wrapper is involved, the wrapper-vs-native spread. Drift in either across checks is a first-class event — name the entry that moved (session reopened, depth thinned, flow skewed), not just the number.
