# Line-by-line verification record — session arena/543ed7f4-prod1

**Date:** 2026-11-20
**Branch:** `arena/543ed7f4-prod1` (from `main @ 3392c0d`, PR #35 merged)
**Method:** Each official Amazon.com listing page was fetched through the `fetch_page` tool (the sandbox cannot reach `www.amazon.com` by curl, so this tool was used for the official-source reads; no values were inferred or guessed). Pages were read chunk by chunk until the buy-box price and the page title appeared.

## 1. Submitted short links → ASINs (register: `data/products.json`)

All five `link.amazon/…` codes resolve to the five registered ASINs. The redirect targets carry no `tag=` parameter (observed 2026-11-19 in earlier sessions; unchanged). Short-link Special-Link compliance remains unresolved and requires an Associates Central login — only the owner can clear it (FLG-001 / SG-01).

| # | Submitted short link | Register ASIN | Official listing URL | Status |
|---|---|---|---|---|
| P1 | https://link.amazon/B04G1MEwY | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 | Resolves to registered ASIN |
| P2 | https://link.amazon/B02NbDxp3 | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R | Resolves to registered ASIN |
| P3 | https://link.amazon/B00hJ57DV | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH | Resolves to registered ASIN |
| P4 | https://link.amazon/B0c8moW59 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 | Resolves to registered ASIN |
| P5 | https://link.amazon/B0f3GKalj | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z | Resolves to registered ASIN |

## 2. Listing pages re-read line by line (official Amazon.com, 2026-11-20)

The page title, buy-box price, stock state and seller were confirmed for every listing. Buy-box prices match the dated snapshots in `data/products.json` exactly.

| # | ASIN | Page title matches register | Buy-box price (live, 2026-11-20) | Register priceNew | Stock / seller | Match? |
|---|---|---|---|---|---|---|
| P1 | B0CDY277D3 | Yes — CHEFMAN 6 Quart Dual Basket Air Fryer Oven | $79.93 | $79.93 | In Stock / Amazon.com | Yes |
| P2 | B09B7SB46R | Yes — Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | $149.99 | $149.99 | In Stock / Amazon.com | Yes |
| P3 | B08DKYBTPH | Yes — Chefman Air Fryer 8 Qt TurboFry 4-in-1 | $69.99 | $69.99 | In Stock / Amazon.com | Yes |
| P4 | B0DHZTCNR5 | Yes — ThermoMaven 1 Sec Professional Digital Meat Thermometer | $16.99 | $16.99 | In Stock / Amazon.com | Yes |
| P5 | B0DZFD6R9Z | Yes — CHEF iQ Sense Smart Wireless Meat Thermometer (3 probes) | $119.99 | $119.99 (3-probe variant) | In Stock / Amazon.com | Yes |

**Source links (manual review):** https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH · https://www.amazon.com/dp/B0DHZTCNR5 · https://www.amazon.com/dp/B0DZFD6R9Z

## 3. What was NOT re-confirmed today (left as register values, dated)

Per the rule "if a value can't be confirmed from an official source, leave it blank and flag it":

- **List prices** ($99.99 / $209.99 / $119.99 / $22.99 / $219.99): not visible in the fetched buy-box chunks; carried from the 2026-11-20 re-verification (session 1b65e5a1) and flagged as dated snapshots (FLG-023 / FLG-033).
- **Ratings and rating counts** (P1 4.2/4,877; P2 4.3/18,380; P3 4.4/16,892; P4 4.6/3,499; P5 4.2/2,178): not visible in the fetched chunks; carried from the register, subject to FLG-024 snapshot drift.
- **Dimensions**: P4 and P5 state no dimensions on the listing — left **blank**, not inferred (FLG-004/FLG-072).
- **Emeril warranty term**: not stated in listing text (warranty PDF linked only) — left as recorded (FLG-005).
- **P3 wattage conflict**: listing states 1000 W in bullets and 1700 W in the Product information table; both published side by side (FLG-022).
- **Short-link attribution**: no Associates report has been read; no session can log in to Associates Central (Q-35 / SG-01).

## 4. Compliance sources read (official)

- Amazon Associates Operating Agreement, updated 2025-10-15, §5 disclosure wording: "As an Amazon Associate I earn from qualifying purchases." — adopted verbatim on every page, above the fold and in the footer. https://affiliate-program.amazon.com/help/operating/agreement
- Amazon Associates Program Policies (updated 2026-04-14): price/availability display only when Amazon serves the link or via Creators/PA API with a 24-hour cache; no price tracking/alerting. This static build therefore shows no live price/rating on shop pages; dated figures stay in the register. https://affiliate-program.amazon.com/help/operating/policies
- Google Search Central: rel="sponsored" on outbound affiliate links; self-canonicalising pages; sitemap lists exactly what the build writes. https://developers.google.com/search/docs/crawling-indexing/
- FTC Disclosures 101: disclosure hard to miss, simple language, no un-tried experience claims. https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers

## 5. Irregularities carried to flagged.html (non-blocking)

FLG-001 (Special Link test), FLG-004/072 (thermometer dimensions), FLG-005 (Emeril warranty), FLG-015 (short links carry no tag), FLG-022 (P3 wattage conflict), FLG-023/033 (dated price figures), FLG-024 (rating-count drift), FLG-037 (API eligibility not read from Amazon), FLG-051 (Pages build source), FLG-070 (three builds on one host). None blocks the merge; all published on `flagged.html` with sources.

## 6. Gates run on the merged tree (this session)

- `python3 build_site.py` — 30 pages, 20 sitemap URLs, 4 consolidated; deterministic (no `datetime.now()` in output)
- `node scripts/check_site.mjs` — CHECK PASSED, 55 HTML files
- `node scripts/check_meta.mjs` — Gate passed, 0 warnings
- `node scripts/check_style.mjs` — Gate passed, 0 warnings
- `node scripts/verify_structure.mjs` — Structure check passed, 0 blocking, 0 warnings

No broken internal links or anchors. No `example.com` placeholder remains. Canonical is uniform per page.