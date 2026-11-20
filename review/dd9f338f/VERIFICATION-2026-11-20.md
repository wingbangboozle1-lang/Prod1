# Verification record — session arena/dd9f338f-prod1 (2026-11-20)

Scope claimed in `COORDINATION.md` (T-DD9-1, T-DD9-2): close open register gaps from the
official listings, re-read the policy sources, and record what was and was not re-verified.
Every quoted value below was read directly from the fetched official page in this session —
nothing was inferred, and nothing was copied from another session's notes.

Fetch method note: this sandbox's `curl` reaches only GitHub/npm/pypi hosts. Amazon.com,
affiliate-program.amazon.com, developers.google.com and ftc.gov were read through the page
fetch tool. Amazon detail pages redirect the fetcher to Amazon's "Product Summary"
(`plpRedirect=mhFallback`) view, which exposes title, ratings, price block, About-this-Item
bullets, Product Description, options, documents and reviews — but **not** the
"Product information" spec tables.

## 1. The five listings — line-by-line against `data/products.json`

### P1 — CHEFMAN 6 Quart Dual Basket Air Fryer Oven (B0CDY277D3)

Source: https://www.amazon.com/dp/B0CDY277D3 (fetched 2026-11-20, chunks 0, 19, 20)

- **Title** — page `<title>` reads exactly *"CHEFMAN 6 Quart Dual Basket Air Fryer Oven with
  Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher
  Safe Frying Baskets, Digital Double Air Fryer - Black"*. Matches register character for
  character. ✅
- **Price block** (Product Summary, chunk 19): *"One-time purchase: $79.93 ( $39.97 / count )
  20% Savings — List Price: $99.99"*. Matches register (`priceNew` $79.93, `priceList`
  $99.99). **No "Deal ends" line on this listing** — unlike P2/P4/P5, this price is not shown
  as a limited-time deal today. ✅
- **Rating block** (Product Summary, chunk 19): *"4.2 out of 5 stars, 4,878 ratings"* —
  register said 4,877 (read 2026-11-20 by session 1b65e5a1). Count moved +1 during the day.
  Register updated to **4,878** with today's date. This is the FLG-024 drift pattern; the
  register is a dated snapshot by design.
- **Wattage / warranty / model** (Product Description, chunk 20): *"cETL approved with
  advanced safety technology for long-lasting durability, & 1-year assurance provided by
  Chefman. 120 Volts/1700 Watts"* and *"Purchase includes a 1-year assurance from Chefman"*
  and *"120 Volts/1700 Watts –RJ38-SQPF-3TDB-2W"*. Matches register (`wattage`, `warranty`,
  bullets). ✅
- **Bullets** (About this Item, chunk 19): dual baskets, dual zone, Sync Finish, 200–450°F,
  viewing windows, dishwasher-safe non-stick baskets. Matches register bullet list. ✅
- Volume metric: *"300+ bought in past week"* (summary view). Register records
  *"1K+ bought in past month"* (standard buy-box metric, different window — no contradiction;
  both kept out of shop pages).

### P2 — Emeril Lagasse 26QT French Door (B09B7SB46R)

Source: https://www.amazon.com/dp/B09B7SB46R (fetched 2026-11-20, chunks 0, 1, 13)

- **Title** — page `<title>` reads exactly the register title (26QT French Door
  Multi-Function Air Fryer Toaster Oven, 24 One-Touch Preset Options, Six Cooking
  Accessories Included). ✅
- **Price block** (Product Summary, chunk 13): *"One-time purchase: $149.99 — 29% Savings —
  List Price: $209.99 — **Deal ends: 1796198399000**"*. Price matches register. The current
  price **is a limited-time deal** ending **2026-12-02 07:59 UTC** (epoch converted).
  **New observation** recorded in the register source note. The site publishes no promotion
  references, so this only affects when the snapshot must be re-read, per Participation
  Requirements §2(b) ("You must remove from your Site any links and related references to
  limited time promotions as soon as that promotion on the relevant Amazon Site ends." —
  read verbatim today, see §3 below).
- **Rating block**: *"4.3 out of 5 stars, 18,380 ratings"* — matches register exactly. ✅
- **FLG-002 (preset count) re-confirmed live:** title says *"24 One-Touch Preset Options"*,
  Product Description says *"24 one-touch cooking presets"*, but the About-this-Item bullet
  says *"25 COOKING PRE-SETS"*. The listing still disagrees with itself. Both values remain
  published side by side in the register. ⚠
- **FLG-021 (accessory count) re-confirmed live:** title says *"Six Cooking Accessories
  Included"*, Product Description says *"Included are 7 premium accessories"* — air fry
  basket, rotisserie spit, bake pan, and more. Both values remain published. ⚠
- **FLG-005 (warranty term) — attempted again:** the Product Guidance & Documents section
  (chunk 13) lists only *[User Manual (PDF)]*; no warranty term appears anywhere in the
  fetched view. Stays blank + flagged. The register's 2026-11-19 note about a warranty PDF
  link is consistent (view differs day to day; neither view states a term). ⚠ open

### P3 — Chefman 8 Qt TurboFry (B08DKYBTPH)

Source: https://www.amazon.com/dp/B08DKYBTPH (fetched 2026-11-20, chunks 0, 15)

- **Title** — page `<title>` includes the ® glyph: *"Chefman Air Fryer 8 Qt | TurboFry®
  4-in-1..."*. Register omits the glyph (noted 2026-11-20 by session 46e39d18; immaterial,
  left as-is rather than silently edited). ✅
- **FLG-022 (wattage conflict) re-confirmed live:** Product Description (chunk 15) ends
  *"cETL approved with advanced safety technology for long-lasting durability and a 1-year
  assurance provided by Chefman. 1700W/120V"* — while the register's bullets record the
  listing's 1000 Watts / 120 Volts (model RJ38-SQSS-8T) from the bullet set. The listing
  still carries two wattage figures; the register still shows both. ⚠
- **Newer-version pointer matches FLG-003:** *"Newer Version Available: Chefman Air Fryer –
  6 QT Compact ... $59.99 , 4.6 out of 5 stars, 7,601 ratings"* (B0CNY1YVDD). ✅
- **Options** (chunk 15): Size 6 / 8 / 9 quarts; Color Black / Stainless steel. Matches the
  register bullet about available sizes/colors. ✅
- **New observation:** Important Information section carries a **California Proposition 65
  warning** for acrylamide with the www.P65Warnings.ca.gov link. Not previously recorded in
  the register; recorded here only (register row untouched — the shop pages correctly carry
  no such claim).
- Rating/price were not re-captured today beyond the title page (register's 2026-11-20
  values from session 1b65e5a1 stand; buy box was not displayed in the chunks fetched).

### P4 — ThermoMaven 1 Sec Instant-Read (B0DHZTCNR5)

Source: https://www.amazon.com/dp/B0DHZTCNR5 (fetched 2026-11-20, chunks 0, 5, 10, 14,
17, 18, 19; plus variant URLs `?th=1&psc=1` and slug URL — all serve the same
Product Summary view)

- **Title** — matches register exactly. ✅
- **Price block** (Product Summary, chunk 18): *"One-time purchase: $16.99 — 26% Savings —
  List Price: $22.99 — **Deal ends: 1796111100000**"*. Matches register ($16.99 / $22.99).
  The price **is a limited-time deal** ending **2026-12-01 07:45 UTC**. **New observation**
  recorded in the register source note. ⚠ NEW
- **Rating** (reviews + summary): *"4.6 out of 5 stars, 3,499 global ratings"* — matches
  register exactly. ✅
- **Bullets** (About this Item, chunk 18): NIST certification for ±0.5℉ accuracy,
  thermocouple sensor 1-second readings, LED screen brightness, waterproof/rinse-clean,
  motion-activated wake/sleep, auto-rotating display, stocking-stuffer positioning. Matches
  register bullets. ✅
- **FLG-004/072 (dimensions) — attempted to close today:** the Product Summary view exposes
  no dimensions. Tried the plain URL, `?th=1&psc=1` variant and the slug URL; the fetcher
  always lands on the same fallback view, which has no Product Information tables.
  Dimensions stay **blank + flagged**. ⚠ open
- **New observation:** *"Newer Version Available"* block points to the Orange variant
  **B0GL7Z4KP4** at $16.99, 4.7★, 144 ratings, In Stock. Recorded here only.
- In Stock, shipped/sold Amazon (buy box area, chunk 0). ✅

### P5 — CHEF iQ Sense, 3 probes (B0DZFD6R9Z)

Source: https://www.amazon.com/dp/B0DZFD6R9Z (fetched 2026-11-20, chunks 0, 19)

- **Title** — matches register exactly. ✅
- **Price block** (Product Summary, chunk 19): *"One-time purchase: $119.99 ( $40.00 /
  count) 45% Savings — List Price: $219.99 — **Deal ends: 1796111999000**"*. Matches
  register (3-probe variant, $119.99 / $219.99). The price **is a limited-time deal** ending
  **2026-12-01 07:59 UTC**. ⚠ NEW
- **Rating**: *"4.2 out of 5 stars, 2,178 ratings"* — matches register exactly. ✅
- **Bullets** (About this Item, chunk 19): 4 internal + 1 ambient sensor (title's "5
  sensors" broken out the same way the register records it), 1000°F heat endurance, WiFi
  unlimited range, hub charges all three probes simultaneously, *"up to 50 hours on a full
  charge"*, *"two-year assurance provided by CHEF iQ"*. ✅
- **NEW intra-listing conflict found today:** the Product Description (same chunk) says
  *"you can get up to 70 hours of usage on a full charge"* and the spec list repeats
  *"70+ hours of probe use on a full charge"* — while the About-this-Item bullet says *"up
  to 50 hours on a full charge"*. The listing disagrees with itself (50 vs 70 hours).
  Recorded in the register source note + COORDINATION request (the FLG register itself
  lives in `build_site.py`, claimed by other active sessions this hour). ⚠ NEW
- **FLG-004/072 (dimensions):** no dimensions in the fetched view; stays blank + flagged. ⚠ open

## 2. Register changes made in `data/products.json` (only fields actually read)

| Field | Change | Evidence |
|---|---|---|
| P1 `ratingCount` | 4,877 → **4,878** | Product Summary rating block, chunk 19, fetched 2026-11-20 |
| P1 `sourceNote` | appended today's re-read line (price $79.93/list $99.99, no deal flag, wattage/warranty/model re-confirmed) | chunks 19–20 |
| P2 `sourceNote` | appended: price is a limited-time deal ending 2026-12-02 07:59 UTC; preset + accessory conflicts re-confirmed live; documents list shows User Manual PDF only | chunk 13 |
| P4 `sourceNote` | appended: price is a limited-time deal ending 2026-12-01 07:45 UTC; rating/bullets re-confirmed; dimensions still absent from the fetched view; newer Orange variant B0GL7Z4KP4 noted | chunks 0, 18, 19 |
| P5 `sourceNote` | appended: price is a limited-time deal ending 2026-12-01 07:59 UTC; rating/bullets/warranty re-confirmed; **50-vs-70-hour conflict found**; dimensions still absent | chunk 19 |

No other field was changed. Nothing was inferred; blanks stay blank.

## 3. Policy sources re-read today (verbatim anchors)

| Source | What was read | Confirms |
|---|---|---|
| [Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) (Updated: October 15, 2025; fetched 2026-11-20, chunks 0–1) | §5 verbatim: *"You must clearly and prominently state the following ... 'As an Amazon Associate I earn from qualifying purchases.'"*; §6: *"any violation of Section 5 and as specified in the Program Policies will be deemed a material breach"* | The site's disclosure strip uses the exact §5 sentence; FLG-021 variant concern does not apply to the current wording |
| [Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (Updated: April 14, 2026; fetched 2026-11-20, chunks 0, 2, 3) | Participation Requirements §1 Enrollment: *"must contain original content and be publicly available"* + third-party materials need *"significant commentary, analysis, or transformation"*; §2(a): Special Links *"must use the Associates ID we have assigned to you"*; §2(b) verbatim: prices/availability only if *(a)* Amazon serves the link with the data or *(b)* Creators API/PA API; plus the **limited-time promotion removal** sentence | Register keeps prices as dated snapshots and the shop pages publish no price/rating figures (FLG-023/032/SG-19 owner decision unchanged); no promotion references anywhere on the site (checked 2026-11-20 by grep — `guide-holiday-deal-check.html` explicitly makes none) |
| [Google — Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) (Last updated 2025-12-10; fetched 2026-11-20) | *"Mark links that are advertisements or paid placements ... with the `sponsored` value."*; *"You may specify multiple `rel` values as a space- or comma-separated list."* | Site's `rel="sponsored nofollow noopener"` pattern |
| [FTC — Endorsement Guides: What People Are Asking](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) (fetched 2026-11-20) | Endorsements *"must be honest and not misleading"*; connections a significant minority wouldn't expect *"should be disclosed clearly and conspicuously"*; guides revised 2023; Disclosures 101 referenced as official short guidance | Disclosure placement + no un-tried experience claims on the site |

## 4. What this session did NOT re-read (honest scope)

- P3 buy-box price and rating count were not re-captured (the register's 2026-11-20 values
  from session 1b65e5a1 stand; the fetched chunks today did not include that listing's price
  block).
- P1's rating-count neighbors (P2/P4/P5 ratings) matched exactly; P1's count moved +1.
- The 7 remaining open gate decisions in `decisions.html` and owner-login items (Special
  Link test FLG-001, analytics host SG-03, domain SG-02, photography SG-04) are unchanged.

## 5. Irregularities found/confirmed this session

1. **Deal-priced snapshots (P2, P4, P5)** — current prices end 2026-12-01/02 UTC. The
   register is a dated snapshot by design and the site publishes no promotion references
   (checked), so no compliance issue on the site; the practical consequence is that the
   register prices must be re-read after the window ends. Logged as a new flag request
   (FLG-073) in COORDINATION — the flag table lives in `build_site.py`, owned by active
   sessions this hour.
2. **P5 battery-life conflict (50 vs 70 hours)** — new intra-listing conflict; both values
   recorded in the register source note; FLG row update requested via COORDINATION (FLG-074).
3. **P1 rating-count drift (+1)** — updated register value with today's date (FLG-024
   pattern).
4. **FLG-002 / FLG-021 / FLG-022 / FLG-004/072 / FLG-005** — all re-checked live; all stay
   open exactly as recorded; no silent fixes.
