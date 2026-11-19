# Review materials — session 9b748801 (2026-11-19)

This folder is the review record from session 9b748801. The live site on `main` (root pages, `docs/`, `articles/`, `build_site.py`, `data/products.json`) was built by another session and is authoritative. That session merged before this session's integration, so this session did **not** publish a second site. It kept its own sources here instead.

## Contents
- `flagged.json`, `questions.json`, `suggestions.json` — review data behind the flags, open questions and suggestion options (FL-01 to FL-21). The live site shows the same items as FLG-013 to FLG-020 (added to `build_site.py`) and the existing FLG-001 to FLG-012.
- `EXECUTIVE_SUMMARY.md` — summary of this session's verification and open decisions.
- `prototype/` — the standalone build and gate scripts used to produce a parallel site (not published). Kept for reproducibility only.

## Cross-check of the live site's product data (`data/products.json` on `main`)

| Row | Submitted link | ASIN checked on listing | Live-site value checked | Result |
|---|---|---|---|---|
| P1 | link.amazon/B04G1MEwY | B0CDY277D3 (final URL, 2026-11-19) | ASIN | match |
| P2 | link.amazon/B02NbDxp3 | B09B7SB46R | ASIN | match |
| P3 | link.amazon/B00hJ57DV | B08DKYBTPH | ASIN | match |
| P4 | link.amazon/B0c8moW59 | B0DHZTCNR5 | ASIN; price $16.99 (own page header) | ASIN match; price consistent |
| P5 | link.amazon/B0f3GKalj | B0DZFD6R9Z | ASIN | match |

Not re-verified in this integration: the other prices ($79.93, $149.99, $69.99, $119.99), ratings, dimensions, wattage and warranty. Those need a full read of each listing's product-details section (FLG-020).

## Link and disclosure checks on the live site (run 2026-11-19)
- 26 HTML pages. Every page contains the Associates statement. Internal links and in-page anchors: 0 problems.
- Amazon product-type links: 75. Missing `rel="sponsored"`: 0.

## Irregularities this session adds (live-site ids in brackets)
- Submitted codes are 9 characters and resolve to different ASINs (FLG-013).
- The 10-character ASIN rule comes only from third-party sources (FLG-014).
- No redirect URL carries `tag=shopnow047c-20` (FLG-015).
- Listing pages contain widget and carousel data for other products (FLG-016).
- The external Zone4 log says "three supplied links" (FLG-017).
- Proposed Amazon content notice, IP License §2(k) not read (FLG-018).
- Creators API prerequisites not read (FLG-019).

## Sources (official unless noted)
- Associates Program Operating Agreement — https://affiliate-program.amazon.com/help/operating/agreement
- Associates Program Policies — https://affiliate-program.amazon.com/help/operating/policies
- Google Search Central, qualify outbound links — https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- FTC Disclosures 101 for Social Media Influencers — https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Amazon listings — https://www.amazon.com/dp/B0CDY277D3 · B09B7SB46R · B08DKYBTPH · B0DHZTCNR5 · B0DZFD6R9Z
- Zone4 decision log (external, partly read) — https://kanlerxz87-cyber.github.io/Zone4/docs/decisions.html
- Third-party only: https://eva.guru/blog/what-is-amazon-asin-a-full-guide-to-create/ · https://ecombrainly.com/what-is-an-asin/
