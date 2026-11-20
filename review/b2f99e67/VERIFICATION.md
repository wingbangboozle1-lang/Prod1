# Verification record — session arena/b2f99e67-prod1 (2026-11-20)

Scope of this pass: the design-prompt, decision-desk and publication-craft lane
(claim in `COORDINATION.md`). This record covers the sources read, the checks run on
this pass's own output, and the irregularities found. It does **not** re-verify the
five product listings — three parallel sessions (`3ca58211`, `7bc009de`, `5da138fb`)
own the re-verification lane this same day; the register's dated values were read
here only for consistency and were **not changed**.

## 1. Official sources read in this session (fetched 2026-11-20)

| Source | URL | What was read line by line | Result |
|---|---|---|---|
| Associates Program Operating Agreement | https://affiliate-program.amazon.com/help/operating/agreement | Header ("Updated: October 15, 2025"), §5 "Identifying Yourself as an Associate" | §5 disclosure sentence confirmed verbatim: "As an Amazon Associate I earn from qualifying purchases." — matches the sentence on every page of the site. §5 also bars other public communication about the Agreement without permission; the site makes none. |
| Google Search Central — qualify your outbound links | https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | `rel="sponsored"` definition, multiple-values rule ("sponsored nofollow" is valid), page updated 2025-12-10 | Confirms the marking used on every outbound product link (`rel="sponsored nofollow noopener"`). |
| Amazon Associates Program Policies | https://affiliate-program.amazon.com/help/operating/policies | Commission Income Statement sections (chunk 1) | Read for the redirect-link and improperly-formatted-link disqualification clauses (relevant to FLG-001/FLG-015 wording). The price/availability display clause was **carried** from the register's dated read (2026-11-20, sessions fbfe1742 / 46e39d18), not re-read in this pass. |
| The five Amazon listing pages | https://www.amazon.com/dp/{ASIN} | — | **Not re-read in this pass.** Owned by the parallel verification sessions today. Every product value on the site remains the register's dated snapshot. |

## 2. Line-by-line check of what this pass publishes

| Item published | Checked how | Outcome |
|---|---|---|
| Slate on `decisions.html` (7 rows, one per gate) | Rendered from `data/decisions.json` gates; every option label appears once per gate; recommended column shows only options whose label carries "(recommended)" in the data | OK — no recommendation invented; gates whose data lacks a "recommended" label show "no recommendation recorded" |
| SG-65…SG-70 rows and Q-45…Q-48 rows | Each claim inside the rows traced to a file or an official page: the hero markup (index.html hero section), the five drawings (`assets/art/`, 5 files), the picker implementation (`assets/app.js`, `localStorage` only), the proposed default rule (`data/decisions.json` defaultRule), the unhosted endpoint (`data/editorial.json` `events.endpoint` empty) | OK — every row cites what it rests on; no popularity, traffic or revenue statement anywhere in the new copy |
| "34 pages" figure in the executive summary | Build output: `pages: 34` | OK |
| Theme-color fix (FLG-085) | `grep -h 'theme-color' *.html` → 34 × `#1E1712`, 0 × `#1F2937` | OK |
| Cross-page anchors introduced (`#slate`, `#FLG-085`, `#suggestions-2026-11-20-b2f`, `#SG-04`, `#SG-34`, `#SG-02`) | `scripts/check_meta.mjs` anchor rule (fails the build on a dead cross-page anchor) | OK — gate green after the flag rows and the `#slate` anchor landed |
| Five-event measurement contract untouched | `scripts/check_measure.mjs` (contract across data, client, server, page) | OK — `PASSED: contract = [chooser_complete, guide_read, outbound_click, page_view, search]` |
| Disclosure + sponsored link rules untouched | `scripts/check_site.mjs` over 59 HTML files | OK — `CHECK PASSED` |
| Design-system coverage of the new markup | `scripts/check_style.mjs` | OK — 0 warnings (new tables reuse existing classes) |
| Determinism | `python3 build_site.py` twice; md5 over all root HTML + sitemap + feed identical (`195af26d…`) | OK |

## 3. Repo consistency sweep (the "REPO WORK" line)

- `.github/workflows/pages.yml` parses; the deploy job rebuilds, refuses drifted
  checkouts, and runs all six gates before upload. Checked by reading the YAML and by
  the successful run history on `main`. No unresolved conflict markers in any shipped
  code/HTML/YAML/JSON file (repo-wide `grep` for `<<<<<<<` matches only COORDINATION.md's
  prose describing past incidents, which quotes the marker text).
- Root `app.js` + root `styles.css` are **not** orphans: they serve the secondary
  `articles/` and `docs/` builds (that build's `../app.js` reference). Their separate
  local-count vocabulary is recorded as **FLG-086**; not edited here (owner scope).
- ID hygiene: this pass reserved SG-65…SG-70, Q-45…Q-48, FLG-085…FLG-092 in the claim
  to avoid the number-collision problem earlier sessions hit (FLG-060/SG-44/45, SG-54…57).
  Used: SG-65…70, Q-45…48, FLG-085, FLG-086. FLG-087…092 stay reserved and unused.
- Mechanical-tell sweep over the built output: no `example.com`, no TODO/FIXME/Lorem,
  no `undefined` renders, canonicals uniform, `theme-color` uniform. Nothing else found
  — recorded as a clean sweep rather than a padded flag row.

## 4. Irregularities carried out of this pass

| ID | What | Status |
|---|---|---|
| FLG-085 | Browser chrome colour was off-palette on all pages; fixed to the brand ink. Two near-identical brand inks (`#171310` / `#1E1712`) left as found | Fixed, owner may accept or revert one line |
| FLG-086 | Second local-measurement vocabulary in root `app.js` (secondary builds) | Open — request to those builds' owner; also covered by SG-51 / FLG-070 |
| carried | FLG-001, FLG-003…005, FLG-008/009, FLG-015, FLG-022…024, FLG-026, FLG-032/033, FLG-051, FLG-070, FLG-080 and the rest of the register | Unchanged by this pass |

## 5. What this pass deliberately did not do

- No listing value read, changed, or presented as re-verified.
- No imagery added (SG-65 is a proposal; the design prompt carries the direction).
- No CTA, disclosure, outbound link, event name, or ledger rule touched.
- No file outside the claimed scope edited: `data/products.json`, `counter-check/`,
  `docs/`, `articles/`, `analytics-endpoint/`, `scripts/`, `.github/` and
  `review/<other-session>/` were read-only.

## 6. Manual-review links (for the owner)

- The slate: https://wingbangboozle1-lang.github.io/Prod1/decisions.html#slate
- The suggestions desk: https://wingbangboozle1-lang.github.io/Prod1/suggestions.html
- The flagged register (FLG-085/086 at the foot): https://wingbangboozle1-lang.github.io/Prod1/flagged.html
- Design prompt §10: `DESIGN_PROMPT.md` in the repository root
- Policy sources: the three URLs in §1 above

## 7. Addendum — pre-PR rebase onto origin/main (2026-11-20)

The branch rebased onto `main` @ `726a977` before the PR; conflicts were resolved with
both sides kept, and everything this pass publishes was re-checked on the merged tree:

- This pass's flags renumbered **FLG-085→FLG-091**, **FLG-086→FLG-092** (parallel passes
  had taken FLG-085/086 for different rows). Every reference in this pass's copy updated.
- `data/decisions.json`: ghost theme ids (Q-43, Q-44, SG-60 — rows deleted in earlier
  merges) removed; four double-classified rows (Q-02, Q-14, SG-33, SG-43) kept in their
  first theme only, as main's new generator gate now requires. Recorded in COORDINATION.md.
- Re-ran on the merged tree: build exit 0, no warnings; `check_site` PASSED (62 HTML),
  `check_meta` PASSED (0 warnings), `check_style` PASSED, `check_measure` PASSED (37
  pages), `verify_structure` PASSED, `counter-check` PASSED. Rebuild byte-identical.
- The §2 claims re-checked against the merged output: slate renders 7 gates; SG-65…70 and
  Q-45…48 rows present and triaged; theme-color `#1E1712` on every page; the five-event
  contract untouched.
