# COORDINATION — shared task board

Repository: `wingbangboozle1-lang/Prod1`. Branch for this session: `arena/bac417a2-prod1` (fixed by the session; the per-task `session-<id>/<task>` branch scheme in the brief is superseded by it). Base: `main` at `86bb372`.

Session ID: **bac417a2**. Integration session: **bac417a2** (this session performs the final integration itself, because no other session has claimed tasks).

Status vocabulary: `unclaimed`, `in progress`, `done`, `needs review`. A `needs review` item is published on the Flagged for Review page and does not block anything.

## Scope of shared files

Only this session has touched files in this branch. Other sessions must not edit files listed under a task they do not own. Files owned by the integration step: `docs/` (generated), `README.md`, `COORDINATION.md`, `.github/workflows/site-checks.yml`.

## Task board

| ID | Task | Status | Owner | Files touched | Notes |
|----|------|--------|-------|---------------|-------|
| T-01 | Repo review; source register | done | bac417a2 | `data/sources.json` | Sources read 2026-11-19 are listed with their status. Zone4 flagged page read for context only. |
| T-02 | Product-intent confirmation records | done | bac417a2 | `data/products.json` | Intended ASIN, official listing URL, confirmation date and source are stored. Observed redirect target is a separate field. Owner confirmation pending (P-03). |
| T-03 | Site build (landing, category, guides, summary, analysis, verification, flagged, suggestions, questions, measurement, policy) | done | bac417a2 | `tools/build_site.py`, `docs/`, `data/guides.json`, `data/questions.json`, `data/suggestions.json`, `data/measurement.json`, `data/ledger.csv` | 16 HTML pages, RSS feed, sitemap, robots.txt. |
| T-04 | Disclosure, sponsored links, policy gate | done | bac417a2 | `tools/check_site.py` | Gate passes. Runs in CI on pull requests. |
| T-05 | Question-shaped guides (four working titles) | done | bac417a2 | `data/guides.json` | Working titles only. No popularity claims. |
| T-06 | Analytics, click counter, measurement | needs review | bac417a2 | `data/measurement.json`, `data/ledger.csv` | No endpoint deployed. GitHub Pages cannot host one (P-10). Five events proposed, not defined in the brief (P-11). |
| T-07 | Flagged for Review, suggestions, questions | done | bac417a2 | `data/flags.json`, `data/suggestions.json`, `data/questions.json` | 19 flags; 16 suggestions awaiting owner choice. |
| T-08 | Publish to GitHub Pages | in progress | bac417a2 | repo settings | Pages source changed from `main /` to `main /docs` (P-18). Merge and deploy check follow. |

## Verification log (2026-11-19)

- Resolved the five submitted short links (S10–S14). Each resolves to one Amazon listing (ASINs B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z). No resolved URL carries `tag=`.
- Read listing headers and titles for the five ASINs (S5–S9). Captured titles as listed. Specification tables and prices were not captured.
- Read Associates Operating Agreement section 5 (S1) and Participation Requirements section 2 (S2).
- Read Google rel="sponsored" guidance (S3) and FTC Disclosures 101 (S4).
- Not performed: Associates Central checks, Special Link test, tracking report review, Search Console verification, IP License notice re-read, Participation Requirements 6(t) re-read.

## Irregularities

Full list with source links and requested actions: `data/flags.json`, published at `docs/flagged.html`. Highlights:

- P-01 Tracking ID supplied but not confirmed active in Associates Central.
- P-02 Special Link test not run; links use the tagged listing format.
- P-03 Short-link codes are not ASINs; intended ASINs read from resolved listings.
- P-05 Prices, availability and ratings withheld by policy.
- P-10 Requested analytics endpoint cannot run on GitHub Pages.

## Handoffs and conflicts

- No conflicts. `main` contained only the initial commit at session start, and no other session claims were found.
- No task was taken over from another session.

## Publication record

- Pull request: _recorded after creation_
- Merge result: _recorded after merge_
- Pages deploy: _recorded after deploy_
