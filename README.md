# Prod1 — The Countertop Guide (Amazon Affiliate Platform)

Spec-backed affiliate publication for air fryers & meat thermometers. Static GitHub Pages site. No build step: edit `data/products.json`, run `python3 build_site.py`, commit.

## Live site
GitHub Pages from `main` (see `.github/workflows/pages.yml`). Canonical is the GitHub Pages URL (`https://wingbangboozle1-lang.github.io/Prod1/`) on every page — a custom domain remains an owner decision (see `flagged.html` FLG-007 and `suggestions.html` SG-02).

## Structure
- `index.html` — publication front page (hero, product line-up, categories, chooser, guides)
- `dashboard.html` — single hub for every dashboard surface (verification, flagged, compliance, method, summary, suggestions)
- `air-fryers.html`, `thermometers.html` — category pages with comparison tables
- `compare.html` — all five side by side + 3-question chooser + counter-space math
- `guide-*.html` — question-shaped guides (basket vs oven, capacity, cleanup/space, multi-function, thermometer accuracy)
- `executive-summary.html` — what is verified / not verified / next gates
- `suggestions.html` — suggestions board (SG-01..SG-18) + design inputs (D-1..D-8) + Q/I/A decision log (Q-01..Q-13)
- `verification.html` — line-by-line source register + product-intent confirmation record
- `flagged.html` — irregularities & unverified items (FLG-001..FLG-020)
- `compliance.html` — disclosure + Amazon/FTC policy checklist
- `methodology.html` — evidence rules, 5 analytics events, empty campaign ledger
- `data/products.json` — single source of truth (verified 2026-11-19, second pass same day)
- `assets/style.css`, `assets/app.js` — design + chooser/search/analytics (local-only)
- `sitemap.xml`, `robots.txt`, `feed.xml` — findability

## Rules (do not break)
1. Disclosure above the fold on every page + footer. Every outbound product link `rel="sponsored"` + labeled.
2. Every product fact links to its Amazon listing. Missing = blank + flagged. Never infer.
3. No hands-on testing / trending / revenue claims without evidence. Seller claims attributed ("per listing").
4. Intended ASIN and observed redirect target stay in separate fields.
5. Prices always carry a snapshot date. Live price on Amazon governs.

## Verify before push
- `python3 build_site.py` (regenerates pages)
- Check: no broken internal links, disclosure on every page, sponsored on every outbound, unique titles.
- See `docs/decisions.md` and `COORDINATION.md`.

## Tracking
Tracking ID `shopnow047c-20`. Outbound format: `https://www.amazon.com/dp/ASIN?tag=shopnow047c-20`.
