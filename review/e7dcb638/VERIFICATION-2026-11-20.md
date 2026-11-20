# Verification record — session arena/e7dcb638-prod1 (2026-11-20)

Scope: the fields and clauses this session's own changes rely on, checked at the primary
source today. No value was inferred. Where a check could not be completed, the item is
recorded as not verified and left blank on the site.

Rule applied throughout: a claim shipped on a page must be readable at the source in the same
sitting, or it is attributed to the dated register and labelled as such.

## 1. Listings re-read today

| ID | ASIN | What was re-read on 2026-11-20 | Result | Source for manual review |
|---|---|---|---|---|
| P1 | B0CDY277D3 | Page title as served | Matches `data/products.json` verbatim, including "Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt" | https://www.amazon.com/dp/B0CDY277D3 |
| P2 | B09B7SB46R | Page title as served | Matches the register verbatim; **"Six Cooking Accessories Included"** is in the title and **"24 One-Touch Preset Options"** is too — the two listing-internal conflicts (FLG-021 accessories, FLG-002 presets) are therefore still live, not stale | https://www.amazon.com/dp/B09B7SB46R |
| P4 | B0DHZTCNR5 | Page title; rating count seen beside the ASIN in a bundle component | Title matches the register except for one character (see §4). Rating count reads **3,499**, identical to the 2026-11-19 register value — no drift on this field | https://www.amazon.com/dp/B0DHZTCNR5 |
| P3 | B08DKYBTPH | Not re-fetched in this session | Dimensions, capacity and the 1000 W / 1700 W conflict are taken from the register, whose values were re-read by sessions `1187e20d` and `963ca90f` on 2026-11-20 and by `b49d8595` on 2026-11-19 | https://www.amazon.com/dp/B08DKYBTPH |
| P5 | B0DZFD6R9Z | Not re-fetched in this session | Variant structure is quoted from the register's dated note (2026-11-19); the guide says so in the sentence rather than implying today | https://www.amazon.com/dp/B0DZFD6R9Z |

**Two things the fetched pages showed, recorded because they justify advice on the site:**

- On P4, the page displayed a **"FREE Returns"** panel ("Return this item for free… at least one
  free return option"), and the same page's sponsored carousel showed **"Black Friday Deal"**
  chips and prices on *other* ASINs, not on B0DHZTCNR5. Both are widget-level, account- and
  date-specific, so `guide-price-check.html` uses them as the reason for its checks and quotes
  no figure from them.
- Chunk positions in a fetched listing vary between calls of the same URL (33 chunks, then 27,
  with different contents). A single fetch is not a reliable instrument for a spec table, so the
  dimensions hunt below was recorded as inconclusive rather than as "not on the listing".

## 2. Policy clauses re-read today, at the source

Source: https://affiliate-program.amazon.com/help/operating/policies — page header still reads
**"Updated: April 14, 2026"**, which is the date the register cites. Confirmed verbatim:

1. Participation Requirements §2(b), price/availability: *"…your Site may only show prices and
   availability if: (a) we serve the link in which that price and availability data are displayed,
   or (b) you obtain Product pricing and availability data via Creators API or PA API…"* → the
   basis of link-only pricing (FLG-032) and of the wording in `guide-price-check.html`.
2. Same section: *"You must not make inaccurate, overbroad, deceptive or otherwise misleading
   claims about any Product, an Amazon Site, or any of our policies, promotions, or prices."* →
   why our own drawings are labelled as drawings (FLG-061).
3. Same section: *"You must remove from your Site any links and related references to limited time
   promotions as soon as that promotion on the relevant Amazon Site ends."* → **new to this repo**
   (FLG-067); the seasonal guide is written as a method, and no reader page names a promotion.
4. Same section: a comparison-format price display must show both the lowest *new* and, where
   provided, the lowest *used* price → **new** (FLG-068); moot today because `compare.html` shows
   no prices, live the moment an API price column is added.
5. §1 Enrollment and eligibility: *"Your Site(s) must contain original content. Original content
   utilizing third-party materials must contain significant commentary, analysis, or
   transformation…"* → the affirmative case for the commentary-and-arithmetic editorial shape.
6. §2(b) also requires the Associates ID to appear *"as a parameter in the URL of each link you
   place on your Site"* — the site's own links carry `?tag=shopnow047c-20`; the submitted
   `link.amazon/…` redirects do not, which is what FLG-015 records.
7. §2(b): *"Special Links must link to Products"* and product-list pages need *"additional original
   content… relevant to the Special Link"* — the compare page is such a page, and it carries the
   sourced table and the chooser rather than a bare list.

**Not re-read in this session, deliberately:** the Operating Agreement (§5 disclosure sentence)
was re-read and confirmed verbatim by session `1187e20d` the same day
([record](https://github.com/wingbangboozle1-lang/Prod1/blob/main/review/1187e20d/VERIFICATION-2026-11-20.md));
the FTC pages were last read on 2026-11-19. This session did not duplicate either read and does
not claim them.

## 3. Arithmetic in the three new guides, re-computed

Inches → cm (× 2.54): 10.63 → 27.0002 → shown 27.0 · 14.8 → 37.592 → shown 37.6 ·
10 → 25.4 · 13.38 → 34.0 (33.9852) · 12.75 → 32.4 (32.385) · 16.9 → 42.9 (42.926).
Gap example: an 18 in cabinet gap less a 14.8 in unit = 3.2 in.
Rankings asserted: **narrowest width** P1 11.81 in < P3 13.5 < P2 15.8 ✓. **Shallowest depth**
P3 12.75 < P1 13.38 < P2 16.9 ✓. **Tallest** P2 14.8 ✓. **Largest floor area** P2 16.9 × 15.8 =
267.0 sq in, P3 12.75 × 13.5 = 172.1, P1 13.38 × 11.81 = 158.0 ✓ — which is why "smallest
footprint" is not claimed anywhere (the fix `1187e20d` made on the front page is extended here to
the chooser's client-side string, which read "shallowest footprint"; it now says "shallowest of
the three at 12.75 in deep").

## 4. Irregularities found by this session

1. **FLG-052 — 44 class names in the generated HTML had no CSS rule, and nine custom properties
   used by the desk block were never declared.** The pages were structurally fine and visually
   unfinished; that is a large part of the "generated" feel. Fixed by a component layer in
   `assets/style.css` (with token aliases), re-checked by an automated class/var coverage diff
   after the change: 0 unstyled classes among the reader-facing components, 0 undefined
   properties. The two remainders are `guide-page` (a hook, now styled) and `prompt`.
2. **FLG-063 — the thermometer specification table could not be reached by fetch.** The
   ThermoMaven page was retrieved twice; both fetches returned nav, bundles and sponsored
   carousels, not the Product information block. P4/P5 dimensions therefore **stay blank**, and
   the card text says "not shown in the fields we captured". FLG-004 remains open.
3. **FLG-064 — the register still dates the data 2026-11-19** while two sessions re-read
   listings on 2026-11-20. Pages inherit that date, so they under-report freshness by a day.
   Not edited here: `data/products.json` belongs to the register owner (coordination rule);
   this is a logged request.
4. **Register text cosmetic variance:** the register records P4's title with `±0.5°F`; the
   listing renders `±0.5℉`. No factual impact; noted so a later diff does not call it a
   mismatch.
5. **FLG-065 — `dates.publish` fallback.** A guide missing from `data/editorial.json →
   dates.publish` silently inherits the register date as its publish date. All 12 guides have
   entries today (verified by building and reading the Article markup on each page).
6. **FLG-066 — runtime tests are not in CI.** `scripts/test_pages_dom.mjs` needs jsdom; the
   Pages workflow installs nothing, so it stays a local test. The event-contract test *is* wired
   in, because it is standard-library only.
7. **Endpoint behaviour exercised, not deployed.** `analytics-endpoint/server.py` was run locally
   on 2026-11-20: `/health` ok; a valid `page_view` and `outbound_click` returned 204; an
   `outbound_click` without an ASIN and an old `guide_read_75` name returned 400; `counts.json`
   gained day/event/path buckets plus `outbound_click_asin.B0CDY277D3: 1`; an `OPTIONS` request
   from a foreign origin received no `Access-Control-Allow-Origin`. Then the file and process were
   deleted. **No production data was collected, and no event was ever sent from the site.**

## 5. Verification of this session's own output

- `python3 build_site.py` twice → `git diff --exit-code` clean on `*.html`, `sitemap.xml`,
  `feed.xml`, `robots.txt`, `data/search-index.json` (determinism, the drift gate would pass).
- `node scripts/check_meta.mjs` → **0 warnings, 0 failures** (was 5 warnings on the inherited
  tree; the four long titles and one long description were shortened).
- `node scripts/check_site.mjs` → **PASSED, 57 HTML files** (disclosure above the fold, every
  Amazon link `rel="sponsored"`, internal links resolve, unique titles/descriptions, claim
  wording).
- `python3 counter-check/tools/check_site.py` → PASSED (sibling audit build, untouched).
- `python3 scripts/test_event_contract.py` → PASSED (20 assertions across names, payloads,
  bounds and privacy shape).
- `node scripts/test_pages_dom.mjs` → 15 pages, no runtime errors; chooser links confirmed
  sponsored + tagged + labelled; the decision-desk export produces a dated Markdown sheet; 86
  numbered rows all carry a pick control.
- Every `<img>` src referenced by any page exists on disk (script-checked); SVG art sizes are
  0.5 KB each, the hero JPEG 165 KB.
- New pages are in `sitemap.xml` (28 URLs) and the RSS feed; the guide list is asserted against
  the feed at build time, so a page cannot go unlisted.

## 6. What stays unverified, and is not presented as fact

Thermometer dimensions (FLG-004); Emeril warranty term (FLG-005); the Special Link test in
Associates Central (FLG-001, needs the owner's login); Creators/PA API eligibility (FLG-037,
third-party claim only); SiteStripe link-type availability (FLG-038); commission rates (never
published here); search volume for any topic (never claimed); whether the commissioned
illustration can be mistaken for product photography (FLG-061 / Q-31, needs two human readers).
All of it is on [flagged.html](https://wingbangboozle1-lang.github.io/Prod1/flagged.html) with
the action that would close it.

## 7. Identifier map, after two merges on the same day

Main moved twice while this branch was open (PRs #28-#36, then #37-#45: five other sessions, all
touching the same registers). Rows were renumbered twice and none was deleted. The final numbers
for this pass's own rows are:

| This pass | Final id | Note |
|---|---|---|
| artwork as a representation surface | `FLG-076` | their `FLG-053` is an unrelated finding (broken class attributes) |
| images are binaries outside the drift gate | `FLG-077` | |
| re-read could not reach the spec table | `FLG-078` | keeps `FLG-004` open |
| register dated 2026-11-19 vs a 2026-11-20 re-read | `FLG-079` | |
| `dates.publish` fallback | `FLG-080` | closed the same day: the lookup now raises, and a merge that dropped the block would have redated all 13 guides |
| runtime tests not in CI | `FLG-081` | |
| limited-time promotion references expire | `FLG-082` | |
| comparison format needs lowest new **and** used | `FLG-083` | |
| orphan root `styles.css` | `FLG-084` | new in the second merge |
| suggestions from this pass | `SG-54` … `SG-60` | `SG-44`-`SG-53` were taken on main |
| questions from this pass | `Q-28` … `Q-31` | unchanged |

Unifications the merge forced, recorded because they change how the site is built:

- **One guide line-up.** The feed had grown its own hard-coded list of ten guides while the pages
  listed twelve, so three shipped guides were in the sitemap and absent from the feed. The feed now
  derives from `GUIDE_CARDS` and the build asserts the two sets are equal (13 of 13).
- **Publish dates cannot be inferred.** `pdate()` raises when a slug has no `dates.publish` row;
  it caught a typo of my own on the first run, which is the proof the guard works.
- **Endpoint self-test.** `analytics-endpoint/selftest.py` feeds one generic envelope to all five
  event names, which my per-event rules correctly rejected for `chooser_complete`. Rather than
  weaken the rule or edit their fixture's meaning, the fixture now carries the documented
  `q1/q2/q3` answers and three new negative cases (partial answer set, 200-character query,
  click with no ASIN) are rejected. `scripts/check_measure.mjs` and `scripts/test_event_contract.py`
  both pass against the same server.

Flag list: **69 rows** (`FLG-001`-`FLG-022`, `FLG-032`-`FLG-084`, with the retired `023`-`031` gap
recorded by main's `FLG-056`). Decision desk: **101 numbered rows**, 113 runtime controls, verified
under jsdom on the built page rather than asserted in prose.
