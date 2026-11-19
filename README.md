# Prod1: Counter Notes (working name)

A static buyer's site for five supplied Amazon links: air fryers, an air-fryer oven, and meat thermometers. It includes question-led guides, product and category pages, and dashboards for analysis, the backlog register, product-intent records, open questions, suggestions, the campaign ledger, analytics, and Flagged for Review.

Live site (after GitHub Pages is enabled from `main` `/docs`): https://wingbangboozle1-lang.github.io/Prod1/

## Layout

| Path | What it is |
|---|---|
| `data/` | Product facts, categories, guides index, sources, flags, questions, suggestions, register, ledger header. JSON, one source of truth. |
| `content/guides/` | Guide bodies (HTML fragments). |
| `site_src/assets/` | Stylesheet and the privacy-preserving tracker. |
| `tools/build.py` | Generates every page, `sitemap.xml`, `feed.xml`, `robots.txt` into `docs/`. |
| `tools/check.py` | Verifies the built site (see below). |
| `docs/` | Generated site. This is the GitHub Pages source. Do not edit by hand. |
| `endpoint/server.js` | Optional first-party event collector. Not deployed (see Analytics). |
| `COORDINATION.md` | Shared task board, sources, and irregularities. |

## Build and check

```bash
python3 tools/build.py && python3 tools/check.py
```

Standard library only; no install step. `check.py` fails the build on: missing or duplicate titles or meta descriptions; the disclosure missing under the masthead or in the footer; Amazon links without `rel="sponsored"`; broken internal links or anchors; table rows with no official source link and no UNVERIFIED flag; currency amounts; any affiliate tag appended to a link; a sitemap or feed that misses a page; or invalid JSON.

External URLs are not fetched by the checker (sandbox network is restricted). Re-check external links by hand before publishing changes.

## Rules the content follows

- Values not confirmed from an official source are left blank and marked UNVERIFIED. Nothing is inferred.
- Prices, ratings, commission rates, and popularity or "trending" claims are not shown.
- Intended ASINs and observed redirect targets are stored in separate fields.
- Supplied short links are kept as submitted. They are not claimed valid or invalid.
- No tracking parameter is appended to any link until the Special Link test is run (see Flagged F-03).

## Analytics

The tracker is off: `TRACKER_ENDPOINT` in `tools/build.py` is empty, so nothing is sent. To turn it on, host `endpoint/server.js` on a server you control, set `TRACKER_ENDPOINT` to its `/collect` URL, and rebuild. It stores daily counts only, with no IP addresses, user agents, or cookies.

## Publishing

GitHub Pages: Settings > Pages > Deploy from a branch > `main` / `/docs`. The `docs/.nojekyll` file disables Jekyll processing.
