# Foundations: how to think about tokenized stocks

The mental models the agent grounds on before answering any tokenized-stock question. Load once per session. These are the frameworks that stay true when specific issuers, tokens, and prices change.

## 1. A tokenized stock is a claim stack, not a share

The token in the wallet is layer 1. The issuer's contract is layer 2. The custodian's share is layer 3. The rights that pass through — price, some dividend, maybe an adjustment — are layer 4. Users think they own layer 3; they hold layer 1; only layer 4 defines what they actually get. Every ownership question starts by naming which layer the question is about.

## 2. Total return decomposes into three legs

R_total = R_price + R_dividend + strip premium/discount. The first two exist for any tokenized share; the third exists only when the share has been stripped into PT and YT. Never quote a single return number without saying which legs it contains and as of when. A "yield" figure that mixes price move and dividend is not a yield.

## 3. The pass-through hierarchy (from the claim stack, ranked)

Price exposure passes through by construction (arbitrage anchors it). Dividend passes through partially, on a lag, net of fees. Corporate-action adjustment passes through per the contract's terms, and often has no live precedent. Voting almost never passes through. Legal shareholder status almost never passes through. Any claim that a token "is" the stock is a layer-3 statement about a layer-1 object.

## 4. Yield stripping: PT is price, YT is dividend

Stripping splits a tokenized share into two tokens that trade separately: PT (principal token) carries price exposure with no dividend claim; YT (yield token) carries the dividend stream with no principal claim. The onchain analog of PO/IO on bonds, applied to stocks via the Pendle-style PT/YT contract. The identity PT + YT ≈ underlying holds when the strip is priced coherently; the residual is the strip premium or discount.

## 5. The implied forward dividend

The YT price implies a forward dividend: implied = (YT price × periods per year) / underlying price. The number is meaningless in isolation — it must be compared to the ACTUAL announced dividend (from the company calendar or the issuer's dividend feed), dated. The gap between implied and actual is the analytical content of the strip. Compare in dollars per share, not percentages: the YT's denominator is a small fraction of the underlying's, so yields quoted on the YT leg inflate arithmetic without adding information.

## 6. Custody & eligibility as a chain, not a checkbox

The dividend path is company → custodian → issuer → token contract → holder wallet. Each hop is a place where value can leak (fee, withholding, delay) or the chain can break (issuer insolvency, custodian failure). Eligibility (non-US, KYC, accredited) is enforced either at the contract layer (permissioned token, ERC-3643) or only at mint/redeem (permissionless secondary) — the two have very different implications for who can hold and who can transfer.

## 7. Corporate actions are first-class, and evidence has three tiers

Splits, mergers, special dividends, spin-offs — each redefines the underlying's cash flow and requires the token contract to specify what happens. Do not describe outcomes as fact. Classify:

- Verified print — a real event occurred; the issuer's response is documented with an onchain trace and a date.
- Terms-only — the contract promises a mechanism, but no live event has tested it.
- Unknown — no source found; treat as an open risk and name it as such.

The honest default when writing about corporate actions is terms-only or unknown, because most tokenized-stock issuers are young and most tickers have not lived through a hard event yet. The exceptions that prove the tiers: xStocks' reinvesting multiplier carries the class's only verified underlying-level dividend print, and Backed's acquisition by Kraken its only issuer-level one — both dated in corporate-action.md.

Corporate actions also arrive at two layers: on the underlying (split, merger, dividend — the issuer processes the event and passes something through) and on the issuer itself (acquisition, pivot, product-line retirement — no pass-through mechanism exists; the outcome arrives as policy, and the one print in the class is Backed's acquisition by Kraken and pivot to xStocks). The event-by-event menu for both layers lives in corporate-action.md.

## 8. Date every number

Prices, dividends, yields, custody arrangements, eligibility rules — all change. Any number in an answer carries an as-of date, or it is not a number, it is folklore. Data comes from the api-routes at query time; the skill's prose never bakes a price.

## 9. Read-only, always

The skill answers, decomposes, and flags risk. It never signs transactions, moves funds, or executes trades. Recommendations describe what to check, not what to click.

## 10. Analogs: the TradFi Rosetta stone

Tokenized stocks are not new physics — it is TradFi primitives re-plumbed onchain. Reach for the analog before inventing a novel frame:

- Tokenized share ↔ depositary receipt (ADR/GDR): a claim on a share held elsewhere, with pass-through defined by a deposit agreement.
- PT/YT strip ↔ PO/IO strip on mortgage bonds, or coupon stripping on Treasuries.
- Implied forward dividend ↔ dividend futures / dividend swaps in TradFi.
- Issuer of a tokenized stock ↔ the depositary bank in an ADR structure.
- Corporate action pass-through ↔ the depositary's notice-and-adjustment mechanism.
- An issuer acquired or pivoting ↔ the ADR depositary bank being bought: the share is untouched, but the servicing of your claim becomes the acquirer's decision.
- Reinvesting multipliers (xStocks', Base's B20) ↔ an accumulating (ACC) ETF share class; dShares' USD+ payout ↔ the distributing (DIST) share class of the same fund.

The Rosetta stone is not a claim that the onchain version is identical — it is a starting point that makes the differences legible.

## 11. A basket is N claim stacks plus a composition layer

A portfolio of tokenized stocks is not one asset with a weighted price — it is N independent claim stacks plus one composition layer, and until a product automates it, that layer is a spreadsheet. The composition inherits the weakest link of every constituent: the thinnest exit gates the rebalance, the strictest eligibility redlines the holder, the smallest dividend pass-through sets the yield floor. Basket yield is the sum of net pass-throughs per leg, in dollars — never the weighted headline. The worked menu is index-composition.md.

## 12. Lending against a token is lending against its claim stack

Securities-based lending assumes the collateral can be delivered to the lender; a tokenized stock cannot always promise that — transfer is eligibility-gated, so a lender who cannot hold the token holds a broken remedy. Liquidation runs around the clock against a collateral whose price follows market sessions; crediting "future yield" in the LTV is writing insurance on a dividend that can be cut. The menu of what breaks first is future-yield-lending.md.
