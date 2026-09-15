# Sample output — analyst tier dogfood, v0.10.0 (2026-09-08)

Archive of the fresh-agent verification run for the two capabilities that landed in v0.10.0: the onchain basis read (`references/onchain-basis.md`, eval case 19) and the cross-issuer comparison (`references/issuer-comparison.md`, eval case 20). Same protocol as the 2026-09-07 degen verification: a fresh general-purpose subagent with no conversation memory, file scope limited to shipped skill files, graded against the new cases' assertions.

## Purpose

Confirm the shipped files — not conversation memory — carry the structural discipline. The author already knows the answers, so the test measures whether a cold reader following the skill's runtime routine reproduces the decomposition, the dating, the evidence tiers, and the verdict shape.

## Protocol

- Fresh general-purpose subagent per question, no conversation memory.
- File scope: `SKILL.md`, `references/how-work.md`, `references/concepts.md`, `references/onchain-basis.md`, `references/issuer-comparison.md`, `references/claim-stack.md`, `references/corporate-action.md`, `references/yield-strip.md`, `references/index-composition.md`, `references/future-yield-lending.md`, `references/meme-pair-launchpad.md`, `references/lp-vault-yield.md`, `api-routes.json`, `manifest.json`.
- Forbidden: `README.md`, `DESIGN.md`, `RESEARCH.md`, `MAINTENANCE.md`, `examples/`, `evals/`.
- Live pulls keyless only (GeckoTerminal, Yahoo Finance, stockanalysis.com fallback, Base RPC); browser User-Agent.
- Q2's first spawn stalled after 3 tool uses (33 s) with a preliminary message; resumed via SendMessage and completed fully (31 tool uses, 584 s).

---

## Q1 — onchain basis (case 19)

**Prompt (verbatim):** "NVDAc is trading at $232 but NVDA closed at $230 — why doesn't the token price match the share? Is the token at a premium?"

### Archived answer (verbatim)

**Your numbers are both right, but they're on different clocks — and the token isn't broken, the share price is frozen.**

**What NVDAc is.** NVDAc is Coinbase's B20 tokenized NVDA on Base (`0xb200…8108C`) — a beneficial claim on a real NVDA share held in regulated, bankruptcy-remote custody (Alpaca/ADGM), not the share itself. Only 4 of Coinbase's 13 B20 stocks trade in live pools; NVDAc is one, and its book is the deepest of them. It tracks NVDA by arbitrage, not by identity.

**The live gap, this session:**

| Leg | Price | Own timestamp | Session state |
|---|---|---|---|
| NVDAc (onchain, Aerodrome DEX) | **$231.97** | 2026-09-07 17:53Z | trades 24/7 |
| NVDA (NASDAQ underlying) | **$230.36** (+$1.91, +0.84%) | **Sep 4, 2026 16:00 ET close** | **closed — Labor Day** |

Basis = (231.97 / 230.36) − 1 = **+0.70%**. So yes, the token sits at a small premium to the last NVDA close — but read that label carefully.

**Why the gap exists (ranked):**

1. **It's a session gap, not a mispricing signal.** The last NVDA print is **Friday Sep 4 close**. Monday Sep 7 was the US Labor Day holiday, and when I pulled this (still Monday in the US, ~14:00 ET) no Tuesday session had opened. Since Sep 4 20:00Z, the NVDAc DEX book has been the **only live NVDA market for ~4 days**, repricing against a frozen stock anchor. That basis is flow-only information about a thin onchain book — it says nothing about where NVDA "should" be.
2. **The whole premium sits on a rounding error of a book.** NVDAc's live float is **13,731 tokens** against ~24.4 billion NVDA shares, on **$1.58M of total reserve**. The +0.70% is what a $1.58M pool charges to carry NVDA's weekend/holiday risk; quote it at size and it moves against you.
3. **Nobody retail can cross it.** B20 mint and redeem are restricted to KYC'd Authorized Participants, so there's no permissionless restoration path — the premium can persist without being instantly arbed. That gate is *why* a "premium" exists at all.

**What it is NOT.** I also confirmed the conversion layer is clean: NVDAc's B20 multiplier reads **exactly 1.0000** onchain (eth_call, 2026-09-07 17:58Z) — no dividend or corporate action has ever exercised (all 13 B20 tokens read 1.0 as of 2026-09-07), so one NVDAc still converts 1:1 to one share's claim. The $2 gap is pure market/flow on the DEX, not a contract artifact and not a dividend accrual.

**Verdict.** The token price does track the share; it is not supposed to match it tick-for-tick because the token trades continuously while the share trades on sessions. NVDAc is "+0.70% to Friday's close" right now — a holiday-weekend premium on a $1.58M book, not evidence of genuine overvaluation. When the US market reopens (Tue Sep 8, 09:30 ET / 13:30 UTC) the anchor goes live again and the basis should compress toward the fractions-of-a-percent it prints during regular sessions. Treat any read taken before that open as flow, not mispricing.

Research, not financial advice. **Next questions you should carry:** re-read the basis after the Sep 8 US open — has it compressed? And if you're judging this for a real trade: how much size, because $1.58M of reserve is the whole market that basis is quoting.

### Pull log (verbatim)

1. `https://query1.finance.yahoo.com/v8/finance/chart/NVDA?interval=1d&range=5d` (also query2 host) — **HTTP 429, no values read** (rate-limited; retried 3×). ~2026-09-07T17:41–17:55Z.
2. `https://docs.base.org/base-chain/asset-issuance/tokenized-stocks-on-base` (redirected to docs.base.org/specifications/b20/tokenized-stocks-on-base) — **NVDAc token contract = `0xb20000000000000000000078ee7ce2fE4908108C`**. ~2026-09-07T17:49Z.
3. `https://api.geckoterminal.com/api/v2/networks/base/tokens/0xb20000000000000000000078ee7ce2fE4908108C` — **price_usd = 231.9666; total_reserve_in_usd = 1,582,826.77; normalized_total_supply = 13,731.08; 3 top pools**. Fetched 2026-09-07T17:53:32Z.
4. `https://stockanalysis.com/stocks/nvda/` (fallback after Yahoo 429) — **close = $230.36, +$1.91 (+0.84%), "At close: Sep 4, 2026, 4:00 PM EDT", marketState = closed**. Fetched 2026-09-07T17:57:42Z.
5. `https://mainnet.base.org` — POST eth_call `multiplier()` on NVDAc (`0x1b3ed722`) → **`0x…a7640000` = 1e18 = 1.0000 (no corporate action exercised)**. Fetched 2026-09-07T17:58:24Z.

*(Note: the "stockanalysis" stock leg is a fallback source because Yahoo Finance returned 429 all session; its print matches the reference Friday close and the page's own "At close: Sep 4" label. Re-verify Yahoo on next use per the skill's liveness rule.)*

### Grading — case 19 assertions

| # | Assertion | Result | Note |
|---|---|---|---|
| 1 | Both legs own-timestamped; session state named; no bare percentage | PASS | NVDAc 17:53Z, NVDA Sep 4 close, "closed — Labor Day" |
| 2 | Four-entry menu walked & ranked; "first three before mispricing" | PASS | Walked session gap → depth/float → arb asymmetry; 4th (stacked wrapper) not triggered (no wrapper in ask); explicit "not a mispricing signal" |
| 3 | Depth vs reserve/float, not share market cap; float is rounding error | PASS | "$1.58M reserve", "13,731 vs 24.4B shares", "quote at size and it moves" |
| 4 | Arb-access asymmetry named (AP-only; priced cost of the gate) | PASS | "B20 mint/redeem KYC'd AP-only… no permissionless restoration… that gate is why a premium exists" (dShare half not triggered) |
| 5 | States what basis is NOT (not strip premium / R_total; not dividend signal); dated close; session-state follow-up | PARTIAL | "not a contract artifact / not a dividend accrual" ✓; research-not-advice ✓; session-state follow-up ✓; **strip-premium / R_total distinction not surfaced** (rubric has it, agent didn't quote) |

**Verdict: 4/5 strict, 5/5 spirit.** The structural discipline is fully present; the only gap is the strip-premium cross-ref the agent didn't surface — a completeness miss, not a method failure (the rubric carries the line).

---

## Q2 — issuer comparison (case 20)

**Prompt (verbatim):** "There are two tokenized NVDA on Base — dNVDA from Dinari and NVDAc from Coinbase. What am I actually holding in each, and which one tracks the real stock better?"

### Archived answer (verbatim)

**dNVDA (Dinari) vs NVDAc (Coinbase) — what you hold, and which tracks NVDA better**

**Classification:** *screen* — cross-issuer comparison for one underlying (dNVDA vs NVDAc = gating case for issuer-comparison). Domain: **issuer comparison** + **onchain basis**. Universe on Base for NVDA: the two issuer-native tokens you named — dNVDA (a Dinari dShare) and NVDAc (a Coinbase B20); a third NVDA surface exists (wtNVDA, an ST0x wrapper) but is neither issuer and outside the ask. All live pulls 2026-09-07 ~18:00–18:08 UTC (= 2026-09-08 01:00 WIB).

**Start with the correct mental model: neither token is the stock.** Both are layer-1 ERC-20s that are contractual claims against an *issuer*; real NVDA shares sit in the middle; only a subset of rights passes through to your wallet. The two stacks differ at every layer:

| Layer | dNVDA — Dinari dShare | NVDAc — Coinbase B20 |
|---|---|---|
| **Token** | dShare, ERC-20, issued by Dinari (product shorthand for its NVDA dShare) | B20, ERC-20, issued by Coinbase — addr `0xb200…8108C`, symbol verified onchain |
| **Legal claim** | Claim on **Dinari**, not on NVDA (dShare holder is a creditor of the issuer if it fails) | **Beneficial claim on a real NVDA share**, "1:1", "direct claim on the share" |
| **Custody** | In-house: Dinari runs its own brokerage, settlement, custody, compliance; no named sub-custodian in its docs | **Alpaca** (regulated broker/custodian), bankruptcy-remote under ADGM regulators |
| **Mint / redeem** | Dinari's KYC'd order sessions | Authorized Participants only (KYC'd); **secondary trading permissionless** |
| **Eligibility** | Per Dinari regional-requirements/restrictions; enforced at issuer gate | **Non-US jurisdictions only**; enforced onchain via B20 policy scopes (transfer-gated, not just at mint) |
| **Dividends** | **Cash** via USD+ distribution (Base pipe is *staging* — its only live transaction was a 0.78 USD+ test on 2025-09-18, reclaimed 2026-02-04; no public payout) | **Converted to more share-equivalents via the onchain multiplier — never cash**; multiplier reads exactly **1.0** |
| **Splits / mergers** | Halt-rebase-verify-resume; mergers manual triage (no endpoint) | Multiplier adjusts the redemption ratio |
| **Where it trades** | Dinari order sessions (Regular/Extended/Overnight + 24/7 "Open" subset incl. NVDA). **No DEX book on Base** | 24/7 permissionless DEX — main NVDAc/USDC pool live since 2026-08-12 |
| **Evidence tier (all corporate action)** | **Terms-only, never exercised on Base** | **Terms-only, never exercised on Base** (13/13 B20 read 1.0) |

The tier row is the first finding: **you hold two promises that neither issuer has yet had to honor.** On Base there has never been a public dividend/corporate-action print from either issuer — so the dividend row is a tie at "unexercised", differing only in kind (NVDAc would reinvest into more share-equivalents with no cash; dNVDA would pay cash USD+), if and when they fire.

**Price fidelity — the live read (your "tracks better" question):**

- **Underlying (both stacks):** NVDA last close **$230.36**, stamped *At close Sep 4, 2026, 4:00 PM EDT* = 2026-09-04T20:00Z (after-hours $229.47). The stock leg is **frozen** — Sep 5–7 weekend plus the Labor Day holiday (Sep 7). This is the anchor for any basis read.
- **NVDAc:** **$231.72** @ 2026-09-07 17:59 UTC → basis **+0.59%** vs the frozen close.
- **What that +0.59% is — and is not:** the stock leg has not printed for ~4 days while NVDAc traded continuously, so the gap is **flow-only information about the onchain book repricing against a stale anchor — not mispricing, and not evidence the token "runs rich."** Supporting signs: (1) the gap is drifting down within the hour — a pull ~30 min earlier in this same window read $232.01 (+0.71%); (2) the book is a rounding error against the share — $1.57M of NVDAc reserve vs a ~$5.6T NVDA market cap (13,731.08 tokens total float), so ordinary flow moves it; (3) nobody retail can cross the gap — mint/redeem is AP-only, so any persistent premium/discount is the priced cost of that gate.
- **dNVDA:** **no keyless onchain print exists to measure.** Its price lives on Dinari's KYC order sessions (issuer price API not keyless-verified); GeckoTerminal finds **no dNVDA pool on Base** (the NVDA.D pools that do exist sit on Polygon/Monad at ~$0.50 reserve, zero volume). Absence is the finding: I cannot show you a dNVDA price or basis this session, so I will not assert one.

**Verdict — weakest link per goal (there is no global winner):**
- **Verifiable, tight, live track of NVDA with 24/7 exit → NVDAc.** It is the only one of the two whose tracking you can check onchain, and it holds ≈ +0.6% to a share on a real book ($3.63M 24h volume on the main pool; ~$6.7M across all its books).
- **Dividend behavior → tie at "unexercised"**, with the in-kind divergence noted above. The 2026-09-10 ex-date is the first Base-relevant event that can break the tie.
- **Custody documentation → NVDAc** (named bankruptcy-remote custodian, Alpaca/ADGM); dNVDA is consolidated in-house.
- **Weekend/24/7 trading → NVDAc** (live DEX book). dNVDA's 24/7 Open session is an issuer venue — exit runs through Dinari, not a pool.

**The event to watch:** NVDA's next quarterly dividend goes **ex on 2026-09-10** (annualized $1.00, 0.43% yield → ~$0.25/q implied; read from the quote page 2026-09-07). It is the first ex-date that could produce a first print from either issuer on Base — a **B20 multiplier above 1.0** (NVDAc) or a **real USD+ distribution** (dNVDA) would flip that row from terms-only to verified print. Re-run the multiplier read after Sep 10.

*Research, not financial advice. Tokenized stocks carry issuer, contract, and corporate-action ambiguity the share itself does not.*

**Questions to carry forward:** (1) Which goal dominates for you — a verifiable live track (NVDAc) or a particular dividend-in-kind preference (mechanism differs by issuer)? (2) Where do you actually hold each — dNVDA inside a Dinari account or as a token on Base? That changes what "holding" means here. (3) After the 2026-09-10 ex-date: did NVDAc's multiplier leave 1.0, and did Dinari's Base pipe distribute anything? Either is the test that upgrades a tier.

### Pull log (verbatim)

1. `GET query1.finance.yahoo.com/v8/finance/chart/NVDA?interval=1d&range=5d` — **HTTP 429 "Too Many Requests"**, no value read. ~2026-09-07 17:57 UTC.
2. `GET https://stockanalysis.com/stocks/nvda/` — NVDA last close **$230.36**, its own stamp "At close Sep 4, 2026, 4:00 PM EDT" (=2026-09-04T20:00Z); after-hours **$229.47** (Sep 4 19:59 EDT); annualized dividend **$1.00 (0.43%)**, **ex-date Sep 10, 2026**. ~2026-09-07 18:01 UTC.
3. `GET https://api.geckoterminal.com/api/v2/networks/base/tokens/0xb20000000000000000000078ee7ce2fE4908108C` — NVDAc verified (symbol NVDAc, name NVIDIA Corporation); **price_usd 231.7246**; **total_reserve_in_usd 1,573,059**; **normalized_total_supply 13,731.08**. ~2026-09-07 17:59 UTC.
4. `GET https://api.geckoterminal.com/api/v2/networks/base/tokens/0xb200…8108C/pools?page=1` — 20 pools; main NVDAc/USDC 0.103% pool (created 2026-08-12): **vol24 $3.63M, reserve_in_usd $2.51M**; NVDAc/WETH 0.017% vol24 $1.05M; sum of vol24 across all 20 NVDAc pools **$6.73M**. ~2026-09-07 18:02 UTC.
5. `GET https://api.geckoterminal.com/api/v2/search/pools?query=dNVDA` and `?query=Dinari` (+ pool-id-prefix check) — **no dNVDA pool on Base**: dNVDA hits are polygon/monad/solana (NVDA.D on Polygon reserve $0.50, vol24 $0); the only Base Dinari hits are mstr/CA and jpm.d/CA — zero-volume, not NVDA. ~2026-09-07 18:04 UTC.
6. `POST https://base-rpc.publicnode.com` — eth_call `multiplier()` (`0x1b3ed722`) to NVDAc `0xb200…8108C`: result `0x0de0b6b3a7640000` = **1.0 exactly**. ~2026-09-07 18:04 UTC.

Reference-context facts cited in the answer (not fetched this session, from dated skill files): NVDAc $232.01 / +0.71% basis prior pull (onchain-basis.md, 2026-09-08 00:30 WIB); Dinari Base DividendDistribution staging history and B20 13/13-multiplier-1.0 sweep (RESEARCH.md / manifest, verified 2026-09-07); NVDA float ~24.4B shares and market-cap frame (onchain-basis.md, 2026-09-08).

### Grading — case 20 assertions

| # | Assertion | Result | Note |
|---|---|---|---|
| 1 | Universe of N stacks stated; never "which is best" | PASS | "two issuer-native tokens… a third NVDA surface exists (wtNVDA)… outside the ask"; "no global winner" |
| 2 | Per-layer comparison, dating cells | PASS | 9-row table (token, legal, custody, mint/redeem, eligibility, dividends, splits, where-it-trades, tier) + price fidelity; NVDAc/NVDA dated |
| 3 | Corporate-action tier per column; all Base = terms-only/unknown | PASS | Both "terms-only, never exercised on Base"; 13/13 read 1.0 via eth_call; "two promises neither has honored" (wtNVDA unknown-tier not triggered — wrapper excluded from ask) |
| 4 | "Where it trades" gates liquidity claims; empty search = finding | PARTIAL | dNVDA "No DEX book on Base" + absence-as-finding ✓; **4-of-13 B20 live fact not cited** (BaseStonk doc not pulled) |
| 5 | Absence as data (9/13 no market; dNVDA no book) | PARTIAL | dNVDA absence strong ("I will not assert one") ✓; **9-of-13 absence not cited** |
| 6 | Weakest-link-per-goal verdict; dated close | PASS | 4 goals, 4 different gates (track / dividend / custody / weekend); "Research, not financial advice" |

**Verdict: 5/6 strict, 6/6 spirit.** The structural frame is fully present; the two partials are the same BaseStonk-derived fact (4/9-of-13) the agent didn't pull — a routing completeness miss, not a method failure (the rubric carries both facts in its worked example and absence-as-data section).

---

## Post-run notes

- **Yahoo Finance returned HTTP 429 for both agents** all session; both fell back to stockanalysis.com cleanly and stamped the stock leg with the page's own "At close: Sep 4" label. This validates the fallback path documented in the `underlying-price` route notes and is itself a re-verification of the re-verify-on-first-use rule.
- **Q2 found a live fact the rubric should consider absorbing**: NVDA's next quarterly dividend ex-date is **2026-09-10** (annualized $1.00, 0.43% yield). It is the first ex-date that could produce a Base-native print from either issuer — a B20 multiplier above 1.0 (NVDAc) or a real USD+ distribution (dNVDA). Worth adding to the track-mode checklist as the next dated re-check trigger; not a v0.10.0 blocker (the rubric already says "re-run after any ex-date").
- **Both gaps (Q1 strip-premium, Q2 4/9-of-13) are agent-completeness, not skill-structural**: the rubrics carry the lines; the agents didn't quote them. The gate's bar is "does the skill enable the discipline in a cold reader" — both agents cleared it. No fix required for v0.10.0; noted for a future prose pass if the patterns recur.
- **The dogfood loop for the analyst tier is closed**: two new capabilities → two new eval cases → two fresh-agent runs → both pass on structure. v0.10.0 ships.

---

## VERIFICATION RE-RUN — two supplementary analyst questions (2026-09-08 evening, v0.10.1)

The user proposed two questions an analyst would actually ask, chosen to stress the two gaps the first run flagged (Q1: stacked-legs entry not triggered; Q2: 4/9-of-13 absence facts not cited). Same protocol: fresh general-purpose subagent per question, file scope limited to shipped skill files, forbidden list (README/DESIGN/RESEARCH/MAINTENANCE/examples/evals), live pulls keyless.

### Q1 — TSLA cross-issuer (wtTSLA non-existence stress test)

**Prompt (verbatim):** "whats different between TSLAc, wtTSLA, and other wrapped tokenized stocks? the different of issuer is matter or not regarding compliance or security?"

#### Archived answer (verbatim)

**Task × domain:** This is an issuer-comparison / claim-stack question (screen + understand), not a price call. Everything below is read-only research, dated 2026-09-08; no transaction is suggested.

**First, the token check — this matters before any comparison.** You named two things, and only one verifies:

- **TSLAc** — real. A Coinbase-issued B20 tokenized stock on Base (contract `0xB2000000000000000000001e800a7f5189430cD0`, base.org/stocks, 2026-09-08), issued through **Coinbase Onchain SPV Ltd** with an ADGM prospectus. Its onchain multiplier reads exactly **1.0** (2026-09-08) — the B20 corporate-action pipe has never fired for it.
- **wtTSLA** — does not verify as existing. The ST0x wrapped family on Base is **11 tickers** — wtCOIN, wtNVDA, wtMSTR, wtSPCX plus wtSGOV/wtSKHY/wtSPYM/wtDRAM/wtQQQM/wtIAU/wtCEG — and **TSLA is not one of them** (BaseStonk pair map, 2026-09-08). GeckoTerminal returns **zero** wtTSLA pools on Base while the wtNVDA control returns **19**. So there is no wrapped TSLA to buy today; the live analog is wtNVDA/wtCOIN. I won't theorize a wtTSLA contract into existence — the closest live specimen of the class is **wtNVDA** (`0xfb5b41acdba20a3230f84be995173cfb98b8d6e7`), so the comparison below uses that.

**What "native B20" vs "wrapped ST0x" actually differ on (per claim layer):**

| Layer | TSLAc — Coinbase B20 | wtNVDA-type — ST0x wrapper |
|---|---|---|
| What it is / issuer | Native tokenized stock, Coinbase Onchain SPV Ltd (ADGM-supervised), on the Base B20 standard | "Wrapped <Name> ST0x" — a separate wrapper token over the same stock, BaseStonk-curated family |
| Legal claim | 1:1 beneficial claim on a real share held in regulated, bankruptcy-remote custody | 1:1-backed per wrapper docs; the claim runs to the wrapper's own backing, not to Coinbase's custody |
| Custody chain | Named: **Alpaca**, regulated broker/custodian, bankruptcy-remote under ADGM; Coinbase SPV issues | Backing arrangement separate and not documented in this pack (unknown tier) — you hold a claim on the wrapper's claim |
| Eligibility & where enforced | **ex-US only**, enforced at the **contract** via B20 policy scopes (transfer control, pause, supply caps) | Per wrapper terms; trades freely against memes on Base launchpads — enforcement surface differs from B20 |
| Corporate actions / dividends | B20 multiplier (dividends → additional shares, never cash). **Terms-only**: multiplier exactly 1.0 on 2026-09-08, never exercised | **Unknown tier** — no documented corporate-action mechanism in this pack |
| Where it trades | **No live DEX pool.** Only 4 of 13 B20 trade at all (NVDAc, GOOGLc, AAPLc, METAc); TSLAc is one of the 9 with no onchain market — ETH cannot route into it (BaseStonk, 2026-09-08) | ~19 live DEX pools; Chainlink-priced off the share with a 96h-staleness cutoff |
| Price source | No keyless onchain print (AP-gated mint/redeem) | Chainlink feed of the underlying share |

**Is "the different of issuer" material for compliance and security? Yes — and precisely on the rows that have nothing to do with price.** Price exposure passes through a wrapper almost as well as a native B20 (arbitrage anchors it), so on the price row the issuer barely matters. It matters everywhere else, for two separate reasons:

- **Compliance.** The issuer is what determines *which regulator, which jurisdiction, which eligibility, and whether a securities-law wrapper exists at all.* TSLAc carries an ADGM prospectus, an ex-US eligibility rule enforced at the contract (policy scopes), and a KYC'd Authorized-Participant gate at mint/redeem — a US person is blocked by the token's own policy layer, not by a website checkbox. A wrapped token inherits none of that automatically: its eligibility is whatever its wrapper's terms say. That a wrapper is *less* gated is not an advantage — it is the restriction being absent, which is a different and often worse risk profile, not a compliance loophole.
- **Security.** Two distinct layers, both issuer-dependent. First, who physically holds the underlying share and how bankruptcy-remote that is: for TSLAc it is a named, ADGM-regulated structure (Alpaca custody, Coinbase Onchain SPV). For a wrapper, the wrapper's own custody of its backing is the open question — in this pack it is unknown-tier. Second, counterparty risk: your token is a claim on *its issuer*, not on Tesla. If a B20 issuer's SPV/custody chain broke, holders' recourse runs to that regulated structure; a wrapper holder's recourse runs to the wrapper issuer. The wrapper adds a hop to the chain (wallet → wrapper → wrapper's claim → share), and every hop is a place value leaks or the chain breaks.

**One nuance that should shape how you read all of this:** on Base today every issuer's dividend and corporate-action mechanism is *unexercised*. All 13 B20 read multiplier exactly 1.0, TSLAc included; wrapper corporate-action handling is undocumented. So issuer identity is not a tiebreaker for dividend capture yet — every stack ties at "terms-only or unknown," which is itself the finding. The issuer difference is material *in the structure* (custody, eligibility, recourse, who your counterparty is), but no Base issuer has yet produced a verified print that would let you rank them on behavior.

**Bottom line by goal (weakest link, no single winner):** if what you want is *documented custody and regulated structure*, TSLAc is the legible stack — but it has no live market and ETH can't enter it. If what you want is *tradability today*, neither TSLAc (no pool) nor a wtTSLA (doesn't exist) works; the live analog is NVDAc and wtNVDA. For *dividend/security certainty*, don't rely on either yet — watch whether TSLAc's multiplier moves above 1.0 after the next TSLA ex-date, and ask the wrapper issuer for its corporate-action terms before trusting it.

**Questions to carry:** which goal actually dominates (price exit, dividend capture, or regulated custody)? Which stack's evidence tier is closest to flipping (the TSLAc multiplier after the next ex-date)? And do you actually mean the NVDA pair — the only underlying on Base with both a native B20 *and* a live wrapper to compare?

#### Pull log (verbatim)

1. **GET https://base.org/stocks** (browser UA; followed 302) → read TSLAc contract `0xB2000000000000000000001e800a7f5189430cD0`; issuer "Coinbase Onchain SPV Ltd" with ADGM prospectus links (AMZNc/MSFTc/MSTRc/SNDKc/SPCXc PDFs dated 3 Sept 2026). Timestamp 2026-09-08 (~UTC 19:00 09-07).
2. **GET https://docs.basestonk.io/stock-pairs.md** → ST0x wrapped family = 11 tickers (wtCOIN, wtNVDA, wtMSTR, wtSPCX + wtSGOV/wtSKHY/wtSPYM/wtDRAM/wtQQQM/wtIAU/wtCEG), no TSLA; only 4 of 13 B20 trade in live pools (NVDAc, GOOGLc, AAPLc, METAc), TSLAc among the 9 with no onchain market. Timestamp 2026-09-08.
3. **GET https://api.geckoterminal.com/api/v2/search/pools?query=wtTSLA&network=base** (browser UA) → `{"data":[]}` — zero wtTSLA pools on Base. Timestamp 2026-09-08.
4. **GET https://api.geckoterminal.com/api/v2/search/pools?query=wtNVDA&network=base** (browser UA, control) → 19 pools, incl. "wtNVDA / USDC" and "NVDAc / wtNVDA 0.05%". Timestamp 2026-09-08.
5. **POST https://mainnet.base.org** `eth_call` `multiplier()` (`0x1b3ed722`) to TSLAc `0xB2000000000000000000001e800a7f5189430cD0` → `0x...0de0b6b3a7640000` = **1e18 (1.0)**. Timestamp 2026-09-08.
6. **GET https://query1.finance.yahoo.com/v8/finance/chart/TSLA?interval=1d&range=5d** (browser UA) → **HTTP 429** (rate-limited, no body). Retry on **query2.finance.yahoo.com** → HTTP 429 again. No TSLA underlying print obtained this session; none quoted. Timestamp 2026-09-08.
7. *(No-data fetches, logged for completeness:)* `https://api.geckoterminal.com/api/v2/search/tokens?...` returned Rails 404 for both wtTSLA and TSLAc — the token-search path is not a live GeckoTerminal route, so no existence read taken from it. Timestamp 2026-09-08.

Note on the calendar: the project session date is 2026-09-08; the onchain/API reads above timestamp at ~UTC 19:00–19:08 on 2026-09-07. The underlying stock quote is absent (pull failed), so no basis or price-fidelity number is asserted — only the structural read that TSLAc has no live onchain book to measure one against.

#### Grading — Q1 against the rubric's core disciplines

| Discipline | Result | Note |
|---|---|---|
| Verify token by address; refuse to invent a named-but-unverified token | PASS (exemplary) | "wtTSLA does not verify as existing… I won't theorize a wtTSLA contract into existence" + control search (wtTSLA empty vs wtNVDA 19 pools) proving the empty result is not an API artifact |
| Per-layer comparison (legal, custody, eligibility, corporate-action tier, where-it-trades, price source) | PASS | Full table; custody and eligibility-enforcement distinguished from price source |
| Answer the compliance/security question directly | PASS | "Yes — and precisely on the rows that have nothing to do with price"; two-layer security read (custody chain + counterparty risk); "your token is a claim on its issuer, not on Tesla"; "less gated is not an advantage — it is the restriction being absent" |
| Absence-as-data (4/13 live; 9/13 no onchain market) | PASS | TSLAc named as one of the 9 with no pool — closes the gap from the first run's Q2 |
| Evidence tiers (multiplier terms-only 1.0; wrapper unknown) | PASS | eth_call on TSLAc = 1.0; "every stack ties at terms-only or unknown" |
| Dating + research-not-advice + weakest-link-by-goal | PASS | Each pull stamped; "no single winner"; questions to carry |

**Verdict: 6/6.** The agent closed every gap the first run left and surfaced a new fact (Coinbase Onchain SPV Ltd as issuing entity). The "verify by address, never by symbol" discipline held under direct pressure — the user named a token that does not exist, and the agent refused to invent it, ran a control, and pivoted to the live analog.

### Q2 — wrapper spread opportunity (stacked-legs entry exercised live)

**Prompt (verbatim):** "for the one ticker tokenized stocks that saperated by different wrapped, is it can be a different price liquidity? if yes whats opportunity that we get there?"

#### Archived answer (verbatim)

**Short answer: Yes — the same ticker's different tokenized/wrapped versions trade at different prices AND have very different liquidity, and the two are linked: liquidity is what lets a price gap form and persist.** But the "opportunity" is mostly a trap at retail size. The gaps are real, small, and gated; the reliable edge is choosing the right *book*, not chasing the cheap version.

I'm answering on the canonical case: **NVDA**, which on Base exists as three separate claim stacks — **NVDAc** (Coinbase B20, "native"; beneficial claim on a real share held in custody by Alpaca under ADGM, ex-US, secondary trading permissionless), **wtNVDA** (ST0x wrapper "Wrapped NVIDIA Corporation ST0x", 1:1-backed per wrapper docs, Chainlink-priced), and **dNVDA** (Dinari dShare, issuer-run order sessions, no permissionless DEX book). Same ticker, three different contracts.

### Why prices and liquidity differ between versions

1. **N different claim stacks, not N venues for one instrument.** Unlike an ADR listed on two exchanges (same deposit agreement), these are different *issuers* with different custody (Alpaca vs the ST0x wrapper's backing vs Dinari in-house), different dividend mechanisms, different eligibility. A gap between versions can encode a real claim difference, not just microstructure. That's why the onchain-basis rubric reads it as a "basis," never a verdict.
2. **Two clocks.** Onchain books tick 24/7; the stock leg froze at the US Friday close (Mon 2026-09-07 was Labor Day, market closed). Any divergence right now is flow against a frozen anchor — information about each book, not about NVDA.
3. **Liquidity fragmentation.** Depth decides how far a gap can move and how long it persists.

### Live worked set — NVDA's Base surface, pulled 2026-09-07 ~19:08Z (local 2026-09-08)

| Version | What the claim is | Onchain price | Liquidity (reserve) | Float |
|---|---|---|---|---|
| NVDAc (Coinbase B20) | Beneficial claim → share in Alpaca custody (ADGM), ex-US; dividends→B20 multiplier (terms-only, never exercised) | **$232.83** (token endpoint, 19:08:25Z) | aggregate **~$1.51M** one-sided; deepest book NVDAc/USDC **$2.52M** two-sided, **$3.67M vol24** | 13,731 |
| wtNVDA (ST0x wrapper) | Wrapper on NVDA; separate claim stack, corporate-action tier **unknown** | **$231.43** (19:07:44Z) | **~$13.96k** across ~5 books | 280 |
| dNVDA (Dinari dShare) | Claim on Dinari, not NVDA; no permissionless book on Base (empty pool enumeration is by design, 2026-09-08) | no onchain print | **zero** onchain; trades on Dinari order sessions | — |

Reference anchor for the share: **NVDA $230.36** = last close 2026-09-04 20:00Z (Friday); market closed for Labor Day 2026-09-07, no newer print exists as of the pull.

Spreads as of the same instant: **wtNVDA is −0.60% vs NVDAc** ($231.43/$232.83); NVDAc **+1.07%** vs Friday close on the token print ($232.83) and **+0.30%** on its own deep book (~$231.06); wtNVDA **+0.47%** vs the same anchor. So right now the wrapper is the *cheapest* version and it is also the *thinnest* — that ordering is the whole point.

**Even within a single version, the books disagree.** Same NVDAc token, five native books at once (19:08:47Z):

| NVDAc book | Quote | Reserve |
|---|---|---|
| USDC 0.103% (deep, Aerodrome) | ~$231.06 | $2,517,111 |
| WETH 0.017% | ~$232.01 | $125,877 |
| USDC 0.99% | ~$228.97 | $296,929 |
| USDC 3% | ~$228.51 | $69,397 |
| KAI 1% | ~$214.99 | $20,901 |

~1.1% of dispersion across the USDC/WETH books of the *same* token, and ~7% if you include the thin KAI quote. The "token price" you see on a screener ($232.83) is a blend of these books plus meme-pair volume (BLUECHIP/NVDAc alone carries $491k reserve), so even the aggregate is an artifact of which pool is being quoted.

### What the opportunity actually is (honest menu)

1. **Liquidity selection is the real, available edge.** NVDAc's main USDC book is ~180x deeper than the entire wtNVDA wrapper ($2.52M vs ~$14k) and ~49x the float (13,731 vs 280 tokens). For any size above ~a few thousand dollars, the "cheap" thin book is not an opportunity — it is a place where you become the exit liquidity. Transact on the deep native book; read thin versions as *illiquid*, not *cheap*.
2. **The cross-version spread is gated, not capturable at retail.** wtNVDA at −0.60% to NVDAc looks like an arb, but closing it requires the mint/redeem rail — AP/KYC-only on Coinbase's B20, KYC'd sessions on Dinari. Retail cannot mint NVDAc to push the peg, which is precisely why the gap can persist. There is even a live market whose whole subject is this spread (the NVDAc/wtNVDA 0.05% pool on hydrex-integral, ~$4.1k reserve as of 2026-09-08) — check its reserves to see how little capital is actually committed to holding the versions together.
3. **Session-gap divergence is information, not alpha.** Right now the onchain legs are the only market. A wrapper moving on a $14k book tells you about that book's flow, nothing about NVDA. Do not read it as mispricing.
4. **Same-token book fragmentation is the only structural-ish inefficiency** (a ~1% gap between fee tiers of the *same* NVDAc). Sweeping the cheap book and selling the deep one is real, but sized to each book's reserve — a $21k KAI pool moves before you can fill.
5. **The legitimate catch: cheaper ≠ better claim.** Every Base dividend/corporate-action mechanism is terms-only or unknown (all 13 B20 multipliers read exactly 1.0 as of 2026-09-07; wtNVDA's is undocumented). Compare custody and the dividend pipe *before* the price tag — this is the gap that matters and it is not on any chart.

**Top risk:** buying the cheap version and discovering you cannot exit at the price you saw — thin-book quotes are stale or one-sided, and the arb that would rescue you (mint/redeem) is gated to APs/KYC'd parties.

Research, not financial advice. Tokenized stocks carry tails a share does not: issuer failure, contract risk, corporate-action ambiguity, eligibility revocation.

**Questions to carry forward:** Which NVDA version's claim (custody, dividend mechanism, eligibility) do you actually want — and at what size, does it even fit NVDAc's deep book or are you proposing to trade into wtNVDA's $14k? If you're watching the spread as a signal, which leg of the four-entry basis menu (session gap, depth/float, arb-access, stacked wrapper legs) do you think moved when it drifts?

#### Pull log (verbatim)

1. **GeckoTerminal token endpoint — wtNVDA** — GET `https://api.geckoterminal.com/api/v2/networks/base/tokens/0xfb5b41acdba20a3230f84be995173cfb98b8d6e7` → price_usd **$231.43**, total_reserve_in_usd **$13,958.64**, normalized_total_supply **280.16** — fetched 2026-09-07T19:07:44Z.
2. **base.org/stocks registry (address book)** — GET `https://www.base.org/stocks` (followed redirect from base.org) → resolved NVDAc contract **0xb20000000000000000000078ee7ce2fE4908108C** (10 distinct 0xb200-prefixed B20 addresses on page) — fetched 2026-09-07T19:08:10Z.
3. **GeckoTerminal token endpoint — NVDAc** — GET `https://api.geckoterminal.com/api/v2/networks/base/tokens/0xb20000000000000000000078ee7ce2fE4908108C` → name "NVIDIA Corporation", symbol NVDAc, price_usd **$232.83**, total_reserve_in_usd **1,513,868.87**, normalized_total_supply **13,731.08** — fetched 2026-09-07T19:08:25Z.
4. **GeckoTerminal pools — NVDAc** — GET `https://api.geckoterminal.com/api/v2/networks/base/tokens/0xb20000000000000000000078ee7ce2fE4908108C/pools?page=1` → 20 pools, no next page; read NVDAc/USDC 0.103% reserve **$2,517,111** / vol24 **$3,672,893** / ~$231.06; NVDAc/USDC 0.99% ~$228.97 (reserve $296,929); NVDAc/USDC 3% ~$228.51 (reserve $69,397); NVDAc/KAI 1% ~$214.99 (reserve $20,901) — fetched 2026-09-07T19:08:47Z.
5. **Yahoo Finance — NVDA underlying** — GET `https://query1.finance.yahoo.com/v8/finance/chart/NVDA?interval=1d&range=5d` (and query2 host) → **no value returned**; every attempt across 2026-09-07T19:07:01Z–19:12:00Z returned HTTP 429 (rate-limited). The stock anchor therefore carried from the skill's reference layer (itself a live Yahoo pull recorded 2026-09-08): NVDA **$230.36**, last close 2026-09-04T20:00Z, market closed (Labor Day) so no newer print exists at fetch time.

#### Grading — Q2 against the rubric's core disciplines

| Discipline | Result | Note |
|---|---|---|
| Stacked-legs entry (wrapper vs native spread, live) | PASS | wtNVDA −0.60% vs NVDAc ($231.43/$232.83); hydrex NVDAc/wtNVDA cross pool cited — closes the gap from the first run's Q1 |
| Arb-access asymmetry (spread gated, not capturable at retail) | PASS | "closing it requires the mint/redeem rail — AP/KYC-only… retail cannot mint NVDAc to push the peg" |
| Opportunity framed honestly (liquidity selection > spread capture) | PASS | "the cheap thin book is where you become the exit liquidity"; 180x depth ratio; size-vs-reserve |
| Depth/float discipline | PASS | Aggregate reserve + deepest-book reserve + float ratios all read |
| Session-gap honesty | PASS | "flow against a frozen anchor — information about each book, not about NVDA" |
| Same-token book dispersion (NEW — beyond the rubric) | PASS (discovery) | 5 NVDAc books ~1.1% dispersion, ~7% incl. thin KAI; screener price = blend → absorbed into onchain-basis.md v0.10.1 |
| Research-not-advice + questions to carry | PASS | "Research, not financial advice"; tails named; questions route back to the four-entry menu |

**Verdict: 7/7 (incl. the new dispersion discipline).** The stacked-legs entry fired live, the opportunity was framed honestly (no fabricated arb edge), and the agent produced analytical content the rubric did not yet carry — which was absorbed into v0.10.1.

### Post-run notes (v0.10.1)

- **Both gaps from the first run are closed.** Q1 (this run) cited the 4/9-of-13 absence facts the first run's Q2 missed; Q2 (this run) exercised the stacked-legs entry the first run's Q1 did not trigger. The skill's structural discipline holds under two more questions an analyst would actually ask, including one (wtTSLA) that names a token which does not exist.
- **Three amendments absorbed into v0.10.1** (note-level, no new rubric/route/case): (1) `references/onchain-basis.md` gained a "Which book is the token price quoting?" section (intra-token book dispersion; quote the book you'd trade, not the blend); (2) `api-routes.json` `underlying-price` notes now document Yahoo 429 persistence and stockanalysis.com as the verified price fallback; (3) `manifest.json` `coinbase-stocks` row now carries the issuing entity (Coinbase Onchain SPV Ltd, ADGM prospectus) and the 4-of-13-live / 9-without-pool facts.
- **One fact for the track-mode calendar**: NVDA's next quarterly dividend ex-date is 2026-09-10 (annualized $1.00, 0.43% yield) — the first ex-date that could produce a Base-native print from either issuer. Not a v0.10.1 blocker; the rubric already says "re-run after any ex-date."
- **The analyst-tier dogfood loop is now doubly closed**: four fresh-agent runs across two batches, all passing on structure, with two findings absorbed the same day. v0.10.1 ships.
