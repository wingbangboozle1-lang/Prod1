# Coordination board

Branch: `arena/a17ba53c-prod1` (session `a17ba53c`), based on `main` at `86bb372dc76781a50966966c39481c5b242a9ea4`.
Branch rule followed: all work on this branch. Only this branch is pushed.

## Task board

| Task | Status | Owner / session | Scope (files) | Notes |
|---|---|---|---|---|
| T-01 Site build: product table, category pages, guides, dashboards, feed, sitemap | done (needs owner review of flagged items) | `a17ba53c` | `data/`, `content/`, `site_src/`, `tools/`, `docs/`, `endpoint/`, `README.md`, `COORDINATION.md`, `.gitignore` | Published output in `docs/`. |
| T-02 Verify five supplied short links | done (observed only) | `a17ba53c` | `data/products.json`, `data/sources.json` | Observed 2026-11-19. Intended ASINs not confirmed. |
| T-03 Special Link test (one per product, Associates workflow) | not run | owner | none | Needs a logged-in Associates session. See F-03. |
| T-04 Analytics collector hosting and consent decision | unclaimed | owner | none | See SG-01, Q-05. |
| T-05 Publishing cadence and next-topic selection from measured queries | unclaimed | owner | none | Needs Search Console (Q-09). See SG-03. |

## Overlap with another session

- Origin branch `arena/cba9af3f-prod1` (commit `02ba93f`) carries a claim, "Build the publication-style affiliate website", over `index.html`, `styles.css`, `site.js`, `guides/`, `review/`, `data/`, `feed.xml`, `sitemap.xml`, `robots.txt`, `README.md`, `COORDINATION.md`.
- This session did not read-write that branch. It builds in `site_src/`, `data/`, `content/`, and `docs/`, so it does not collide with the file paths in that claim. The two builds still overlap in purpose.
- Logged request for the owner: choose which build publishes (SG-08 on the suggestions page, F-09 on the flagged page). This session did not merge or rewrite the other branch.
- No merge conflict occurred. Nothing from the other session's work was discarded.

## Verification log

| Date | Check | Source | Result |
|---|---|---|---|
| 2026-11-19 | Each supplied `link.amazon` short link opened; redirect target, title and breadcrumb read | Amazon.com listing pages (SRC-01 to SRC-05) | 5 of 5 resolved to `amazon.com/dp/` pages. Observed ASINs B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z. |
| 2026-11-19 | Associates disclosure wording | Operating Agreement Section 5 (SRC-06); search excerpt | Confirmed. Full page not fetched. |
| 2026-11-19 | rel="sponsored" for paid links | Google Search Central (SRC-08) | Fetched; last updated 2025-12-10 UTC. |
| 2026-11-19 | ASIN format (10 characters) | Seller Central forum (SRC-11) | Secondary. No Amazon help-centre page located. F-01. |
| 2026-11-19 | Build and checks | `tools/build.py`, `tools/check.py` | Build: 21 pages. Check: passed. Negative test: planted bad link, bad table row, currency, and tag were all caught. |
| 2026-11-19 | Endpoint behaviour | `endpoint/server.js` run locally | Valid event 204; unknown event 400; oversized body 413; GET 404; CORS limited to site origin. |

## Irregularities and unverified items

See the site's **Flagged for Review** page (`docs/flagged/`) for the full list with sources. Summary:

- F-01 Short-link slugs are 9 characters; ASINs are 10.
- F-02 No intended ASIN confirmed for any link.
- F-03 Special Link test not run; links kept as submitted.
- F-04 Tracking ID `shopnow047c-20` not verified; no tags generated.
- F-05 Prices, ratings, commissions not published.
- F-06 "Five defined events" not listed in the brief; five proposed.
- F-07 Analytics endpoint not hosted; tracker off.
- F-08 No author named; "Counter Notes" is a working name.
- F-09 Overlapping claim by another session (see above).
- F-10 Zone4 references are not official sources.
- F-11 Register rows S-07, S-20, S-25 have no source and no status.
- F-12 No product photography used.
- F-13 Repository was a blank starter.

## Merge and deploy record

Pending. Filled in after the pull request is opened and merged (see the bottom of this file once recorded).
