# DESIGN_PROMPT.md — the brief behind the visual overhaul

This file is the design prompt for The Countertop Guide. It exists so the site's look
can be reviewed and revised as a *brief*, not as scattered CSS. Every section states the
decision and the suggestion that fed it (SG-xx on
[suggestions.html](https://wingbangboozle1-lang.github.io/Prod1/suggestions.html)).
Nothing here overrides the compliance rules: disclosure above the fold, sponsored links
labeled, no copied/generated product photography (S-18), no unverifiable claims.

## 1. Positioning

**Read like a shop, not an audit.** The product and the buyer question lead every page;
the verification machinery lives one click away (footer + "The desk" nav group) instead
of in the reader's face. Trust is shown, not announced: dated snapshots, source links,
and honest blanks do the persuading.

- Voice (D-12/S-12): plain, specific, lightly warm. Short sentences. Numbers over
  adjectives. Seller claims always attributed ("per listing").
- Headlines are buyer questions or concrete promises ("Five real products. Every number
  sourced. Zero hype."). No superlatives the data cannot carry.

## 2. Brand

- Name: **The Countertop Guide** (settled, S-15/D-18).
- Mark: wordmark in a warm display serif, "Guide" in terracotta. No fake badges or seals.
- One-line promise: *spec-backed comparisons from the listing — no hype, no fake testing.*

## 3. Palette and type (implemented in assets/style.css)

| Role | Value | Why |
|---|---|---|
| Page background | `#FBF6EE` warm cream | Food-magazine warmth, not dashboard gray |
| Ink | `#221810` espresso | Softer than black; editorial |
| Accent | `#B4432B` terracotta | Appetite + action; used for CTAs and kickers |
| Secondary | `#245B4E` deep teal / `#A4691C` amber | Category tiles; price/gold CTA |
| Display type | Fraunces (fallback Georgia) | Distinctive editorial serif — kills the "AI slop" look |
| Body type | Inter (fallback system-ui) | Screen legibility at small sizes |

Mobile-first rules: fluid type with `clamp()`, 44–48 px tap targets everywhere, single
column under 640 px, sticky compare bar on the compare page (S-20).

## 4. Layout system

- **Front page** = publication front (S-17/D-21): hero → category tiles → product picks
  → fresh guides → chooser → trust strip. Dashboards are reachable from the footer and
  one nav group ("The desk"), never mixed into the shopping flow.
- **Category pages** = product cards first, then the sourced comparison table.
- **Guides** = question-shaped articles in three clusters (air-fryer choosing,
  thermometers, seasonal) with a shortlist and FAQ schema at the end (S-07, S-24).
- **Cards**: price-forward product cards; left-rule guide cards; gradient category tiles.
  Every buy button is amber-gold and labeled "sponsored"; every card links its source record.

## 5. Imagery policy (SG-04, FLG-009, S-18)

- **Never copied and never generated product photography.** Amazon's Program Content
  (images included) is licensed to us, not owned; generated product shots would mislead.
- Until owner-shot or manufacturer-permitted photos exist, imagery is CSS/SVG graphics
  only (gradient tiles, typographic hero). The og-image is a brand card, not a photo.
- When photography lands (SG-04): real, consistent lighting, kitchen context, no staged
  "hands-on test" implications unless the testing protocol (SG-09) is real.

## 6. Seasons and clusters (SG-05, SG-14)

- Seasonal layer runs through the holiday window (Nov–Dec 2026): holiday-hosting and
  gift-by-budget guides, gift tiers tied to dated snapshots, return-window notes quoted
  from the listings. Refresh snapshots Dec 1 and Dec 15 (SG-14).
- Clusters: air-fryer choosing (5 guides) · thermometers (1) · seasonal (2). Pillars:
  the two category pages + compare. Every guide links its pillar, the comparison and the
  buying guides index (S-24).

## 7. Measurement before optimization (Priority 4)

No layout or copy is "optimized" without data. The five defined events
(page_view, outbound_click, search, chooser_complete, guide_read) are privacy-preserving
and local-only until the endpoint is hosted (SG-03). The campaign ledger stays empty
until authorized first-party reports exist. See methodology.html.

## 8. Open design questions (see the review desk)

1. Photography direction once SG-04 is decided (lifestyle vs white-seamless).
2. Whether the chooser grows a counter-depth input with units (SG-06).
3. Custom domain vs github.io canonical (SG-13) — the design assumes the Pages URL.
4. December gift-guide refresh cadence (SG-14).

## 9. Polished-marketing direction (feeds the design prompt — owner to approve)

This section answers the brief's core ask: *the site should read like a polished marketing
affiliate publication with catchy, spec-backed articles and topics that earn organic traffic —
not like generated filler.* Everything here is a **suggestion for the design prompt**, not a
decision. Nothing is implemented until a reviewer marks it Approve / Reject / Defer with a date
on `suggestions.html`. (Section 9 was written by two sessions in parallel and merged here; both
sets of suggestions are kept.)

### 9.1 What "polished marketing, not AI slop" means (the tell is structural)

- **Lead with the buyer's question, not the pipeline.** Every page opens with the question a
  person types ("Will a 26-quart air fryer fit my counter?"), then answers it with the verified
  spec. The verification machinery stays one click away in the footer and the "Review desk" nav
  group. A page that opens with "here is how we verified" reads as a register; a page that opens
  with the answer reads as a shop.
- **One opinion per page.** A polished site takes a position inside the bounds of the data
  ("the shallowest of the three", "the one to reach for if you cook two things at once") rather
  than listing facts symmetrically. Opinions are built only from fields the listing states.
- **Numbers, not adjectives.** "16.9 in (42.9 cm) deep" beats "spacious". Adjectives are where
  generated copy fills space.
- **Honest gaps as content.** "The listing does not state the warranty period" is a sentence a
  buyer trusts more than a polished lie. Gap callouts are a marketing asset, not a weakness.
- **No emoji-as-icon, no gradient glow, no badge soup.** Warm paper + one clay accent + one
  teal; a display serif + a grotesque. That restraint is what makes it read published, not
  templated.

### 9.2 Catchy, spec-backed article topics (question-shaped; working hypotheses)

Headlines are buyer questions a person would type, not promises about outcomes. Each title is
tied to fields that exist in `data/products.json`, so no article can claim a number the listing
does not carry. None is a popularity, volume or superiority claim.

- "Basket or oven-style air fryer: what should you compare?" — dual-basket (P1) vs French-door
  oven (P2): capacity, counter depth, what each is genuinely good for.
- "A no-hype checklist for comparing air fryer capacity" — 6 Qt vs 8 Qt vs 26 QT, how the listed
  capacity maps to people and counter space, with the exact numbers from the listings.
- "How to assess cleanup and counter-space trade-offs" — dishwasher-safe baskets vs oven racks,
  footprint math from the register (158.0 / 267.0 / 172.1 sq in), what fits under a cabinet.
- "Questions to ask before buying a multi-function kitchen appliance" — presets, wattage,
  circuits, shared outlets, what the listing does and does not say.
- "Instant-read vs wireless thermometer: do you need both?" — P4 read time and tolerance vs P5
  probes, range, heat rating; one listing states no accuracy figure — say so.
- "Will a 26-quart air fryer actually fit on your counter?" — depth math from the verified
  footprint (16.9 in / 42.9 cm).
- "Two baskets or one: what dual-zone cooking actually changes" — Sync Finish, from the listing.
- "Air fryer for a small kitchen: what actually fits" — depth-led shortlist, blanks left blank.
- "What \"dishwasher-safe\" really means for cleanup" — from the bullets, attributed.
- "Holiday air fryer gifts: how to choose one that gets used" — seasonal, spec-first, tied to
  dated snapshots.
- "Wattage, circuits and shared outlets: what the listing does and does not say" — 120 V /
  1000–1700 W from the register, circuit advice kept general, no electrical claims.

The twelve-topic calendar on `topics.html` is the live version; this list is the *direction* for
the prompt.

### 9.3 Article anatomy (the whole shape — nothing is padded)

Each topic gets one shortlist, one at-a-glance spec table, one honest "what the listing cannot
tell you" callout, and one "see today's price on Amazon" button marked sponsored.

### 9.4 Organic-traffic hooks (findability, not forecasting)

- One canonical site under one host, self-canonicalising pages, sitemap + RSS written by the
  build, robots.txt, per-page Open Graph and unique question-shaped titles/descriptions.
- Intent landings ("shop by goal": small kitchen, holiday gift, family oven) built only from
  verified fields, each added to sitemap and feed at publish.
- Question-shaped H2s in every guide — the page answers the exact phrase the reader typed.
- Internal-link spine: every guide links its pillar category, the comparison page and the
  buying-guides index. One question, one canonical answer.
- `rel="sponsored"` on every outbound link; structured data (Organization / Article / FAQPage)
  that matches the visible content.
- Search Console is the topic picker: after 28 days of queries, the next four topics come from
  arriving queries our pages do not answer — never from instinct. Until then the calendar is a
  stated plan.
- Reader capture via a public GitHub issue ("Suggest a topic") — nothing collected silently,
  nothing pre-filled to look busy.

### 9.5 Anti-AI-slop rules for marketing copy (enforced by the gate)

- Second person, active voice, one idea per sentence. Numbers instead of adjectives.
- Never: "we tested", "we loved", "game-changer", "must-have", "best-in-class", "top rated",
  "trending now", "viral", "#1", "guaranteed", "act now". The banned-phrase list lives in
  `data/editorial.json` and `scripts/check_meta.mjs` fails the build on a hit.
- No invented scarcity, countdowns, or "everyone is buying" lines. Any "trending" wording appears
  only next to a dated snapshot from an official source, or not at all.
- Every claim names its source in the same breath, or it is not written. Seller claims are
  attributed ("per listing").
- Where a spec is missing, the page says so in the sentence where the reader wanted it. A blank
  with a date is more trustworthy than a guessed number.

### 9.6 Imagery

Brand diagrams and typography only until SG-04 (photography licence) clears. A single ownable
visual — the counter-depth scale comparing 32.4 / 34.0 / 42.9 cm — is the strongest
non-photographic hero the site can carry, and it is built from our own derived numbers, so it
cannot be mistaken for stock.

### 9.7 What this layer is not (so it cannot be misread)

- Not a forecast of traffic, ranking, clicks or revenue. The campaign ledger is empty by design
  until authorized first-party Associates reports exist.
- Not hands-on testing. No page claims use; a testing programme is SG-09 and requires a funded
  protocol first.
- Not a price or rating display on shop pages. Prices and ratings stay dated register
  observations; the button links to Amazon where Amazon serves the live figure.

## 10. Front page, pass of 2026-11-20 (session 84799c33)

The brief's first instruction is "lead with the products, not with the verification process".
This pass changed the order of the front page to obey it, and nothing else on the site moved.

**New order, top to bottom**

1. **Hero that sells a number, not a process.** Headline: *"Five countertop appliances,
   priced in the space they take."* Lede names counter depth as the deciding figure. The
   three "hero facts" now describe the shelf (5 products, 1 decision table, 0 use claims)
   instead of the audit.
2. **"All five at a glance" table**, directly under the hero, above the seasonal band:
   product, the job it wins, capacity as titled, counter depth in inches *and* centimetres,
   what to check before ordering, and one `Check price` button per row marked sponsored.
   Generated by `shelf_table()` from `data/products.json`, so no cell can drift from the
   register. Two cells print an honest gap (thermometer depth) rather than a guess.
3. **Three picks by job** in the hero side column, each with its depth and width, so the
   visual weight sits on the products.
4. Seasonal band, picks, full cards, chooser, guides, topic calendar - unchanged.
5. Trust strip and the review-desk cluster stay in the footer, one nav group, as before.

**Rules this pass did not bend**

- No price, rating, badge or "bought in past month" figure on the shelf. `Check price`
  links to Amazon, which serves the live figure (Program Policies; `data/editorial.json`).
- Every "pick it if" line is a reading of listing fields, not a test result, and is
  recorded as such in FLG-084 on `flagged.html`.
- Rooms for later, not built: a variant-aware price module (blocked by the 24-hour caching
  rule and the missing API), and photography (blocked by SG-04). Neither is faked with a
  stock photo.
## 11. Suggestions for the next design pass (session b2f99e67, 2026-11-20)

These are suggestions feeding this prompt, not decisions. Each has a row on
[suggestions.html](https://wingbangboozle1-lang.github.io/Prod1/suggestions.html)
(SG-65…SG-70) with options, and each is pickable on the
[decision slate](https://wingbangboozle1-lang.github.io/Prod1/decisions.html#slate).
Nothing below ships until a reviewer approves its row. Sources re-read for this section:
[Operating Agreement §5](https://affiliate-program.amazon.com/help/operating/agreement)
and
[Google's outbound-link qualification](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
(both read 2026-11-20); the design constraints from Amazon's Program Policies are carried
from the register's dated reads (see verification.html).

### 11.1 Editorial illustration layer (SG-65) — recommended direction

- One hero scene and one seasonal band drawing, **our own line drawings in the existing
  `assets/art/` language**: flat fills, one stroke weight, warm paper, no rendering of any
  specific listed unit. Captioned "our drawing" the way the footprint diagrams are.
- What it must never do: depict a product as if photographed, imitate a listing image,
  or imply handling or testing. The imagery policy (§5) is a floor, not a prohibition on
  art the site owns.
- Brand surfaces to harmonise when the layer lands: the favicon and og-card ink
  (#171310) against the stylesheet ink (#1E1712) — pick one ink in one commit
  (FLG-091).

### 11.2 Decision-making surfaces (SG-66) — shipped, awaiting ratification

- The register now carries a **slate**: seven gates, one row each, the recommendation
  beside it, a per-gate option picker and a JSON export. This is the "review and choose
  the best path before implementing anything" surface; the board (90+ rows) stays the
  evidence layer behind it.
- Design rule for future rows: every suggestion that reaches the board must land in
  exactly one register theme (the build enforces it) and must state its recommended path
  in the row itself, so the slate can render it without opening the card.

### 11.3 Findability without claims (SG-67)

- Internal-link anchors should read like the question the reader typed ("how much
  capacity is real", not "read more"). One inventory pass over the built HTML, one diff,
  no new pages — and no traffic claim follows from it, by the rule in §9.4.
- Search Console (SG-28) remains the only source allowed to say anything about
  demand. Until it exists, the topic calendar is labelled a plan.

### 11.4 The holiday window gets a closing bracket (SG-69)

- Seasonal dressing (band, chips) is generated per build date and stops rendering after
  2027-01-05; guides stay published and indexed. Snapshot refreshes stay on the SG-57
  dates (Dec 1, Dec 15). An expired skin is a one-line generator change, not a cleanup
  project.

### 11.5 Measurement gates the marketing layer (SG-68, SG-70)

- No CTA copy, button colour or layout test starts until the five defined events record
  real counts (SG-03 / D-04). The thresholds and the funnel are pre-registered in the
  ledger schema first. Reader capture, if it grows beyond the GitHub-issue intake, uses
  the same host decision — one privacy surface, not two.
