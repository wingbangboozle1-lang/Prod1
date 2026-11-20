# Re-verification record — session arena/1187e20d-prod1 (2026-11-20)

Scope: a fresh, dated check of the five supplied short links, the Associates disclosure source, and the live site. No values were inferred. Where a value could not be confirmed it is left as recorded elsewhere and flagged.

## 1. Short link → ASIN (line by line)

Each `link.amazon/<code>` was fetched on 2026-11-20. The resolved page title and URL were compared with `data/products.json`.

| ID | Short link (submitted) | Resolved ASIN (2026-11-20) | Matches `data/products.json`? | Listing title as resolved | Source (manual review) |
|---|---|---|---|---|---|
| P1 | https://link.amazon/B04G1MEwY | B0CDY277D3 | Yes | CHEFMAN 6 Quart Dual Basket Air Fryer Oven… | https://www.amazon.com/dp/B0CDY277D3 |
| P2 | https://link.amazon/B02NbDxp3 | B09B7SB46R | Yes | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven… | https://www.amazon.com/dp/B09B7SB46R |
| P3 | https://link.amazon/B00hJ57DV | B08DKYBTPH | Yes | Chefman Air Fryer 8 Qt \| TurboFry 4-in-1… | https://www.amazon.com/dp/B08DKYBTPH |
| P4 | https://link.amazon/B0c8moW59 | B0DHZTCNR5 | Yes | ThermoMaven 1 Sec Professional Digital Meat Thermometer… | https://www.amazon.com/dp/B0DHZTCNR5 |
| P5 | https://link.amazon/B0f3GKalj | B0DZFD6R9Z | Yes | CHEF iQ Sense Smart Wireless Meat Thermometer… | https://www.amazon.com/dp/B0DZFD6R9Z |

Observations:
- The resolved URLs carry Amazon tracking parameters (`lv=`, `btn_ref=`, `plpRedirect=`) and **no `tag=` parameter**. This matches FLG-015. The tag is applied by the site's own `affiliateUrl` field, not by the short link.
- Ratings and prices seen on "Customers also viewed" widgets belong to other ASINs (for example, a $74.99 widget beside P1 belongs to a different listing). Those figures are not used. This matches FLG-016.

## 2. Associates disclosure source

- Source: Associates Program Operating Agreement, "Updated: October 15, 2025", fetched 2026-11-20 — https://affiliate-program.amazon.com/help/operating/agreement (Section 5, "Identifying Yourself as an Associate").
- Section 5 text, verbatim: "As an Amazon Associate I earn from qualifying purchases."
- The site disclosure (masthead and footer on every page) uses that exact sentence. **Match confirmed.**
- Section 5 also requires that the statement be "clearly and prominently" stated on the Site. The site's placement is a review item for the owner (see `compliance.html`).

## 3. Live site

- https://wingbangboozle1-lang.github.io/Prod1/ returned the publication front page on 2026-11-20 with the disclosure above the fold and sponsored tagged links.

## 4. Irregularity found and corrected

- **Claim checked:** the front-page pick card for the Chefman 8QT TurboFry read "Smallest footprint".
- **Listing values (from `data/products.json`, read 2026-11-19):** P1 13.38"D × 11.81"W; P3 12.75"D × 13.5"W. P3 has the shallowest depth of the three fryers. By floor area P1 is smaller (≈158 vs ≈172 sq in).
- **Action:** the label was changed to "Shallowest of the fryers" in `build_site.py` (regenerated `index.html`). The footprint claim is no longer made.
- Other pages still say "shallow footprint" in the "Good for" line. That phrase is a judgement, not a measured claim, and it is left for owner review.

## 5. Not verified in this session (remain open)

- FLG-001 — The Associates **Special Link** test (one link per product in the enrolled Associates workflow, with the tracking report) requires logging in to Associates Central. No session can do this without the owner. Still open.
- FLG-023 / FLG-024 — The Program Policies rules on displaying prices and ratings were not re-read this session.
