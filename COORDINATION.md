# Coordination board

Shared task board for parallel agent sessions. Statuses: unclaimed, in progress, done, needs review.
Rule: claim by committing and pushing your session ID and file scope before starting. Edit only your claimed files.

## Active branches

| Branch | Session | Scope | Notes |
|---|---|---|---|
| `arena/b4c6c619-prod1` | `b4c6c619` | `docs/` (site output), `scripts/`, `analytics-endpoint/`, `package.json`, `README.md`, `COORDINATION.md` | This session. Base `86bb372` (main). |
| `arena/cba9af3f-prod1` | `cba9af3f` | Root-level `index.html`, `styles.css`, `site.js`, `guides/`, `review/`, `data/`, `feed.xml`, `sitemap.xml`, `robots.txt`, `README.md`, `COORDINATION.md` | **Overlap:** builds a publication site for the same products and task. Not merged into main. Not touched by `b4c6c619`. Logged as LOG-02. |

## Task board

| Task | Status | Owner | Files touched |
|---|---|---|---|
| T-01 Repo review and irregularity log | done | `b4c6c619` | `docs/flagged.html` (generated from `data/flags.json`) |
| T-02 Product-intent confirmation record (intended ASIN, official URL, confirmation date, source; observed redirect kept separate) | done, with unverified fields left blank | `b4c6c619` | `data/products.json`, `docs/products.html` |
| T-03 Publication-style site: front page, category pages, guides, sources, analysis, suggestions, flagged page | done | `b4c6c619` | `scripts/build.mjs`, `docs/**`, `data/**` |
| T-04 Click and conversion measurement (five events, browser-local; self-hosted endpoint code) | done in code; endpoint not hosted (see FLAG-06) | `b4c6c619` | `docs/assets/measure.js`, `analytics-endpoint/**` |
| T-05 Disclosure and sponsored-link compliance gate in the build | done | `b4c6c619` | `scripts/build.mjs` |
| T-06 Guides (question-shaped working titles) + feed + sitemap | done | `b4c6c619` | `data/guides.json`, `docs/guides/**`, `docs/feed.xml`, `docs/sitemap.xml` |
| T-07 Integration: build, link check, PR to main, merge, Pages deploy | in progress (see LOG-03 for the PR and deploy record) | `b4c6c619` | `docs/**`, `COORDINATION.md` |
| T-08 Google Search Console verification and sitemap submission | needs review (requires the owner's Google account) | unclaimed | none |
| T-09 Real product photography (S-18) | needs review (decision D-22 open) | unclaimed | none |
| T-10 Hosted analytics endpoint | needs review (decision D-43 open) | unclaimed | none |

## Logs

### LOG-03: completion record for T-01 to T-06 (2026-11-19)
- Sources checked: Operating Agreement (Section 5 line by line), Program Policies (existence and date only), FTC Disclosures 101 (read in full), Google `rel="sponsored"` (read in full), five short links and five Amazon product pages (fetch tool). Full list: `data/sources.json`, `docs/sources.html`.
- Verification performed: each product row has an official Amazon source link; blank fields are shown as Unverified; the build's publishing gate passed (disclosure above main and in footer, sponsored Amazon links, internal links, unique titles and descriptions, banned claim words, product table, sitemap and feed). Gate failure cases were tested in a scratch copy and fail as expected.
- Endpoint test: `analytics-endpoint/server.py` accepted a valid outbound_click, rejected an unknown event and a malformed ASIN, and wrote daily counts only.
- Irregularities: FLAG-01 to FLAG-12 in `data/flags.json`, published at `docs/flagged.html`.
- Not done, and why: intended ASINs, confirmation dates, prices and ratings (no official, attributable value; see FLAG-02 and FLAG-04); Search Console (needs owner account; FLAG-07); hosted endpoint (FLAG-06); named author (FLAG-08); product photography (FLAG-09).

### LOG-01: claim by `b4c6c619` (2026-11-19)
Claimed T-01 to T-07 on `arena/b4c6c619-prod1`. Scope is limited to the files listed above.

### LOG-02: overlap with `cba9af3f` (2026-11-19)
Branch `arena/cba9af3f-prod1` (commit `02ba93f`, "docs: claim publication site build") claims the same publication-site task with root-level files. This session did not read or edit that branch's content beyond its COORDINATION.md. Integration decision needed: which site output is published to Pages. This session publishes from `docs/` on main, so the Pages source is set to `main:/docs`.

## Verification and source notes (T-01 to T-06)

Sources were fetched in this session. Date of check: 2026-11-19.

| Source | Used for | What was checked |
|---|---|---|
| https://affiliate-program.amazon.com/help/operating/agreement | Disclosure wording (Section 5) | Section 5 text verified line by line: "As an Amazon Associate I earn from qualifying purchases." Page states "Updated: October 15, 2025". |
| https://affiliate-program.amazon.com/help/operating/policies | Policy references | Page exists; states "Updated: April 14, 2026". Participation Requirements text (6(v), 6(w)) **not** verified line by line in this pass. |
| https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers | Disclosure placement | Verified: disclosure should be "hard to miss", not only on an About page or behind "click MORE". Page dated November 2019. |
| https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` | Verified: `rel="sponsored"` for paid links. Page "Last updated 2025-12-10 UTC". |
| https://link.amazon/B04G1MEwY, `B02NbDxp3`, `B00hJ57DV`, `B0c8moW59`, `B0f3GKalj` | Observed redirect targets | Resolved with the fetch tool (sandbox `curl` cannot reach link.amazon). Recorded as observed only. |
| Amazon product pages `/dp/B0CDY277D3`, `B09B7SB46R`, `B08DKYBTPH`, `B0DHZTCNR5`, `B0DZFD6R9Z` | Observed titles and redirect targets | Page `<title>` read. Prices and ratings **not** recorded (see FLAG-04). |
| Sister register https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html (not an official source) | Event names (five events), decision references | Tracker event names read from the public repo (`analytics-endpoint/server.py` EVENT_NAMES). Not treated as verification of any product or policy fact. |

## Irregularities / needs review

See the site page "Flagged for Review" (`docs/flagged.html`, generated from `data/flags.json`).
