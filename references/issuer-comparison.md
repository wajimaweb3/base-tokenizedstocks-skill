# Same underlying, N claim stacks: comparing issuers per layer

The question "dNVDA or NVDAc — which should I hold" is malformed. There is no ranking; there are **N claim stacks** for one underlying — three for NVDA as of 2026-09-08: a Dinari dShare, a Coinbase B20, and an ST0x wrapper — and each stack answers the ownership question differently at every layer. The comparison is per layer, and the verdict is the **weakest link per holder goal**, never "which is best". A row that says "X is better" has skipped the work; a row that says "for goal G, stack X's weakest layer is L, stack Y's weakest layer is M" has done it.

## The row set — what to record per stack

Read every stack down this list, dated. Skipping a row is itself a finding (write "no keyless route verified — issuer-gated" rather than leaving it blank).

1. **Legal claim and issuer status.** What the token legally is, who issues it, and whether the issuer is active, legacy, or off-Base. (`claim-stack.md`, `manifest.json`.)
2. **Custody chain.** Who physically holds the share, in what legal structure, and how bankruptcy-remote that structure is. The custody row is where the stack's risk lives first.
3. **Mint and redeem access.** Who can create and destroy the token, and at what gate. This is also the peg's restoration path — see entry 3 of `onchain-basis.md`. AP-only, KYC'd issuer sessions, and open mint are three different mechanisms.
4. **Eligibility and where it is enforced.** Who may hold, and whether the enforcement sits at the contract (policy scopes) or only at the issuer's gate. (`eligibility-custody` route.)
5. **Corporate-action mechanism and its evidence tier.** USD+ push distribution, B20 multiplier, wrapper pass-through — each with a tier (verified print / terms-only / unknown). On Base every dividend mechanism is terms-only or unknown as of 2026-09-08 (`corporate-action.md`); the comparison is between tiers of unexercised mechanisms, which is itself the finding.
6. **Where it trades.** Issuer order sessions, permissionless DEX pools, or both — and which tickers actually have a live book. This row gates every liquidity claim that follows: a stack with no permissionless book has its price on the issuer venue, and an empty pool enumeration is a finding about where the market lives, not proof the product is dead.
7. **Float, reserves, volume.** The onchain depth at your size, read from `reserve_in_usd` and `normalized_total_supply` (the token endpoint; see `onchain-basis.md` for keys). Thin reserves here make every other row's verdict conditional on exit.
8. **Price fidelity.** The basis against the underlying, and where a wrapper is involved, the basis against the native token. (`onchain-basis.md`.)

## Worked example — NVDA, three stacks, 2026-09-08

| Layer | dNVDA (Dinari dShare) | NVDAc (Coinbase B20) | wtNVDA (ST0x wrapper) |
|---|---|---|---|
| Legal claim | dShare, Dinari-issued | B20 beneficial claim, "1:1 against a real share" | "Wrapped NVIDIA Corporation ST0x", 1:1-backed per wrapper docs |
| Custody | consolidated in-house (brokerage, settlement, custody, compliance by Dinari) | Alpaca, regulated broker & custodian, bankruptcy-remote under ADGM | wrapper backing — walk wrapper docs (unknown in this pack) |
| Mint/redeem | issuer sessions, KYC'd | AP-only, KYC'd Authorized Participants; secondary permissionless | wrap terms (not documented here) |
| Eligibility | regional-requirements/restrictions pages; enforced at issuer gate | ex-US only; enforced at contract via B20 policy scopes | per wrapper terms |
| Corporate action | USD+ push distribution (Base pipe **staging**, terms-only); splits halt-rebase-verify-resume; mergers manual triage | multiplier (dividends → shares); **terms-only**, 13/13 read 1.0 on 2026-09-07 incl. names past ex-dates | **unknown tier** — no documented mechanism (v0.9.0 finding) |
| Where it trades | Dinari order sessions (Regular/Extended/Overnight + 24/7 Open subset, 9 tickers incl. NVDA; page updated 2026-08-11); no permissionless DEX book on Base | permissionless DEX — which B20 trade live is session-derived (route `token-price`, enumerate registry → check books); 2026-09-08 snapshot: 4 of 13 (NVDAc, GOOGLc, AAPLc, METAc; BaseStonk doc) — re-derive | ~5 DEX books (Aerodrome Slipstream, hydrex ×2, uni-v4, + bankr meme legs); Chainlink-priced (96h staleness refusal) |
| Float / reserve / vol24 | price/mcap/vol24 keyless via CoinGecko (dshare-price route), but no onchain depth — no DEX book, reserve absence stated | 13,731 / $1.58M / $6.79M | 280 / $14.0k / $6.6k |
| Price fidelity | reference basis vs underlying via CoinGecko (dshare-price route) — a reference print, not an onchain print | basis +0.71% vs Friday close (2026-09-08) | basis +0.47% vs underlying, −0.25% vs NVDAc; live cross market NVDAc/wtNVDA 0.05% hydrex (created 2026-08-26, $4.1k reserve) |

## Absence is data

Watching the "which tokens have a market" row is itself a session fact. **The set of B20 with no onchain market flips as pools launch** — 9 of 13 read as marketless on 2026-09-08 ("buyers must already hold the stock, and ETH cannot route into them", docs.basestonk.io/stock-pairs.md), and more pools have gone live since; derive the set per session from the registry and pool enumeration (route `token-price` on each registry address). A pool enumeration that returns empty for a token is the market telling you where it lives, not proof the token is dead — but state it with a date and the token's full set, never a stale count.

Two absences are first-class findings, not gaps to fill in with a guess. **dNVDA has no permissionless DEX book on Base** (GeckoTerminal search "dNVDA" / "Dinari" on Base returns empty, 2026-09-08); its price lives on Dinari's order sessions, and the keyless read of that price is CoinGecko's reference print (the `dshare-price` route) — a reference price, not a DEX price, while the issuer's own API is keyed (X-API-Key-Id + X-API-Secret-Key, enterprise-only). State the absence with a date; do not infer liquidity that was not pulled.

## Universe discipline (screen mode)

A cross-issuer comparison is a screen, so it inherits `how-work.md`'s screen rules: state the universe explicitly (which stacks exist for this underlying, dated), state the comparison axis (per layer, never a single metric), and flag the noise (terms-only mechanisms, thin reserves, stale prints, unknown-tier wrapper rows). "Which NVDA token should I look at" is a universe question before it is a verdict question — enumerate the stacks first (`meme-stock-pools` route for the native and wrapped legs; `token-price` for the onchain print; the `dshare-price` route for the dShare reference print), then compare.

## Verdict shape — weakest link per goal

No column wins the table. Each holder goal reads a different row as the gate:

- **Weekend or 24/7 exit** → the stack with a permissionless book (NVDAc; wtNVDA on a far thinner book). dNVDA's 24/7 Open session is an issuer venue, not a pool — exit goes through Dinari.
- **Dividend capture** → the stack whose mechanism has the highest evidence tier. On Base every dividend mechanism is terms-only or unknown as of 2026-09-08, so the row reads as a tie at "unexercised" — itself the finding, and the reason `corporate-action.md` sweeps this per ex-date.
- **Custody documentation** → the stack with a named, bankruptcy-remote custodian (NVDAc → Alpaca/ADGM). dNVDA's custody is consolidated but in-house; wtNVDA's backing is unknown-tier in this pack.
- **Permissionless entry** → the stack with no gate at the secondary (NVDAc, wtNVDA). dNVDA entry is KYC'd at the issuer.

The verdict names the gate per goal; it never collapses three stacks into a recommendation. Close with the follow-up questions the user should carry: which goal dominates, which row's evidence tier is closest to flipping (a B20 multiplier above 1.0 after the next ex-date), and which absence (a dShare onchain book, a wrapper corporate-action doc) the user should re-check before acting.
