# Questions, information and answers — session 62786810, 2026-11-20

The working form of the Q/I/A register on `suggestions.html` (rows Q-33 to Q-37 are this
session's additions). It exists because "what should we do next?" cannot be answered until
it is clear which facts are in hand, which are missing, and who can obtain each missing fact.

Each row states four things: **the question**, **what we actually know with its source**,
**what is missing**, and **who can get it and how**. Nothing here is filled in by inference.
Where a fact is absent, the row says absent.

---

## A. The five questions this pass could not close

| # | Question | Known, with source | Missing | Who can get it, and how | What it blocks |
|---|---|---|---|---|---|
| A1 | Is a click on any of the five outbound links credited to `shopnow047c-20`? | All five buttons carry `tag=shopnow047c-20` on `/dp/` URLs built from the ASINs; the ASINs were re-checked against the listings today | A report row. No Associates data of any kind has been read by any session — no login exists here | **Owner only.** One click per product from a clean browser, then Reports → Tracking IDs the same day. Five clicks, ~10 minutes | Every statement about earning. **Not** a publishing blocker |
| A2 | What tolerances does the CHEF iQ Sense carry? | The listing (B0DZFD6R9Z) states 1000 °F heat safety, 3 probes, 4 internal + 1 ambient sensor, WiFi range, ~50 h per charge. It states **no** ± figure in the fields captured (FLG-071) | The tolerance figure; the manual is a linked PDF that was not opened | **Owner or next session.** Open the manual linked in the listing's Product guides section, or ask the seller through the listing | Any accuracy comparison between P4 and P5. The new guide reports the absence instead of filling it |
| A3 | Are the listings' dimensions the packed or unpacked dimensions? | Dimensions are quoted exactly as the listing states them, unit preserved. P4 shows `Item Length` 6.5 in and nothing else (FLG-072) | Packed vs unpacked, and whether width/height exist at all for the thermometers | **Nobody, from the listing.** A manufacturer spec sheet naming the same model code, or a physical unit | Counter-fit advice — the site's central promise. Until then every page says "as listed" |
| A4 | Which build under this hostname is the publication? | Root site: 20 sitemap URLs, self-canonical, `noindex` on its 7 internal surfaces (FLG-069). `docs/` and `counter-check/site/` are also served, with no `noindex` (FLG-070) | The owner's intent for those two | **Owner.** One sentence is enough; adding `noindex` is then a 10-minute change | A clean Search Console property, and any ranking statement |
| A5 | Who is accountable for the writing? | Every page names "The Countertop Guide editorial desk"; structured data types the author as an Organization; `about.html` says no individual is named (Q-33) | A name, a one-line credential, a real contact route | **Owner.** The build already reads the byline from one field in `data/editorial.json` | Trust signals only. Not a launch blocker |

---

## B. Questions this pass answered

| # | Question | Answer | Where the evidence is |
|---|---|---|---|
| B1 | Did the site ever load the typefaces its design names? | **No.** `assets/style.css` and `DESIGN_PROMPT.md` both specify Fraunces and Inter; there was no `@font-face` rule and no font file in the repository. Every visitor saw Georgia and the system UI font | FLG-067; fixed with four self-hosted woff2 files (182 KB) whose OFL 1.1 licences are committed beside them |
| B2 | Did any page tell the reader which section they were in? | **No.** The nav was byte-identical on all 30 pages with no `aria-current`, although the stylesheet already had a `[aria-current]` rule. Now generated per page from one link list | FLG-068 |
| B3 | Was the sitemap the shop or the audit? | **Both.** 26 URLs, 7 of them internal surfaces. Those 7 are now `noindex, follow` and out of the sitemap; 20 buying URLs remain, and `verification.html`, `flagged.html` and `compliance.html` stay indexed because a buyer checking a spec benefits from them | FLG-069 |
| B4 | Did the 2026-12-08 calendar topic ever ship? | It had not. It is now published as `guide-instant-read-vs-wireless.html` and moved in the calendar, the sitemap and the RSS feed in one commit, so the three cannot disagree | `data/editorial.json → cadence.queue`, `TOPICS`, `feed.xml` |
| B5 | Is the disclosure still the exact Operating Agreement sentence? | **Yes.** §5 fetched today, headed "Updated: October 15, 2025": "As an Amazon Associate I earn from qualifying purchases." The strip and footer match character for character, on all 30 pages | `review/62786810/VERIFICATION.md` §3; `check_meta.mjs` fails a page that drifts |
| B6 | Has the visual result been looked at? | **No.** Two browser installs failed in this environment. Structure is proven mechanically (`scripts/verify_structure.mjs`, 0 blocking, 0 warnings); taste is not | `review/62786810/VERIFICATION.md` §7 |

---

## C. The route to each missing fact, in the order that unblocks the most

1. **Search Console (A4 then A3's sibling question).** Settle which build is the publication,
   then verify the property and submit `sitemap.xml`. This is the cheapest item on the list
   and it converts the editorial calendar from a stated plan into a measurement.
2. **The Associates click test (A1).** Five clicks. It retires the oldest open flag on the
   site (FLG-001/FLG-015) and it is the only way any earning statement becomes possible.
3. **The CHEF iQ manual (A2).** Two minutes on the listing. It closes the one place where
   the site currently reports an absence in its main buying cluster.
4. **The byline decision (A5).** Cheap, and it changes how every page reads.
5. **Dimensions (A3).** Only a purchase or a spec sheet closes this, so it stays open. It is
   already disclosed everywhere the derived counter-space arithmetic appears.

Nothing in this list blocks the site being live. Each one blocks a specific sentence we are
currently not allowed to write.
