# Review log — session arena/2d5ebe5b-prod1 (2026-11-19)

Line-by-line re-verification performed in this session by fetching each official source
page directly (Amazon listing pages, Amazon Associates Operating Agreement). Every
changed value below is tied to the fetched text; nothing was inferred.

## Official sources fetched (manual review links)

| Source | URL | What was read |
|---|---|---|
| Associates Program Operating Agreement (updated 2025-10-15) | https://affiliate-program.amazon.com/help/operating/agreement | §1 Program Content / Special Links; §5 disclosure sentence (verbatim), fetched 2026-11-19 |
| P1 Chefman 6QT Dual-Basket | https://www.amazon.com/dp/B0CDY277D3 | Buy box $79.93; List $99.99; used $59.95; rating 4.2 (4,876); dims 13.38"×11.81"×10.63"H; capacity 6 liters field; "120 Volts/1700 Watts" bullet; 1-year assurance bullet; cETL bullet; Amazon's Choice; 1K+ bought; 200–450°F range |
| P2 Emeril 26QT French-Door | https://www.amazon.com/dp/B09B7SB46R | Buy box $149.99 (Black Friday Deal); List $209.99; rating 4.3 (18,375); dims 16.9"×15.8"×14.8"H; capacity 24.6 liters field; **Product information: Wattage 1700 watts / 120 volts**; warranty = PDF link only; bullets "25 COOKING PRE-SETS" vs title "24 One-Touch"; description "7 accessories" vs title "Six Cooking Accessories" + 6 item-details components; 8K+ bought |
| P3 Chefman 8QT TurboFry | https://www.amazon.com/dp/B08DKYBTPH | Buy box $69.99 (Black Friday Deal); List $119.99; used $45.49; rating 4.4 (16,892); dims 12.75"×13.5"×10"H; capacity 8 quarts; **bullets "1000 Watts/120 Volts – RJ38-SQSS-8T" vs Product information "1700 watts"** (same-page conflict); Warranty Description "1-Year Limited Warranty"; Amazon's Choice; 3K+ bought; newer model B0CNY1YVDD ($59.99, 4.6/7,602) |
| P4 ThermoMaven Instant-Read | https://www.amazon.com/dp/B0DHZTCNR5 | Buy box $16.99; List $22.99; rating 4.6 (3,499); Specification Met: NIST, NSF; calibration certificate in included components; IP67/rinse bullets; ±0.5°F bullet; 5K+ bought; Amazon's Choice; holiday returns to Jan 31, 2027 (Nov 1–Dec 31 purchases); newer model B0GL7Z4KP4 ($16.99, 4.7/144); dimensions NOT in captured fields |
| P5 CHEF iQ Sense Wireless | https://www.amazon.com/dp/B0DZFD6R9Z | 3-probe buy box $119.99 / List $219.99 (variants: 1P $99.99/$129.99, 2P $99.99/$179.99, 4P $142.49/$249.99); rating 4.2 (2,178); bullets: 4 internal + 1 ambient sensors, 1000°F-safe, up to 50 h charge, 3 probes, "two-year assurance", dishwasher-safe probes; no ±°F figure anywhere captured; 1K+ bought; dimensions NOT in captured fields |

## Data changes made (data/products.json)

1. `site.canonical` → `https://wingbangboozle1-lang.github.io/Prod1/` (fixes the
   `build_site.py` regression that re-emitted the `example.com` placeholder; closes
   FLG-007 at the source).
2. `site.disclosure` → exact OA §5 sentence ("As an Amazon Associate I earn from
   qualifying purchases.") + the price-snapshot note. Closes I-02; publishing gate now
   reports zero disclosure warnings.
3. P2: ratingCount 18,371 → **18,375**; boughtPastMonth 7K+ → **8K+**; wattage filled
   **"1700 watts / 120 volts (Product information table)"** (was blank — FLG-005
   partially resolved); warranty filled precisely ("warranty PDF linked; no term stated
   in listing text").
4. P3: ratingCount 16,890 → **16,892**; wattage now records **both** the bullet figure
   (1000 W) and the Product information figure (1700 W) with FLG-022 reference.
5. All five `sourceNote` fields updated with the re-read provenance (2026-11-19).

No value was filled by inference. The two rating-count moves are snapshot drift on the
same day, both re-read from the live pages.

## Irregularities found in this session

- **FLG-021 (new):** Emeril accessory count conflict on one page (title/item-details 6
  vs description "7 premium accessories" / configuration "7 Accessories").
- **FLG-022 (new):** Chefman 8QT wattage conflict on one page (bullets 1000 W vs
  Product information 1700 W). Both published; neither dropped.
- **I-06 closed:** P1 $79.93 / $99.99 reproduced twice against the live buy box and the
  Frequently-bought-together block (the earlier doubt came from a $74.99 widget price
  for a *different* ASIN — FLG-016 explains the trap).
- **FLG-004 unchanged:** thermometer dimensions remain absent from listing fields.
- **FLG-001/FLG-015 unchanged:** short-link compliance and the missing `tag=` on
  redirect targets remain open manual gates; no claim made either way.

## Checks run

- `python3 build_site.py` — pages written; sponsored post-step done.
- `node scripts/check_site.mjs` — PASSED, 45 HTML files (disclosure incl. footer,
  sponsored Amazon links, internal links, unique titles/descriptions, claim wording).
  3 warnings remain for the word "trending" inside rule/disclaimer text (not claims).
- `python3 counter-check/tools/check_site.py` — PASSED (16 pages, 5 products, 21 flags).
- `python3 counter-check/tools/build_site.py` — rebuild is deterministic (R-05 closed;
  fixed BUILD_DATE constant).
- `.github/workflows/pages.yml` — now runs the publishing gate before upload (closes
  I-05 / request R-01).
