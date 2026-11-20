# Verification record — session e05155a0 (2026-11-20)

All checks below were performed in this session by fetching the official pages directly
(the sandbox `curl` reaches only `github.com`/`api.github.com`/npm/pypi; `www.amazon.com`,
`affiliate-program.amazon.com` and `developers.google.com` are reached through the page
fetch tool, not guessed). Every quoted clause is copied from the fetched page.

## 1. Amazon Associates Operating Agreement — disclosure wording (§5) and breach (§6)

Source: <https://affiliate-program.amazon.com/help/operating/agreement> (Updated: October 15, 2025).

- **§5 Identifying Yourself as an Associate**, verbatim: *"You must clearly and prominently
  state the following, or any substantially similar statement previously allowed under this
  Agreement ... : 'As an Amazon Associate I earn from qualifying purchases.'"*
- The site's disclosure strip and footer carry exactly **"As an Amazon Associate I earn from
  qualifying purchases."** on every page — character-for-character match. ✅
- **§6 Term and Termination**: *"...any violation of Section 5 and as specified in the Program
  Policies will be deemed a material breach of this Agreement."* This is why the exact wording
  is treated as a launch requirement, not a nicety. ✅

## 2. Amazon Associates Program Policies — price/availability, ratings, short links, tracking

Source: <https://affiliate-program.amazon.com/help/operating/policies> (Updated: April 14, 2026).

- **Participation Requirements §1 Enrollment**: a Site *"must contain original content and be
  publicly available."* The site is original, spec-backed commentary. ✅
- **§2(b) Links on Your Site**, verbatim: *"Product prices and availability may vary from time
  to time. ... your Site may only show prices and availability if: (a) we serve the link in
  which that price and availability data are displayed, or (b) you obtain Product pricing and
  availability data via Creators API or PA API and you comply with the requirements ..."*
  → The site's policy of **not** printing price/rating figures on shop pages (and keeping them
  only as dated register observations) is the compliant reading. ✅
- **§6(t) Content on your Site**, verbatim: *"You will not display or otherwise use any of our
  customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a
  link to that customer review or star rating through Creators API or PA API ..."* → the site
  does not print star ratings on shop pages. ✅
- **§6(w)**, verbatim: *"You will not use a link shortening service, button, hyperlink or other
  ad placement in a manner that makes it unclear that you are linking to an Amazon Site."* → The
  published links are full `https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20` URLs, so the
  reader always sees Amazon. The **submitted** `link.amazon/<code>` short links are the input
  only; the site never publishes them. Their Associates-workflow compliance is the owner's to
  confirm (FLG-001) — not claimed either way here. ✅ (as published)
- **§6(y)**, verbatim: *"Unless otherwise agreed by Amazon, your Site must not have price
  tracking and/or price alerting functionality."* → the site has no such feature. ✅

## 3. Google — qualifying outbound links

Source: <https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links>
(Last updated 2025-12-10).

- *"Mark links that are advertisements or paid placements (commonly called paid links) with the
  `sponsored` value."* and *"You may specify multiple `rel` values as a space- or comma-separated
  list."*
- The site tags every outbound Amazon link `rel="sponsored nofollow noopener"`. ✅

## 4. The five submitted links → registered ASINs → listing titles

Each `https://www.amazon.com/dp/<ASIN>` page was fetched 2026-11-20 and the page title read.
The register's `asin`, `officialListingUrl` and `title` all match the live listing.

| ID | ASIN | Title on the live Amazon.com listing (2026-11-20) | Matches register |
|---|---|---|---|
| P1 | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black | ✅ |
| P2 | B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included | ✅ |
| P3 | B08DKYBTPH | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel | ✅ |
| P4 | B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black | ✅ |
| P5 | B0DZFD6R9Z | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3 | ✅ |

Manual-review links (official listing pages):
- <https://www.amazon.com/dp/B0CDY277D3>
- <https://www.amazon.com/dp/B09B7SB46R>
- <https://www.amazon.com/dp/B08DKYBTPH>
- <https://www.amazon.com/dp/B0DHZTCNR5>
- <https://www.amazon.com/dp/B0DZFD6R9Z>

**Note on volatile figures.** The buy-box price and rating for each listing are live values and
change; the site deliberately does not print them on shop pages (§2(b)/§6(t)). The dated
snapshots in `data/products.json` are unchanged and remain labelled as observations, not as
live facts. The "Customers who viewed this item also viewed" prices seen on these pages belong
to *other* ASINs and were **not** read as this product's price.

## 5. What this session did NOT re-read

Field-level re-reads of every spec cell (dimensions, wattage, warranty, accessory counts) were
performed by the 2026-11-20 register pass recorded in `COORDINATION.md` (session `1b65e5a1`).
This session confirmed the ASIN→title mapping and the policy clauses above; it did not
re-derive the spec cells, so any value not re-read here stays attributed to its original
verification date rather than to this session.
