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
