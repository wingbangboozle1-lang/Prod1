# Prod1: Kitchen Buyer's Desk

A static affiliate-guide site for three air fryers and ovens and two digital meat thermometers, published with GitHub Pages from `docs/` on `main`.

Live site: https://wingbangboozle1-lang.github.io/Prod1/

## What is here

| Path | What it is |
|---|---|
| `data/` | Source of truth: products (observed and intended fields kept apart), guides, sources, flags, suggestions, questions, ledger, site settings. |
| `scripts/build.mjs` | Generates `docs/` from `data/` and runs the publishing gate. Fails with exit code 1 if any gate fails. |
| `scripts/assets/` | Stylesheet and the five-event measurement script (browser-only by default). |
| `docs/` | Generated site. Do not edit by hand; edit `data/` and run the build. |
| `analytics-endpoint/` | Self-hosted, privacy-preserving event counter (Python standard library). Not hosted in this build. |
| `COORDINATION.md` | Shared task board for parallel sessions. |

## Build

```bash
npm run build      # or: node scripts/build.mjs
```

## Publishing gate

The build refuses to publish if any of these fail:

1. Disclosure strip above the main content on every page, repeated in the footer. Text: "As an Amazon Associate I earn from qualifying purchases." (Operating Agreement, Section 5.)
2. Every link to an Amazon host carries `rel="sponsored"`.
3. Every internal link resolves to a file in `docs/`.
4. Every page has a unique title and meta description.
5. No banned claim words (for example "trending", "bestseller", "top rated", "guaranteed").
6. Every product row has an official Amazon source; an intended ASIN, if present, is in ASIN format; a blank intended ASIN is shown as Unverified.
7. The sitemap lists every page; the feed includes every guide.

## Sources and flags

Verified sources, with the date of check and what was read: `docs/sources.html`. Irregularities and unverified items, each with source links and the action needed: `docs/flagged.html`.

## Publishing

GitHub Pages serves `main:/docs`. Pages settings: branch `main`, folder `/docs`.
