# Prod1 — The Countertop Guide

A spec-backed Amazon Associates publication for air fryers and meat thermometers. The live site is a static GitHub Pages site built from a source register; it is not currently an AI product-research or campaign-optimization service.

**Live site:** <https://wingbangboozle1-lang.github.io/Prod1/>

**Associates tracking ID:** `shopnow047c-20`

## What is live

- `index.html` — publication front page with product-led navigation and featured guides.
- `air-fryers.html`, `thermometers.html`, `compare.html` — category pages and a five-product comparison/chooser.
- `guides.html`, `guide-*.html`, `topics.html` — question-shaped buyer guides and editorial calendar.
- `suggestions.html`, `decisions.html` — a dedicated suggestion and decision desk with options, trade-offs, and a question/information/answer register.
- `executive-summary.html` — current state, evidence, limits, and owner decisions.
- `verification.html`, `flagged.html`, `compliance.html`, `methodology.html`, `review-desk.html` — source register and review surfaces, reachable from navigation/footer.
- `data/products.json` — the product-intent records (submitted short link, intended ASIN, official listing URL, confirmation date/source, and observed redirect kept separately).
- `sitemap.xml`, `feed.xml`, `robots.txt` — generated publication discovery files.

All outbound product buttons use tagged Amazon `/dp/ASIN` URLs and are marked sponsored. The supplied short links and their observed redirects are recorded separately; testing their Special-Link behavior in the enrolled Associates account remains an open review item. See `flagged.html` and `suggestions.html`.

## Automation and limits

The Python build generates static pages from repository data. Five CI gates check site-wide disclosure/link requirements, metadata and editorial rules, stylesheet coverage, measurement-contract consistency, and document structure. The self-hosted analytics endpoint has code and a passing local contract test, but it is **not deployed or configured**; client events remain local. The campaign ledger is intentionally empty until authorized first-party reports exist.

No AI agent currently researches products, estimates commissions, generates/publishes articles automatically, or optimizes campaigns. No Search Console data or conversion reports are connected. Article titles are editorial hypotheses, not claims about search volume or popularity. These boundaries and the missing-information questions are documented in `executive-summary.html`, `methodology.html`, `suggestions.html`, and `decisions.html`.

GitHub Pages currently uses its legacy branch source. The workflow runs the five publishing gates on pushes to `main`, but in legacy mode it does not publish a Pages artifact itself; a failed gate produces a failed workflow, and branch-protection enforcement has not been verified. See `flagged.html#FLG-051` and the Pages workflow comments. Moving Pages to the Actions source is an owner decision.

## Edit and validate

Generated HTML should not be edited by hand. Change source data or the generator, then rebuild and run all checks:

```sh
python3 build_site.py
node scripts/check_site.mjs
node scripts/check_meta.mjs
node scripts/check_style.mjs
node scripts/check_measure.mjs
node scripts/verify_structure.mjs
python3 counter-check/tools/check_site.py
```

A deterministic rebuild should leave generated outputs unchanged after the first build. Product facts that could not be confirmed remain blank and are flagged; do not infer values or merge an intended ASIN with an observed redirect.

## Repository notes

- `DESIGN_PROMPT.md` records the publication visual direction and editorial guardrails.
- `analytics-endpoint/` contains the not-yet-hosted endpoint and local self-test.
- `review/` contains dated verification notes with source links.
- `docs/`, `articles/`, and `counter-check/` are auxiliary repository surfaces; whether to consolidate or exclude them from the published host remains documented for review.
