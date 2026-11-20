# Verification record — session arena/87e5be8d-prod1, 2026-11-20

Scope, stated plainly: a **full line-by-line read** of all five listing pages on 2026-11-20
(product-details tables, buy boxes, returns panels, item details), plus the repository work
this session shipped. Where a figure below is dated 2026-11-20, it is from this read; where
it is dated 2026-11-19 it is carried forward unchanged and labelled as such.

## 1. The five listings, read 2026-11-20

| Ref | Page | What the read captured |
|---|---|---|
| P1 | https://www.amazon.com/dp/B0CDY277D3 | Title match. Rating 4.2 / **4,878** (register had 4,877). Buy box **Buy New $79.93**, **$39.97 per count**, 20 percent savings; List Price $99.99 (re-confirmed); used offer $62.85 / $31.43 per count. Item details: **Unit Count 2 Count** (Number of Packs 1), Included Components "User Guide", model RJ38-SQPF-3TDB-2W, weight **13.3 lb**. Features & Specs: 93 °C min / 450 °F max. Ships from and sold by Amazon.com. Returns panel: FREE refund/replacement until Jan 31, 2027, at least one free return option. Two-count structure recorded as FLG-082. |
| P2 | https://www.amazon.com/dp/B09B7SB46R | Title match (still "24 One-Touch Preset Options", "Six Cooking Accessories Included"). Buy box **$149.99**, seller Amazon.com, In Stock. Item details: Configuration "Air Fryer Toaster Oven Combo with **24 Functions and 7 Accessories**"; Included Components **Rack, Bake Pan, Drip Tray, Crisper Basket, Rotisserie Spit, Fetch Tool** (six pieces named); model 4-00675-02X-VN; Unit Count 1 Count. Features & Specs: Output Wattage **1700 watts** / 120 volts (confirms the register); 75 °F min / 500 °F max. Product description repeats **seven** premium accessories. FLG-021 conflict now present in three places on the same page. Rating 4.3 / 18,380 (re-confirmed). $209.99 List Price carried from 2026-11-19, not re-observed in the captured text. |
| P3 | https://www.amazon.com/dp/B08DKYBTPH | Title match. Rating 4.4 / **16,894** (register had 16,892). Buy box **$69.99** (42 percent savings), List Price $119.99 (re-confirmed). Features & Specs: Output Wattage **1700 watts** / 120 volts; Measurements: 12.75"D x 13.5"W x 10"H, Capacity 8 quarts, **Item Weight 12.8 lb**. Item details: Warranty Description **"1-Year Limited Warranty"**, model RJ38-SQSS-8T, Unit Count 1 Count. The bullets' 1000 W reading stands as the minority (FLG-022); the product description also closes "1700W/120V". Newer 6QT B0CNY1YVDD still shown in the page's own carousel (FLG-003 corroborated). Black Friday Deal chip present beside the buy box. |
| P4 | https://www.amazon.com/dp/B0DHZTCNR5 | Title match (holiday keywords still in it). Rating 4.6 / 3,499 (re-confirmed). Buy box **$16.99** (26 percent savings), List Price $22.99 (re-confirmed); "New (7) from $16.99". Features & Specs: Upper Temperature Range **572 °F**, Response Time **1 second**, Resolution 0.1°, **Immersion Depth 6.5 inches**, 1 AAA battery included, Specification Met **NIST, NSF**. Item details: Item Length **6.5 inches**, Unit Count 1 Count, model **HT07**, Included Components **1×Meat Thermometer, 1×AAA Battery, 1×User Manual, 1×Calibration Certificate**. Warranty & Support states only that the manufacturer's warranty can be requested from customer service — no term (register corrected, FLG-084). Returns panel: **"FREE Returns"**, "at least one free return option: no shipping charges". No width/height published, so FLG-004 stays open. |
| P5 | https://www.amazon.com/dp/B0DZFD6R9Z | Title match (Gen3, 5 Sensors, 3 Ultra-Thin Probes). Rating 4.2 / 2,178 (re-confirmed). Buy box **$119.99** (3-probe variant, 45 percent savings), **$40.00 per count**, List Price $219.99 (re-confirmed). Variants re-read: 1 probe $99.99/$129.99, 2 probes $99.99/$179.99, 3 probes $119.99/$219.99, 4 probes $142.49/$249.99. Item details: **Warranty Description "3 Year"** against the RESOURCES bullet "two-year assurance provided by CHEF iQ" — both published, FLG-083; Included Components **"3 Probes, Hub"**; Unit Count 3 Count; Item Length 4.75 inches; model CQ60-3C-Z1-E. No width/height published; FLG-004 stays open. |

Method note: every listing page carries widget blocks ("Customers who viewed", product
summaries, sponsored carousels) that show other ASINs' prices and ratings. None of those
figures were used, per FLG-016. Each price above was attributed to the product's own buy
box before being recorded.

## 2. Corrections made to the register as a result

- P1 `ratingCount` 4,877 → **4,878**; P3 `ratingCount` 16,892 → **16,894**.
- P4 `warranty` corrected: it named the calibration certificate, which the listing lists
  under Included Components; the Warranty & Support section states no term (FLG-084).
- P5 `warranty` now publishes both stated terms instead of the bullet alone (FLG-083).
- New register fields captured for all five where the listing states them: unit count and
  price per count (FLG-082 pairing rule), item weight (P1 13.3 lb, P3 12.8 lb; P2/P4/P5 not
  stated in captured fields), temperature range, warranty statement as the listing words it,
  included components, model number.

## 3. FLG-074 dates: derivation method

For each guide slug, `main`'s first-parent history was walked in order and the first commit
whose tree contains `<slug>.html` was taken; its **author date** is the publication date now
recorded in `data/editorial.json → dates.publish`. Twelve guides resolve to commits authored
2026-11-19 (UTC) and `guide-instant-read-vs-wireless.html` to a commit authored 2026-11-20
(UTC). Caveat recorded on the flag row: most guides first reached `main` through merge commit
`141604a` (authored 2026-11-19, Pacific time); the dates used are the authoring dates of the
commits that wrote the pages, not the merge moment. A naive first-parent attribution of the
*generator* source (`git log -S`) resolves every slug to the merge commit and was discarded
as invalid evidence; the file-presence walk is what was used.

## 4. Policy sources (re-read 2026-11-20, carried conclusions)

The Associates Operating Agreement (updated 2025-10-15), Program Policies, FTC Disclosures
101, 16 CFR 255.5 and Google's helpful-content / product-review / spam guidance were read
through the official pages this session and earlier on 2026-11-20. The operative rules this
build implements: the exact Section 5 disclosure sentence, above the fold and in the footer;
no price/availability display without Amazon-served or API-served data; no stored Program
Content imagery; prompt removal of ended promotions; material-connection disclosure that is
hard to miss and near the endorsement; review content that shows first-hand evidence,
measurements, original analysis and pros/cons rather than thin affiliate summary.
