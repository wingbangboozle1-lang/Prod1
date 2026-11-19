# Coordination Board — Prod1 (arena/9969fd0c-prod1)

**Session branch:** `arena/9969fd0c-prod1` (fixed; this session does not create or switch branches)
**Session ID:** `session-arena-9969fd0c`
**Base commit:** `86bb372dc76781a50966966c39481c5b242a9ea4` (main)
**Remote:** `https://github.com/wingbangboozle1-lang/Prod1.git`

## How to read this board
- `unclaimed` — available for any session to claim
- `in progress` — claimed by a session; do not touch its files
- `needs review` — published on the Flagged for Review page; does not block other work
- `done` — completed, committed, sources recorded
- Claim a task by writing your session ID + file scope, commit and push the claim immediately.
- Never start a task another session has claimed. Keep scopes non-overlapping.
- Shared outputs (table data, index, navigation) are changed only by the final integration session.

## Tasks

| ID | Task | Status | Owner | File scope | Sources / verification | Irregularities |
|----|------|--------|-------|------------|------------------------|----------------|
| T-01 | Create COORDINATION.md task board | done | session-arena-9969fd0c | COORDINATION.md | — | — |
| T-02 | Build site structure + publication landing page (leads with products) | done | session-arena-9969fd0c | index.html, assets/css/style.css, assets/js/main.js | S-04, S-17, D-21 | IR-01, IR-02 |
| T-03 | Category subpages (air fryers, kitchen) | done | session-arena-9969fd0c | category-air-fryers.html, category-kitchen.html | S-04, S-24 | IR-02 |
| T-04 | Dashboard/table page: entries + findings table | done | session-arena-9969fd0c | dashboard.html | Verification rule | IR-01 |
| T-05 | Disclosure strip above the fold + in footer on every page | done | session-arena-9969fd0c | all HTML | S-05, FTC S-07/S-24 | — |
| T-06 | rel="sponsored" on every outbound affiliate link | done | session-arena-9969fd0c | all HTML | S-05, Google qualify-outbound | — |
| T-07 | SEO: unique title + meta description per page, sitemap.xml, robots.txt | done | session-arena-9969fd0c | sitemap.xml, robots.txt, each HTML | S-04, Google snippets | — |
| T-08 | Structured data + social preview image (OG/Twitter) | done | session-arena-9969fd0c | each HTML, assets/images/og-default.png | S-09, S-18 (photo decision needed) | S-18 needs decision |
| T-09 | Click + conversion measurement: outbound-click counter, self-hosted analytics endpoint, 5 events | done | session-arena-9969fd0c | assets/js/analytics.js | Privacy-preserving | endpoint gate pending backend |
| T-10 | Product-intent confirmation record (ASIN, listing URL, confirmation date, source; redirect separate) | done | session-arena-9969fd0c | data/confirmations.json | Amazon ASIN definition | IR-01 (9-char ASINs) |
| T-11 | Suggestions section (review-before-implement) | done | session-arena-9969fd0c | suggestions.html | — | — |
| T-12 | Executive summary | done | session-arena-9969fd0c | executive-summary.md | — | — |
| T-13 | Line-by-line verification against official sources | done | session-arena-9969fd0c | all data files | Official sources only | IR-01, IR-02 |
| T-14 | GitHub Pages: build, no broken links, deploy live | in progress | session-arena-9969fd0c | GitHub Pages settings | — | — |
| T-15 | PR to main + merge + record result | unclaimed | — | GitHub PR | — | — |

## Irregularities / flagged items

| ID | Description | Source | Status |
|----|-------------|--------|--------|
| IR-01 | Supplied `link.amazon/…` short links embed 9-character tokens (B04G1MEwY, B02NbDxp3, B00hJ57DV, B0c8moW59, B0f3GKalj). Amazon ASINs are exactly 10 alphanumeric characters. Cannot verify against Amazon.com (host not in allowed outbound set). Treated as unverified; do not infer or fill values. | Amazon ASIN definition (affiliate help) | open |
| IR-02 | S-18 real product photography: Amazon Operating Agreement §1 treats images as Program Content; generated/copied photography not permitted. No photo source available yet. Needs a decision before publishing product images. | Amazon OA §1 | open — needs decision |

## Claims log
- session-arena-9969fd0c claimed T-01 (COORDINATION.md) at branch arena/9969fd0c-prod1 — committed.
- session-arena-9969fd0c completed T-02..T-13 on branch arena/9969fd0c-prod1 — committed. T-14 (GitHub Pages) in progress.
