# DESIGN_PROMPT.md — the brief behind the site's look

Version 1.1, amended 2026-11-20 by session `arena/e7dcb638-prod1` to describe what is
actually shipped, not what was intended. This file exists so the look can be reviewed and
revised as a *brief* rather than as scattered CSS. Every section names the decision and the
suggestion that fed it (`SG-xx` / `Q-xx` on
[suggestions.html](https://wingbangboozle1-lang.github.io/Prod1/suggestions.html)).

Nothing here overrides the compliance rules: disclosure above the fold on every page,
every outbound product link marked `rel="sponsored"` and labelled, no Amazon Program Content
stored or imitated, no unverifiable claim in any voice.

## 1. Positioning

**Read like a shop, not an audit.** The product and the buyer question lead every page; the
verification machinery lives behind one nav group and the footer, not in the reader's face.
Trust is *shown* by dated sources and honest blanks, never announced with a badge.

- Voice: plain, specific, lightly warm. Short sentences. Numbers over adjectives. Seller
  claims always attributed ("per listing").
- Headlines are the buyer's own question, or a concrete, defensible promise.
- What the copy may never do: imply anyone cooked with a product, quote a price it cannot
  keep true, or borrow urgency from a promotion.

## 2. Brand

- Name: **The Countertop Guide** (settled).
- Mark: wordmark in the display serif, "Guide" in terracotta, with a two-tone square glyph
  drawn in CSS. No seals, no "certified" ribbons, no invented awards.
- Promise line: *spec-backed comparisons from the listing — no hype, no fake testing.*

## 3. Palette and type — as implemented in `assets/style.css`

| Role | Value | Note |
|---|---|---|
| Page background | `#FBF6EE` warm cream | food-magazine warmth, not dashboard grey |
| Ink | `#221810` espresso | softer than black |
| Accent | `#B4432B` terracotta | CTAs, kickers, rules |
| Secondary | `#245B4E` teal · `#A4691C` amber | category chips, buy button |
| Display type | `Fraunces, Iowan Old Style, Palatino, Georgia, serif` | **no webfont is loaded** — see §3.1 |
| Body type | `Inter, system-ui, Segoe UI, Roboto, Helvetica, Arial` | same caveat |

Mobile-first: fluid `clamp()` type, 44–48 px tap targets, single column under 640 px,
sticky compare bar, `prefers-reduced-motion` respected, one visible focus ring style
(3 px amber outline) for the whole site.

### 3.1 The typography decision is still open (SG-45 / Q-28)

The tokens name Fraunces and Inter; the pages load neither, so readers see Georgia and the
system UI stack. Three ways out, none taken without an owner:

1. **Keep the local stack** (status quo, zero bytes, no third party). Tune scale and
   tracking instead of chasing a typeface.
2. **Self-host subsetted woff2** of both families. Verify each family's licence *on its own
   project page* (not in a tutorial) and record the byte count — Q-28.
3. **A third-party font host.** Rejected for now: it sends every visitor's IP to another
   company, and the site's privacy line does not currently cover that. If the owner chooses
   it, `about.html` has to change in the same commit.

## 4. Layout system — what shipped 2026-11-20

- **Front page** = publication front: hero (offer + illustration) → three-step "start here"
  → shop-by-the-job tiles → quick picks → the five product cards → chooser → fresh guides →
  topic calendar → trust strip. Register, flags and method are never in this flow.
- **Category pages** = product cards first, the sourced comparison table second.
- **Guides** = question-shaped articles in clusters, each ending in the picks and an FAQ,
  every claim linked to the listing it came from.
- **Product card anatomy** (`.prod`): our drawing → form chip → name → one-line job → live
  price button line → spec grid (capacity / footprint / depth / height / power / features) →
  *Good for* → *Check before you buy* → sponsored CTA → source record link. No price figure,
  no star rating: `data/editorial.json → display` keeps them off every shop page.
- **Why §4 existed at all**: 44 class names in the generated HTML had no CSS rule, and nine
  custom properties used by the desk block were never declared (FLG-052). A page can be
  factually perfect and still look generated because nobody styled the components.

## 5. Imagery policy — ours, or none (SG-04, SG-46, FLG-053)

- **Never copied, never AI-generated *product* photography.** Program Content images are
  licensed, not owned, and a synthetic picture of a real SKU would be a misleading claim
  about a Product (Program Policies §2(b), read 2026-11-20).
- What ships instead: five hand-authored SVG drawings of appliance **forms**, one
  commissioned illustration of a generic kitchen counter, and gradient category tiles. Each
  is captioned as ours, in the reader's line of sight, and never presented as the product.
- Real photography arrives only with owner-shot or manufacturer-permitted images (SG-04),
  consistent lighting, kitchen context, and no staged "we tested this" implication unless the
  testing protocol (SG-09) becomes real.
- Images are committed binaries; the determinism gate does not see them (FLG-054).

## 6. Seasons and clusters

- 12 guides in four clusters: choosing (form, capacity, cleanup, height, in-the-box),
  specs (wattage), thermometers (accuracy), seasonal (gifts, hosting, budget, price-check).
- Seasonal copy is a **method**, not a promotion: "how to check a price claim", never
  "these five are on sale". A named limited-time promotion obliges us to take the page down
  the day it ends (FLG-059), and a static build has no expiry job.
- Snapshot refresh is a standing duty, not a memory: see FLG-040 and FLG-056.

## 7. Measurement before optimisation (Priority 4)

The five defined events (`page_view`, `outbound_click`, `search`, `chooser_complete`,
`guide_read`) are counted locally and never sent while the endpoint is unset. The contract
between client and endpoint is enforced by `scripts/test_event_contract.py` in CI;
`scripts/test_pages_dom.mjs` checks runtime behaviour locally. The campaign ledger stays
empty until authorized first-party reports exist. No layout is "optimised" without data —
which is why SG-50 asks what a shop pass would even be measured by.

## 8. Paste-ready blocks for the next design pass

Each block is self-contained, states its constraint, and can be handed to a designer or an
agent without extra explanation.

**A — Visual system.** "Extend the component layer in `assets/style.css` for three more
surfaces: a product-card hover state that lifts 3 px and deepens the shadow; a
`figure` treatment for guide pages using only our own drawings; and a sticky two-line
'where this number comes from' footnote bar for tables. Keep the palette tokens, the 44 px
tap targets and the focus ring. Do not add badges, seals, countdowns, or stock photography.
Every new rule must be matched to a class the generator emits — no decorative one-off CSS."

**B — Editorial anti-slop checklist (mechanical, so it can be gated).** "Vary sentence
length; delete every sentence that could appear on any product's page anywhere; state the
source in the same breath as the claim; where a field is absent, say it is absent in the
sentence where the reader wanted it; no 'elevate', 'game-changer', 'must-have', 'we tested',
'best-in-class'; no promotion names; no forecast of traffic or revenue. The banned list and
the em-dash rhythm check live in `data/editorial.json → voice` and run in CI."

**C — Decision desk.** "Keep one control per numbered row on `suggestions.html`, stored in
the browser, exported as dated Markdown for `docs/decisions.md`. A suggestion may only move
to 'shipped' when a commit and a source are named. Never let the board assert that a
decision was made."

## 9. Open design questions

1. Photography direction once SG-04 decides (lifestyle vs white-seamless).
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
3. Custom domain vs `github.io` canonical (SG-02) — the design assumes the Pages URL.
4. December gift-guide refresh cadence (SG-14) and the snapshot re-read clock (FLG-040).
5. Q-31: can a reader mistake our drawing for the product? Two fresh eyes, then decide how
   far the art system may go.
