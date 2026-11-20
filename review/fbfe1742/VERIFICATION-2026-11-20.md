# Verification report — session arena/fbfe1742-prod1 (2026-11-20)

Line-by-line review of the published site and register. Every claim below names the
official source it was checked against, fetched live in this session where marked
**[live]**, or carried from a dated same-day record by another session where marked
**[carried]**. Nothing is marked verified without a source; nothing was inferred.

Manual-review links (official):

- Operating Agreement: https://affiliate-program.amazon.com/help/operating/agreement
- Program Policies: https://affiliate-program.amazon.com/help/operating/policies
- FTC Disclosures 101: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Listings: https://www.amazon.com/dp/B0CDY277D3 · /dp/B09B7SB46R · /dp/B08DKYBTPH · /dp/B0DHZTCNR5 · /dp/B0DZFD6R9Z

## 1. Product register — live spot-check 2026-11-20 [live]

| Field checked | Result | Source |
|---|---|---|
| P1 B0CDY277D3 title ("CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, …") | matches register | Amazon listing page title, fetched 2026-11-20 |
| P1 buy box price $79.93 | matches register (`priceNew`), snapshot re-confirmed | listing buy box "Buy New $79.93", fetched 2026-11-20 |
| P2 B09B7SB46R title ("Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| … Six Cooking Accessories Included") | matches register; title states **six** accessories — corroborates FLG-021 (listing description says seven) | listing page title, fetched 2026-11-20 |
| P3 B08DKYBTPH title ("Chefman Air Fryer 8 Qt \| TurboFry 4-in-1 with 450°F Hi-Fry Option …") | matches register | listing page title, fetched 2026-11-20 |
| P4 B0DHZTCNR5 title, rating 4.6 / 3,499, price $16.99, list $22.99, "5K+ bought in past month" | all match register | listing product block, fetched 2026-11-20 |
| P5 B0DZFD6R9Z title ("CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes … Gen3") | matches register | listing page title, fetched 2026-11-20 |
| P1–P5 submitted short links → ASINs | **[carried]** re-resolved 2026-11-20 by session `arena/1187e20d-prod1` (re-verify short links) and 2026-11-19 by earlier sessions; observed targets recorded in the register's separate `observedRedirectTarget` field | COORDINATION.md records; register rows |

**[carried]** P2 rating 4.3 / 18,375 · P3 rating 4.4 / 16,892 · P5 4.2 / 2,178 · P2 $149.99/$209.99 · P3 $69.99/$119.99 · P5 $119.99/$219.99 — read on the same listing pages on 2026-11-20 by session `arena/963ca90f-prod1` (re-verification of five ASINs) and 2026-11-19 by sessions `8e82d03c`/`2d5ebe5b`; recorded in COORDINATION.md with the same links. Not re-read a third time the same day; rating counts drift hourly and are presented on the site only as dated snapshots in the register (FLG-032/FLG-033 policy open).

Blanks kept blank (rule: never infer): P4/P5 dimensions — no dimensions field found on the listings (FLG-004); Emeril warranty term — listing links a warranty PDF but states no term (FLG-005).

## 2. Policy quotes — live re-read 2026-11-20 [live]

| Quote on the site | Verdict | Source |
|---|---|---|
| Disclosure sentence "As an Amazon Associate I earn from qualifying purchases." | **verbatim match** with OA §5 ("You must clearly and prominently state the following … : 'As an Amazon Associate I earn from qualifying purchases.'") | OA, fetched 2026-11-20 |
| "any violation of Section 5 … will be deemed a material breach" | confirmed (OA §6, termination clause (a)) | OA, fetched 2026-11-20 |
| Service Offerings include "data, images, text" | confirmed (OA §7 disclaimers, caps in original) | OA, fetched 2026-11-20 |
| "your Site may only show prices and availability if: (a) we serve the link … or (b) you obtain Product pricing and availability data via Creators API or PA API …" | **verbatim match** with Participation Requirements §2 (this is the basis of FLG-032/FLG-033, still open as an owner decision) | Program Policies, fetched 2026-11-20 |
| Special Links must carry the Associates tag "as a parameter in the URL" (format XXXXX-##) | confirmed (Participation Requirements §2(b)); site URLs use `?tag=shopnow047c-20` | Program Policies, fetched 2026-11-20 |
| "You must not make inaccurate, overbroad, deceptive or otherwise misleading claims about any Product…" | confirmed (Participation Requirements §2) | Program Policies, fetched 2026-11-20 |
| OA updated date "October 15, 2025" / Policies updated date "April 14, 2026" as shown on compliance.html | both match the live pages' "Updated:" lines | fetched 2026-11-20 |
| Program Policies §6(t) star-rating rule and §6(y) no price-tracking rule | **[carried]** quoted on compliance.html; read line-by-line 2026-11-19 by sessions `b49d8595`/`2d5ebe5b` with the same link; not re-read today | compliance.html rows cite the source |

FTC Disclosures 101 placement guidance ("hard to miss", plain language) — **[carried]** read 2026-11-19 by sessions `ab9cbcdc`/`8e82d03c` (link above). Applicability remains a reviewer judgment, as recorded.

## 3. Structural audit of the published register [live, automated]

- `verification.html`: every product-fact row carries a source link to `amazon.com` (50 `amazon.com/dp` links on the page). Intended ASIN and observed redirect target are separate rows and never merged (the brief's rule), with the open caution preserved: the submitted nine-character codes cannot themselves be validated as ASINs (FLG-013/FLG-045, owner confirmation Q-03 pending).
- Empty/blank cells exist exactly where values could not be confirmed and are flagged (FLG-004, FLG-005). No invented values found.
- `data/products.json` → `observedRedirectTarget` is a separate field from `asin`; `confirmationDate`/`confirmationSource` present on all five.

## 4. Machinery verified in this session [live, automated + runtime]

- **Measurement contract unified.** `assets/app.js`, `analytics-endpoint/server.py`, `data/editorial.json` (`events.five`) and `methodology.html` now agree on exactly the five defined events: `page_view`, `outbound_click`, `search`, `chooser_complete`, `guide_read`. Requests R-06/R-07 closed; the legacy tracker `assets/js/analytics.js` (third vocabulary, unreferenced, invented client-side conversion events) deleted; root `app.js` verified network-silent.
- **Endpoint runtime probe.** `python3 analytics-endpoint/selftest.py`: 17/17 checks pass (five events accepted with the client envelope, old vocabulary `guide_read_75` rejected, malformed rejected, daily counts + per-ASIN bucketing, no query text or per-event timestamps stored). Live HTTP probe (server started, real POSTs): all five events → 204; `guide_read_75` → 400; malformed → 400. Nothing leaves any visitor's device while `events.endpoint` is empty.
- **New publishing gate.** `scripts/check_measure.mjs` runs in the Pages workflow before upload; negative-tested with three planted defects (server vocabulary drift, client gate removal, legacy tracker reappearance) — all three blocked; clean tree passes.
- **One site to index.** Generated `robots.txt` now disallows `/counter-check/`, `/docs/`, `/articles/`, `/review/`, `/analytics-endpoint/` (FLG-039 remediation; reversible; deletes nothing). Sitemap continues to list exactly the 25 canonical pages.
- **Determinism.** `python3 build_site.py` twice → byte-identical output.
- **Gates green:** `check_site.mjs` PASSED (54 HTML files), `check_meta.mjs` PASSED (5 pre-existing non-blocking title/description length warnings), `check_measure.mjs` PASSED, `counter-check/tools/check_site.py` PASSED (16 pages, 5 products, 21 flags).

## 5. Irregularities found or carried (all published on flagged.html, none blocking)

- **New this session — none.** The spot-check found no drift between the register and the live listings for the fields read today.
- Carried, unchanged: FLG-001/FLG-015 (Special Link test in Associates Central is a manual owner gate — Q-01), FLG-003, FLG-004, FLG-005, FLG-021, FLG-022, FLG-032/033 (price/rating display vs Participation Requirements §2 — owner ratification), FLG-039 (now robots-suppressed), FLG-051 (Pages build source).
- Observation, not a defect: the live P4 listing currently shows a "Black Friday Deal" badge and the holiday return window (returns until Jan 31, 2027 for Nov 1–Dec 31 purchases). Promotions change; per Participation Requirements §2 any promotion mention must be removed when the promotion ends — the site makes none, and the guide copy tells readers to check Amazon. No action needed.

## 6. What this session did not verify

- The Associates Central Special Link test and tracking report (requires the owner's enrolled account; SG-01/Q-01).
- Search Console, analytics hosting, and reader capture (owner decisions: SG-02/SG-03/SG-07).
- Third-party claim sources behind FLG-037/FLG-038 (flagged as third-party claims only).
