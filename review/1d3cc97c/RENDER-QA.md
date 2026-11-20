# Rendered-page QA harness — session 1d3cc97c

Date: 2026-11-20 (UTC). Scope: the root publication only. This PR adds a reusable harness and this note. It changes **no site output**.

## What this PR adds

`scripts/render_qa.mjs`: renders every root `*.html` page at desktop (1366 px) and phone (390 px) width in headless Chromium, with the stylesheet, fonts and art served from the checkout, and reports:

- horizontal overflow of the document, and boxes that pass the right edge of the viewport (ignoring anything inside a horizontally scrollable wrapper);
- images that did not load, after scrolling so lazy images are requested;
- declared web fonts that did not load;
- page errors and console errors;
- any request not served from the checkout.

It writes screenshots to `/tmp/render-qa` (outside the repo) and prints JSON. `--strict` exits non-zero if any run has a problem. It is not wired into CI: the repository does not install a browser.

## Why it needed interception

The pages reference their stylesheet, fonts and art by absolute `https://wingbangboozle1-lang.github.io/Prod1/…` URLs. Without interception, a browser outside GitHub Pages renders them unstyled. The harness serves those URLs from the working tree, so the render matches what the live site ships.

## Result on current main (5810211)

Run with `--strict` on this branch, which differs from main only by the two files above: **37 pages × 2 widths = 74 runs, 0 with issues.**

## Relation to other sessions' work (overlap, stated plainly)

- Session `8aa7237d` (commit `ee36edd`, "first browser-based visual QA") ran a browser QA of all pages on main and fixed the two defects this session also found: `suggestions.html` status pills forcing an 801 px-wide page on a phone (`nowrap`), and `decisions.html` grid tracks (`1fr`) forcing a 456 px page. Its fixes are on main; this branch's `assets/style.css` is identical to main.
- This session therefore made **no further site change**. Its earlier edits to the same two rules were dropped in favour of main's equivalent fixes during rebase.
- What this PR adds beyond `8aa7237d`: the harness as a committed, reproducible script, instead of an ad-hoc run.

## Not checked here

- Visual taste: this is a mechanical check, not a design review.
- Live github.io fetch and interactive surfaces (search, chooser, decision desk): not exercised by this harness.

## Reproduce

```
mkdir -p /tmp/chr && cd /tmp/chr && npm init -y >/dev/null && npm i @sparticuz/chromium@131 puppeteer-core@23
# unpack node_modules/@sparticuz/chromium/bin/al2023.tar.br (brotli) and extract; set LD_LIBRARY_PATH to its lib dir
cd /home/user/Prod1 && LD_LIBRARY_PATH=/tmp/chr/libs/lib node scripts/render_qa.mjs --deps /tmp/chr --strict
```

Tooling sources (not product data): [puppeteer-core on npm](https://www.npmjs.com/package/puppeteer-core) (23.11.1), [@sparticuz/chromium on npm](https://www.npmjs.com/package/@sparticuz/chromium) (131.0.1).
