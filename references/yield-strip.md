# Yield stripping: separating the price leg from the dividend leg

Use this rubric when a user asks "is this yield strip fairly priced", "what does the YT price imply", "can I separate price from dividend", "why is the implied yield 4% when the real dividend is 0.03%". As of 2026-09-06 no venue offers PT/YT strips of tokenized equities in production (Pendle and peers have not launched an equity market on any chain), so this rubric is forward-looking: the frameworks below describe how to reason about a strip the moment one appears, and how to recognize a mispriced one before others do. The trap to defuse first: the YT is a market forecast of a dividend, not the dividend itself — the number the YT price implies is a bet that only becomes a fact if the announced distribution ratifies it. Answer every strip question by writing down both numbers, dated: what the YT price implies, and what the company has actually announced. The gap between them is the entire analytical content of the trade.

## The strip decomposition (the mechanics in one pass)

Stripping separates a tokenized stock's total return into two tradable claims: the PT (principal token) carries price exposure only, the YT (yield token) carries the dividend stream only — the onchain PO/IO strip, Pendle's PT/YT applied to equity. The identity to check first: PT price + YT price ≈ underlying token price, and the residual is the strip premium/discount, the market's charge for the separation itself. Decompose total return before judging either leg: R_total = R_price + R_dividend + strip premium/discount, each leg dated separately.

## The implied forward dividend (the core valuation move)

The YT price is a forecast: implied forward dividend = (YT price × periods per year) / underlying price, dated. That implied number means nothing in isolation — only against the ACTUAL announced dividend (dated, from the company or issuer calendar). The gap between implied and actual is the entire analytical content of a strip. Compare dollars, not percentages across different denominators: the YT's price is a fraction of the underlying's, so yields quoted on the YT leg explode arithmetic without saying anything new.

## The gap menu (ranked: what actually explains implied ≠ actual, most common first)

1. A special or one-off dividend — the market pricing a distribution the trailing yield does not show. Check the dividend calendar for announced specials before calling anything mispriced.
2. A fee or leak in the pass-through — the issuer or the strip contract takes a cut between the company's payment and the YT holder. The implied number is gross; what reaches the holder is net. Find the net.
3. Illiquidity and stale pricing — thin YT markets print prices that do not clear. Check depth and the age of the last trade before trusting the implied calculation.
4. A genuine expectation of a raise or cut — the market trading ahead of an announcement. This is the only menu entry that is actually a view, so it is the last resort, not the first guess.
5. True mispricing — what remains after 1–4, sized honestly against the spread and the exit.

Questions that separate a priced strip from a hopeful one: which strip contract and term is live today (dated), what annualized dividend actually reaches the YT holder after every fee and lag in the chain, what is that expressed as a yield on the YT's own price (not the underlying's), who has authority to alter the strip's terms mid-term, and which corporate-action events fall inside the current term's window?

## The custody & eligibility chain

Who physically holds the underlying share, and how does the dividend reach the YT holder on the ex-date: company → custodian → issuer → strip contract → YT holder, each hop dated and fee-marked. Then the strip-specific question: what happens at term end — does the YT expire worthless after the final ex-date, roll into a new term, or redeem? And who is eligible to hold either leg at all (non-US, KYC)?

## Corporate actions: the asymmetry that defines the trade

A corporate action does not hit both legs equally, and that asymmetry is the analytical point: a split re-denominates the PT's price leg mechanically, while the YT's claim is on dividend dollars whose per-share path the contract must define; a cash merger can collapse the future dividend stream the YT was pricing while redeeming the PT near deal value; a dividend cut is the YT's tail risk and a raise is the PT holder's subsidy. Do not assert any adjustment path as fact — read it from the strip's terms, and classify the evidence (verified print / terms-only / unknown) as in the claim stack. When the path is terms-only or unknown, name it as the open risk it is.
