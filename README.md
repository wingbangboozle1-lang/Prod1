# Prod1 — The Countertop Guide (Amazon affiliate publication)

A spec-backed affiliate site for air fryers and meat thermometers, built from five Amazon
listings. Static GitHub Pages, generated HTML — never hand-edit a page.

Live: https://wingbangboozle1-lang.github.io/Prod1/
Tracking ID: `shopnow047c-20` · Outbound format: `https://www.amazon.com/dp/ASIN?tag=shopnow047c-20`

## Edit workflow

```
python3 -m pip install pillow        # once: regenerates the social card
# edit data/products.json (facts + sources) or data/editorial.json (voice, policy, cadence)
python3 build_site.py                # writes all 25 pages (21 in the sitemap, 4 consolidated), sitemap, feed, robots, search index
python3 scripts/make_og.py           # writes assets/og-image.png + assets/favicon.svg
node scripts/check_meta.mjs          # publishing gate (same one CI runs)
```

CI re-runs the build and **fails the deploy** if the committed HTML differs from the
generated HTML, or if the gate finds a violation. So a hand-edited page cannot merge.

## Structure

Reader-facing: `index.html` (front page: picks, products, chooser, guides) ·
`air-fryers.html`, `thermometers.html` (category pages with spec tables) ·
`compare.html` (all five + three-question chooser + counter-space maths) ·
`guides.html` + `guide-*.html` (six question-led guides) · `topics.html` (topic calendar: eight spec-backed working titles, five published) · `about.html`.

Review desk (internal surfaces, one nav group + footer): `review-desk.html` ·
`verification.html` (line-by-line register, intended ASIN separate from observed redirect) ·
`flagged.html` (FLG-001…FLG-050; the ranges are three sessions' passes merged into one register, see `COORDINATION.md`) · `suggestions.html` (SG board, Q/I/A register, DI design inputs, design prompt) · `design-brief.html` (parallel brief, owner picks one) ·
`methodology.html` (automation map, five events, empty campaign ledger) ·
`compliance.html` (policy reads, quoted) · `executive-summary.html`.

Also in this repository, owned by other sessions and *not* part of this publication:
`counter-check/site/` and `docs/` + `articles/`. See `flagged.html#FLG-039` — three builds on
one host is a findability problem the owner has to settle.

## Rules the gate enforces

1. The Associates statement appears verbatim — "As an Amazon Associate I earn from
   qualifying purchases." — above the fold and in the footer of every page (Operating
   Agreement §5).
2. Every outbound Amazon link carries `rel="sponsored nofollow noopener"` and a visible
   "sponsored" label, **including links built by JavaScript**.
3. No price, rating, badge or "bought in past month" figure on shop pages: Program Policies
   allow price display only via an Amazon-served link or the Creators/PA API, with 24-hour
   caching limits. Dated observations live in the register, not on the shelf.
4. Every product fact links to the listing it came from. A field we could not confirm stays
   blank and gets flagged — never inferred.
5. Unique `<title>` + meta description per page; self-referencing absolute canonical;
   absolute raster `og:image`; sitemap lists exactly what the build writes; feed dates are
   RFC-822.
6. Voice rules and a banned-phrase list (`data/editorial.json`) apply to reader-facing pages,
   body text *and* meta/alt attributes. No testing claims, no scarcity, no "trending"
   without a dated snapshot.
7. The build is deterministic: no `datetime.now()` in generated output.

## Notes

- Analytics: five documented events, counted in the visitor's browser only. No endpoint is
  configured, so nothing is transmitted. See `methodology.html` and `COORDINATION.md` R-06.
- No product photography anywhere: diagrams and brand art only, until a licence decision
  (`suggestions.html#SG-04`).
- Decisions waiting on the owner are on `suggestions.html`; nothing there is implemented
  until a row is marked approved.
