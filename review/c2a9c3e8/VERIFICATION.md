# Verification — session c2a9c3e8 (2026-11-20)

Fresh line-by-line pass. Every source below was fetched live in this session via the page-fetch tool (the sandbox socket cannot reach amazon.com / affiliate-program.amazon.com / ftc.gov directly). No value was inferred. Where a field could not be re-read today it stays labelled with its original date.

## Official sources read

| Ref | Source (manual-review link) | What it settled |
|---|---|---|
| S1 | [Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) — Updated: October 15, 2025 (shown on live page) | §5 disclosure sentence verbatim: “As an Amazon Associate I earn from qualifying purchases.” §6: violation of §5 is a material breach. §7: Service Offerings include “data, images, text”. Site disclosure matches §5 character-for-character (plus a plain-language second sentence). |
| S2 | [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) — Updated: April 14, 2026 (shown on live page) | Participation Requirements §2: “your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API…” — confirms FLG-032 link-only pricing. §2 Special Links: tag must appear as `XXXXX-##` parameter — `shopnow047c-20` matches the pattern. §2: “You must not make inaccurate, overbroad, deceptive or otherwise misleading claims…” — the no-hallucination rule. |
| S3 | [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | Disclose material connections, hard-to-miss placement, simple language (“sponsored”), never claim experience with a product you have not tried. Site: disclosure strip above the fold + footer on every page; every outbound product link labelled “sponsored” with `rel="sponsored nofollow noopener"`; no “we tested” claims (voice gate). |
| S4 | [Google Search Central — canonical](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) | Self-referential canonical + sitemap inclusion as stacked signals. Site: every page self-canonicalises; sitemap lists exactly what the build writes (20 URLs before this pass, 21 after). |

## The five listings — identification fields re-read 2026-11-20

Titles below are the live `<title>` strings returned by Amazon today. All five match `data/products.json` (P3 differs only by the `®` in “TurboFry®”, which the register omits — noted, not treated as drift).

| ID | ASIN | Live title (2026-11-20) | Register title | Match |
|---|---|---|---|---|
| P1 | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black | Same | ✓ |
| P2 | B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included | Same | ✓ |
| P3 | B08DKYBTPH | Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel | Same minus `®` | ✓ (symbol only) |
| P4 | B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black | Same (℉ vs °F) | ✓ |
| P5 | B0DZFD6R9Z | CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3 | Same | ✓ |

Manual-review links: [P1](https://www.amazon.com/dp/B0CDY277D3) · [P2](https://www.amazon.com/dp/B09B7SB46R) · [P3](https://www.amazon.com/dp/B08DKYBTPH) · [P4](https://www.amazon.com/dp/B0DHZTCNR5) · [P5](https://www.amazon.com/dp/B0DZFD6R9Z)

## Buy-box prices re-read 2026-11-20 (register values confirmed, no drift)

Read from each listing’s own Buy New block (not the “Customers who viewed” widget, which carries other ASINs’ prices — FLG-016 re-confirmed today: e.g. P1’s page shows $74.99 for B0B7C327LK, not for B0CDY277D3).

| ID | Buy box today | Register `priceNew` | Match |
|---|---|---|---|
| P1 | $79.93 | $79.93 | ✓ |
| P2 | $149.99 | $149.99 | ✓ |
| P3 | $69.99 | $69.99 | ✓ |
| P4 | $16.99 | $16.99 | ✓ |
| P5 (3-probe) | $119.99 | $119.99 (3-probe variant) | ✓ |

Prices remain **off shop pages** per S2/FLG-032; they live only in the verification register as dated observations. No register value was changed in this pass.

## New observation (not in the register) — holiday returns window

All five listings show the same Returns block today: “FREE refund/replacement until Jan 31, 2027 — For the 2026 holiday season, eligible items purchased between November 1 and December 31, 2026 can be returned until January 31, 2027.” This is Amazon’s holiday returns policy as displayed on the listing, not a seller claim. It is used in the new guide (guide 11) with attribution and date, and flagged as **FLG-074** for owner review (whether to keep a returns-window sentence on a buying guide). No other new fact was added.

## What was NOT re-read today (stays dated 2026-11-19/20 as recorded)

- Rating counts, list prices, used prices, dimensions, wattage, warranty, bullets: carried from the 2026-11-19/20 passes (sessions 1b65e5a1, 62786810, fbfe1742). The fetch tool returns the buy box and title reliably but truncates the Product-information table; re-reading those fields a third time today would add noise, not evidence. They are labelled “carried”, never presented as re-verified here.
- Thermometer dimensions (P4/P5): still blank in the register (FLG-004). P4’s `Item Length` 6.5 in was found by session 62786810 (FLG-072); a single axis is not a dimension set, so the register stays blank.
- P2 accessory count (FLG-021) and P3 wattage conflict (FLG-022): listing-internal disagreements, both values published side by side. Not re-read today; unchanged.
- Short-link redirects: carried from 2026-11-19/20 (all five resolve to the registered ASINs; no `tag=` on the redirect path — FLG-015). Not re-followed today.
- Special Link test (FLG-001): requires Associates Central login. No session can close it. Still the one gate only the owner can clear.

## Irregularities found in this pass

- **FLG-074 (new):** Holiday returns window observed on all five listings 2026-11-20. Published in guide 11 with attribution; owner to confirm it stays.
- **FLG-075 (new):** P3 title carries `TurboFry®` on the live page; the register omits the `®`. Cosmetic; recorded so a future title-diff does not look like drift.
- **FLG-076 (new):** Widget prices on listing pages ($74.99, $229.99, $59.99, $16.99-for-B0GL7Z4KP4, $139.99…) belong to other ASINs in “Customers who viewed”. Re-confirms FLG-016. No widget figure was used as a product price in this pass.

## Gates run on this branch

`python3 build_site.py` · `node scripts/check_site.mjs` · `node scripts/check_meta.mjs` · `node scripts/check_style.mjs` · `node scripts/verify_structure.mjs` · `python3 counter-check/tools/check_site.py` — see COORDINATION.md completion record for results.

## Addendum — gate and calendar irregularities found while publishing (2026-11-20)

| ID | What was checked | Evidence read | Action |
|---|---|---|---|
| FLG-077 | Does the reader voice gate actually cover the new guide? | `scripts/check_meta.mjs` selects reader pages with `/^guide[-a-z]*\.html$/`. The first build named the page `guide-26qt-counter-fit.html`; the gate's own "Reader pages under voice rules" list omitted it, proving the page was unchecked rather than passing. Renamed to `guide-counter-fit.html`; re-run of the gate lists it and passes with 0 warnings. | Gate script left untouched (another session owns `scripts/`). Request logged in `COORDINATION.md` to widen the pattern or select by body class. |
| FLG-078 | Do the calendar rows describe distinct questions? | Topic 11 "Counter space math: will a 26-quart oven fit your kitchen?" is the same question as topic 06, now published; topic 09 overlaps topics 01/03. https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls (fetched 2026-11-20): consolidate duplicates, one canonical per page. | Row 11 marked `Consolidated` and points at the live guide; row 09 re-scoping left to the next editorial pass, flagged publicly on `flagged.html`. |
| — | Two drafted sentences in guide 11 were not supportable. | "roughly two side-by-side toaster ovens" contradicts 15.8 in; "a full kitchen-circuit load" is an unverified electrical claim. Register fields used instead: P2 `wattage` = "1700 watts / 120 volts (Product information table on listing, read 2026-11-19)". | Removed; replaced with the labelled derivation 1700 ÷ 120 ≈ 14.2 A and a pointer to the wattage guide and the manual. |
