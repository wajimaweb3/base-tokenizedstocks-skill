# Degen dogfood batch — paired run (2026-09-07)

Three raw degen questions written by the user (verbatim, unpolished). This run tests the three degen features shipped in v0.6.0–v0.8.2: the meme/launchpad rubric, the trending screen, and the LP/vault yield rubric. Protocol identical to the normie batch (2026-09-07): with-skill run archived below, baseline run by a fresh agent without the skill files, both graded against the eval assertions, then independent blind grading.

## Questions (user's own words)

1. "what memecoin paired with COIN that trending recently?"
2. "how can i LP in memecoin pair tokenized stock in base chain?"
3. "what is memecoin launcpad on base chain that have more deploy tokens currently?"

---

## WITH-SKILL RUN (archived 2026-09-07, all live pulls this session)

### Q1 — what memecoin paired with COIN that trending recently?

**None — a verified negative, not a gap in the scan (as of 2026-09-07).**

- COINc is Coinbase Global's tokenized stock on Base (B20 standard, issued by Coinbase, registry address `0xb200…3ecfb`).
- The only honest way to answer "memecoin paired with COIN" is to enumerate pools containing the registry address — every pool returned then has the real stock leg by construction. Name search is unusable here (display names drift; "COIN" in a memecoin's name is branding, not a pairing).
- That enumeration returns **zero pools — not zero meme pools, zero pools of any kind**. The token-level read agrees: no price, total reserve $0. An onchain `name()`/`symbol()` read confirms the address is the genuine COINc, so this is not a bad address.
- Sanity control: the same check on TSLAc returns price $353.23 and ~$109k of reserves — the method works; the emptiness is COINc-specific.
- Why it's empty: this genre swarms around a stock's own book. Where a stock has its own USDC/WETH book, memes cluster (NVDAc ~12 meme pools on a ~$2.5M book; SPCXc ~11 within 72 hours of listing). COINc has no book yet, so there is nothing to pair against and no swarm.
- If your screener shows something "paired with COIN": two traps — (a) name-only confusion, a memecoin calling itself COIN-adjacent; (b) address vanity-squatting — one memecoin has already ground the `0xb200…` prefix shared by all thirteen real B20 tokens. The registry address is the only tie-breaker.
- Next check: re-run the enumeration once COINc gets a main USDC pool. In this genre the first meme pools follow a book within days.

### Q2 — how can i LP in memecoin pair tokenized stock in base chain?

This skill is read-only — it never constructs, signs, or walks through a transaction. What it can do is tell you what the position is, what to verify before it, and which numbers to rebuild:

**What the position is.** You deposit both legs (memecoin + stock token) in ratio into an AMM pool, earn swap fees, and take impermanent loss. In a meme/stock pair this is not ordinary LP:

1. **It is short options on the meme/stock spread.** If the meme runs, the pool mints meme against your stock reserve — you end up heavier in meme exactly at the top. If the meme dies, the fee income dies with it. The carrot is paid in the risk asset.
2. **The legs run on different clocks.** The stock leg prints on market sessions and depegs on weekends (its last confirmed print is Friday's close); the meme leg trades 24/7. The weekend gap lands in your pool first.
3. **The hook decides more than the fee tier.** Launch pools are Uniswap v4-style pools with the launchpad's hook — the hook can control fees, block adds/removes, and take at settlement. The fee tier on these pools is not a static number a screener shows; demand the hook's permission mask from the launchpad's docs (o1 Exchange — o1.exchange/docs; bankr — bankr.bot/docs; Flaunch — flaunch.gg/docs; all verified live 2026-09-07).
4. **No vault layer exists for meme pairs.** Beefy's stock vaults cover only the four stock/USDC main pools — LPing a meme pair is a manual position with no auto-compounder.
5. **Rebuild the yield legs dated, in order:** fee flow = volume × fee tier ÷ reserves (tier unknown → demand it, don't assume); incentives — verify payer and end date, none verified in this genre; IL — the session-clock kind above; costs — gas plus any hook take.

**Before depositing (the short checklist):** stock leg verified by registry address; hook permissions read or demanded; reserves read (never the FDV sticker — it swung 5x within one day on the same pool this week); lifecycle stage checked — a graduated meme moves its main book to its own USDC pool, and the stock-paired pool you'd be LPing may be the abandoned one; weekend exposure stated; exit sized against reserves.

Live context, dated 2026-09-07: the biggest meme/stock book is BLUECHIP/NVDAc (o1) — ~$800k/day volume on ~$509k reserves, meme leg −5% on the day while the NVDAc/USDC book moved +0.08%: genre bleed, not a stock repricing.

Research, not financial advice — no transaction is constructed here.

### Q3 — what is memecoin launchpad on base chain that have more deploy tokens currently?

**o1-launchpad — o1 Exchange (o1.exchange) — by a wide margin, within the only universe verifiable without keys (2026-09-07).**

- The countable universe is pools paired with registered B20 stock tokens, enumerated by address: ~37 meme pools across the three enumerated stocks (NVDAc ~12, SPCXc ~11, AAPLc ~14). o1 dominates roughly two-thirds of them, including SPCXc's entire launch swarm. bankr is second (IPOD, PrinterInkCoin).
- Base's official B20 ecosystem announcement (2026-08-24) names exactly three launchpad-type venues: o1 ("01 Exchange"), bankr, and Flaunch. Flaunch has zero stock-paired pools observed so far.
- Direct AMM launches (Uniswap v3/v4 without a launchpad — KUMA, BLAPE, JACKET) are the third path: a venue, not a launchpad.
- Fresh signal from today's dex listing pull: o1's top-20 active pools already include stock pairs beyond the three enumerated stocks (BLUE/METAc, BRTC/MSTRc) — the genre is spreading, and a full count means re-enumerating per stock.
- Honest scope: **total platform-wide deployments** (all memecoins, not just stock pairs) are not keylessly verifiable right now — the dex endpoint returns only the top-20 active pools. If someone quotes "launchpad X has deployed N tokens total," ask for the source. Within the verifiable slice, o1 leads.
- And "most deployed" is not "best": the rubric's checklist (hook permissions, pool age, reserves) decides whether any given pool is touchable, not the launchpad's deployment count.

---

## Post-run verification notes (2026-09-07)

- The COINc zero-pool finding was double-checked: onchain `name()`/`symbol()` ("Coinbase Global Inc." / "COINc") confirms the address; TSLAc ($353.23, ~$109k reserves) confirms the method.
- ~~GeckoTerminal's dex-pools endpoint returns top-20 active only, no pagination~~ **CORRECTED same day**: the endpoint paginates with an explicit `?page=` even when the response's next-link is null. The baseline run used it (~80 o1 pairs over four pages). Trust page walking, not the link field.
- The o1 dex listing revealed stock pairs on METAc and MSTRc not present in the 2026-09-07 morning enumeration (which covered NVDAc/SPCXc/AAPLc only) — the genre's universe is wider than the ledger's three stocks.

## AMENDMENT — the wrapper surface (found by the user + the baseline run, 2026-09-07; shipped as v0.9.0)

The Q1 answer above is correct about COINc the registry token and wrong about where the COIN-paired meme action actually lives. The user checked basestonk.io — a launchpad not in Base's official ecosystem article — and found pairs against **wtCOIN**, not COINc. Verified by hand:

- wtCOIN = "Wrapped Coinbase Global Inc **ST0x**" at `0x5cDa0E1CA4ce2af96315f7F8963C85399c172204` (onchain name/symbol read; supply ~1,343). One of an eleven-token 1:1-backed family (wtCOIN, wtNVDA, wtMSTR, wtSPCX + wtSGOV/wtSKHY/wtSPYM/wtDRAM/wtQQQM/wtIAU/wtCEG) per docs.basestonk.io's Pairs page.
- Live wrapped-leg meme pairs found via search: BALD/wtCOIN (~$247k/day), CDAQ/wtCOIN (+74% on the day), GAYBASE/wtCOIN (bankr, launched 2026-09-06) [baseline findings, spot-verified for BALD via pool search].
- Why the wrapper family exists at all: BaseStonk's docs state most of the 13 B20 tokens had no on-chain market (per their docs, only NVDAc/GOOGLc/AAPLc/METAc traded live pools) — buyers "must already hold the stock, and ETH cannot route into them." The wrapper gives the other names DEX liquidity.

**The lesson, now shipped in the rubric (v0.9.0):** registry-address enumeration is verification by construction *for native legs only* — it is blind to wrapped legs by design. A "paired with COIN/NVDA/SPY" question must first ask which token: native B20 or wrapped wt-\*. A wt-leg is a separate claim stack (wrapper issuer, 1:1 backing, unknown-tier corporate-action behavior), not an impersonation by default. Gating case 18 added; `basestonk-launches` route added (keyless per-launchpad API); manifest rows `basestonk-launchpad` added.

## PAIRED GRADING (2026-09-07)

Graded against the degen-case assertions (15/16/17 adapted), both runs by the same rubric. Honest scores:

| Q | With-skill | Baseline (no skill) | Notes |
|---|---|---|---|
| 1 (trending memes on COIN) | **partial** | **strong** | The skill's verified negative was true for COINc-native but incomplete: it did not know the wrapped surface existed, so it answered a narrower question than asked. The baseline found wtCOIN, identified the family, and ranked the actual pools (BALD, CDAQ). The skill's traps (name-only, vanity-squat) remain valid, and its dated/verified discipline held — but on discovery it lost. Fixed in v0.9.0. |
| 2 (how to LP a meme/stock pair) | **strong** | **partial** | The skill decomposed (short-options framing, two clocks, hook control, no vault layer for meme pairs, dated live context) and stayed read-only. The baseline gave execution steps (buy both legs, pick a range, add liquidity) with correct IL warnings but no decomposition of what the yield legs are, and conflated wtCOIN with "the stock." |
| 3 (which launchpad deploys most) | **partial** | **strong** | Both correctly named o1. The skill's honesty flag ("platform-wide counts not keylessly verifiable") was factually wrong — the dex endpoint paginates, and the baseline walked it (~80 o1 pairs) plus found bankr's wt-surface detail. The skill's caveat "most deployed ≠ best" remains the right discipline. Corrected in v0.9.0. |

**Verdict:** the batch did its job — it caught a structural blind spot (wrappers), a wrong endpoint assumption (pagination), and a venue outside the official list, exactly the way the normie batch caught a dead route. The skill's core disciplines (dated numbers, claim-stack separation, read-only, decomposition before judgment) all held; its *universe knowledge* was beaten by a general agent with a search box. The fixes are universe-level: wrapper surface, launchpad API route, non-exhaustive-list lesson. Assertion-level scores for the archive: with-skill 9/15, baseline 10/15 — the baseline edges it on this batch, which is the honest result and the argument for the v0.9.0 fixes.

## INDEPENDENT BLIND GRADING (2026-09-07)

Second grader, anonymized A/B, no knowledge of which set was which. Mapping (disclosed after grading): Q1 A=skill/B=baseline; Q2 A=baseline/B=skill; Q3 A=baseline/B=skill.

| Q | Skill | Baseline | Blind grader's decisive notes |
|---|---|---|---|
| 1 | 3/4 | 3/4 | Tie. Skill scored the identity/trap/dating assertions but 0 on ranking ("asserts zero pools exist, does not rank any"); baseline ranked live pools but "gives the address but no trap warning." |
| 2 | **4/4** | 2/4 | Skill sweep: baseline missed both the market-clock assertion and the hook-control assertion. |
| 3 | 4/4 | 4/4 | Tie — both named o1 with evidence, both honest about scope, neither treated count as quality. |
| **Total** | **11/12** | **9/12** | — |

**De-anonymized verdict.** The blind grader's overall call ("B answers the trader better, decisive margin is Q2") de-anonymizes to: the skill's structured read (Q2: short-options framing, clocks, hook, legs) is the decisive win, Q1 and Q3 tie. This is consistent with the self-grading's substance while flipping its headline: self-grading (15-assertion format, weights discovery heavily) had baseline 10/15 vs skill 9/15; blind grading (12-assertion format) has skill 11/12 vs baseline 9/12. The two passes agree on every per-question fact: **Q1 was a genuine skill failure on universe discovery (the wrapper surface), Q2 a genuine skill win on structure, Q3 a tie with one wrong endpoint assumption on the skill side (dex pagination), now corrected.** The v0.9.0 fixes target exactly the lost assertions: the wrapper surface (case 18), the launchpad census route, and the pagination correction.

Dogfood verdict: the batch earned its keep — it cost one question to find a structural blind spot, and the fix ships the same day.

---

## VERIFICATION RE-RUN — Q1 against the v0.9.0 fix (2026-09-07, post-fix, same day)

Purpose: the blind grader's Q1 call was that the skill's answer was "correct about COINc-native but does not rank any" — the two lost assertions were wrapper discovery and ranking. This re-run tests whether the **shipped files** fix it, not the author's memory of the conversation.

Protocol: a fresh general-purpose agent with no conversation context, given only the files the skill's runtime routine names (SKILL.md → references/how-work.md, references/concepts.md, references/meme-pair-launchpad.md, api-routes.json, manifest.json; explicitly forbidden from reading README/DESIGN/RESEARCH/evals/examples), asked Q1 verbatim, required to pull live state. Read-only.

### Archived answer (verbatim)

**Which memecoin paired with COIN is trending?** There is no COINc-native market — the native Coinbase B20 registry token (COINc, `0xb200…3ecfb`) has zero pools on Base per GeckoTerminal as of 2026-09-07. The entire meme/stock activity sits on the **wrapped** surface: **wtCOIN** (Wrapped Coinbase Global Inc ST0x, `0x5cDa0E1…72204`), a 1:1-backed ST0x-family wrapper of COIN stock, trading at ~$187.61 as of the live pull.

Meme pairs on wtCOIN, ranked by 24h momentum (as of 2026-09-07, ~15-min delayed):

| Rank | Meme | Pool | 24h Vol (USD) | 6h Vol Share | Acceleration | Reserve (USD) | Flow (Buys/Sells) | Age | Launchpad | 24h Chg |
|------|------|------|--------------|-------------|-------------|-------------|----------------|-----|-----------|---------|
| **1** | **BALD** | BALD/wtCOIN 0.3% | **$250,575** | 31% of 24h (77k/251k) | **accelerating** | **$93,140** | 802 / 744 (52%/48%) | 15 days (Aug 23) | o1 (v4) | -1.12% |
| 2 | MEME | MEME/wtCOIN 0.3% | $55,835 | 14% (7.8k/55.8k) | fading | $42,390 | — | Aug 17 | o1 (v4) | -0.95% |
| 3 | GAYBASE | GAYBASE/wtCOIN | $41,181 | **1%** (428/41k) | **dead** | **$1,983** | **603 / 1,947 (24% buys)** | 1 day (Sep 6) | bankr | -2.52% |
| 4 | CDAQ | CDAQ/wtCOIN 1% | $36,526 | 9% (3.4k/36.5k) | fading | $28,227 | — | Aug 19 | o1 (v4) | -1.02% |
| 5 | BM | BM/wtCOIN 0.3% | $18,486 | 13% (2.3k/18.5k) | fading | $12,379 | — | 1 day (Sep 6) | o1 (v4) | -1.16% |
| 6 | SHIT | SHIT/wtCOIN 0.3% | $10,653 | 7% (753/10.7k) | dead | $15,690 | — | Aug 17 | o1 (v4) | -1.71% |

All remaining ~50 meme pools on wtCOIN have sub-$5k daily volume — the band below is $0 volume dead pools.

**BALD is the only meme currently trending on wtCOIN.** Momentum is accelerating (31% of 24h volume in the last 6 hours — well above the ~25% uniform-day baseline); flow is balanced (52% buys vs 48% sells — unlike GAYBASE which is 24% buys, distribution in progress); depth is the best in the genre at $93k reserve — 47x deeper than GAYBASE's $2k. BALD launched against wtCOIN via the o1 launchpad (Uniswap v4) on 2026-08-23; at 15 days old it is past the initial swarm window, and the graduation check (its own USDC/WETH pool) belongs in the next check, since the stock-paired pool ranked here may no longer be its main book. GAYBASE is the newest launch (bankr, Sep 6) but already in post-launch distribution: 1% 6h share, 24% buys, sub-$2k reserve — do not confuse "recently launched" with "trending."

Stock-leg context: wtCOIN itself tracked ~$187.61 (2026-09-07), own USDC books (Aerodrome, Uniswap, hydrex) doing a combined ~$456k/24h across ~$230k reserves; every meme pair was down ~1–2.5% on the day while the stock leg moved roughly 0% — genre bleed, not a COIN repricing.

Claim-stack twist: wtCOIN is a wrapper claim on Coinbase Global stock — 1:1-backed ST0x token with its own issuer, custody chain, and unknown-tier corporate-action behavior; what a B20 multiplier update does at the wrapper layer is undocumented until exercised. The stock leg does not trade weekends; the meme trades Saturday night against a stale peg. Hook permissions remain the load-bearing factory-layer question this screen cannot answer.

Checks before any position: hook permission mask (o1 docs) for the BALD/wtCOIN pool; graduation check for BALD's own USDC/WETH pools; wtCOIN backing mechanism (1:1 mint/redeem, custodian) before treating it as a COIN proxy; weekend gap exposure; BALD's contract verified against the pool's base_token address, not by name.

Research, not financial advice — the base rate of thin-reserve launch pools under two weeks old is itself the headline risk.

### Pull log (verbatim)

1. `GET https://docs.base.org/base-chain/asset-issuance/tokenized-stocks-on-base/` — 200; B20 token address table: COINc = `0xb200000000000000000000c85a31389D71F3ecfb`.
2. `GET api.geckoterminal.com/…/base/tokens/0xb200…3ecfb/pools` — 200; `{"data":[]}` — COINc-native zero pools.
3. `GET …/base/tokens/0x5cDa0E1CA4ce2af96315f7F8963C85399c172204/pools?include=base_token,quote_token&page=1` — 200; 20 pools (BALD/wtCOIN $250k vol24 + MEME, CDAQ, BM, SHIT, GAYBASE, wtCOIN own books).
4. Same endpoint `page=2` — 200; 20 pools (CLARK, ARMSTRONG, COIN/wtCOIN, WORTH, STONKS… all sub-$1k).
5. Same endpoint `page=3` — 200; 20 pools ($0 dead pools).
6. `GET …/base/tokens/0x5cDa…72204` — 200; wtCOIN $187.61, ~$935k aggregate 24h volume.

### Grading — the blind grader's four Q1 assertions

| Assertion | v0.8.2 with-skill run | v0.9.0 re-run (fresh agent, files only) |
|---|---|---|
| Identity/traps (registry verification; native vs wrapped distinguished; name-drift) | earned | earned — native address resolved from the official registry page, enumerated by address; wrapper walked as its own claim stack |
| Ranking of live pools, dated | **lost** ("asserts zero pools exist, does not rank any") | **earned** — six pools ranked in a dated table; BALD named trending on three separate signals |
| Trending method (momentum/flow/depth/age, not volume alone) | implied | earned explicitly — 25% h6 baseline, 24%-buys distribution read, reserve depth comparison (47x), 15-day age vs swarm window, graduation check, genre-bleed attribution |
| Dating discipline | earned | earned — as-of stamps, delayed-print note, dated pool ages |

**Verdict: 4/4 — both previously lost assertions are earned by an agent that read nothing but the shipped skill files.** The path taken to the wrapped surface was the wtCOIN contract address written into the `meme-stock-pools` route notes (GeckoTerminal enumeration by address), not the `basestonk-launches` route — both are sanctioned by the rubric; the basestonk live endpoint remains unexercised. The fix is verified; the skill no longer answers a narrower question than asked.

### New dated facts contributed by the re-run (2026-09-07, evening)

- The wrapped surface is **larger than the entire native genre**: ~60 pools on wtCOIN across three pages, vs ~37 native meme pools across three stocks. Six live books: BALD $250.6k (h6 share 31% = accelerating; 802/744 buys/sells; $93.1k reserves; created 2026-08-23; o1 v4), MEME $55.8k, GAYBASE $41.2k (bankr, 2026-09-06; h6 share 1%, buys 24%, $2.0k reserves — the distribution-read example), CDAQ $36.5k, BM $18.4k, SHIT $10.7k; the tail is sub-$5k dead pools.
- wtCOIN itself: $187.61; own USDC/WETH books ~$456k/24h on ~$230k reserves (Aerodrome, Uniswap, hydrex).
- The re-run resolved the native leg from docs.base.org's registry table (COINc `0xb200…3ecfb`) — consistent with the onchain `name()`/`symbol()` verification from the morning run.
