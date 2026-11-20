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

## 9. Polished marketing layer (suggestions — owner decides whether to ship)

This section feeds the visual design prompt with concrete, catchy article topics and
organic-traffic hooks. Every item is a proposal, not a decision: none is implemented
until it lands on the suggestions board (`suggestions.html`) and a reviewer marks it
Approve / Reject / Defer with a date.

### 9.1 Catchy trendy article topics (question-shaped, spec-backed)

Headlines are buyer questions a person would actually type, not promises about
outcomes. Each title below is tied to fields that exist in `data/products.json`, so no
article can claim a number the listing does not carry.

Working titles (all hypotheses — not popularity, volume or superiority claims):

- "Basket or oven-style air fryer: what should you compare?" — dual-basket (P1) vs
  French-door oven (P2): capacity, counter depth, what each is genuinely good for.
- "A no-hype checklist for comparing air fryer capacity" — 6 Qt vs 8 Qt vs 26 QT, how
  the listed capacity maps to people and counter space, with the exact numbers from the
  listings.
- "How to assess cleanup and counter-space trade-offs" — dishwasher-safe baskets vs
  oven racks, footprint math from the register (158.0 / 267.0 / 172.1 sq in), what fits
  under a cabinet.
- "Questions to ask before buying a multi-function kitchen appliance" — presets,
  wattage, circuits, shared outlets, what the listing does and does not say.
- "Instant-read vs wireless thermometer: do you need both?" — P4 read time and tolerance
  vs P5 probes, range, heat rating; one listing states no accuracy figure — say so.
- "Air fryer for a small kitchen: what actually fits" — depth-led shortlist from the
  dimension column, blanks left blank.
- "Thermometer as a holiday gift: what to check before you order" — probes, range,
  return window, warranty, gift tiers tied to dated snapshots.
- "Wattage, circuits and shared outlets: what the listing does and does not say" — 120 V /
  1000–1700 W from the register, circuit advice kept general, no electrical claims.

Each topic gets one shortlist, one at-a-glance spec table, one honest "what the listing
cannot tell you" callout, and one "see today's price on Amazon" button marked sponsored.
That is the whole article anatomy — nothing is padded.

### 9.2 Organic traffic hooks (findability, not forecasting)

- One canonical site under one host, self-canonicalising pages, sitemap + RSS written by
  the build, robots.txt, per-page Open Graph + unique titles/descriptions.
- Intent landings ("shop by goal": small kitchen, holiday gift, family oven) built only
  from verified fields, each added to sitemap and feed at publish.
- Question-shaped H2s in every guide — the page answers the exact phrase the reader
  typed, which is what earns the click.
- Internal-link spine: every guide links its pillar category, the comparison page and
  the buying-guides index (S-24). One question, one canonical answer.
- Search Console is the topic picker: after 28 days of queries, the next four topics come
  from arriving queries our pages do not answer — never from instinct. Until then the
  calendar above is a stated plan.
- Reader capture via a public GitHub issue ("Suggest a topic") — nothing is collected
  silently, nothing is pre-filled to look busy.

### 9.3 Anti-AI-slop rules for marketing copy (SG-13, SG-14, enforced by the gate)

- Second person, active voice, one idea per sentence. Numbers instead of adjectives:
  "34.0 cm deep" not "compact".
- Never: "we tested", "we loved", "game-changer", "must-have", "best-in-class", "top
  rated", "trending now", "viral", "#1", "guaranteed", "act now". The banned-phrase list
  lives in `data/editorial.json` and `scripts/check_meta.mjs` fails the build on a hit.
- No invented scarcity, countdowns, or "everyone is buying" lines.
- Every claim names its source in the same breath, or it is not written. Seller claims
  are attributed ("per listing").
- Where a spec is missing, the page says so in the sentence where the reader wanted it.
  A blank with a date is more trustworthy than a guessed number.

### 9.4 What this layer is not (so it cannot be misread)

- Not a forecast of traffic, ranking, clicks or revenue. The campaign ledger is empty by
  design until authorized first-party Associates reports exist.
- Not hands-on testing. No page claims use; a testing programme is SG-09 and requires a
  funded protocol first.
- Not a price or rating display on shop pages. Prices and ratings stay dated register
  observations; the button links to Amazon where Amazon serves the live figure.

### 9.5 Structural rules for polished marketing (from the PR #48 review pass — additive)

PR #48 wrote a "polished-marketing direction" as section 9 of its own design prompt. Its
structural rules are recorded here because they answer the same brief; nothing below
replaces 9.1–9.4, it sharpens them. The tell that copy is generated is structural, not
stylistic:

- **Lead with the buyer's question, not the pipeline.** Every page opens with the question a
  person types ("Will a 26-quart air fryer fit my counter?"), then answers it with the
  verified spec. The verification machinery stays one click away in the footer and the
  review-desk nav group. A page that opens with "here is how we verified" reads as a
  register; a page that opens with the answer reads as a shop.
- **One opinion per page.** Take a position inside the bounds of the data ("the shallowest
  of the three", "the one to reach for if you cook two things at once") rather than listing
  facts symmetrically. Opinions are built only from fields the listing states — which is
  what the build's claim-integrity gate already enforces for superlatives.
- **Numbers, not adjectives.** "16.9 in (42.9 cm) deep" beats "spacious". Adjectives are
  where generated copy fills space.
- **Honest gaps as content.** "The listing does not state the warranty period" is a sentence
  a buyer trusts more than a polished lie. Gap callouts are a marketing asset, not a
  weakness — the flag register already runs on this principle.
- **No emoji-as-icon, no gradient glow, no badge soup.** The palette is warm paper + one
  clay accent + one teal; the type is a display serif + a grotesque (section 3). That
  restraint is what makes a page read published rather than templated.
- **Findability rails to keep:** one canonical host, one sitemap of buying URLs, one RSS
  feed, per-page question-shaped title + meta description, `rel="sponsored"` on every
  outbound link, and structured data (Organization / Article / FAQPage) that matches the
  visible content. All of these are enforced or generated today; none is optional.
- **Imagery:** brand diagrams and typography until SG-04 (photography licence) clears. A
  single ownable visual — the counter-depth scale comparing 32.4 / 34.0 / 42.9 cm — is the
  strongest non-photographic hero the site can carry, and it is built from derived numbers,
  so it cannot be mistaken for stock. PR #46's raster hero (a counter photograph) stays
  excluded until it has provenance; a JPEG with no licence record is not a brand asset.
- **Rule for any "trending" or "catchy" wording:** it may only appear next to a dated
  snapshot from an official source, or not at all. The banned-phrase gate enforces this on
  every page.
