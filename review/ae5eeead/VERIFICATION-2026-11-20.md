# Verification record — session arena/ae5eeead-prod1, 2026-11-20

Scope, stated plainly: a **line-by-line re-read of the five listings** and of the two policy documents
the site's rules rest on, plus the copy changes this session made. Figures that move were re-sampled
and the register was updated; figures that did not move were confirmed. Anything the pages state is
traceable to a fetch made in this session or to a row already in the register with its own date.

Base: `origin/main @ f237c4a` (fast-forwarded before any edit — the branch had been cut 30+ commits
behind, which is why the first build on it failed its own triage gate and three publishing gates
reported sponsored-link failures that did not exist on `main`).

## 1. The five listings, read 2026-11-20

Every page below was fetched in this session. Quoted values are what the page showed, not a
carry-over from an earlier pass.

| Ref | Page read | Values confirmed on the page | Values that had drifted and were updated | Still not stated on the listing |
|---|---|---|---|---|
| P1 | https://www.amazon.com/dp/B0CDY277D3 | Title; 4.2 stars, **4,878** ratings; buy box **$79.93**; list **$99.99**; used **$62.85**; 13.38"D x 11.81"W x 10.63"H; capacity field 6 liters; special features; bullets; 120 V / 1700 W; cETL and 1-year assurance ("1-year assurance provided by Chefman") | rating count 4,877 → **4,878** | in-box contents |
| P2 | https://www.amazon.com/dp/B09B7SB46R | Title ("24 One-Touch Preset Options", "Six Cooking Accessories Included"); 16.9"D x 15.8"W x 14.8"H; capacity field 24.6 liters; special features; bullets (4–6 people, 6-lb rotisserie chicken, 12-inch pizza, **25 COOKING PRE-SETS**); buy box **$149.99** | — | warranty period (a PDF is linked, no term in text); dimensions of the accessory set |
| P3 | https://www.amazon.com/dp/B08DKYBTPH | Title (TurboFry 4-in-1, 450°F Hi-Fry); 12.75"D x 13.5"W x 10"H; capacity field 8 quarts; special features; bullets (**1000 Watts/120 Volts – RJ38-SQSS-8T**, 200–400°F, top-rack dishwasher-safe basket and flat tray, cETL, 1-year warranty); variant selector **6 / 8 / 9 quarts**, stainless steel or black; buy box **$69.99**, list **$119.99** | — | in-box contents |
| P4 | https://www.amazon.com/dp/B0DHZTCNR5 | Title (±0.5°F, NIST&NSF, IP67); specification field **NIST, NSF**; included components **1 thermometer, 1 AAA battery, 1 user manual, 1 calibration certificate**; care instructions "Wipe Clean"; bullets (thermocouple, 1-second read, motion wake, auto-rotate); buy box **$16.99** | — | product dimensions; warranty period; a heat rating |
| P5 | https://www.amazon.com/dp/B0DZFD6R9Z | Title (3 Ultra-Thin Probes, 1000°F, 5 Sensors, Gen3); special features "5 Sensors, Unlimited Range"; specification field lists NIST, NSF and 18 other standards; included components **3 Probes, Hub**; connectivity Bluetooth, Wi-Fi; care "Dishwasher Safe"; bullets (4 internal + 1 ambient sensor, 50 hours per charge, two-year assurance); variant selector **1 / 2 / 3 / 4 probes**, 3-probe buy box **$119.99** | — | **no ±°F accuracy figure anywhere in the listing text** (FLG-004 stays open); product dimensions |

Method note, unchanged from earlier passes: each listing page also renders "customers who viewed"
and sponsored blocks that show **other ASINs'** prices and star counts. None of those figures were
used. Where a buy box could not be attributed to the product, nothing was recorded (FLG-016).

## 2. Policy sources read 2026-11-20

| Source | Read | What it settles for this session |
|---|---|---|
| https://affiliate-program.amazon.com/help/operating/agreement (header: **Updated October 15, 2025**) | 2026-11-20, §§1, 4, 5, 6 | §5 requires the disclosure "As an Amazon Associate I earn from qualifying purchases." (or a substantially similar statement previously allowed) — the site carries it verbatim. §1 defines Special Links as links that "properly use the special 'tagged' link formats we provide", which is why the site builds `https://www.amazon.com/dp/ASIN?tag=shopnow047c-20` and does not treat the submitted `link.amazon` short links as validated. |
| https://affiliate-program.amazon.com/help/operating/policies (header: **Updated April 14, 2026**) | 2026-11-20, Commission Income Statement §5–6, Participation Requirements §1 | Nothing in this session's changes contradicts the policies: no price, availability, rating or "bought in past month" figure is printed on a shop page; the campaign ledger stays empty. |

No page in this session states a commission rate, a revenue figure or a traffic forecast. The
`link.amazon` short-link compliance question (**FLG-001 / Q-01**) is **not** resolved here and is not
claimed to be: the register resolves the five codes to five ASINs and stops there.

## 3. What changed, and the check behind each change

| Change | File(s) | Verification |
|---|---|---|
| Buyer brief + scaled depth chart above the spec table on `air-fryers.html`; same brief on `thermometers.html` | `build_site.py`, `assets/style.css`, generated HTML | Depth values read from `data/products.json`, which was re-read from the listings today (table 1). Chart uses a native `<meter>` with `min=0`, so the bar length is the number, not a decoration. |
| Product cards now print **in-box contents**, **warranty as listed** and **features**, and print nothing where the listing is silent | `build_site.py`, `data/products.json` (`includedComponents`, `warranty`, `careNotes`, `amazonCategory`, `recheckDate`), generated HTML | P4 and P5 in-box lists are the listing's own "Included Components" field; P2's warranty line reproduces the listing's silence and links FLG-005; P1/P3 in-box fields are blank because the pages state none (FLG-083). |
| Front page rebuilt as a publication front: five product entries by "what you cook", the chooser as the sixth card, seasonal band, guide grid, "how this desk works" | `build_site.py`, generated `index.html` | Every sentence re-checked against table 1. `scripts/check_meta.mjs` voice rules pass on the page; the claim audit's four needles were re-pointed to the new sentences and re-run (a build fails if the sentence and the audit disagree). |
| `guides.html`: guide count computed from the cards; the "consolidated URLs" paragraph reworded as "Pages that moved" and turned into a table | `build_site.py`, generated `guides.html` | The count was typed ("Ten") against 13 cards, then 16 after a parallel session's merge — a stale number on an index page. Now computed; the build asserts the token is gone. |
| `decisions.html`: each gate gains an **Answer ‹gate›** panel that builds the one-line reply the board asks for, for copying — nothing is submitted or stored | `build_site.py`, `assets/app.js` (`ctgDecision`), `assets/style.css` | Client-side only; no network call, consistent with `data/editorial.json` `events.endpoint` being empty. The measurement-contract gate still reports the five events and nothing else. |
| Sponsored-link post-step in `build_site.py` rewritten | `build_site.py` | The old regex only matched `<a href="…">` with nothing after the href, so five hand-written citations in `executive-summary.html` shipped without `rel="sponsored"` and `check_site.mjs` failed. The new pattern matches the tag and adds the attributes only when `rel` is absent. Gate now passes on 62 files. |
| Board rows added and triaged | `build_site.py` (SG-58, Q-42), `data/decisions.json` | `build_site.py` refuses to write `suggestions.html` unless every `SG-`/`Q-` id is classified in exactly one theme; both new rows are triaged (D-06, D-07) and the build passes. |

## 4. Gates run on the final tree (all five, plus two extra)

- `python3 build_site.py` — 37 pages, 27 sitemap URLs, 4 consolidated pages; deterministic rebuild, second run byte-identical.
- `node scripts/check_site.mjs` — PASSED, 62 HTML files.
- `node scripts/check_meta.mjs` — passed, 0 warnings (metadata, voice, price policy, sitemap/feed/noindex consistency).
- `node scripts/check_style.mjs` — passed, 129 classes, 0 undefined.
- `node scripts/check_measure.mjs` — passed; five-event contract identical across data, client, server and the published page.
- `node scripts/verify_structure.mjs` — passed, 37 pages, 0 blocking, 0 warnings.
- `python3 counter-check/tools/check_site.py` — independent audit build: PASSED.
- Local link crawl over the built root (every `href`/`src`, including anchors): 0 broken links, 0 missing anchors.

## 5. Irregularities filed or kept open

- **FLG-083 (new)** — three of five product cards can print no in-box list because the listings state none; the field is left empty rather than filled from the title or from a related listing. Owner action: none, but a seller question is recorded (Q-42).
- **FLG-002, FLG-005, FLG-021, FLG-022, FLG-004** — re-confirmed as still open by today's reads; nothing was "fixed" by guessing.
- **FLG-001 / Q-01** — the submitted `link.amazon` short links still have no documented compliance status, and this session did not test them inside Associates Central (it has no login). Not called invalid, not called valid.
- **FLG-023** — price, rating, rating count and "bought in past month" remain in the register as dated observations and are still not printed on shop pages. P1's rating count moved again today (4,877 → 4,878), which is the reason for that rule, not an exception to it.

## 6. One bug this session introduced, and how it was caught

The decision-desk helper (`window.ctgDecision`) was first appended inside the existing suggestion-board
IIFE, **after** its `if(!board) return;` guard. On any page without `#suggestion-board` — which is
every page except `suggestions.html` — the function would never have registered, so the new "Build the
answer line" button on `decisions.html` would have done nothing. No gate could catch this: the static
gates read source text, not runtime state. It was found by loading `assets/app.js` in Node with a stub
`document` and calling the function. Moved to top level; re-tested with a selected option (returns
`D-04 = option 2, <date>, evidence: …`) and with none (`Pick a path first.`). Recorded here because a
silent no-op button is exactly the kind of failure a "looks published" site hides.
