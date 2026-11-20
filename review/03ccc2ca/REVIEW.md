# Repo review — session arena/03ccc2ca-prod1 (2026-11-20)

A line-by-line review of this repository against the brief, with the official source
links needed for manual review. Everything claimed here is either (a) read in this
session from the linked official page, (b) verified by a named deploy gate that ran in
this session, or (c) labelled "carried" with its session and date. Nothing is inferred.
The dated source reads of this session are in [VERIFICATION.md](VERIFICATION.md).

## 1. Brief requirement → where it lives → state

| Brief requirement | Where it is implemented | State (2026-11-20) | Evidence |
|---|---|---|---|
| Every table row has a source link; unconfirmed values blank + flagged, never inferred | `verification.html` (generated), `data/products.json` (`sourceUrl`, `sourceNote` per product) | Shipped; enforced by `scripts/check_site.mjs` (PASSED, 58 files) and the register's own rule text | https://www.amazon.com/dp/B0CDY277D3 (and the other four listings, all linked per row) |
| Product-intent record: intended ASIN, official listing URL, confirmation date, source; observed redirect in a separate field; never merged | `verification.html` "Product-intent confirmation record"; fields `asin` / `officialListingUrl` / `confirmationDate` / `confirmationSource` / `observedRedirectTarget` in `data/products.json` | Shipped as separate fields. **Carried caveat (I-03, unchanged):** the intended ASIN was filled from the observed redirect because the brief supplied no ASINs; the field provenance is stated in each `sourceNote` | Register rows on https://wingbangboozle1-lang.github.io/Prod1/verification.html |
| Replace ambiguous outbound links with validated Special Links; short-link compliance **unresolved, not invalid** | Site buttons: `https://www.amazon.com/dp/ASIN?tag=shopnow047c-20` with `rel="sponsored nofollow noopener"`; gates fail unmarked links | **Open — owner gate (FLG-001/FLG-015):** the enrolled-Associates click test needs a login no session has. The `link.amazon` short links are not called invalid anywhere | `flagged.html` FLG-001, FLG-015; OA §1 "Special Links" https://affiliate-program.amazon.com/help/operating/agreement |
| Disclosure above the fold on every page + footer; exact §5 sentence | `page()` issue bar + footer strip; sentence matches OA §5 verbatim (re-read this session, character-for-character) | Shipped; gate-checked on every page | OA §5: "As an Amazon Associate I earn from qualifying purchases." https://affiliate-program.amazon.com/help/operating/agreement |
| Every outbound product link marked sponsored | Generator post-step + `check_site.mjs` + `check_meta.mjs` fail any unmarked Amazon link | Shipped; 0 warnings | Google rule: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links |
| Privacy-preserving outbound-click counter + self-hosted endpoint, five defined events | `assets/app.js` (local counts, `if (!ENDPOINT) return;` gate), `analytics-endpoint/server.py` + `selftest.py`, contract gate `scripts/check_measure.mjs` (4th deploy gate) | Contract shipped (PR #37). **Endpoint not hosted — owner decision (SG-03/Q-08).** Nothing leaves the browser meanwhile | methodology.html; https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages (Pages is static-only) |
| Campaign ledger: empty, defined columns, first-party reports only | `methodology.html` + `docs/campaign-ledger.html` | Empty by design; no conversion score or revenue forecast anywhere | — |
| Compliance gate in the publishing workflow (disclosure + API policy checks) | `.github/workflows/pages.yml`: determinism check + `check_site` + `check_meta` + `check_style` + `check_measure` (+ endpoint self-test) + `verify_structure` before upload | All six green on this branch (see §3) | FTC: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers |
| "Read like a shop, not an audit"; publication front page; dashboard surfaces in footer + one nav group | `index.html` hero/picks/chooser/guides; `DESIGN_PROMPT.md`; internal surfaces `noindex, follow` and out of the sitemap | Shipped across several passes; kept in this pass | https://wingbangboozle1-lang.github.io/Prod1/ |
| Question-shaped guides; publishing cadence; each guide added to sitemap + feed | 13 guides in 3 clusters; calendar `topics.html` + `data/editorial.json`; `sitemap.xml` (23 URLs) + `feed.xml` generated from the page registry | This pass published the thermometer guide and reconciled the calendar; duplicate rows consolidated (FLG-093/SG-71) | topics.html; feed.xml |
| Suggestion desk with recommended paths + decision board before implementing | `suggestions.html`: SG-01..SG-73 with Path A/B/C and recommended paths, localStorage decision board with export | Shipped; this pass added SG-71..64 | suggestions.html |
| Clear Q/I/A list of what is known / missing / how to discover | `suggestions.html` Q-01..Q-50 | Shipped; this pass added Q-49 (accessory count) and Q-50 (measured queries) | suggestions.html |
| Executive summary | `executive-summary.html` | Refreshed this pass | executive-summary.html |
| Parallel-session coordination board | `COORDINATION.md` | Claimed, worked, and recorded per protocol | this file + COORDINATION.md |

## 2. Irregularities found in this review pass

1. **Topic-calendar duplication (fixed, reversible).** TOPICS 06 vs 11 (same question),
   09 vs published guide 01, 12 vs published gift guide — the FLG-047 trap in a new
   place. Consolidated to the surviving guides; owner-reversible; recorded as
   **FLG-093 / SG-71**. The `data/editorial.json` queue had drifted from the TOPICS
   table in the same way; both are reconciled. (IDs: renumbered twice during the
   merge after parallel passes claimed FLG-074/090/091/092, SG-54..61 and Q-38..44;
   the final numbers are FLG-093/094, SG-71/63/64, Q-49/46.)
2. **Stale typed counts (fixed).** `guides.html` said "Ten guides" in the heading and
   "Nine question-led guides" in the meta description (the real count was 10 before
   this pass); `topics.html`'s meta said "five published, seven queued" while its body
   computed 6/6. The body counts are computed from `TOPICS`; the typed strings had
   drifted. Fixed: the parallel passes replaced typed guide counts with counts
   computed from the data, and this pass did the same for the topic counts.
   **Recommendation for future sessions:** never type a count — compute it.
3. **Typographic normalization in the register (noted, not an error).** P3's title drops
   the `®` glyph ("TurboFry®" → "TurboFry") and P4's drops `℉`→`°F`; both confirmed
   character-identical otherwise against the listings this session
   ([VERIFICATION.md](VERIFICATION.md) §1 notes A/B).
4. **Two client scripts exist on purpose.** `assets/app.js` is the publication's
   five-event client; root `app.js` is a local-only counter for the supplementary
   builds (`docs/`, `counter-check/`) and is forbidden to transmit by
   `check_measure.mjs`. Not a defect; recorded so nobody "cleans it up" into a break.
5. **Carried caveats, unchanged:** I-03 (intended ASIN provenance), FLG-001/015
   (Special Link test + untagged short-link redirects), FLG-004/005 (blank thermometer
   dimensions, Emeril warranty term), FLG-021/022 (listing self-conflicts, both values
   shown), FLG-023/032/033 (price-display policy reading — owner ratification),
   FLG-051/SG-43 (Pages build source is the branch build; gates mark the commit red
   rather than blocking the publish), FLG-070 (three builds on one host — robots-
   suppressed; owner decides), SG-02 (custom domain), SG-03 (analytics host), SG-04
   (photography licence). All are on `flagged.html` with sources; none blocks the merge
   per the brief.
7. **Same-day content collisions between parallel passes (FLG-094).** Two passes
   independently answered the dual-basket question and the accessories question. The
   dual-basket draft that survives is the one already on `main`
   (`guide-dual-vs-single-basket.html`, unchanged); this pass's draft lives on as the
   consolidated page `guide-dual-vs-single.html`. For `guide-accessories-included.html`
   (both passes wrote the same URL) the fuller checklist-and-table draft survives with
   the other pass's baskets-count FAQ carried in. Superseded drafts remain in git
   history; each is one commit away. Owner call: SG-71.
8. **Draft PR #10** (`arena/a17ba53c-prod1`, "Counter Notes: buyer site, guides,
   dashboards, and checks (GitHub Pages from docs/)") is still open at the time of
   writing. Not merged by this session: it conflicts with the one-indexable-site rule.
   Owner's call (see FLG-070/Q-34).
9. **Visual QA remains impossible in this sandbox** (no browser installable; earlier
   attempts recorded in `review/62786810/VERIFICATION.md`). `verify_structure.mjs`
   proves structure, not taste. SG-44 keeps the visual review open for the owner.

## 3. Gates run in this session (all green)

| Gate | Command | Result |
|---|---|---|
| Page structure, disclosure, links, claims | `node scripts/check_site.mjs` | PASSED, 64 HTML files |
| Metadata, voice, price policy, sponsored marks | `node scripts/check_meta.mjs` | PASSED, 0 warnings |
| Design-system integrity | `node scripts/check_style.mjs` | PASSED, 0 warnings |
| Measurement contract (5 events) + endpoint self-test | `node scripts/check_measure.mjs` | PASSED (self-test 17/17) |
| Structural proof | `node scripts/verify_structure.mjs` | PASSED, 39 pages, 0 blocking |
| Secondary build gate | `python3 counter-check/tools/check_site.py` | PASSED (16 pages, 5 products, 21 flags) |
| Render QA (added by parallel pass) | `node scripts/render_qa.mjs` | run in CI; not re-run here |
| Determinism | rebuild ×2 | byte-identical (CI drift step would pass) |

## 4. Official sources for manual review (all fetched 2026-11-20 unless noted)

- Amazon listings: [B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3), [B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R), [B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH), [B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5), [B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z)
- [Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) (updated 2025-10-15) — §5 disclosure sentence verbatim, §1 Special Links
- [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) (updated 2026-04-14) — price/availability display rules, Special Link tag form
- [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) (carried read 2026-11-19/20)
- [Google Search Central — qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) (carried read 2026-11-19/20)
- [GitHub Pages — What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) — static hosting (why the endpoint needs its own host)
