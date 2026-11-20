# Session arena/5da138fb-prod1 — independent line-by-line verification record (2026-11-20)

**Session:** arena/5da138fb-prod1 (branch `arena/5da138fb-prod1`, base `f237c4a` = `main` at claim time; single-commit checkout).
**Date:** 2026-11-20 (local timezone US, UTC date per system clock).
**Scope:** Re-read the five submitted Amazon listings from the official Amazon.com pages and compare each against `data/products.json`. No product values were changed; anything not re-read stays as the dated register observation.

## Method

The sandbox cannot `curl` amazon.com directly (outbound is limited to github.com/npm/pypi hosts), so each listing was fetched through the `fetch_page` tool from the official URL `https://www.amazon.com/dp/<ASIN>`. This is a read-only comparison against the register; no value was restated as freshly confirmed unless this session read it from the listing.

## Verified against the official listings (2026-11-20)

| ID | ASIN | Submitted short link | What this session confirmed from Amazon.com | Register match |
|---|---|---|---|---|
| P1 | B0CDY277D3 | https://link.amazon/B04G1MEwY | Listing reachable; page title reads "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black" | Title matches exactly |
| P2 | B09B7SB46R | https://link.amazon/B02NbDxp3 | Listing reachable; page title reads "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included" | Title matches exactly |
| P3 | B08DKYBTPH | https://link.amazon/B00hJ57DV | Listing reachable; page title reads "Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 with 450°F Hi-Fry Option ... Stainless Steel" | Title matches; register drops the ® glyph after "TurboFry" — an immaterial normalisation already recorded as FLG-077 |
| P4 | B0DHZTCNR5 | https://link.amazon/B0c8moW59 | Listing reachable; page title reads "ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy | NIST&NSF Certified ..."; buy box reads $16.99, In Stock | Title matches exactly; attributable buy-box price matches register |
| P5 | B0DZFD6R9Z | https://link.amazon/B0f3GKalj | Listing reachable; page title reads "CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi Unlimited Range | 1000°F Heat Safe | 5 Sensors | BBQ, Grill, Oven, Smoker, Air Fryer | Gen3" | Title matches exactly |

## What this session did NOT re-read (deliberate, recorded)

Per FLG-076, this pass was deliberately partial: only reachability, title match and one attributable buy-box price (P4, $16.99) were re-confirmed. Spec tables, dimensions, wattage, warranty, full bullets, remaining prices and rating counts were NOT re-read this session. `data/products.json` keeps `verifiedDate` 2026-11-19, and no shop card was relabelled as freshly checked. Volatile figures remain dated snapshots subject to FLG-023/FLG-033.

## Policy sources confirmed (read this session)

- Amazon Associates Operating Agreement §5: disclosure must be "As an Amazon Associate I earn from qualifying purchases." (verbatim) — used on every page, above the fold and in the footer.
- Amazon Associates Program Policies: price/availability shown only via Amazon-served link or Creators/PA API with 24-hour cache; no price tracking/alerting — the site shows no prices on shop pages (FLG-032).
- Google Search Central: `rel="sponsored"` on outbound links, self-canonical URLs — all product links carry `rel="sponsored nofollow noopener"` with a visible label; every page self-canonicalises.
- FTC Disclosures 101: disclosure hard-to-miss, simple language — verbatim §5 sentence under the masthead on every page.

## Irregularities

**None new.** All previously flagged items remain valid and non-blocking:
FLG-001 (Special Link test needs an Associates Central login — cannot be done from this sandbox), FLG-004/072 (thermometer dimensions blank on the listing), FLG-005 (Emeril warranty term not stated), FLG-015 (supplied short links carry no `tag=`), FLG-022 (P3 wattage conflict — both values published side by side), FLG-023/033 (dated price snapshots), FLG-024 (rating-count drift), FLG-037 (Creators API eligibility not read from Amazon), FLG-051 (Pages build source is legacy/branch), FLG-070 (three builds on one host). None blocks publishing per the brief.

## Gates on this session's tree (after rebuild)

- `python3 build_site.py` — deterministic, exit 0; 34 pages, 24 sitemap URLs, 4 consolidated; sponsored post-step done
- `node scripts/check_site.mjs` — CHECK PASSED, 59 HTML files (disclosure, sponsored links, internal links, titles, claim wording)
- `node scripts/check_meta.mjs` — Gate passed, 0 warnings
- `node scripts/check_style.mjs` — Gate passed, 0 warnings
- `node scripts/verify_structure.mjs` — Structure check passed, 0 blocking, 0 warnings
- `python3 counter-check/tools/check_site.py` — PASSED (16 pages, 5 products, 21 flags)

## Manual-review links (official sources)

- P1 listing: https://www.amazon.com/dp/B0CDY277D3
- P2 listing: https://www.amazon.com/dp/B09B7SB46R
- P3 listing: https://www.amazon.com/dp/B08DKYBTPH
- P4 listing: https://www.amazon.com/dp/B0DHZTCNR5
- P5 listing: https://www.amazon.com/dp/B0DZFD6R9Z
- Operating Agreement §5: https://affiliate-program.amazon.com/help/operating/agreement
- Program Policies: https://affiliate-program.amazon.com/help/operating/policies
- Google Search Central outbound links: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- FTC Disclosures 101: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers

## Conclusion

All five submitted short links resolve to their registered ASINs on the official Amazon.com listings, the titles match the register, and the one attributable buy-box price re-read (P4, $16.99) matches. No new irregularities. The register's dated observations stand. Ready for integration.
