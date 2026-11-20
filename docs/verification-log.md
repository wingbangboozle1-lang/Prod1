# Verification log

## 2026-11-19 — Initial verification pass
- Fetched all 5 submitted short links; resolved to ASINs B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z.
- Fetched each Amazon listing (title, rating, buy-box price, purchase-options table, bullets) and recorded fields in data/products.json with per-product source URLs.
- Fetched Amazon Associates Operating Agreement (upd. 2025-10-15), Program Policies (upd. 2026-04-14), FTC Disclosures 101 (Nov 2019).
- Irregularities logged as FLG-001..FLG-012 in flagged.html. Missing fields left blank.
- Next: re-fetch thermometer dimensions + Emeril wattage; manual Special Link test (SG-01).

## 2026-11-19 — Full line-by-line re-verification (session arena/2ec8638e-prod1)
- Re-fetched all five Amazon.com listing pages line by line (buy box, rating block, purchase-options table, Product information table, About-this-item bullets) and reconciled every field in data/products.json.
- Re-fetched all five supplied short links: each still resolves to the ASIN registered for it (B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z). Redirect targets still carry no tag= parameter (FLG-015 unchanged).
- Confirmed P1 in full: $79.93 buy box (list $99.99, used $59.95), 4.2 / 4,876, Amazon's Choice, 1K+ bought, 13.38"D x 11.81"W x 10.63"H, 6 liters / 6 Quart, 1700 W / 120 V, special features and bullets — resolves I-06 (price dispute).
- P2: $149.99 (list $209.99), 4.3 / 18,375 (updated), 8K+ bought (updated), dimensions/capacity/materials confirmed; wattage captured 1700 W / 120 V per the listing's Product information table (closes FLG-005 wattage half). Warranty period not stated on the listing (PDF link only) — FLG-005 warranty half stays open. New FLG-021: accessory count disagrees across title (six), item details (7 accessories) and included components (6).
- P3: $69.99 (list $119.99, used $45.49), 4.4 / 16,892 (updated), Amazon's Choice, 3K+ bought, dimensions/capacity confirmed; bullets confirm 1000 W/120 V RJ38-SQSS-8T and 1-year Chefman warranty. New FLG-022: listing-internal wattage discrepancy (bullets 1000 W vs Product information table 1700 W).
- P4: $16.99 (list $22.99), 4.6 / 3,499, Amazon's Choice, 5K+ bought, included components (incl. calibration certificate), NIST/NSF, IP67, bullets confirmed. Dimensions not listed on the listing page — FLG-004 stays open. Newer model B0GL7Z4KP4 confirmed (FLG-003).
- P5: $119.99 (3-probe variant; list $219.99), 4.2 / 2,178, 1K+ bought, variant prices 1/2/3/4-probe ($99.99/$99.99/$119.99/$142.49) confirmed, two-year CHEF iQ assurance per bullets, 5-sensor claim and 1000°F rating confirmed. Dimensions not listed — FLG-004 stays open.
- Machinery: fixed build_site.py canonical placeholder (was writing https://example.com/; now writes the live GitHub Pages URL) so rebuilds reproduce the committed pages; preserved the index-only docs footer links (P-21) in the generator; added the publishing gate to .github/workflows/pages.yml (R-01).
- Verification sources: Amazon.com listing pages for all five ASINs (fetched 2026-11-19); Amazon Associates Operating Agreement and Program Policies; FTC guidance (links on verification.html and compliance.html).
- Result: all five intended ASINs and every listed field reconcile with data/products.json except the three open items (thermometer dimensions, Emeril warranty, Chefman 8QT wattage discrepancy), which remain blank/attributed and flagged (FLG-004, FLG-005, FLG-021, FLG-022).

## 2026-11-20 — Second line-by-line re-verification (session 1b65e5a1)
- Re-fetched every official Amazon.com listing (B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z) on 2026-11-20 and re-read title, rating, rating count, buy-box price, list price, dimensions, capacity, features, wattage and bullets line by line. Full per-field evidence and source links: review/1b65e5a1/VERIFICATION.md.
- Re-confirmed the Associates Operating Agreement §5 disclosure sentence against the official agreement page (fetched 2026-11-20); every page renders it verbatim.
- Displayed fields all matched the register. Volatile snapshot figures drifted and were updated in data/products.json: P1 rating count 4,876→4,877 and used price $59.95→$62.85; P2 rating count 18,375→18,380. site.verifiedDate bumped to 2026-11-20; all five confirmationDate bumped to 2026-11-20.
- P2 Item-details table re-confirmed the accessory-count discrepancy (configuration "24 Functions and 7 Accessories" vs title "Six Cooking Accessories") → FLG-021 stays open.
- Scope notes (carried from the 2026-11-19 register, not re-captured this pass, recorded as attributed on FLG-060): P2 wattage (1700 W/120 V); P4 rating value and list price. P4 buy-box $16.99 and count 3,499, and all of P3 and P5, were re-confirmed in full.
- Short-link redirect targets were not re-tested this pass (the direct /dp/<ASIN> pages were fetched); observedRedirectTarget stays "observed 2026-11-19" and FLG-001 (short-link compliance) remains unresolved.
- New flag **FLG-060** records this pass and its drifts on flagged.html.
