# Source-link audit — session arena/7bc009de-prod1 (2026-11-20)

Read-only audit against `main @ f237c4a`. No shared output (HTML, data, sitemap, feed, board rows) was edited. Board tasks: T-7BC-1 (per-row source links), T-7BC-2 (reachability of cited official URLs), T-7BC-3 (requests to owners).

Rule audited (brief, *Verification*): "Every table row must have a source link to an official site. If a value can't be confirmed from an official source, leave it blank and flag it as unverified."

Reproduce: `python3 review/7bc009de/audit_source_links.py` (script in this folder; writes nothing).

## 1. Result

| Measure | Value |
|---|---|
| HTML pages scanned | 34 |
| Data rows scanned (header-only rows skipped) | 478 |
| Rows with a per-row official or internal source link | 131 |
| Rows **without** a per-row source link | **347** |

The 347 gaps are not one problem. They fall into three groups with different fixes.

### Group A — product data rows with no per-row source (the brief's rule is not met)

These are the spec tables a buyer reads. Each value is traceable on the site to the register (`verification.html`), but the row itself carries no link.

| Page | Rows without a per-row link | Examples |
|---|---|---|
| `air-fryers.html` | 9 of 11 | Form; Capacity (title); Capacity field; Dimensions; Counter depth; Footprint; Capacity per sq in (derived); Power; Cleanup |
| `compare.html` | 9 of 12 | Category/form; Capacity; Power; Dimensions; Key differentiator; per-product derived-figure table |
| `thermometers.html` | 8 of 10 | Type; Accuracy claim; Read/monitoring; Probes; Heat rating; Waterproof; Battery; Dimensions (FLG-004) |
| `guide-instant-read-vs-wireless.html` | 7 of 8 | Stated accuracy; Read time; Readings; Range; Heat rating; Water; Power |
| `guide-gifts-by-budget.html`, `guide-holiday-hosting.html`, `guide-thanksgiving-counter.html` | 5 + 3 + 3 | Budget-band rows (product name is linked; the spec claim beside it is not) |

**Why this matters:** a cell such as "120 V / 1700 W (bullets)" is a claim about a product listing. The source for that claim should sit beside it, not three clicks away on another page.

**Not filled in by this session.** Adding links is a markup change in `build_site.py`, which five open PRs also edit (#46, #48, #50, #54, #56). Per the board rule, the change is requested in §4 rather than made here.

### Group B — register rows that name the source but do not link it

`verification.html`, "Confirmation date" row, one per product (5 rows, tables 0–4). The row reads "2026-11-20 — Amazon.com product page for ASIN B0CDY277D3", with no URL. The same tables do link the listing in the row above, so the fix is small.

Also in this group: `verification.html` table 6 (per-product re-read notes, P1–P5) and table 7 (claim-check rows). These refer to pages by name, not by URL.

### Group C — internal record rows (not product data)

`suggestions.html` (101 gaps), `flagged.html` (61), `decisions.html` (57), `methodology.html` (25), `design-brief.html` (17), `review-desk.html` (8), `about.html` (4). These are decision, suggestion, flag and method rows. They cite FLG/SG/Q identifiers, which link to the register. Whether they need an external official source depends on the claim in each row. That call belongs to the register owner, so it is not changed here.

`topics.html` passes (15 of 15). `compliance.html` and `executive-summary.html` pass 5 of 9 each.

## 2. Official URLs cited by the site — reachability (T-7BC-2)

All checks are fetch_page reads on 2026-11-20 (outbound fetch from the sandbox is limited to a few hosts, so this was done with the fetch tool).

| # | URL cited | Observed title / text (2026-11-20) | Result |
|---|---|---|---|
| 1 | https://www.amazon.com/dp/B0CDY277D3 | "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black" (resolved to `?lv=shuf&...`, same ASIN) | Reachable; title matches register |
| 2 | https://www.amazon.com/dp/B09B7SB46R | "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven ... 24 One-Touch Preset Options ... Six Cooking Accessories Included" | Reachable; title matches; "24 presets" and "six accessories" are the title's own words (FLG-002, FLG-021 remain open) |
| 3 | https://www.amazon.com/dp/B08DKYBTPH | "Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option..." | Reachable; title matches (the ® is present on the page; the register omits it, as already noted in the verification log) |
| 4 | https://www.amazon.com/dp/B0DHZTCNR5 | "ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified ... Black"; buy box **$16.99**, "In Stock", seller Amazon.com | Reachable; price matches register snapshot |
| 5 | https://www.amazon.com/dp/B0DZFD6R9Z | "CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors ... Gen3" | Reachable; title matches |
| 6 | https://affiliate-program.amazon.com/help/operating/agreement | "Associates Program Operating Agreement — **Updated: October 15, 2025**" | Reachable; date matches `compliance.html` |
| 7 | https://affiliate-program.amazon.com/help/operating/policies | "Associates Program Policies — **Updated: April 14, 2026**" | Reachable; date matches `compliance.html` |
| 8 | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | "Disclosures 101 for Social Media Influencers", footer "November 2019" | Reachable; content read (see §3, item 3) |
| 9 | https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews | Endorsements, Influencers, and Reviews hub | Reachable |
| 10 | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | "How to Specify a Canonical with rel=\"canonical\" and Other Methods" | Reachable |
| 11 | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | "Qualify Your Outbound Links to Google" — `rel="sponsored"` for paid links; "Last updated 2025-12-10 UTC" | Reachable; supports the sponsored-link rule |
| 12 | https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/ | Federal Holidays 2026 table | Reachable; used for the holiday-window dates on the guides |

Other cited hosts (`schema.org`, `rssboard.org`, `github.com` issue templates) were not fetched in this pass; they are listed as not checked.

**Limits.** The reachability check reads the first page chunk of each URL. It does not re-read every figure on every listing. Buy-box prices for P1, P2, P3 and P5 are not in the first chunk of the fetched pages, so this audit does **not** re-confirm them. The dated register values stand as recorded in `verification.html` and FLG-023.

## 3. Build-level checks run on the same tree (all read-only)

- `python3 build_site.py`: exit 0, output unchanged after rebuild (`git status` clean).
- `scripts/check_site.mjs`, `check_meta.mjs`, `check_style.mjs`, `verify_structure.mjs`, `check_measure.mjs`: all exit 0.
- `counter-check/tools/check_site.py`: exit 0.
- Amazon anchors (`https://www.amazon.com/dp/…`): **148 found, 0 missing `rel="sponsored"`**.
- Verbatim Associates sentence ("As an Amazon Associate I earn from qualifying purchases.") present on **34 of 34** pages.
- Stray `example.com` canonicals: none in live pages. The one mention is a historical line in `docs/verification-log.md`.

## 4. Irregularities and requests (logged on COORDINATION.md; not edited here)

1. **Group A, product spec rows (33 rows across 4 pages).** Add a per-row source link (the ASIN's Amazon listing, or the register row) to each spec cell in `air-fryers.html`, `compare.html`, `thermometers.html`, and the instant-read and gift guides. Owner: the owner of `build_site.py` table rendering. Request only.
2. **Group B, five "Confirmation date" rows in `verification.html`.** Link the source text to `https://www.amazon.com/dp/<ASIN>` for each product (B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z). Owner: the verification-table owner.
3. **FTC placement, for the compliance owner to decide.** The FTC *Disclosures 101* page (fetched 2026-11-20) says the disclosure "should be placed with the endorsement message itself" and "hard to miss", and warns that disclosures "are likely to be missed if they appear only on an ABOUT ME or profile page ... or anywhere that requires a person to click MORE." The site's disclosure is a strip under the masthead (required by this brief) and repeated in the footer. That is prominent, but it is not "with the endorsement." Recommendation: the compliance owner decides whether a short "As an Amazon Associate I earn from qualifying purchases." line should also sit beside each product card, and records that decision in the register. This session makes no claim that the current placement is non-compliant. The FTC page is a guide, not a legal determination.
4. **Group C rows.** The register owner decides which rows need an external source and which are internal records. Not changed here.
5. **Not re-verified here.** Buy-box prices for P1, P2, P3, P5 on the live listings; rating counts (FLG-024, FLG-067); the P2 accessory count (FLG-021). These remain as stated in `verification.html` and their FLG entries.
6. **Shortened links.** The five submitted `link.amazon` short links still carry no tag (FLG-015) and their compliance status is unresolved (FLG-001). Nothing in this audit changes that.

## 5. Sources (official, fetched 2026-11-20)

- Amazon.com product pages: the five ASINs in §2, rows 1–5.
- Amazon Associates Program Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement
- Amazon Associates Program Policies: https://affiliate-program.amazon.com/help/operating/policies
- FTC, Disclosures 101 for Social Media Influencers: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- FTC, Endorsements, Influencers, and Reviews: https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews
- Google Search Central, canonicalisation: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Google Search Central, qualify outbound links: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- OPM, Federal Holidays: https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/

## 6. Irregularity count

Blocking: **0**. Non-blocking flags: **5** (§4 items 1–3, 5, 6). Nothing here is presented as verified beyond what the cited pages show on 2026-11-20.
