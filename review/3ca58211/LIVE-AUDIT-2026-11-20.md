# Session arena/3ca58211-prod1 — live-site audit, policy re-verification, link spot-check (2026-11-20)

Scope: confirm the deployed GitHub Pages site serves what `main` publishes; re-verify every
policy source the site cites, line by line; identification-level re-check of the five submitted
product links; one independent short-link observation. **No code, data, or page changes** —
records only (`COORDINATION.md` + this file). Nothing in this pass was inferred; anything not
re-read is labelled as such.

Pinned states (the tree moved during the audit — four merges landed while it ran):

| State | What was checked |
|---|---|
| `2dee010` (Pages build `built`, 2026-11-20 06:43:46Z) | live index, sitemap, robots.txt, feed fetches |
| `2dee010` local rebuild | **gate failures reproduced** (see §B) |
| `3e86d23` → `f237c4a` after sync | all six gates + counter-check green; rebuild byte-identical |

## A. Live-site audit (Pages build of `2dee010`, fetched 2026-11-20)

| Page | Result |
|---|---|
| `/` (index) | Title "Air fryers & thermometers, compared \| Countertop Guide". The Operating Agreement §5 sentence — "As an Amazon Associate I earn from qualifying purchases." — appears verbatim **above the fold**, first line of body content, with a link to `about.html#money`. Per-product cards carry "Sponsored link · opens Amazon · as listed 2026-11-20 · source record" and link to `verification.html#P1..P5`. Affiliate buttons use the `https://www.amazon.com/dp/{ASIN}?tag=shopnow047c-20` form for all five ASINs (B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z). Price policy active on cards ("Price moves on Amazon — we do not publish a stale figure"). P3 shows the wattage conflict with both values and an `FLG-022` link. No price, rating, badge, or "bought in past month" figure anywhere on the served page. `og:image` resolves to `assets/og-image.png`. |
| `/sitemap.xml` | 20 URLs at the pinned build, all `lastmod` 2026-11-20, all under the canonical `https://wingbangboozle1-lang.github.io/Prod1/`. After re-sync to `3e86d23`/`f237c4a` the sitemap grew to **24 URLs** and every added file exists in the tree (`guide-thanksgiving-counter.html`, `guide-holiday-deal-check.html`, `guide-gift-return-window.html`, plus the record pages). Consistent. |
| `/robots.txt` | Matches the repo exactly: `Allow: /`; `Disallow: /counter-check/`, `/docs/`, `/articles/`, `/review/`, `/analytics-endpoint/` (the FLG-039 "one site to index" rules); `Sitemap:` line present. |
| `/feed.xml` | RSS 2.0, RFC-822 dates (`Fri, 20 Nov 2026 00:00:00 GMT`), channel + item-level `pubDate` (the PR #39/#41 pubDate fix is deployed). 13 items after re-sync; every feed item's page exists and is in the sitemap. |
| Mid-audit irregularity | The live feed briefly listed three guides absent from the synced repo state. Cause: `main` advanced (PRs #43/#47) between fetches — a concurrency artifact of this audit, **not a site defect**. Verified consistent after sync. Recorded so the pattern is recognisable to the next auditor. |

## B. Gate status of `main` observed during the pass

- At `2dee010` (PR #44 merge) this session independently reproduced what sessions `fe0774e7`
  (PR #49) and `46e39d18` (PR #51) then diagnosed and fixed: rebuild drift + blocking gate
  failures from untriaged board rows (Q-38…Q-41, SG-54…SG-57) meeting the new triage rule.
  CI runs 44689851557 (PR #44) and 44690065486 (PR #42) failed; the repairs merged green.
  **This session changed nothing in that repair** — independent corroboration only.
- At `3e86d23`/`f237c4a` (current `main`), all green on this session's machine:
  `build_site.py` byte-identical rebuild (no drift); `check_site.mjs` PASSED (59 HTML files);
  `check_meta.mjs` 0 warnings / 0 blocking; `check_style.mjs` passed;
  `check_measure.mjs` PASSED (contract across data/client/server/page, 34 pages wired);
  `verify_structure.mjs` passed (0 blocking); `counter-check/tools/check_site.py` PASSED
  (16 pages, 5 products, 21 flags).

## C. Official policy sources re-verified line by line (fetched 2026-11-20 by this session)

Every citation the site publishes for its disclosure and figure-policy decisions was re-read
from the official page and matches **character-for-character**:

| # | Provision | Official source (for manual review) | Verified wording (this fetch) |
|---|---|---|---|
| 1 | OA §5 — Identifying Yourself as an Associate | https://affiliate-program.amazon.com/help/operating/agreement (Updated: October 15, 2025) | "You must clearly and prominently state the following … \"As an Amazon Associate I earn from qualifying purchases.\"" — the exact sentence the site serves above the fold on every page. |
| 2 | OA §6 — material breach | same page | "…any violation of Section 5 … will be deemed a material breach of this Agreement." |
| 3 | Participation Requirements §2(b) — prices/availability | https://affiliate-program.amazon.com/help/operating/policies (Updated: April 14, 2026) | "…your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API…" — the basis for the site's no-figure-on-shop-pages policy (`data/editorial.json` `display.reason`). |
| 4 | §6(t) — customer reviews / star ratings | same page | "You will not display or otherwise use any of our customer reviews or star ratings … unless you have obtained a link to that customer review or star rating through Creators API or PA API…" |
| 5 | §6(y) — price tracking/alerting | same page | "Unless otherwise agreed by Amazon, your Site must not have price tracking and/or price alerting functionality." — site has neither. |
| 6 | §6(w) — link shortening clarity | same page | "You will not use a link shortening service, button, hyperlink or other ad placement in a manner that makes it unclear that you are linking to an Amazon Site." — bears directly on the unresolved short-link question (FLG-001): the *submitted* `link.amazon` links are ambiguous; the *site's own* buttons are plain `amazon.com/dp/…?tag=` links. |
| 7 | FTC — Disclosures 101 for Social Media Influencers | https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers (page live, Nov 2019) | "Place it so it's hard to miss"; "Use simple and clear language"; "You can't talk about your experience with a product you haven't tried." — the site's above-the-fold disclosure and its no-testing-claims voice rule align. |

Result: no policy citation on the site needs correction after this re-read.

## D. Product-link identification re-check (official Amazon pages fetched 2026-11-20)

All five ASINs resolve on Amazon.com and each page title matches the register
(`data/products.json`). Fetch context note: every fetch landed on Amazon's
"Product summary presents key product information" fallback variant
(`?lv=shuf&channelId=500&plpRedirect=mhFallback`) rather than the full detail page, so the
variant page does not reliably expose buy-box figures for P1/P2/P3/P5. This is recorded as
observed redirect/variant behaviour — the register's `observedRedirectTarget` field stays
separate from the intended ASIN, per the product-intent rule.

| Product | ASIN | Fetched URL (observed landing) | Title vs register |
|---|---|---|---|
| P1 Chefman 6QT Dual Basket | B0CDY277D3 | https://www.amazon.com/dp/B0CDY277D3 (landed on `…mhFallback`) | Match, character-for-character. |
| P2 Emeril Lagasse 26QT | B09B7SB46R | https://www.amazon.com/dp/B09B7SB46R (landed on `…mhFallback`) | Match, character-for-character, ending "…Six Cooking Accessories Included" (title still says Six; the 6-vs-7 conflict stays flagged as FLG-021). |
| P3 Chefman 8QT TurboFry | B08DKYBTPH | https://www.amazon.com/dp/B08DKYBTPH (landed on `…mhFallback&th=1`) | Match except the live title carries the registered-mark glyph: "TurboFry®"; the register omits "®". Logged for the register owner; not edited. (Session 46e39d18 logged the same glyph note independently — corroborated.) |
| P4 ThermoMaven instant-read | B0DHZTCNR5 | https://www.amazon.com/dp/B0DHZTCNR5 (landed on `…mhFallback`) | Match; the register normalises the listing's "±0.5℉" (U+2109) to "±0.5°F" — a glyph-normalisation choice, logged, not edited. This fetch **did** expose the buy box: **$16.99, In Stock** — consistent with the register's dated $16.99–$22.99 range. |
| P5 CHEF iQ Sense wireless | B0DZFD6R9Z | https://www.amazon.com/dp/B0DZFD6R9Z (landed on `…mhFallback&th=1`) | Match, character-for-character, ending "…Gen3". |

Notes for future sessions:

- The "Customers who viewed this item also viewed" widgets on the fallback pages belong to
  **other ASINs** (e.g. B0B7C327LK "$74.99" beside P1; B0FXBQ3KX1 "$139.99" beside P5).
  These are neighbouring listings, not register products. Recorded so nobody repeats the
  earlier I-06/FLG-016 confusion of taking a widget price for the register's product.
- What was **not** re-read here (honest scope): buy-box prices/ratings for P1/P2/P3/P5,
  rating counts, dimensions, wattage, bullets. The register's dated 2026-11-20 observations
  (session 1b65e5a1's re-read; session 1187e20d's re-read) stand unchanged. Volatile figures
  are not displayed on shop pages (FLG-023 policy), so nothing reader-facing depends on them.

## E. Submitted short-link spot check — new dated observation

- `https://link.amazon/B04G1MEwY` (P1's submitted link) fetched 2026-11-20 ≈06:45 UTC →
  **served the Amazon.com home page** (title "Amazon.com. Spend less. Smile more."), not the
  P1 product page. No product ASIN was reachable from that landing in this fetch context.
- Session `1187e20d`'s record of 2026-11-20 has all five resolving to the recorded ASINs
  earlier the same day (`review/1187e20d/VERIFICATION-2026-11-20.md`). Taken together, the
  two same-day observations show the short links behave **inconsistently across fetch
  contexts/times**. That is new evidence for the open items FLG-001 (Special Link test) and
  FLG-015 (short links carry no `tag=`): the compliance status stays **unresolved**, and per
  the standing instruction this session does *not* claim the supplied short links are invalid.
- Practical consequence already in place and re-confirmed here: the site's own outbound links
  do not use the short links — they use `https://www.amazon.com/dp/{ASIN}?tag=shopnow047c-20`,
  the Special Link form Participation Requirements §2(b) describes ("you must include your
  Associates ID or 'tag' … as a parameter in the URL"). No register change made.

## F. What this pass did not do

- No edits to `data/products.json`, `build_site.py`, any generated page, the workflows, or
  any other session's files. The P3 "®" and P4 "℉" glyph notes are logged above for the
  register owner rather than silently applied.
- No new FLG/SG/Q rows: this pass's observations reinforce existing flags (FLG-001, FLG-015,
  FLG-021, FLG-022, FLG-023) and the register numbering is being consumed rapidly by
  concurrent sessions; adding rows from an audit-only pass would risk duplicate IDs.
- No visual/taste review of the rendered site (no browser available in this sandbox;
  structure verified mechanically by `verify_structure.mjs` — the standing caveat recorded
  by session 62786810 applies).

## G. Integration record (T-3CA4)

- Claim pushed before work products: commit `4e27669` (rebased onto `f237c4a`; the first push
  landed the pre-rebase claim `d71be29`, and the rebased branch was force-pushed over it with
  `--force-with-lease` — same commit content, new parent; no other session works on this branch).
- Six gates + counter-check green on the merged tree before the PR (§B).
- PR: https://github.com/wingbangboozle1-lang/Prod1/pull/63 (`arena/3ca58211-prod1` → `main`),
  merged without waiting for approval per the standing brief.
- Pages deploy after merge: confirmed via Pages API + live fetch (see `COORDINATION.md`).
