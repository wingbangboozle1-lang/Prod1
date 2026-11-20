# Verification record — session arena/03ccc2ca-prod1 (2026-11-20)

Line-by-line re-verification of what this session publishes. Every row below was read
**in this session** from the official page named, fetched 2026-11-20. Anything not
re-read here is labelled "carried" with its session and date — never presented as
re-verified here. Nothing is inferred; where a value could not be read it stays blank
and flagged.

## 1. Product identification fields (Amazon.com listing pages, fetched 2026-11-20)

| Field | P1 Chefman 6QT Dual | P2 Emeril 26QT | P3 Chefman 8QT TurboFry | P4 ThermoMaven | P5 CHEF iQ Sense |
|---|---|---|---|---|---|
| ASIN page resolves to recorded ASIN | ✓ B0CDY277D3 | ✓ B09B7SB46R | ✓ B08DKYBTPH | ✓ B0DHZTCNR5 | ✓ B0DZFD6R9Z |
| Listing title matches `data/products.json` | ✓ exact | ✓ exact | ✓ match, typographic note A | ✓ match, typographic note B | ✓ exact |
| Buy box re-read this session | ✓ $79.93, In Stock, ships/sold Amazon.com | not re-read (carried: fbfe1742, 2026-11-20 "title confirmed"; buy box $149.99 carried from 2ec8638e, 2026-11-19) | not re-read (carried: 963ca90f, 2026-11-20 title match) | ✓ $16.99, In Stock | not re-read (carried: 1b65e5a1, 2026-11-20) |
| Sources | https://www.amazon.com/dp/B0CDY277D3 | https://www.amazon.com/dp/B09B7SB46R | https://www.amazon.com/dp/B08DKYBTPH | https://www.amazon.com/dp/B0DHZTCNR5 | https://www.amazon.com/dp/B0DZFD6R9Z |

- **Typographic note A (P3):** the listing title shows "TurboFry® 4-in-1"; the register
  stores "TurboFry 4-in-1" (registered-mark glyph dropped). Character-for-character
  identical otherwise. Recorded as a normalization, not a data error. Source (above).
- **Typographic note B (P4):** the listing title shows "±0.5℉" (U+2109); the register
  stores "±0.5°F" (degree sign + F). Same reading, different glyph. Source (above).
- **Dated listing observation (P1 buy box, 2026-11-20):** the listing carries the
  holiday return notice "eligible items purchased between November 1 and December 31,
  2026 can be returned until January 31, 2027." Quoted where used in seasonal content,
  attributed to the listing and dated. Source: https://www.amazon.com/dp/B0CDY277D3
- **Volatility:** prices, rating counts and badges are live figures and move between
  reads (FLG-024). Shop pages do not display them (`data/editorial.json` display rule,
  per Program Policies Participation Requirements §2 — see below); they live only in the
  verification register as dated observations.

## 2. Policy sources (fetched 2026-11-20, official)

| Item | Read this session | Result | Source |
|---|---|---|---|
| Operating Agreement — updated date | ✓ | "Updated: October 15, 2025" — matches the register | https://affiliate-program.amazon.com/help/operating/agreement |
| OA §5 disclosure sentence | ✓ | Verbatim: "As an Amazon Associate I earn from qualifying purchases." — the site's disclosure strip matches this exact sentence (first sentence of the strip) | same as above |
| OA §6(a)/§5 material-breach link | ✓ | "any violation of Section 5 and as specified in the Program Policies will be deemed a material breach" — read this session | same as above |
| Program Policies — updated date | ✓ | "Updated: April 14, 2026" — matches the register | https://affiliate-program.amazon.com/help/operating/policies |
| FTC Disclosures 101 | carried (fbfe1742 + prior sessions, 2026-11-19/20) | unchanged; disclosure placement gate (`check_site.mjs`) green in T-03E | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |
| Google Search Central — `rel="sponsored"` | carried (prior sessions, 2026-11-19/20) | unchanged; every outbound product link carries `rel="sponsored nofollow noopener"` (gate-checked) | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links |

## 3. What this session did **not** verify (stated, not hidden)

- P2/P3/P5 buy-box prices and all rating counts beyond P1/P4: carried from the dated
  same-day session records cited above. Not re-read in this session.
- The five `link.amazon` short links' redirect targets: carried from 1187e20d
  (2026-11-20). Their compliance status remains **unresolved** (FLG-001/FLG-003) —
  this record does not claim the short links are invalid or valid.
- The enrolled-Associates Special Link test (destination + tracking report): needs an
  Associates Central login no sandbox session has (FLG-001). Blocks nothing in the
  publish per the brief.
- P5 dimension fields and P2 warranty term: still blank/flagged (FLG-004/FLG-005);
  never inferred.

## 4. Irregularities found in this pass

1. **The planned-topic list duplicates itself** (the FLG-047 trap, in a new place):
   TOPICS 06 ("Can a 26-quart oven fit on your counter?") and 11 ("Counter space math:
   will a 26-quart oven fit your kitchen?") are the same question; 09 ("basket vs oven:
   which one fits your counter?") overlaps published 01 ("Basket or oven-style: what
   should you compare?") and planned 07 ("Two baskets or one"); 12 ("Holiday air fryer
   gifts") overlaps published `guide-gift-picks.html`. Publishing these as new pages
   would put two pages on one host answering one question. Remediation in T-03B:
   consolidate the plan (each question keeps one answer), publish only the distinct
   queued questions. Owner can reverse any merge from the topic table.
2. **`data/editorial.json` queue vs `TOPICS` drift:** the queue's 2027-01-05 wattage
   topic is marked "blocked" although `guide-wattage-outlets.html` already answers it
   (published in T-2D2); queue rows and the TOPICS table carry different titles for
   overlapping questions. T-03B reconciles both to one calendar.
3. No new product-data drift found. All five titles and both read prices match the
   register (typographic notes A/B aside).
