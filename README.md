# Prod1 — The Countertop Guide (Amazon Affiliate Platform)

Spec-backed affiliate publication for air fryers & meat thermometers. Static GitHub Pages site, built to read like a publication: editorial typography, a topic calendar, and a decision desk for suggestions. No build step: edit `data/products.json`, run `python3 build_site.py`, commit.

## Live site
GitHub Pages from `main` (see `.github/workflows/pages.yml`). Canonical URLs are per-page on the live GitHub Pages address (fixed 2026-11-19; see `flagged.html` FLG-021). A custom domain is still an owner decision (`suggestions.html` SG-02).

## Structure
- `index.html` — publication front page (hero, ticker, stories, topic band, products, chooser, RSS band)
- `topics.html` — topic calendar: eight spec-backed working titles (5 published, 3 queued) with sources
- `design-brief.html` — design-prompt suggestions for the redesign (visual directions, anti-AI-slop rules, editorial calendar)
- `air-fryers.html`, `thermometers.html` — category pages with comparison tables
- `compare.html` — all five side by side + 3-question chooser + counter-space math
- `guide-*.html` — question-shaped guides (basket vs oven, capacity, cleanup/space, multi-function, thermometer accuracy)
- `suggestions.html` — decision desk: design & content suggestions (DES), operational suggestions (SG), and the Q/I/A list; pick a path per item and export a review sheet
- `executive-summary.html` — what is verified / not verified / next gates, and what changed in this build
- `verification.html` — line-by-line source register + product-intent confirmation record
- `flagged.html` — irregularities & unverified items (FLG-001..FLG-023)
- `compliance.html` — disclosure + Amazon/FTC policy checklist
- `methodology.html` — evidence rules, 5 analytics events, empty campaign ledger
- `data/products.json` — single source of truth (product facts verified 2026-11-19)
- `styles.css` — editorial design system (root site + docs pages)
- `assets/app.js` — chooser, search, local analytics counter, suggestion-desk picks
- `sitemap.xml`, `robots.txt`, `feed.xml` — findability

## Rules (do not break)
1. Disclosure above the fold on every page + footer, using the exact Operating Agreement Section 5 sentence: "As an Amazon Associate I earn from qualifying purchases." Every outbound product link `rel="sponsored"` + labeled.
2. Every product fact links to its Amazon listing. Missing = blank + flagged. Never infer.
3. No hands-on testing / popularity / revenue claims without evidence. Seller claims attributed ("per listing"). Popularity claims require a dated snapshot from an official source.
4. Intended ASIN and observed redirect target stay in separate fields.
5. Prices always carry a snapshot date. Live price on Amazon governs.

## Verify before push
- `python3 build_site.py` (regenerates pages; generator emits per-page canonicals)
- `node scripts/check_site.mjs` — disclosure, sponsored links, internal links, unique titles/descriptions, claim wording
- See `docs/decisions.md` and `COORDINATION.md`.

## Tracking
Tracking ID `shopnow047c-20`. Outbound format: `https://www.amazon.com/dp/ASIN?tag=shopnow047c-20`.

## Session note (2026-11-19)
The sandbox cannot reach Amazon.com or link.amazon, so listing values from the 2026-11-19 register were not re-fetched and were not changed this session (`flagged.html` FLG-022).
