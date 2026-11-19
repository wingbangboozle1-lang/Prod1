# Decisions log

| Date | Decision | Rationale | Source |
|---|---|---|---|
| 2026-11-19 | Brand: "The Countertop Guide" — spec-backed, no fake testing | Honest positioning; S-06 hands-on content not adopted until tested | Owner brief; FTC endorsement honesty |
| 2026-11-19 | Outbound buttons use official listing URL + tag, not link.amazon short links | Short-link compliance unresolved (FLG-001); official URL is checkable | Operating Agreement §1 (Special Links) |
| 2026-11-19 | No Amazon product images; SVG/CSS only | Program Content / IP licence risk until photography decided | Operating Agreement §1 |
| 2026-11-19 | Prices/ratings shown as 2026-11-19 snapshots with live-price disclaimer | Prices change; dated snapshot is the only honest form | Listing buy boxes 2026-11-19 |
| 2026-11-19 | Static site, no build step; Python generator from products.json | Reliable GitHub Pages deploy; single source of truth | Repo constraints |
| 2026-11-19 | Analytics: local-only counter, endpoint stub | Privacy-preserving; endpoint needs hosting decision (SG-03) | Owner brief (5 events) |
