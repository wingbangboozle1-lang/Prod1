# Line-by-line verification — session arena/0f8382dd-prod1 (2026-11-20)

Integration re-verification of the combined register, per the brief ("verify line by line
from official verified trusted sources, no hallucinations") and the coordination protocol
("the final integration session … re-verifies the combined data line by line").

Everything below was fetched in this session on 2026-11-20 (UTC) through the sandbox's
page-fetch tool. Nothing is transcribed from memory. Where this session could not observe
a value directly, the entry says so and keeps the earlier dated snapshot — values are
never inferred.

Official sources read in this pass (manual-review links):

| Source | URL | Read for |
|---|---|---|
| Amazon listing P1 (Chefman 6QT dual-basket) | https://www.amazon.com/dp/B0CDY277D3 | title, buy box, list/used price, rating count, spec table, bullets |
| Amazon listing P2 (Emeril 26QT French door) | https://www.amazon.com/dp/B09B7SB46R | title, rating, buy box, list price, spec table, bullets |
| Amazon listing P3 (Chefman 8QT TurboFry) | https://www.amazon.com/dp/B08DKYBTPH | title, rating, buy box, list price, size selector, spec table, bullets |
| Amazon listing P4 (ThermoMaven instant-read) | https://www.amazon.com/dp/B0DHZTCNR5 | title, buy box, review count, spec table, bullets |
| Amazon listing P5 (CHEF iQ Sense wireless) | https://www.amazon.com/dp/B0DZFD6R9Z | title, rating, buy box, list price, variant prices, spec table, bullets |
| Associates Program Operating Agreement (Updated: October 15, 2025) | https://affiliate-program.amazon.com/help/operating/agreement | §1 Special Links definition; §5 disclosure sentence, verbatim |
| Associates Program Policies (Updated: April 14, 2026) | https://affiliate-program.amazon.com/help/operating/policies | §2(b) tag format; §2 price/availability display rule; §6(t) star ratings; §6(w) link shortening; §6(y) price tracking |

## P1 — Chefman 6QT Dual-Basket (B0CDY277D3)

| Field | Register value | Live read 2026-11-20 (this session) | Verdict |
|---|---|---|---|
| Title | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, … - Black | identical on the listing page title and H1 | confirmed |
| Buy box (new) | $79.93 | $79.93, In Stock, ships from / sold by Amazon.com (buy-box JSON in page) | confirmed |
| List price | $99.99 | $99.99 ("20 percent savings") | confirmed |
| Used price | $62.85 | Used - Like New $62.85, sold by Amazon Resale | confirmed |
| Rating / count | 4.2 (4,877) | 4.2 (4,878) | **drift +1** — snapshot updated, prior value kept in the note (see FLG-024) |
| Amazon's Choice badge | shown on listing | shown ("Amazon's Choice") | confirmed |
| Bought past month | 1K+ | "1K+ bought in past month" | confirmed |
| Dimensions | 13.38"D x 11.81"W x 10.63"H | identical (Product Dimensions row) | confirmed |
| Capacity | title 6 Quart (2 × 3 Qt) / field 6 liters | identical (Capacity row: 6 liters) | confirmed |
| Color / Material | Black, Gray / Metal, Plastic | identical | confirmed |
| Special features | +2Min Button, Automatic Shut-Off, Dual Zone Features, Hi-Fry, Mute | identical | confirmed |
| Wattage / warranty | 120 V / 1700 W; 1-year assurance, cETL (bullets) | identical ("RESOURCES" bullet) | confirmed |
| Bullets | 5 bullets in register | all five present verbatim in "About this item" | confirmed |

Extra observation (not a register field): the listing states the 2026 holiday return
window — items purchased Nov 1–Dec 31, 2026 can be returned until Jan 31, 2027. Used by
`guide-gift-return-window.html`; the wording matches that guide's claim.

## P2 — Emeril Lagasse 26QT French-Door (B09B7SB46R)

| Field | Register value | Live read 2026-11-20 (this session) | Verdict |
|---|---|---|---|
| Title | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| … Six Cooking Accessories Included | identical | confirmed |
| Rating / count | 4.3 (18,380) | 4.3 (18,380) | confirmed |
| Bought past month | 8K+ | "8K+ bought in past month" | confirmed |
| Buy box | $149.99 | $149.99 Black Friday Deal ("29 percent savings"), buy-box JSON NEW $149.99 | confirmed |
| List price | $209.99 | $209.99 | confirmed |
| Dimensions | 16.9"D x 15.8"W x 14.8"H | identical | confirmed |
| Capacity | title 26QT / field 24.6 liters | identical | confirmed |
| Special features | Automatic Shut-Off, Programmable, Temperature Control, Timer | identical | confirmed |
| Preset discrepancy | title 24 vs bullets 25 (FLG-002) | title "24 One-Touch Preset Options" vs bullet "25 COOKING PRE-SETS" — both still live | confirmed (conflict persists; both values shown) |
| Bullets | 5 bullets in register | all present (toast auto-off; 26-qt for 4–6, rotisserie 6-lb chicken, 12" pizza; French doors + interior light; six accessories per title) | confirmed |

## P3 — Chefman 8QT TurboFry (B08DKYBTPH)

| Field | Register value | Live read 2026-11-20 (this session) | Verdict |
|---|---|---|---|
| Title | Chefman Air Fryer 8 Qt \| TurboFry 4-in-1 with 450°F Hi-Fry Option … Stainless Steel | identical (listing shows "TurboFry®") | confirmed |
| Rating / count | 4.4 (16,892) | 4.4 (16,894) | **drift +2** — snapshot updated (FLG-024) |
| Bought past month | 3K+ | "3K+ bought in past month" | confirmed |
| Amazon's Choice | shown on listing | shown | confirmed |
| Buy box | $69.99 | $69.99 ("42 percent savings") | confirmed |
| List price | $119.99 | $119.99 | confirmed |
| Used price | $45.49 | offer wall now shows "New & Used (3) from $43.39" — different measure (offer floor, not the used buy box); register value left unchanged and marked stale in the note | carried (see note) |
| Dimensions | 12.75"D x 13.5"W x 10"H | identical | confirmed |
| Capacity | 8 quarts | 8 quarts; size selector 6 / 8 / 9 quarts | confirmed |
| Wattage | 1000 W / 120 V (bullets) vs 1700 W (spec table), FLG-022 | bullet "1000 Watts/120 Volts – RJ38-SQSS-8T" still live; both values still shown in register | confirmed (conflict persists) |
| Warranty | 1-year, cETL (bullets) | identical | confirmed |
| Bullets | 5 bullets in register | all present | confirmed |
| Newer model note | B0CNY1YVDD, $59.99, 4.6 / 7,602 (FLG-003) | "newer model" widget: B0CNY1YVDD $59.99, 4.6 (7,601) | **drift −1** on the newer model's count — FLG-003 text updated |

## P4 — ThermoMaven 1-Second (B0DHZTCNR5)

| Field | Register value | Live read 2026-11-20 (this session) | Verdict |
|---|---|---|---|
| Title | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5°F Accuracy \| NIST&NSF Certified, … Black | identical | confirmed |
| Rating / count | 4.6 (3,499) | review count 3,499 shown beside the listing title block | confirmed (count; star value not rendered in the static view — carried from the 2026-11-20 snapshot) |
| Buy box | $16.99 | $16.99 NEW (buy-box JSON), In Stock, ships from and sold by Amazon.com | confirmed |
| List price | $22.99 | not visible in this session's chunks | carried (2026-11-19/20 snapshots) |
| Dimensions | blank (FLG-004) | the Product-information table again has **no dimensions row** | confirmed — staying blank is correct |
| Special features | Auto Off, Fast Reading System, High Accuracy, Ultra Clear Screen, Waterproof | identical | confirmed |
| Included components | 1× Calibration Certificate (register note) | "1*Meat Thermometer, 1*AAA Battery, 1*User Manual, 1*Calibration Certificate" | confirmed |
| Specification | NIST, NSF | "Specification Met: NIST, NSF" | confirmed |
| Warranty note | calibration certificate (per included-components) | identical | confirmed |
| Bullets | 5 bullets in register | all present (NIST ±0.5°F; thermocouple 1-second; LED; IP67 rinse-clean; motion wake/sleep + auto-rotate) | confirmed |
| Newer model note | B0GL7Z4KP4 Orange, $16.99, 4.7 / 144 (FLG-003) | "newer model" widget: same values | confirmed |

## P5 — CHEF iQ Sense wireless (B0DZFD6R9Z)

| Field | Register value | Live read 2026-11-20 (this session) | Verdict |
|---|---|---|---|
| Title | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| … Gen3 | identical | confirmed |
| Rating / count | 4.2 (2,178) | 4.2 (2,178) | confirmed |
| Bought past month | 1K+ | "1K+ bought in past month" | confirmed |
| Buy box (3-probe) | $119.99 | $119.99 ("45 percent savings") | confirmed |
| List price (3-probe) | $219.99 | $219.99 | confirmed |
| Variant prices | 1-probe $99.99, 2-probe $99.99, 3-probe $119.99, 4-probe $142.49 | identical (variant selector) | confirmed |
| Dimensions | blank (FLG-004) | Product-information table has **no dimensions row** | confirmed — staying blank is correct |
| Special features | 5 Sensors, Unlimited Range | identical | confirmed |
| Included components | 3 Probes, Hub (register bullets) | "3 Probes, Hub" | confirmed |
| Connectivity | Bluetooth + WiFi (register bullet) | "Bluetooth, Wi Fi" | confirmed |
| Warranty | two-year assurance (bullets) | "two-year assurance provided by CHEF iQ" | confirmed |
| Bullets | 5 bullets in register | all present (flip reminders/rest timers/estimates/recipes; 4 internal + ambient sensors; 1000°F; 50 hours; hub charges three probes) | confirmed |

## Policy quotes (verbatim checks)

| Quote used on the site | Source | Verdict |
|---|---|---|
| "As an Amazon Associate I earn from qualifying purchases." | OA §5, https://affiliate-program.amazon.com/help/operating/agreement | exact match |
| Price/availability display rule ("…only show prices and availability if: (a) we serve the link… or (b) you obtain Product pricing and availability data via Creators API or PA API…") | Program Policies §2, https://affiliate-program.amazon.com/help/operating/policies | exact match |
| §6(t) star ratings/reviews require Creators API or PA API | same | exact match |
| §6(w) no link shortening that makes the Amazon destination unclear | same | exact match |
| §6(y) no price tracking / price alerting | same | exact match |
| §2(b) tag parameter format "XXXXX-##" | same | matches `?tag=shopnow047c-20` construction |
| OA "Updated: October 15, 2025"; Policies "Updated: April 14, 2026" | pages' own headers | matches what compliance.html and README record |

## Drift found in this pass (recorded, not silently resolved)

1. **FLG-024 (rating snapshot drift) extends to P1 and P3 within 2026-11-20 itself:**
   P1 count 4,877 → 4,878 and P3 count 16,892 → 16,894 between earlier sessions' reads
   and this one. Register snapshots updated to this session's read with the prior value
   kept in `sourceNote`. Counts move intraday; the register is a dated snapshot, not a
   live feed (and shop pages deliberately show no ratings — Program Policies §6(t)).
2. **FLG-003 text:** the "newer model" widget for P3 now shows 7,601 ratings where the
   flag row said 7,602. Flag row text updated; the delta is Amazon-side churn.
3. **P3 used-price field:** register keeps $45.49 (the used buy-box snapshot from
   2026-11-19/20 reads). The offer wall today floors at $43.39 "New & Used (3) from" —
   a different measure. Not overwritten; noted in `sourceNote`.

## What this pass did NOT verify (and why)

- **Star values rendered as widgets (P1 4.2, P4 4.6):** the summary view Amazon serves to
  this fetcher renders the star widget in JavaScript; the count is in the static HTML but
  the star value is not. P2/P3/P5 star values *were* visible in static headers. Where not
  visible, the dated 2026-11-20 snapshot stands, unchanged.
- **P4 list price $22.99:** not visible in the chunks fetched today. Carried from the
  2026-11-19/20 snapshots (dated).
- **Short-link compliance (FLG-001):** `link.amazon/B0…` short links are the owner's
  supplied inputs. Their compliance status as Special Links remains **unresolved** —
  this pass makes no claim that they are valid or invalid (Program Policies §6(w) read;
  the test belongs in Associates Central, an owner action).
- **Anything from `counter-check/`, `docs/`, `articles/`:** secondary builds kept out of
  the index (robots.txt, FLG-039); not re-verified here.

## Cross-check against prior sessions' dated evidence

Consistent with `review/543ed7f4/VERIFICATION.md`, `review/42e09357/VERIFICATION-2026-11-20.md`,
`review/46e39d18` records and `review/e05155a0/VERIFICATION.md` (open PR #48 at the time of
this read): titles, buy boxes and spec tables match across all passes. The only deltas are
the intraday rating-count drift above.
