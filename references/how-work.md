# Task modes: understand, valuate, screen, track, build

Five modes cover every job a user brings to this skill. The domain rubrics (claim-stack, yield-strip, corporate-action, and the ones that follow) say WHAT to think about; this file says HOW to shape the answer for the job the user is actually doing. Every mode inherits the operating rules from SKILL.md (dated numbers, decomposed total return, claim-stack reading, evidence tiers, read-only).

Content style (threads, tables, one-pagers) is a delivery layer that rides on top of these modes, not a mode of its own. When a user asks for a "thread on this strip" or a "comparison table of issuers", pick the underlying mode (usually valuate or screen), do the work, then render in the requested format under the content rules below.

## Understand: explaining the primitive

For questions like "what is yield stripping", "how does an onchain dividend work", "what does bNVDA actually give me", "how would borrowing against tokenized stocks even work". The user is not asking for a position — they are asking for the mental model. The failure mode is jargon-first prose that leaves the user more confused; the fix is TradFi anchors that already live in their head.

Shape of the answer:

1. One-sentence definition, plain, no jargon.
2. The TradFi anchor from `references/concepts.md` §10 (tokenized share ↔ ADR/GDR; PT/YT ↔ PO/IO strip; implied forward dividend ↔ dividend swaps), plus one line on what the anchor hides — the onchain version is never identical.
3. One live example with numbers pulled fresh this session and dated. A worked case teaches more than a definition.
4. The top risk in one sentence, named as a first-class thing (not a footnote).
5. Two questions the user should be able to answer after reading — the test that they actually got it.

Depth is layered on request, not front-loaded. A normie who asked "what is a strip" does not need the corporate-action asymmetry paragraph unless they ask.

## Valuate: assessing one strip, position, or claim

For questions like "is bNVDA-YT fairly priced", "should I hold this strip through earnings", "what am I actually owed by this token", "should I borrow against my dNVDA instead of selling". The user has a specific instrument in mind and wants a judgment, not an education. The failure mode is giving a number without the decomposition that makes it meaningful.

Shape of the answer:

1. Identify the asset in one line: what it is, who issues it, what claim layer it sits in.
2. Walk the claim stack (from `claim-stack.md`): which rights pass through to this specific token, dated.
3. Decompose total return: R_price + R_dividend + strip premium/discount, each leg dated. For a spot token (not a strip), the gap leg is the onchain basis against the underlying — compute it (token-price vs underlying-price, each leg stamped with its own timestamp and the stock leg's session state named) and walk the four-entry menu in `references/onchain-basis.md` before calling the gap a mispricing.
4. If a strip, run the gap menu (from `yield-strip.md`): implied vs actual dividend, and which of the five entries explains the gap.
5. Trace the custody and eligibility chain: who holds the underlying, how the dividend reaches the wallet, who is allowed to hold this at all.
6. Classify any corporate-action assumption into the three evidence tiers, at both layers — underlying-level and issuer-level (`corporate-action.md`).
7. Verdict in one paragraph, with the conditions it depends on (size, horizon, exit) and the invalidation triggers that would flip it.
8. Close with the follow-up questions the user should carry into their next check.

Every assessment carries a one-line disclaimer that this is research, not financial advice, and that tokenized stocks carry tails the traditional share does not (issuer failure, contract risk, corporate-action ambiguity, eligibility revocation).

## Screen: scanning the universe for gaps

For questions like "which YT has the biggest implied-vs-actual dividend gap", "compare all NVDA strips across issuers", "which tokenized stocks pass dividends through cleanly", "which dShares could form a dividend basket", and the cross-issuer comparison ("dNVDA vs NVDAc — what am I actually holding", "which NVDA token should I look at", "compare the issuers for one underlying"). The user is not asking about one instrument — they are asking the skill to sort a universe. The failure mode is a table of numbers without the honesty about which numbers are noise (thin liquidity, stale prints, unverified terms). For the cross-issuer case, the row set and the weakest-link verdict frame live in `references/issuer-comparison.md` — the comparison is per claim layer, never a single ranking.

Shape of the answer:

1. State the universe explicitly: which issuers, which tickers, which venues, dated. A screen that hides its universe is not a screen.
2. State the ranking metric explicitly and its formula. If it is implied forward dividend, show the calculation; if it is a fee-adjusted yield, show the fee source. Metrics without formulas are marketing.
3. Rank, but flag the noise: mark any row whose YT print is stale (age of last trade), whose depth is thin (visible size vs typical trade), or whose corporate-action path is unverified (terms-only or unknown). A screen that does not flag noise recommends noise.
4. Pull the top two or three candidates into a mini-valuate — the screen surfaces, the valuate judges. Never recommend from screen output alone.
5. State what the screen missed: which strips it could not price (no data), which issuers were excluded and why. Absent-from-list is information.

Every screen output states the survivorship problem: strips that failed, delisted, or halted are absent from live data; recency bias is structural.

## Track: monitoring an existing position for events

For questions like "the dividend just changed — how does that hit my strip", "there is a corporate action coming, alert me", "why did the implied yield spike this week". The user already holds something and wants to know what changed. The failure mode is a wall of unchanged data; the fix is a diff, not a snapshot.

The recurring event surface for a tokenized-stock position (for a multi-token portfolio it scales linearly in the number of constituents — the tracking burden is part of a composition's cost; see `index-composition.md`):

1. Dividend calendar: announced amount, ex-date, pay-date; any change vs the last reading is a first-class event. For reinvesting tokens (xStocks), the arrival check is the multiplier activation log (multiplier-history route): a new entry dated ex-date+1 is the dividend landing onchain, and no entry after an ex-date that has already passed is itself a finding. For dShares on Base there is no activation log — the arrival check is the wallet itself: USD+ credited (or wrapped dShares added) after the pay-date, verified as a distribution transaction on Basescan, and its absence past the documented lag is a first-class finding. For Coinbase's B20 stocks the arrival check is the multiplier itself: one eth_call (multiplier(), WAD-scaled — anything above 1e18 is the dividend compounding in; the b20-multiplier route); all thirteen live tokens read exactly 1.0 as of 2026-09-07, so no B20 dividend has landed yet.
2. Corporate actions: splits, mergers, spin-offs, special dividends, tender offers — pull from the underlying's filings, then cross-check against the issuer's response (or absence of one). The event menu and its evidence tiers live in `corporate-action.md`. Issuer-side detection gap worth knowing: Dinari documents no merger endpoint — a disappearing position is the programmatic signal, so reconcile positions and cash together.
3. Strip metrics (if a strip is held): implied forward dividend vs actual; strip premium/discount vs the last reading; term-end approach and roll/expiry mechanics.
4. Custody and issuer state: any issuer announcement affecting redemption, fees, eligibility, or the underlying custody arrangement — including ownership changes at the issuer itself (acquisition, pivot, product-line retirement), the layer with no pass-through mechanism at all.
5. Contract or terms diffs: token contract upgrades, issuer Terms & Conditions changes — an amended redemption clause days before a gate is a documented pattern in adjacent markets and deserves the same watch here.
6. Eligibility changes: jurisdictions added or removed from allowed-holder lists, KYC requirements tightening.
7. Token-vs-underlying basis (if a spot token is held): the onchain basis against the underlying, and for a wrapper the wrapper-vs-native spread. Drift in either across checks is a first-class event — name the entry that moved (session reopened, depth thinned, flow skewed), not just the number. See `references/onchain-basis.md`.

Shape of the answer:

1. State the position in one line, dated as of last check.
2. List the events since the last check, most impactful first. No change on a line is a valid answer — say "unchanged" rather than repeating the value silently.
3. For each event, name the mechanism: how it hits the specific claim the user holds (PT? YT? spot token?), not the abstract "the market".
4. Recommend one action per event or none: watch, size down, exit, do nothing. Action without a mechanism is a hunch.
5. Restate the next check cadence (weekly for calendar events, immediate for corporate actions and terms diffs).

## Build: mapping the surface for a developer

For questions like "what can I build on Base tokenized stocks", "what frameworks, tools, or schemes does Base provide", "what launchpad details do I need before building", "what is the whitespace — what does not exist yet". The user is a developer asking about the surface, not a holder asking about a position. The failure mode is answering a build question as a position question (a price, a yield) or repeating an ecosystem tagline as a live venue.

Shape of the answer:

1. Classify the build intent: integrate (plug into a live venue), extend (build on an existing rail), or fill (build the whitespace — a primitive that does not exist yet). The three intents read different parts of `references/build-surface.md`.
2. Map the three layers from `build-surface.md`: rails (contract-level primitives that exist — B20 standard, registry, custody chain, data rails), integration points (live venues — Aerodrome pools, Beefy vaults, launchpads), and whitespace (dated negatives — no strip venue, no lending market, no index product, the B20-without-a-pool set derived from the registry per session; 9 of 13 on 2026-09-08, re-derive).
3. Name every rail and venue by address, not ticker (rule 8), and state the read a builder must do before trusting it: the B20 multiplier, the hook permission mask, the policy scopes.
4. Date the negatives that bound the build. Whitespace is the volatile layer — "no strip venue" was true on 2026-09-06 and is a one-launch fact; re-verify before asserting it.
5. State what the build inherits: the weekend gap (two clocks), the terms-only dividend (multiplier 1.0), eligibility gating (policy scopes), and issuer risk (a claim stack, not a share). A design that ignores one of these breaks on the first weekend, the first ex-date, or the first policy action.
6. Read-only: describe what to check and what the surface supports, never scaffold, deploy, or sign. The skill maps the surface; it does not build on it.

## Content style (delivery, not a mode)

When any of the five modes is asked to deliver as a thread, comparison table, one-pager, or explainer for a specific audience, the rules that always apply:

1. Never state or imply a future yield. Any dividend, implied yield, or return number is dated and marked variable.
2. No "safe", "riskless", "guaranteed", "insured" — tokenized stocks have issuer risk, contract risk, and corporate-action ambiguity that a share does not.
3. Every superlative ("largest strip", "first tokenized dividend") carries a source and date, or it gets cut.
4. Every named asset is identified on first mention (what it is, who issues it, what claim layer). No unexplained tickers.
5. Format for scanning: tables for comparisons, labeled lines for calendars and decompositions, prose only where reasoning needs sentences. A wall of correct text loses to a table plus three sharp paragraphs.
6. Jurisdictional tripwires (US persons, securities-adjacent language, geo-gated products marketed globally) are flagged, not improvised past.
