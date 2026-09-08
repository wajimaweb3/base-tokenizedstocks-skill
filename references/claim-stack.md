# Claim stack: what a tokenized stock actually gives you

Use this rubric when a user asks "is dNVDA the same as owning NVDA", "does bNVDA still pay the dividend now that Backed stopped issuing", "do I actually get the dividend", "can I vote", "what happens if the stock splits or gets acquired". The trap to defuse first: a tokenized stock is a contractual claim against an issuer, not shareholding — the word "ownership" hides three layers between the wallet balance and the underlying share, and users assume rights that never leave the middle. Answer every ownership question by walking those layers in order and marking which rights actually reach the holder; the gap between the assumption and the pass-through is where the answer lives.

## The claim stack (read top to bottom before judging anything)

1. The token — the balance in your wallet (ERC-20, or ERC-3643 if permissioned). This is the only thing you actually hold.
2. The issuer claim — what the token gives you against the issuer (Dinari for active dShares; Coinbase for B20 stocks — NVDAc and peers, 1:1, ex-US; Backed's bTokens — a line retired when the issuer, acquired by Kraken, pivoted all-in to xStocks, with redemption left open; and others as they emerge). A contractual claim, not a shareholder claim. Issuer status itself matters: a token from an issuer that has stopped new issuance is still tradable, but the redemption path and future support are on a different clock than an actively-issued one.
3. The underlying — the real share the issuer (or its custodian) holds in the traditional market.
4. The pass-through — the subset of underlying rights that actually flow from layer 3 to layer 1.

You hold layer 1, you think you own layer 3, and the truth is somewhere in layer 4. Everything below is about measuring that gap precisely.

## The pass-through menu (ranked, strongest → weakest)

1. Price exposure — the token tracks the underlying's price. Strongest because it needs no active pass-through: mint/redeem arbitrage and the issuer's peg keep it anchored. Still ask what the anchor is (1:1 to the share, or a basket, or a stale oracle) and what the peg breaks against.
2. Dividend — partial and conditional. The issuer receives the dividend as registered holder, then may pass it through after fees and lag. The mechanism varies by product, even on one chain: dShares pay cash (USD+, with a distribution floor); Coinbase's B20 stocks reinvest through an onchain multiplier — Base-native but never yet exercised, all thirteen tokens reading 1.0 on 2026-09-07; xStocks — Backed's active line — reinvest the same way (net of withholding tax) and carry the one dividend pipe with a verified onchain print to date (`corporate-action.md`). Ask: does the dividend reach the token at all, through which mechanism, what fraction survives fees, and on what lag (dated).
3. Corporate-action adjustment — splits usually adjust (rebased balance, or a changed conversion rate); mergers and special dividends are messier. Ask what the terms promise, and whether any real event has tested it.
4. Voting — almost never passes through. You are not a shareholder of record; the custodian or issuer holds the vote.
5. Legal shareholder status — almost never. Your claim runs against the issuer, not the company. If the issuer fails, you are a creditor of the issuer — not an owner of the share, and not a creditor of the company.

Questions that separate a real claim from a promised one: which layer is the user actually holding today (dated), which rights does the issuer's contract enumerate as pass-through, which of those have been EXERCISED against a live event versus only written down, and what remains of the claim if the issuer — not the underlying company — becomes insolvent?

## The custody & eligibility chain

Who physically holds the underlying share? Trace the dividend path company → custodian → issuer → token contract → your wallet, and mark every hop where value can leak (fee, delay, withholding) or where the chain can break (issuer insolvency, custodian failure). Then map eligibility: who is allowed to hold the token at all (non-US, accredited, KYC), and does the token itself enforce that onchain or is it enforced only at mint/redeem?

## Corporate actions: a first-class risk, not a footnote

A split is the easy case (even it has a window where 1 token ≠ 1 new share while the adjustment propagates). A merger of the underlying is the hard case: the underlying is exchanged for cash or another stock, and your token's claim must be redefined. An acquisition of the issuer itself is a different layer entirely — no pass-through mechanism, only policy. For each case, classify the state of evidence rather than guessing:

- Verified print — a real event happened and the issuer's response is documented (dated, with an onchain trace).
- Terms-only — the contract promises a mechanism, but no live precedent has exercised it.
- Unknown — no source found; treat it as an open risk, and say so.

When the evidence is terms-only or unknown, do not describe the outcome as fact. The honest answer names what the document promises and flags that it has not been tested by a real event. The event-by-event menu — both layers, the dividend plumbing in full, and the class's one issuer-level print (Backed→Kraken) — is worked in `corporate-action.md`.
