# Countertop Check (working name)

A static product-listing site for five Amazon links (air fryers/ovens and meat thermometers). Live from `main:/docs` on GitHub Pages: https://wingbangboozle1-lang.github.io/Prod1/

- Source data: `data/products.json` (product records), `data/flagged.json` (Flagged for Review), `data/questions.json` (open questions), `data/suggestions.json` (decisions).
- Guides: `src/guides.mjs`. Styles: `src/assets/site.css`. Event counter: `src/assets/analytics.js`.
- Build: `npm run build` writes `docs/` (no dependencies; Node 18+).
- Gate: `npm run check` fails on a missing disclosure, a non-sponsored Amazon link, a broken internal link, a missing sitemap/RSS entry, or a product row without a source.

Read first: [Executive summary](EXECUTIVE_SUMMARY.md) · [COORDINATION.md](COORDINATION.md) (task board and log).

Blank fields are unverified on purpose. See the Flagged for Review page for each item and its source link.
