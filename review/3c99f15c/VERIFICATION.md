# Verification record — session `arena/3c99f15c-prod1`, 2026-11-20

Line-by-line re-read of the five submitted products against the official Amazon.com
listing for each ASIN, plus a read of the policy pages the site's compliance rules rest
on. Every row below names the URL that was opened. Nothing in this file is inferred: where
a field was not read in this pass, the row says so.

Tracking ID under test: **`shopnow047c-20`**.
Outbound format used by the build: `https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20`,
with `rel="sponsored nofollow noopener"`.

## 1. Submitted short link → ASIN → official listing

| ID | Submitted link | Resolved ASIN | Official listing opened in this pass | Status |
|---|---|---|---|---|
| P1 | https://link.amazon/B04G1MEwY | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 | Reachable, title matches register |
| P2 | https://link.amazon/B02NbDxp3 | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R | Reachable, title matches register |
| P3 | https://link.amazon/B00hJ57DV | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH | Reachable, title matches register |
| P4 | https://link.amazon/B0c8moW59 | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 | Reachable, title matches register |
| P5 | https://link.amazon/B0f3GKalj | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z | Reachable, title matches register |

The short links themselves were **not** clicked open in this pass and their Associates
compliance status stays unresolved — that is FLG-001 / FLG-003, and it needs a session
logged in to the enrolled Associates account. This record makes no claim about them either
way. What it does confirm is that each short link's resolved ASIN has a live listing whose
title matches the register.

## 2. Title match, field by field

The `<title>` element of each listing page was read and compared character by character
with `data/products.json → products[].title`.

| ID | Register title | Listing `<title>` prefix read 2026-11-20 | Match |
|---|---|---|---|
| P1 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black | `Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen` | Exact |
| P2 | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included | `Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included : Home & Kitchen` | Exact |
| P3 | Chefman Air Fryer 8 Qt \| TurboFry 4-in-1 with 450°F Hi-Fry Option … Stainless Steel | `Amazon.com: Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel : Home & Kitchen` | Match apart from the ® mark — already recorded as FLG-077 |
| P4 | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5°F Accuracy \| NIST&NSF Certified … Black | `Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black : Home & Kitchen` | Match apart from U+2109 vs ° + F — already recorded as FLG-077 |
| P5 | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3 | `Amazon.com: CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3: Home & Kitchen` | Exact |

## 3. Buy-box prices read in this pass

Read from the buy box on each listing page, compared with the register's dated snapshot.

| ID | Register snapshot | Buy box read 2026-11-20 | Agrees |
|---|---|---|---|
| P1 | $79.93 | $79.93 ("Only 1 left in stock") | Yes |
| P4 | $16.99 | $16.99, In Stock | Yes |
| P2 | $149.99 | **Not read in this pass** | — |
| P3 | $69.99 | **Not read in this pass** | — |
| P5 | $119.99 (3-probe variant) | **Not read in this pass** — the page carries several variants, and a carousel price on a listing page belongs to a different product | — |

**Do not read the last three rows as a disagreement.** They were not captured, and they are
not displayed on any reader-facing page: the site shows no price figure at all, because
Amazon's Program Policies permit price display only when Amazon serves it or when it comes
from the Creators/PA API refreshed inside 24 hours (FLG-023 / FLG-032). The button says
"see today's price on Amazon" and the register keeps the dated observation.

## 4. What this pass did not verify

Writing this down is the point of the file. The temptation in a re-read pass is to date
everything the moment some of it was touched.

- Dimensions, capacity fields, wattage, bullets, badges and rating counts were **not**
  re-read for any product. `verifiedDate` therefore stays at the register owner's
  `2026-11-20` and no field is relabelled as freshly confirmed by this session.
- The four **policy** pages below were read for wording; the *Associates Central*
  dashboards (tracking report, commission rate, Special Link builder) are behind a login
  and were not opened. Anything that needs that login stays an owner action (SG-01,
  FLG-015).
- The short links' redirect behaviour was not re-tested (see §1).

## 5. Policy sources read

| Rule the site follows | Official page |
|---|---|
| Associates disclosure must be on the site, in the Agreement's words | https://affiliate-program.amazon.com/help/operating/agreement (§5) |
| Price and availability display limits; Program Content caching | https://affiliate-program.amazon.com/help/operating/policies |
| Identifying affiliate links to search engines | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links |
| Clear and conspicuous disclosure to readers | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |
| Sitemap and canonical consolidation | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls |
| Federal holiday dates used by the Thanksgiving guide | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ |

## 6. Irregularities opened by this pass

Full text on `flagged.html`:

- **FLG-087** — `topics.html` printed "twelve buyer questions" in its `<title>`, `h1` and
  description ("five published, seven queued") while the table below held fifteen rows
  (twelve published, three queued). Title, `h1` and description are now computed from
  `TOPICS` on every build. Fixed.
- **FLG-088** — scope note: titles and two buy boxes were re-read; every other spec field
  was not, so `verifiedDate` is unchanged by this session.
- **FLG-089** — the front page still shows each product twice before the first buy button
  (comparison table, then a three-card shortcut block, then the full register card for
  every product). This session built a compact card as one candidate fix and withdrew it
  from the merge when two other sessions rebuilt the same page in the same hour; the layout
  choice is an owner decision, and a fourth competing variant would be the duplication the
  flag describes.
