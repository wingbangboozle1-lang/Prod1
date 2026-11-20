# Verification record — session arena/1035d1e2-prod1 (2026-11-20)

Scope: a dated, line-by-line check of (a) the policy text this site relies on, re-read today, and (b) the machine-checkable claims in the build. Where a value could not be re-read today it is labelled as carried from an earlier pass and is **not** presented as re-verified here.

Every claim below is either quoted from an official page fetched in this session, or produced by a command in this repository that anyone can re-run.

---

## 1. Policy sources — re-read 2026-11-20

| # | Source (official) | What it governs here | Read | Result |
|---|---|---|---|---|
| S1 | [Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) — "Updated: October 15, 2025" | §1 defines Special Links ("must properly use the special 'tagged' link formats we provide"); §5 requires the disclosure sentence; §2 makes compliance a condition of commission | 2026-11-20 | Agreement page title and the §1 text read directly. The update date shown is unchanged from the 2025-10-15 already recorded. **No change to the site's obligations.** |
| S2 | [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Commission Income Statement §2 (disqualified purchases), Program Policies §6 (content on your site), Participation Requirements (price/availability display), §6(t) (ratings) | 2026-11-20 | Read the Commission Income Statement §2–4 and Program Policies §3–6. The revision date shown on the page is **2026-04-14**, unchanged. **No change.** |
| S3 | [Google Search Central — Qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) | `rel="sponsored"` for advertisements and paid placements; multiple rel values allowed | 2026-11-20 | Verbatim: "Mark links that are advertisements or paid placements … with the `sponsored` value"; multiple values may be space- or comma-separated. Page last updated **2025-12-10** (as shown on the page). The site's `rel="sponsored nofollow noopener"` satisfies this. |
| S4 | [FTC — Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) | Disclosure must be hard to miss, in simple clear language, and placed with the endorsement | 2026-11-20 | Quoted: "Place it so it's **hard to miss**"; "Disclosures are likely to be missed if they appear only on an ABOUT ME or profile page, at the end of posts or videos, or anywhere that requires a person to click MORE"; "You can't talk about your experience with a product you haven't tried." **Directly relevant:** see finding F-4 below. |

### Findings from the policy read

- **F-1 (no action).** The site's disclosure strip sits directly under the masthead, above `<main>`, on every page, and is repeated in the footer. This matches S4's "hard to miss / not only on an about page" requirement and S1 §5.
- **F-2 (no action).** Every Amazon outbound link — static and script-built — carries `rel="sponsored"`, satisfying S3. Checked mechanically over 54 HTML files plus `assets/app.js`.
- **F-3 (carried).** The price/rating display decision (no figures on shop pages; dated observations in the register) rests on S2's Participation Requirements and §6(t). Those clauses were read on 2026-11-19 and the policy page's revision date is unchanged today; this session did not re-read the clause text word for word, so the register keeps **FLG-032** open as the owner's ratification item. **Not upgraded to "re-verified" here.**
- **F-4 (new — recorded as FLG-058).** S4 states the disclosure should be "placed with the endorsement message itself". On this site the endorsement is effectively the product cards and the buy button. The statement is above the fold on every page and beside every buy button through the "Sponsored link · opens Amazon" line, but the *Agreement* sentence itself is not repeated inside each card. A strict reading of S4 could ask for it. This is an owner/compliance call, not something this session will change unilaterally.

---

## 2. Product identification — status of each field

The five listings were read line by line on **2026-11-19** and re-read by two later sessions on 2026-11-20 (see `review/1187e20d/VERIFICATION-2026-11-20.md` and the `963ca90f` record in `COORDINATION.md`). **This session did not re-open the five Amazon listings.** It:

1. read `data/products.json` in full;
2. confirmed the register's internal consistency (intended ASIN separate from observed redirect; confirmation date and source present on all five);
3. re-ran the metadata gate, which fails if a listing URL does not contain its own ASIN.

| ID | ASIN in register | Listing URL contains it | Confirmation date | Intended-ASIN field | Status carried |
|---|---|---|---|---|---|
| P1 | B0CDY277D3 | yes | 2026-11-19 | blank (submitted code is not an ASIN) | observed-only — **FLG-045** |
| P2 | B09B7SB46R | yes | 2026-11-19 | blank | observed-only — FLG-045 |
| P3 | B08DKYBTPH | yes | 2026-11-19 | blank | observed-only — FLG-045 |
| P4 | B0DHZTCNR5 | yes | 2026-11-19 | blank | observed-only — FLG-045 |
| P5 | B0DZFD6R9Z | yes | 2026-11-19 | blank | observed-only — FLG-045 |

**Explicit limit of this session's product verification:** the listing *values* (titles, dimensions, capacity, wattage, bullets) are carried from the 2026-11-19 reads. They are not re-asserted as verified on 2026-11-20. Anyone reading a page should treat the date on the page as the source of truth, which is why every page states it.

---

## 3. Machine-checkable claims — run in this session

All run from the repository root.

| Claim | Command | Result (2026-11-20) |
|---|---|---|
| The build is deterministic | `python3 build_site.py && python3 scripts/make_og.py && git diff --exit-code` | **No diff.** Rebuild reproduces the committed HTML exactly. |
| Disclosure, sponsored marking, internal links, titles, claim wording | `node scripts/check_site.mjs` | **PASSED — 54 HTML files**, 0 failures. |
| Metadata, voice, price policy, sitemap/feed integrity | `node scripts/check_meta.mjs` | **PASSED — 29 pages, 25 sitemap URLs, 0 warnings, 0 blocking.** |
| Every HTML class has a CSS rule; every `var()` resolves; no duplicate ids | `node scripts/check_style.mjs` | **PASSED — 29 pages, 1,612 class uses, 91 classes defined, 28 custom properties, 0 warnings.** |
| Independent audit build | `python3 counter-check/tools/check_site.py` | **PASSED** (unchanged by this pass; `counter-check/` is outside this session's scope). |
| No dead cross-references in the register | scan of every `FLG-nnn` / `SG-nn` mention in the built HTML against the ids that exist | **0 dead references.** |
| No duplicate element ids | scan over all 29 root pages | **0 pages with duplicates** (a duplicate pair found during the pass was removed — see FLG-059). |
| HTML structure | parse of all 29 pages for unclosed/mis-nested tags | **0 pages with structural problems.** |
| Stylesheet parses | `tinycss2` parse of `assets/style.css` | **228 rules, 10 at-rules, 0 errors, 1,848 declarations.** |
| No inline styles remain | `node scripts/check_style.mjs` rule 6 | **0 pages.** |

---

## 4. Defects found and repaired in this pass

| ID | Defect | Evidence | Fix | Verified by |
|---|---|---|---|---|
| FLG-052 | 44 CSS classes emitted with no rule; 9 undefined custom properties | class inventory of the built HTML vs `assets/style.css` | full design system rewrite; gate added | `check_style.mjs` = 0 failures |
| FLG-053 | 3 suggestion rows had malformed `class` attributes swallowing the badge and row text | regex scan for escaped quotes inside `class="…"` | corrected in the generator; gate now rejects the pattern | gate rule 4 |
| FLG-054 | Social card text overlapped the subtitle; two bar captions sat under the footer band | the committed `assets/og-image.png` was rendered and read | measured layout + two assertions in `make_og.py`; card regenerated | image read back after regeneration |
| FLG-055 | No reader route to submit a suggestion | page inventory: desk had owner paths only | GitHub-issue intake + honest count of 0 | count renders 0 from `data/reader-suggestions.json` |
| FLG-056 | Register ids FLG-023…FLG-031 are gaps | id scan of `flagged.html` | recorded as retired numbers, not renumbered | 0 dead references |
| FLG-058 | Disclosure not repeated inside each product card (strict FTC reading) | FTC S4 "placed with the endorsement message itself" | **not changed** — logged for the owner | this record |
| FLG-059 | Duplicate `id` attributes (`sg-export`, `sg-print`, `sg-reset`) introduced while adding a review panel | duplicate-id scan | the redundant panel was removed (the original one already had the buttons) | scan = 0 duplicates; gate now checks |

---

## 5. What this session did **not** do, stated plainly

- Did not log in to Associates Central. The **Special Link test** (FLG-001) and the short-link compliance question remain open and require the owner.
- Did not create a Search Console property. No search-volume, traffic or ranking claim is made anywhere.
- Did not re-read the five Amazon listings. Values are dated 2026-11-19.
- Did not change `counter-check/`, `docs/` or `articles/`. The three-builds-on-one-host question (FLG-039) stays an owner decision.
- Did not deploy a code change to GitHub Pages beyond the normal push-to-`main` build; deployment is confirmed from the Actions run and the Pages API, because this sandbox cannot fetch `github.io`.
