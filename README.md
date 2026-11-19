# Prod1 — The Countertop Guide

A product-led Amazon Associates publication comparing air fryers and meat thermometers from dated listing captures. It does not claim hands-on testing. Product-intent records remain blank until independently confirmed; candidate tagged links have not been validated in Associates Central.

## Public publication

The intended canonical is `https://wingbangboozle1-lang.github.io/Prod1/`. GitHub Pages publishes one curated root-site artifact from `_site/`; separate `docs/`, `articles/`, and `counter-check/site/` outputs are deliberately excluded from this artifact. Search Console ownership, indexing, Amazon Special Link attribution, and the analytics host remain unresolved account/hosting gates.

## Source and generated files

- `data/products.json` — historical listing observations, separate observed redirect fields, blank intended-product confirmations, and candidate affiliate URLs.
- `data/guides.json` — buyer-guide metadata and proposed editorial cadence; source for RSS entries.
- `build_site.py` — writes the root HTML pages and local search index from the product records.
- `scripts/build_publication.py` — canonicalizes the generated pages, creates the root sitemap/feed/robots metadata, and stages the curated Pages artifact in `_site/`.
- `assets/app.js`, `assets/style.css` — local search, product shortlist, browser-local aggregate metrics, and the local-only Suggestions board controls.
- `analytics-endpoint/server.py` — optional, unhosted aggregate counter. Its setting is blank on the public pages until a separate HTTPS host and privacy decisions are completed.
- `scripts/check_site.mjs` and `scripts/check_publication.py` — HTML quality and curated-artifact gates.

## Build and validate

From the repository root:

```sh
python3 scripts/build_publication.py
node --check assets/app.js
node scripts/test_app.mjs
python3 -m unittest discover -s analytics-endpoint -p 'test_*.py' -v
python3 scripts/check_publication.py --root _site
node scripts/check_site.mjs --root _site
git diff --check
```

`_site/` is a generated artifact and is not committed. The Pages workflow runs the same build and checks, verifies the checked-in generated root pages are current, and uploads only `_site/`.

## Publication rules

1. Show the Amazon Associate disclosure above the main content and repeat it in every footer.
2. Mark every Amazon-bound link `rel="sponsored"`; the publication gate checks rendered links.
3. Keep intended ASIN/listing/date/source fields separate from historical redirect observations. Do not infer product intent from a redirect.
4. Link product facts to the corresponding listing source. Preserve historical date/provenance, leave uncaptured values blank, and flag discrepancies.
5. Do not claim product performance, testing, popularity, search demand, conversions, commissions, or revenue without evidence.
6. Keep the campaign ledger empty until authorized first-party reporting supplies attributable data.

## Tracking ID

The project-selected candidate tag is `shopnow047c-20`. Candidate tagged URLs are not a substitute for the enrolled Associates workflow test; confirm each intended product and check the tracking report before scaling.
