# Line-by-line verification log — session arena/0c26f71b-prod1 — 2026-11-20 (second same-day pass)

Every value below was read by this session directly from the official source on 2026-11-20, from this
sandbox, using its own fetches. The previous session (54d3e366) could not reach amazon.com; this one
could, so this pass is an independent re-read rather than a carry-over. Register values were changed
only where the live source differs from the register, and every change carries a dated note in
`data/products.json`. Nothing was inferred; a value that could not be re-read today keeps its earlier
dated attribution (notably the P1 wattage field, whose Product-information table was not captured in
this pass's fetch set - it keeps the 2026-11-19/20 attribution from the earlier sessions).

## 1. The five listings (official Amazon.com product pages)

| Product | ASIN | Source (official) | Re-read today |
|---|---|---|---|
| P1 Chefman 6QT Dual-Basket Air Fryer Oven | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 | Title (character-for-character), rating **4.2 out of 5 stars (4,877)**, Amazon's Choice badge, "1K+ bought in past month", buy box **$79.93 with 20 percent savings**, **List Price $99.99**, Used - Like New **$62.85 with 37 percent savings**, Special Feature "+ 2Min Button, Automatic Shut-Off, Dual Zone Features, Hi-Fry, Mute", Product Dimensions **13.38"D x 11.81"W x 10.63"H**, Color "Black, Gray", Capacity **"6 liters"**, Material "Metal, Plastic", About-this-item bullets (2 baskets / dual zone / Sync Finish / 200-450°F). **No register value changed.** |
| P2 Emeril Lagasse 26QT French-Door | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R | Title, rating **4.3 (18,380 global ratings)** (confirmed twice: review block and "Customers say" summary), "8K+ bought in past month", **Black Friday Deal promo badge (new - register badge updated with dated note)**, buy box **$149.99 with 29 percent savings** (confirmed in the buy-box data block), **List Price $209.99**, Special Feature "Automatic Shut-Off, Programmable, Temperature Control, Timer", Product Dimensions **16.9"D x 15.8"W x 14.8"H**, Color/Material "Stainless Steel", Capacity **"24.6 liters"**, About-this-item bullets (**"25 COOKING PRE-SETS"** in bullets vs "24 One-Touch Preset Options" in title - FLG-002 stands; 26-quart / 4-6 people / 6-lb chicken / 12" pizza). Product Summary block: "Included are 7 premium accessories" vs title "Six Cooking Accessories Included" - FLG-021 stands. |
| P3 Chefman 8QT TurboFry | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH | Title, rating **4.4 out of 5 stars**, count **(16,894)** - register said 16,892; **updated with dated note** (same-day drift, consistent with the known snapshot-drift pattern). Amazon's Choice badge + **Black Friday Deal promo badge (new)**, "3K+ bought in past month", **$69.99 with 42 percent savings**, **List Price $119.99**, In Stock, Special Feature "Automatic Shut-Off, LED Shake Reminder, Programmable", Product Dimensions **12.75"D x 13.5"W x 10"H**, Capacity **"8 quarts"**, Material "Plastic, Stainless Steel", bullets (four presets, 200-400°F, top-rack dishwasher-safe basket and tray, cETL + **1-year warranty provided by Chefman**, **"1000 Watts/120 Volts - RJ38-SQSS-8T"**), "There is a newer model of this item: Chefman 6QT **B0CNY1YVDD**" - FLG-003 stands. |
| P4 ThermoMaven 1-Sec Instant-Read | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 | Title, rating **4.6 out of 5 stars (3,499)**, Amazon's Choice badge, **Black Friday Deal promo badge (new)**, "5K+ bought in past month", buy box **$16.99 with 26 percent savings** (buy-box data block), **List Price $22.99**, product-info table (Brand ThermoMaven; Special Feature "Auto Off, Fast Reading System, High Accuracy, Ultra Clear Screen, Waterproof"; Color Black; Included Components "1*Meat Thermometer, 1*AAA Battery, 1*User Manual, 1*Calibration Certificate"; Outer Material Plastic; Specification Met "NIST, NSF"; Display Digital). **No Product Dimensions row in the captured table - FLG-004/FLG-072 stay open, dimension field stays blank.** New observations, recorded with dates: a **ClimeCo Certified** sustainability feature (carbon impact) is shown; a newer Orange model **B0GL7Z4KP4** is shown - FLG-003 already covers it. |
| P5 CHEF iQ Sense (3 probes) | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z | Title, rating **4.2 out of 5 stars (2,178)**, "1K+ bought in past month", **Black Friday Deal promo badge (new)**, variant price list read in full (**1-probe $99.99, 2-probe $99.99, 3-probe $119.99 with 45 percent savings, 4-probe $142.49**), buy-box data block **$119.99**, **List Price $219.99**, product-info table (Special Feature "5 Sensors, Unlimited Range"; Color Black; Included Components "3 Probes, Hub"; Outer Material Stainless Steel; Connectivity "Bluetooth, Wi Fi"; Display App; Product Care "Dishwasher Safe"). Bullets: 4 internal + 1 ambient sensor, 1000°F, unlimited WiFi range, up to 50 hours, **"two-year assurance provided by CHEF iQ"**. **No Product Dimensions row and no +/-F tolerance figure in the captured fields - FLG-004 and FLG-071/Q-36 stay open.** |

Register changes made by this pass (all with dated notes in `data/products.json`):
1. P3 `ratingCount` 16,892 → **16,894** (same-day drift).
2. Badge fields for all five updated/re-confirmed with a 2026-11-20 read date (Black Friday Deal promo on P2, P3, P4, P5; P1 shows Amazon's Choice, no deal badge observed in its capture).
3. P2 `warranty` field extended: the listing-linked owner's manual (FAFO-001) was read today and states no warranty term either.
4. `sourceNote` on each product gained a "second same-day read (session 0c26f71b)" line listing exactly what was confirmed.

## 2. Owner's manual for P2 (official document linked from the listing)

Source: https://m.media-amazon.com/images/I/B1U+TqJDuaL.pdf (linked from the B09B7SB46R listing's
"Product Guidance & Documents" block as "User Manual (PDF)"). Fetched 2026-11-20.

- Appliance specifications table: Model **FAFO-001**, Supply Power **120 V/1700 W/60 Hz**, Rated Power **1700 W**, Capacity **26 quarts (1519 cubic inches)**, Temperature **75°F - 500°F**, LED display.
  - The 1700 W / 120 V figures match the register's P2 wattage field - now double-sourced (listing table 2026-11-19 + manual 2026-11-20).
  - The manual states no warranty term. Its table of contents lists a **"Money-Back Guarantee"** section - a money-back guarantee is not a manufacturer warranty term, so **FLG-005 stays open** (its register text was updated today to record this read).
  - Safety note 15 requires **at least 5 inches of free space on the top, back and sides** - recorded here as available manufacturer guidance for clearance content; not added to shop pages in this pass.
  - Accessory load limits: grill 11 lb, fry basket 11 lb, rotisserie spit **6 lb** - consistent with the listing's "rotisserie a 6-lb chicken" bullet.
- Also observed on the listing today (Amazon's own review-summary module): 564 customers mention durability, 445 negative, citing heating-element failures within 9-14 months. Recorded as an observation of the listing with a date; not published on shop pages (it is Amazon's generated summary, not a spec and not our test). Candidate for a future guide only with owner approval.

## 3. Policy pages (official)

| Source | Read today | Result |
|---|---|---|
| Associates Program Operating Agreement, https://affiliate-program.amazon.com/help/operating/agreement | 2026-11-20 | Header confirms **Updated: October 15, 2025** (matches prior records). **Section 5 read in full**: the required statement is verbatim **"As an Amazon Associate I earn from qualifying purchases."** The site's disclosure uses exactly this sentence - still compliant, no change. |
| Associates Program Compliance / Section 2 and termination provisions (same page) | 2026-11-20 | Section 2 (compliance), Section 6 (termination, incl. "any violation of Section 5 … will be deemed a material breach") re-read. Consistent with the site's compliance page. |
| Amazon.com listing pages (all five) | 2026-11-20 | See section 1. |

The Program Policies page, FTC pages and Google Search Central pages were re-read and character-matched
by sessions 62786810 and fbfe1742 earlier on this same date (2026-11-20, see
`review/62786810/VERIFICATION.md` and `review/fbfe1742/VERIFICATION-2026-11-20.md`); they are not
re-fetched a third time today, and their citations on the site keep their 2026-11-20 dates.

## 4. What this pass could not verify (stays blank / stays flagged - never inferred)

- **P4/P5 dimensions** - the captured product-information tables have no dimensions row. FLG-004/FLG-072 stay open; fields stay blank.
- **P5 accuracy tolerance** - no +/-F figure appears in the captured fields. FLG-071 stays open.
- **P2 warranty term** - neither the listing nor the linked manual states one. FLG-005 stays open (text updated with the manual read).
- **P1 wattage Product-information table** - not captured in this pass's fetch set; the register value keeps its earlier dated attribution from the 2026-11-19/20 reads.
- **Special Link attribution** - only the owner can run the Associates click test (FLG-001/SG-53). Nothing in this session can confirm or deny attribution, and no claim is made either way.

## 5. Irregularities logged this pass

- **Rating-count drift continues** (P3 16,892 → 16,894 within one day). Handled the way the register
  already handles it: dated update, no flag added (the pattern is known).
- **Black Friday Deal promo badges appeared on four of five listings** (P2, P3, P4, P5) - seasonal
  volatility; recorded in the register badge fields with read dates. The shop pages display no badges,
  so nothing published changes.
- **Duplicate-topic row in the calendar** (queued 2026-12-01 topic overlaps published topic 01) -
  logged as **SG-59** on the suggestion desk with a recommended path; not changed, editorial is the
  owner's call. See `suggestions.html#SG-59`.
