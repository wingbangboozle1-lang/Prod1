# COORDINATION.md — shared task board

Branch for this session: `arena/9b748801-prod1` (fixed by the session; not renamed).
Session ID: `9b748801`. Base commit: `86bb372` (`main`).

Status values: `unclaimed` · `in progress` · `done` · `needs review`
("needs review" = published on the Flagged for Review page; does not block anything.)

| Task | Status | Owner | Files in scope |
|---|---|---|---|
| T1 Repo review + irregularity log | in progress | 9b748801 | `data/*.json`, `FLAGGED.md`, `docs/flagged/` |
| T2 Product intent confirmation records (5 links) | in progress | 9b748801 | `data/products.json`, `docs/products/` |
| T3 Site build (landing, categories, guides, dashboards) | in progress | 9b748801 | `scripts/`, `src/`, `docs/` |
| T4 Compliance gate (disclosure, rel=sponsored, link + data checks) | in progress | 9b748801 | `scripts/check.mjs`, `src/templates/` |
| T5 Measurement scaffold (5 events, outbound click counter, endpoint slot) | in progress | 9b748801 | `src/assets/analytics.js` |
| T6 Executive summary + suggestions/questions | in progress | 9b748801 | `EXECUTIVE_SUMMARY.md`, `src/content/suggestions.json`, `src/content/questions.json` |
| T7 Integration: merge, re-verify, build, PR to `main`, merge, Pages check | unclaimed | — | all |

## Claims log

- 2026-11-19 · session 9b748801 · claimed T1–T6 (all files above). Working branch is `arena/9b748801-prod1` per session rule (not `session-<id>/<task>`); all tasks are in one session, so no cross-session conflicts are expected.
- Note: GitHub Pages was already enabled for this repo (source `main` `/`). This session changes the source to `main` `/docs` to serve the built site.

## Sessions log

- 2026-11-19 · 9b748801 · Repo was a single README. No other sessions visible on `origin` at claim time (`git ls-remote` showed only `main` and `HEAD`).

## Merge / deploy record

_To be filled in by T7 (PR link, merge result, Pages deploy status)._
