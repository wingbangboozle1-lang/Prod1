# Executive recommendations, buyer-information gaps and a review path

**Session:** `arena/35638f92-prod1` · **Date:** 2026-11-20 · **Scope:** review documentation only
**Compiled from:** this checkout at `main` (PR #59 merged), plus official pages fetched by this session (listed in §7).
**Not a certification.** Nothing here approves a claim, a price, a rate or a publication step. Where a value could not be read from an official page, it is left blank and listed as missing.

---

## 1. Executive summary

The repository already ships what most affiliate briefs ask for and rarely get: a generated static site with one canonical host, a sitemap and feed written by the same build that writes the pages, per-page Associates disclosure, `rel="sponsored"` on every outbound product link, a separate register of intended ASINs versus observed redirects, a five-event measurement contract with a working endpoint that is deliberately **not** hosted, and publishing gates that have blocked a deploy when a register row was untriaged. On this checkout (rebased onto `main` after PR #48 and #73 merged) the build writes 37 pages / 27 sitemap URLs / 33 search-index entries, and all five node gates plus the generator pass (§6).

The gap is no longer "does the site exist". It is three things:

1. **Nothing is measured yet.** The endpoint runs nowhere (`data/editorial.json` → `events.status = "defined, local-only"`, `events.endpoint = ""`), Search Console has never been claimed, and the campaign ledger is empty by design. Every statement about which page or product earns a click is therefore unknown, not merely unproven. The brief's own order — measure before optimizing — is still at step zero, and only the owner can move it.
2. **The shop copy is honest but thin in the one place Google rewards.** The site's differentiator is real (dated, sourced specs; counter-space arithmetic; explicit "what the listing leaves out"). But a large share of the per-product prose is a paraphrase of seller bullets, which is the pattern Google's spam policies call *thin affiliation*. The fix is not more pages; it is more original decision material per page.
3. **The review surface has drifted from itself.** The suggestions board now carries 57 SG rows and 39 Q rows; `decisions.html` generates the count correctly, while two live places still quote "43 suggestions and 27 questions" and "42 suggestions and 26 questions". Four rows are classified into two decision themes at once. A reader who checks the numbers finds a site that miscounts its own board — the exact credibility cost the site exists to avoid.

Recommendations, in the order that unblocks the most: §5. Each has options, a recommended path, effort, the evidence it needs and what it blocks.

---

## 2. What this session verified from official pages

All reads were made 2026-11-20 through the page-fetch tool against `www.amazon.com` product pages. Only what appears below was read; nothing was inferred.

| # | ASIN | Page title read (matches register) | Buy box read | Register `priceNew` | Register `priceList` | Match |
|---|---|---|---|---|---|---|
| P1 | B0CDY277D3 | CHEFMAN 6 Quart Dual Basket Air Fryer Oven … - Black | $79.93, In Stock, shipped and sold by Amazon.com | $79.93 | $99.99 | Title and buy box match |
| P2 | B09B7SB46R | Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven … | $149.99, In Stock | $149.99 | $209.99 | Title and buy box match; list price not seen in the chunk read |
| P3 | B08DKYBTPH | Chefman Air Fryer 8 Qt / TurboFry® 4-in-1 with 450°F Hi-Fry … | $69.99, In Stock | $69.99 | $119.99 | Title and buy box match; list price not seen in the chunk read |
| P4 | B0DHZTCNR5 | ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ … Black | $16.99 (−26%), list price $22.99, In Stock, 7 new offers from $16.99 | $16.99 | $22.99 | Title, buy box and list price match |
| P5 | B0DZFD6R9Z | CHEF iQ Sense / Smart Wireless Meat Thermometer / 3 Ultra-Thin Probes … Gen3 | $119.99 (−45%), list price $219.99, In Stock | $119.99 | $219.99 | Title, buy box and list price match |

Also read directly off the listing pages this session (register agrees where it records them):

| Fact | Listing | Value read 2026-11-20 | Register |
|---|---|---|---|
| Rating and count, P4 | B0DHZTCNR5 | 4.6 out of 5, 3,499 ratings; "Amazon's Choice"; "5K+ bought in past month" | 4.6 / 3,499 — agree (badge recorded as a listing snapshot) |
| Rating and count, P5 | B0DZFD6R9Z | 4.2 out of 5, 2,178 ratings; "1K+ bought in past month" | 4.2 / 2,178 — agree |
| P4 in-the-box list | B0DHZTCNR5 | "1*Meat Thermometer, 1*AAA Battery, 1*User Manual, 1*Calibration Certificate" | Site already says a calibration certificate is included |
| P4 "newer model" module | B0DHZTCNR5 | Orange B0GL7Z4KP4, $16.99, 4.7 (144), In Stock | Already flagged as FLG-003 |
| P5 variant caveat | B0DZFD6R9Z | Price shown as "$119.99 ($40.00 per count)" with a variant selector | Register records "$119.99 (3-probe variant)" — consistent |

**Deal-badge observation (new).** Both thermometer listings carried a live "Black Friday Deal" banner with a percent saving on 2026-11-20, and P4's offer block read "7 new offers from $16.99". The air-fryer pages read in this session showed no such banner in the chunks that contain price and availability, but that is not proof of absence — the banner sits higher in the page and this session did not read it for those three. See flag I-1.

**What this session did not verify:** commission rates or commission reports (requires Associates Central login), whether the five submitted `link.amazon/…` short links are compliant Special Links (unresolved, FLG-001 — they are **not** called invalid here), Search Console data, the analytics endpoint (not hosted), Pages settings or branch protection, the Emeril warranty term (FLG-005), the thermometer dimensions (FLG-004, still blank on the site), and any hands-on performance of any product.

---

## 3. How the shop reads today — evidence, not taste

| Question | Finding (evidence) | Recommendation |
|---|---|---|
| Does a buyer get to a product fast? | Front page leads with a hero, three "quick picks" cards, then a five-card comparison, then guides (`index.html`). Category pages carry the comparison tables. | Keep. The order is right. |
| Is any spec unsourced? | Every register field carries a `sourceUrl` and a `sourceNote` with a re-read date; unreadable fields are blank (thermometer dimensions). `verification.html` publishes the register beside the redirect observation. | Keep. This is the asset. |
| Is the copy original enough? | Much per-product prose is a paraphrase of listing bullets ("Good for", "Check before you buy"). Some pages are genuinely original: counter-footprint drawing and square-inch math, the three-question chooser, the gift-return checklist, the wattage discrepancy shown both ways. | Add one original decision artefact per product page: a "who this fits / who should skip" verdict written from the verified fields, and the counter-space number for the two thermometers once dimensions exist. |
| Are price and rating figures displayed? | No. Shop pages say "Today's price sits on Amazon"; dated snapshots live only in the register. This satisfies the Program Policies rule that price/availability on a site come from an Amazon-served link or the Creators/PA API. | Keep until Creators/PA access is approved; see §5, R4. |
| Is disclosure where it must be? | Verbatim Operating Agreement §5 sentence in a strip under the masthead and again in the footer, on every generated page; `compliance.html` renders it from the same `site.disclosure` field. | Keep. Optionally add one plain sentence naming the disclosure's meaning for screen-reader users in the strip's `aria-label` (cosmetic, gate-checked). |
| Is there a privacy statement? | Not as a standalone text. `about.html` explains no cookies / no identifiers / local-only counts, and `assets/app.js` confirms: `localStorage` for the chooser and counts, no network call while the endpoint is unset. | Add a short "Privacy" section to `about.html` (or a `privacy.html`) that states: no cookies set by this site, the only storage is your browser's own local storage, and outbound clicks go to Amazon whose own policies apply. Program Policies §3(e) expects an accurate disclosure of cookies/pixels and data use; the honest version today is "none, and here is how to clear it". |
| Do readers have a way in? | A "Suggest a topic" link opens a prefilled public GitHub issue (`data/reader-suggestions.json` inbox). | Keep; add one sentence saying the request and your GitHub username are public. That is a consent statement, not decoration. |

---

## 4. Questions, information and answers needed before decisions

Format per row: **Q** the question · **I** what we hold now · **A** what an answer would require · **Discover** the step that produces it · **Blocks** what stays frozen without it.

### Gate A — money and attribution

- **Q A1.** Does a click from this site reach Amazon carrying `tag=shopnow047c-20`, and does it appear in an Associates report?
  **I:** Outbound format is `https://www.amazon.com/dp/ASIN?tag=shopnow047c-20`, marked sponsored. The five submitted `link.amazon/…` targets were observed to carry no `tag=` (FLG-015); their compliance status is unresolved, not disproved.
  **A:** Owner-only, from Associates Central: one test click per product, destination check plus the tracking report.
  **Discover:** Link test in Associates Central → SiteStripe or product-link builder → click each of the five → read "Reports → Link Type / Tracking ID". Record date, report screenshot reference, per product.
  **Blocks:** any statement that this site earns commission; the whole ledger (§5, R1).

- **Q A2.** What commission rate applies to these two categories?
  **I:** Nothing. No page states a rate, and none should until read from the console.
  **A:** The rate card as it appears in Associates Central on the day it is read.
  **Discover:** Associates Central → Commission income → category rate table; record the date and whether the rate is fixed or tiered.
  **Blocks:** revenue math, "high-converting" wording, any prioritization between air fryers and thermometers.

- **Q A3.** Where do clicks and conversions get counted, and under what retention?
  **I:** Five events defined (`page_view`, `outbound_click`, `search`, `chooser_complete`, `guide_read`); endpoint code passes its self-test; `events.endpoint` is empty so nothing is sent.
  **A:** A host, an HTTPS origin, a retention period, and one sentence of privacy text.
  **Discover:** Owner picks any small HTTPS host → set `CTG_ALLOWED_ORIGIN` → set `events.endpoint` → rebuild → confirm one beacon per event. Cheapest compliant option: a single small VPS or PaaS instance in front of `server.py`.
  **Blocks:** "measure before optimizing" (the brief's own priority), topic selection from queries, any claim of traffic.

### Gate B — one site, findable

- **Q B1.** Which build is the publication, and on which address?
  **I:** Three builds are reachable on one host (root, `counter-check/site/`, `docs/`); only the root is in a sitemap; `robots.txt` disallows the other three trees; three consolidated URLs canonically point at their surviving guide.
  **A:** Owner intent for the two secondary builds; optionally a custom domain.
  **Discover:** Choose root-only, then either delete the secondary builds or add `noindex` to their pages; if a domain is wanted, add the CNAME and re-point `canonical`/sitemap/feed in one rebuild.
  **Blocks:** every ranking statement and a clean Search Console property (FLG-039 / FLG-070 / Q-34).

- **Q B2.** Has the sitemap been submitted, and is anything indexed?
  **I:** `sitemap.xml` lists 24 URLs, all written by the build; `feed.xml` carries 14 items and every sitemap guide is in the feed.
  **A:** Property verification plus the Coverage/Pages report after 28 days.
  **Discover:** Search Console → Domain or URL-prefix property → submit `sitemap.xml` → export the Queries report at day 28.
  **Blocks:** topic selection from demand (the calendar is a plan until then).

- **Q B3.** Is Pages publishing from the branch or from Actions?
  **I:** The workflow rebuilds, diff-checks and runs five gates on every push to `main`; in legacy branch mode it gates the commit rather than the artifact (FLG-051).
  **A:** Settings → Pages → Build source = GitHub Actions.
  **Discover:** Owner flips the source and re-runs the workflow once; confirm the deployed artifact equals the gated build.
  **Blocks:** the claim that a failed gate cannot reach production.

### Gate C — compliance and evidence

- **Q C1.** Are the five submitted short links acceptable Special Links?
  **I:** They resolve to the five registered ASINs; their targets carry no tag; no session may call them invalid.
  **A:** A written answer from Associates support, or retirement of the short links in favour of console-generated tagged links (which is what the site already publishes).
  **Discover:** Ask Associates support in writing; keep the answer with the register.
  **Blocks:** nothing reader-facing (the site never links the short codes); it blocks closing FLG-001.

- **Q C2.** Is Creators/PA API access available to this account?
  **I:** Repeated third-hand; never read on an Amazon page (FLG-037).
  **A:** The Tools page state, with a date.
  **Discover:** Associates Central → Tools → Creators API / PA API; note whether credentials can be issued and under which sub-features.
  **Blocks:** any live price/rating display, any automated refresh, any "API-driven" marketing wording.

- **Q C3.** Who is accountable for the words?
  **I:** Bylines read "The Countertop Guide editorial desk"; `about.html` says no individual credential is shown and flags the missing named author. Google's site-reputation guidance treats stated authorship and editorial responsibility as review factors.
  **A:** A named author or desk owner plus a correction address.
  **Discover:** Owner names one; add the name, a two-line bio and a correction contact to `about.html` and the guide byline.
  **Blocks:** E-E-A-T style trust signals, media-kit style outreach, and any "our expert" wording.

- **Q C4.** Is the imagery licensed?
  **I:** All product visuals are the site's own SVG drawings, labelled "Our drawing… not a photograph of the product". No Amazon Program Content is copied. No photography licence exists (FLG-009 / FLG-041).
  **A:** A licence or a permission decision, or a decision to stay with drawings.
  **Discover:** Two quotes from stock libraries for countertop lifestyle shots, plus a written permission request to the two brands if product photography is wanted.
  **Blocks:** the lifestyle half of any visual upgrade.

### Gate D — the board itself

- **Q D1.** Which numbers does the board publish about itself?
  **I:** `suggestions.html` says "43 suggestions and 27 questions"; FLG-050 says the board "now holds 42 suggestions and 26 questions"; the rendered board carries 54 SG rows and 36 Q rows. All three disagree.
  **A:** One rule — the counts are generated, never typed — plus a corrected sentence in both places.
  **Discover:** Print the counts from the row tables at build time and inject them into the copy; add a gate that fails when a hand-typed count does not match.
  **Blocks:** the board's credibility; nothing reader-facing on the shop pages.

- **Q D2.** Who approves, and on what rhythm?
  **I:** 54 suggestions and 36 questions await an owner pick; seven decision gates (D-01…D-07) consolidate them; four rows sit in two themes at once (SG-43, Q-02, SG-33, Q-14).
  **A:** An approval cadence and a decision on whether a row may belong to two themes.
  **Discover:** Pick a weekly 20-minute pass; approve/reject/defer with a date; make theme membership single-valued or say plainly that a row may gate two themes.
  **Blocks:** every implementation item on the desk.

---

## 5. Recommendations with options

Each recommendation states the buyer or business problem, the options, the recommended path, effort, evidence needed and what it unblocks. Nothing below is implemented by this session.

**R1 — Host the endpoint and turn on the five events (highest value, smallest change).**
Problem: the brief's first instruction is to measure before writing anything else, and the site currently records nothing outside the visitor's browser.
Options: (a) leave it local-only; (b) host `analytics-endpoint/server.py` on one small HTTPS instance; (c) adopt a third-party analytics product.
Recommended: **(b)**. It is already written, contract-tested by `check_measure.mjs`, collects only daily aggregate counts per event and path, stores no addresses/user agents/referrers/query text, and needs one environment variable plus one `events.endpoint` value.
Effort: under an hour once a host exists. Evidence needed: one beacon observed per event, plus the retention sentence. Unblocks: R2 and every future topic choice.

**R2 — Claim Search Console before writing another guide.**
Problem: the editorial calendar is currently an editorial guess; four of its rows are labelled as hypotheses.
Options: (a) keep publishing on cadence and read queries later; (b) claim the property, submit the sitemap, wait 28 days, then choose topics from queries the site does not answer.
Recommended: **(b)**, and in the meantime publish at most one guide from the existing calendar. Unblocks: honest "trending topic" language, which the site may not use today.

**R3 — Make each product page answer one decision the listing cannot.**
Problem: bullet paraphrase is the thin-affiliation pattern; the site's own differentiators (footprint math, "what the listing leaves out") appear only in places.
Options: (a) add more guides; (b) add one original verdict block per product built only from verified fields: "fits if / skip if / measure this" plus the counter-space number and the known conflict for that unit (e.g. P3's dual wattage).
Recommended: **(b)**. It costs no new facts and strengthens the two things Google's guidance names as value — original comparison and navigation. Evidence needed: nothing new; every input is already in the register. Unblocks: R5.

**R4 — Decide the price-display question once, in writing.**
Problem: prices and ratings are withheld, which is safe and compliant, but it also makes the shop less useful than it could be.
Options: (a) stay as is; (b) apply for Creators/PA API and show dated, refreshed figures with a 24-hour cache; (c) show "as of" snapshots from manual reads (not compliant with the price/availability rule, and the site already rejects it).
Recommended: **(a) now, (b) only after Q C2 is answered in writing.** Note that "bought in past month" and "Amazon's Choice" stay off the site either way — they are Amazon page furniture, not our evidence.

**R5 — Add the missing decision artefacts, in this order.** (1) Thermometer dimensions, read from the listings' Product information tables; if absent there, ask each seller in writing — do not estimate. (2) The Emeril warranty term from the linked PDF. (3) A privacy paragraph. (4) A named author/correction address. Each is small, sourced, and closes a row that is currently blank.

**R6 — Fix the board's self-count and its double-classified rows (R6 = Q D1 + D2).** Generated counts, one theme per row (or an explicit rule allowing two), and a stated review rhythm. This is the only recommendation whose absence is visible to a reader today.

**R7 — Guard the automation ambition.** The brief asks for an agent that "generates SEO-optimized articles … continuously optimizes campaigns". Google's spam policies cover *scaled content abuse* and *thin affiliation* directly, and Amazon's Agreement §5 requires that nothing be misrepresented about the relationship. Recommended framing for anything built later: automation may draft and refresh **from the register only**; a human approves each page; no page is published without a source for every factual line; no page claims testing, trend, popularity or earnings. This is a design constraint, not a compliance certification.

---

## 6. Verification performed in this session

```
python3 build_site.py            → 37 pages | 33 search-index entries | 27 sitemap URLs | 4 consolidated; sponsored post-step done
node scripts/check_site.mjs      → CHECK PASSED: 62 HTML files (disclosure, sponsored links, internal links, titles/descriptions, claim wording)
node scripts/check_meta.mjs      → Gate passed: 0 warnings, no blocking items
node scripts/check_style.mjs     → Gate passed: 0 warnings, no blocking items
node scripts/check_measure.mjs   → SELFTEST PASSED; MEASURE GATE PASSED: contract [chooser_complete, guide_read, outbound_click, page_view, search] across data, client, server and the published page
node scripts/verify_structure.mjs→ 37 pages walked, 0 blocking, 0 warnings
git diff --check                 → clean
```

Cross-checks read by hand (not gate output):

| Check | Result |
|---|---|
| Sitemap vs. generated pages | 27 URLs, of which 16 are guides; 3 consolidated guides and 7 internal surfaces deliberately excluded; no guide published as a guide is missing from the sitemap |
| Feed vs. sitemap | 16 items; every sitemap guide is in the feed |
| Consolidated pages | `guide-holiday-gifts`, `guide-small-kitchen`, `guide-holiday-roast` each self-canonicalise to their surviving guide and are out of the sitemap — consistent with Google's "consolidating several pages into one" example of a legitimate redirect |
| Disclosure | Verbatim §5 sentence in the masthead strip and the footer of every generated page; `compliance.html` renders it from the same field |
| Outbound links | Only `https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20`, marked sponsored; the five `link.amazon/…` codes appear only on review pages as submitted-link records, never as reader links |
| Duplicate FLG ids | None in `flagged.html` (78 rows) |
| Decision register | Every board row classified across 7 themes (D-01…D-07); 4 rows classified twice (SG-43, Q-02, SG-33, Q-14) — the duplication already noted in `COORDINATION.md` |
| Board counts | 57 SG + 39 Q rendered; `decisions.html` prints that count from the same data, but the board copy and FLG-050 still say "43/27" and "42/26" — see I-2 |

---

## 7. Sources (official pages fetched by this session, 2026-11-20)

- Amazon Associates Program Operating Agreement — §1 (Special Links, tagged format), §5 (the exact disclosure sentence: "As an Amazon Associate I earn from qualifying purchases."), §6: <https://affiliate-program.amazon.com/help/operating/agreement>
- Amazon Associates Program Policies — Commission Income Statement (click/session window), Participation Requirements §2 (Special Links must carry your tag; prices/availability only via an Amazon-served link or Creators/PA API), §3(e) (privacy/cookie disclosure duty), §6 (no alteration of Program Content; no ML training use), Trademark Guidelines (marks only alongside a Special Link), IP License §1–2: <https://affiliate-program.amazon.com/help/operating/policies>
- Product listing pages: <https://www.amazon.com/dp/B0CDY277D3>, <https://www.amazon.com/dp/B09B7SB46R>, <https://www.amazon.com/dp/B08DKYBTPH>, <https://www.amazon.com/dp/B0DHZTCNR5>, <https://www.amazon.com/dp/B0DZFD6R9Z>
- Amazon Return Policy (2026 holiday extended window, Nov 1 – Dec 31 2026 → Jan 31 2027), which is what the gift guides point at: <https://www.amazon.com/gp/help/customer/display.html?nodeId=GKM69DUUYKQWKWX7>
- Google Search Central, Qualify your outbound links (`rel="sponsored"`): <https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links>
- Google Search Central, Spam policies — *thin affiliation*, *scaled content abuse*, *sneaky redirects*, site-reputation examples that turn on authorship and editorial responsibility: <https://developers.google.com/search/docs/essentials/spam-policies>
- Google Search Central, SEO Starter Guide (organise the site, descriptive URLs, reduce duplicate content, descriptive titles/snippets): <https://developers.google.com/search/docs/fundamentals/seo-starter-guide>
- FTC, *Endorsement Guides: What People Are Asking* — a single home-page disclosure is not enough; a "DISCLOSURE" button is not enough; placement, readability and clarity decide whether a disclosure is clear and conspicuous: <https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking>

---

## 8. Irregularities flagged for review (new in this pass)

**I-1 — "deal badges across the board" is not backed by a per-listing record.**
`guide-holiday-hosting.html` says: "Listings read that day showed deal badges across the board (a dated observation, not a claim about today)." This session read live deal banners on the two thermometer listings and read none in the price/availability blocks of the three air-fryer listings, without reading the banner region of those pages. The blanket phrase is therefore unverified as written. Recommend: either restate it per listing ("the two thermometer listings carried a Black Friday deal banner when read on 2026-11-20; check the live page") or drop the sentence. Owner: the generator's editor. Non-blocking.

**I-2 — The board misstates its own size in two live places.**
`suggestions.html` copy (and its Q-14 row) says "43 suggestions and 27 questions"; FLG-050 says the board "now holds 42 suggestions and 26 questions"; the rendered board carries **57 SG rows and 39 Q rows**, which is exactly what `decisions.html` computes from `data/decisions.json`. So the generated count is right and the hand-typed ones are wrong. Recommend extending the same generated count to the board copy and FLG-050 (§5 R6). Non-blocking, but it is the one error a reader can catch without leaving the site.

**I-3 — Four decision rows sit in two themes.**
SG-43, Q-02, SG-33, Q-14 each appear under two themes in `data/decisions.json`. Already logged in `COORDINATION.md`; restated here because it interacts with R6 (a review cadence is meaningless if a row has two owners-by-implication). Non-blocking.

**I-4 — No privacy statement page; the honest statement currently lives in `about.html` prose.**
Program Policies §3(e) expects an accurate disclosure, via a privacy policy or otherwise, of cookies/pixels and of how visitor data is collected and used. This site sets none and sends none, which is the easiest case to state — but it is stated in a paragraph, not in a place a reader looking for "privacy" would find. Recommend a short standalone section with an anchor (`about.html#privacy`) linked from the footer. Non-blocking.

**I-5 — Third-party offers exist beside the buy box on at least one listing.**
P4's page read "New (7) from $16.99" and its buy box was Amazon.com's. The register's `priceNew` is the buy-box figure and is correct; the risk is only that a reader may land on a third-party offer page after clicking. Worth one sentence on the product page ("sold by Amazon.com when read; check the seller line"), not a data change. Non-blocking.

**Carried forward from the register, still open and still blocking a claim:** FLG-001 (Special Link test), FLG-004 (thermometer dimensions), FLG-005 (Emeril warranty), FLG-008 (endpoint not hosted), FLG-009 (no photography licence), FLG-015 (short-link targets carry no tag), FLG-022 (Chefman 8QT wattage conflict — both values shown), FLG-037 (Creators/PA eligibility unread), FLG-039/FLG-070 (three builds on one host), FLG-051 (Pages build source), Q-05 (commission rate), Q-06 (search demand).
