# Rendered-page QA — session 1d3cc97c (T-1D3-A / T-1D3-B)

Date: 2026-11-20 (UTC). Base: `main` at bebe082 (after PR #38). Scope: the root publication only.

## What was checked

Every root `*.html` page (30 pages), at two widths: desktop 1366 px and mobile 390 px (touch, device pixel ratio 1). 60 renders in headless Chromium, with the stylesheet, fonts and art served from the checkout.

Per render:

- horizontal overflow of the document, and elements whose box passes the right edge of the viewport (ignoring anything inside a horizontally scrollable wrapper);
- images that failed to load, after scrolling the page so lazy images are requested;
- declared web fonts that did not load;
- page errors and console errors;
- requests that were not served from the checkout (none allowed through).

Tool: `scripts/render_qa.mjs` (new, in this branch). It is a reproducible harness, not a CI gate: the browser is not installed by the repository.

## Method and why it needed a harness

The pages reference their stylesheet, fonts and art by absolute `https://wingbangboozle1-lang.github.io/Prod1/…` URLs. A browser outside GitHub Pages therefore renders them unstyled. The first attempt rendered exactly that, and it looked like the "unstyled" defect the design-system fix (FLG-052) addressed. The harness intercepts those URLs and serves the matching file from the working tree. It then renders what the live site ships.

Browser: Chromium build from the npm package `@sparticuz/chromium` (131.0.1), driven by `puppeteer-core` (23.11.1), both installed outside the repository in `/tmp/chr`. The Playwright CDN is not reachable from this sandbox, so Playwright's own browser download failed. Shared libraries came from the same package (`al2023` bundle).

Tooling sources (not product data, so no product row cites them): [puppeteer-core on npm](https://www.npmjs.com/package/puppeteer-core) (installed 23.11.1), [@sparticuz/chromium on npm](https://www.npmjs.com/package/@sparticuz/chromium) (installed 131.0.1).

## Results (final run, after the fix)

Re-run on the merged tree (main at 863fac5 with this branch rebased on it): 60 runs, 0 with issues. The table below is from the first post-fix run on bebe082; the merged-tree run was identical.

Runs: 60. Runs with an issue: **0**. Overflow, off-screen elements, broken images, failed fonts, page errors, console errors and unserved requests: all **0**. Loaded fonts on every page: Fraunces and Inter.

| Page | Desktop | Mobile | Result |
|---|---|---|---|
| about.html | ok | ok | none |
| air-fryers.html | ok | ok | none |
| compare.html | ok | ok | none |
| compliance.html | ok | ok | none |
| dashboard.html | ok | ok | none |
| design-brief.html | ok | ok | none |
| executive-summary.html | ok | ok | none |
| flagged.html | ok | ok | none |
| guide-basket-vs-oven.html | ok | ok | none |
| guide-capacity-checklist.html | ok | ok | none |
| guide-cleanup-counter-space.html | ok | ok | none |
| guide-gift-picks.html | ok | ok | none |
| guide-gifts-by-budget.html | ok | ok | none |
| guide-holiday-gifts.html | ok | ok | none |
| guide-holiday-hosting.html | ok | ok | none |
| guide-holiday-roast.html | ok | ok | none |
| guide-instant-read-vs-wireless.html | ok | ok | none |
| guide-multifunction-questions.html | ok | ok | none |
| guide-small-kitchen.html | ok | ok | none |
| guide-thermometer-accuracy.html | ok | ok | none |
| guide-wattage-outlets.html | ok | ok | none |
| guides.html | ok | ok | none |
| index.html | ok | ok | none |
| methodology.html | ok | ok | none |
| review-desk.html | ok | ok | none |
| search.html | ok | ok | none |
| suggestions.html | ok | ok | none |
| thermometers.html | ok | ok | none |
| topics.html | ok | ok | none |
| verification.html | ok | ok | none |

## Defect found and fixed

- **suggestions.html, mobile (390 px): page 447 px wider than the screen.** Cause: `.badge-ok`, `.badge-warn` and `.badge-flag` in `assets/style.css` set `white-space: nowrap`. A long status badge inside a paragraph (the SG-49 status line, line ~403 of the generated page) could not wrap, so it pushed the document wider. Tables on the same page were already in `.table-scroll` containers and were not the cause, though they were the first suspect.
- **Fix:** badges now wrap (`white-space: normal; max-width: 100%; overflow-wrap: anywhere`). Stylesheet only; no generated HTML changed.
- **Before:** 1 run with issues (suggestions.html mobile, 447 px overflow). **After:** 0 runs with issues.

## Not checked, and why

- **Taste.** This is a mechanical render check. The look was judged from screenshots of the front page only (desktop and mobile). It was not reviewed page by page. A human still decides whether the site looks designed.
- **Live github.io.** The live site was not fetched through this harness. The sandbox fetch tool has its own access. Earlier sessions recorded live checks on the same deploy; this session did not repeat them.
- **Interactive states.** Search, chooser, decision-desk picks and the sticky compare bar were not exercised. They run in JavaScript and need a separate test.
- **Screenshots** are written to `/tmp/render-qa` outside the repository and are not committed.

## Reproduce

```
# once, outside the repo
mkdir -p /tmp/chr && cd /tmp/chr && npm init -y >/dev/null && npm i @sparticuz/chromium@131 puppeteer-core@23
# the browser needs the bundled al2023 shared libraries (libnss3 etc.)
# unpack node_modules/@sparticuz/chromium/bin/al2023.tar.br and set LD_LIBRARY_PATH to its lib dir
cd /home/user/Prod1 && LD_LIBRARY_PATH=/tmp/chr/libs/lib node scripts/render_qa.mjs --deps /tmp/chr
```
