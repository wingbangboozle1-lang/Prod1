# Verification record — session 62786810, 2026-11-20

Every line below is something this session actually fetched or actually ran. Where a value
was **not** re-read today, it says so and the register keeps its original date. Nothing in
this file is inferred, and no figure is copied from another session's notes.

## 1. The five submitted links and the five ASINs

| Product | Submitted link | Resolved ASIN | Re-verified today | Notes |
|---|---|---|---|---|
| P1 | https://link.amazon/B04G1MEwY | B0CDY277D3 | **yes** — link followed, landed on `/dp/B0CDY277D3?lv=shuf&channelId=500&plpRedirect=mhFallback` | Title matched `data/products.json` word for word |
| P2 | https://link.amazon/B02NbDxp3 | B09B7SB46R | **yes** — link followed, landed on `/dp/B09B7SB46R?lv=shuf&btn_type=ss…` | Title matched; accessories count conflict in FLG-021 still present on the listing |
| P3 | https://link.amazon/B00hJ57DV | B08DKYBTPH | listing re-read **yes**; short link not re-followed today | Title matched |
| P4 | https://link.amazon/B0c8moW59 | B0DHZTCNR5 | listing re-read **yes**; short link not re-followed today | Title matched; rating 4.6 (3,499) matched the register exactly |
| P5 | https://link.amazon/B0f3GKalj | B0DZFD6R9Z | listing re-read **yes**; short link not re-followed today | Title matched, including "3 Ultra-Thin Probes" |

Official listing URLs used as the source of record:
`https://www.amazon.com/dp/B0CDY277D3`, `/B09B7SB46R`, `/B08DKYBTPH`, `/B0DHZTCNR5`,
`/B0DZFD6R9Z`.

**Observation on the two followed links:** after redirect, the landing URL carries Amazon's
own tracking parameters (`lv`, `channelId`, `plpRedirect`, `btn_ref`) and **no `tag=`**.
That is consistent with FLG-015 and is not evidence of anything about the short links
themselves. Their compliance status as Special Links remains unresolved (FLG-001) and this
session makes no claim either way.

## 2. Figures observed today versus the register

| Field | Register value (2026-11-19) | Observed 2026-11-20 | Verdict |
|---|---|---|---|
| P1 buy box | $79.93 | $79.93 | unchanged |
| P1 List Price | $99.99 | $99.99 | unchanged |
| P1 buy-box unit price | not recorded | $39.97 per count | new field, not published (policy: no prices on shop pages) |
| P4 rating | 4.6 (3,499) | 4.6 (3,499) | unchanged |
| P4 item length | not captured | **6.5 in** (`Item Length`, Measurements block) | new — recorded in FLG-072 |

Ratings, prices and badges are volatile Program Content. They live in the register as dated
observations and are **not** displayed on shop pages; the policy reason is on
`compliance.html` and `flagged.html#FLG-032`.

## 3. Policy text re-read today

| Source | What was read | Result |
|---|---|---|
| https://affiliate-program.amazon.com/help/operating/agreement | §5, verbatim, from the page headed "Updated: October 15, 2025" | The sentence is exactly: "As an Amazon Associate I earn from qualifying purchases." The site's strip and footer match it character for character, including the period. |
| same | §6(a) | "any violation of Section 5 … will be deemed a material breach" — the reason the wording is treated as a launch item |
| same | §1 | Special Links are "the special 'tagged' link formats we provide" — the basis for FLG-001 remaining open |
| same | §7 | Service Offerings include "data, images, text" — the basis for the no-photography rule |

Not re-read today, and therefore not re-asserted: Program Policies (last read 2026-11-19),
FTC Disclosures 101, Google Search Central. Their quotes on `compliance.html` keep their
original read date.

## 4. Fonts — licence and provenance

| File | Source | Licence |
|---|---|---|
| `assets/fonts/fraunces-latin-wght-normal.woff2` (36,620 B) | `@fontsource-variable/fraunces@5.3.0`, latin subset, weight axis | SIL OFL 1.1 — `assets/fonts/OFL-Fraunces.txt`, header verified against https://raw.githubusercontent.com/google/fonts/main/ofl/fraunces/OFL.txt (fetched today: "Copyright 2018 The Fraunces Project Authors") |
| `assets/fonts/fraunces-latin-wght-italic.woff2` (45,656 B) | same | same |
| `assets/fonts/inter-latin-wght-normal.woff2` (48,256 B) | `@fontsource-variable/inter@5.3.0`, latin subset | SIL OFL 1.1 — `assets/fonts/OFL-Inter.txt` |
| `assets/fonts/inter-latin-wght-italic.woff2` (51,832 B) | same | same |

Total 182,364 bytes. Self-hosted: no request leaves the visitor's browser to a font CDN, which
is both a privacy choice and a rule the new style gate enforces by warning on any
`fonts.googleapis.com` link.

**Irregularity found while doing this (published as FLG-067):** the license file inside the
Fraunces package named the *Inter* project in its first line. That is an upstream packaging
artifact, not a licensing ambiguity — the authoritative OFL text from the Fraunces repository
was fetched and the local header corrected to match it. Both fonts are OFL 1.1 regardless.

## 5. What this session changed, and the check that proves each one

All run on the built tree, in this order, after the last edit:

```
python3 build_site.py            -> 30 pages, 26 search entries, 20 sitemap URLs, 4 consolidated
node scripts/check_site.mjs      -> CHECK PASSED, 55 HTML files
node scripts/check_meta.mjs      -> Gate passed, 30 pages, 20 sitemap URLs, 0 warnings
node scripts/check_style.mjs     -> Gate passed, 30 pages, 1793 class uses, 96 classes, 28 properties
node scripts/verify_structure.mjs-> 30 pages walked, 0 blocking, 0 warnings
python3 counter-check/tools/check_site.py -> PASSED (16 pages, 5 products, 21 flags)
```

| Change | Proof |
|---|---|
| Fonts ship and are used | `check_style.mjs` new rule 8: a family with no `@font-face` fails, a `@font-face` with no file on disk fails. Ran a negative test — moved `inter-latin-wght-normal.woff2` aside and the gate failed with the exact path. |
| Nav marks the current section | `aria-current="page"` present on the owning link of each of 30 pages, verified page by page |
| Sitemap is the shop, not the audit | 20 URLs, every one a buying or reference page; the 7 internal surfaces carry `noindex, follow`. `check_meta.mjs` now fails a page that is in neither the sitemap nor noindex, and fails a noindex page that is still listed |
| Guide 10 exists in all three places | `grep guide-instant-read` → sitemap 1, feed 1, guides.html 1, topics.html 1, index 2 |
| Rebuild is deterministic | ran `build_site.py` twice; `git status` shows no further change beyond the intended edits |

## 6. What could not be verified, and why

| Item | Why not | Where it is published |
|---|---|---|
| Whether a click on any of the five links is attributed to `shopnow047c-20` | requires an Associates Central login; no session credential exists | FLG-001, SG-53, Q-30 |
| Search Console queries, impressions, position | property does not exist | SG-52, methodology.html |
| CHEF iQ temperature tolerance | not stated anywhere in the listing's fields; the manual is a linked PDF this session did not open | FLG-071, Q-31 |
| Full dimensions for either thermometer | P4 gives `Item Length` only; P5 gives none | FLG-004, FLG-072 |
| Emeril warranty term | the listing links a warranty PDF; no term in the listing text | FLG-005 |
| Whether the listings' dimensions match the shipped unit | requires a physical unit | Q-32 |
| Anything about traffic, revenue or ranking | no first-party report exists; the ledger is empty by design | methodology.html, FLG-011 |

## 7. Visual review — the honest limitation

No browser could be installed in this sandbox (`npx playwright install chromium` and
`npx puppeteer browsers install chrome-headless-shell` both failed at download). There is
therefore **no screenshot-based verification** of the visual result in this pass, and the
site is not claimed to have been looked at.

What stands in for it is structural: `scripts/verify_structure.mjs` proves the documents
parse, that every asset the HTML names exists, that fonts resolve to files, that headings
are ordered, that images declare dimension and alt, and that no card carries a fixed pixel
width. What it cannot prove is whether the result looks good. That is a human check, and it
is called out as such in the script header and on `executive-summary.html`.
