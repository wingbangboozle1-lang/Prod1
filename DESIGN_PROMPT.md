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
3. Custom domain vs `github.io` canonical (SG-02) — the design assumes the Pages URL.
4. December gift-guide refresh cadence (SG-14) and the snapshot re-read clock (FLG-040).
5. Q-31: can a reader mistake our drawing for the product? Two fresh eyes, then decide how
   far the art system may go.
