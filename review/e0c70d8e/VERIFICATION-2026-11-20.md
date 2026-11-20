# Line-by-line verification — session `arena/e0c70d8e-prod1`

**Date of this pass:** 2026-11-20
**Branch:** `arena/e0c70d8e-prod1`, branched from `3392c0d`, fast-forwarded to `bebe082` (PR #38) before any edit.
**What this pass changed:** guide structured data, per-guide social cards, one truncated sentence, the masthead's date label, two gates, and the records on `flagged.html` / `suggestions.html`.
**What this pass did not change:** `data/products.json`, any established figure, any price, any policy page's wording, and every file outside the root publication scope.

Every row below is something I opened and read in this session. Where I could not read a source, the row says so and the value stays blank on the site rather than inferred. Nothing in this document is carried as "verified" that was not fetched today.

---

## 1. Official policy sources

| # | Source (link for manual review) | What I read | Verdict against the site | Date read |
|---|---|---|---|---|
| P1 | [Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement) | Header states **"Updated: October 15, 2025"**. §5 *Identifying Yourself as an Associate*, verbatim: "As an Amazon Associate I earn from qualifying purchases." §6 makes a §5 violation a **material breach**. | The site's disclosure is **character-for-character identical** to the §5 sentence, appears under the masthead above the fold on every page, and repeats in the footer. No change needed. | 2026-11-20 |
| P2 | [Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies) | Header states **"Updated: April 14, 2026"**. Participation Requirements §2(b): "you must include your Associates ID or 'tag' (appearing as XXXXX-## …) as a parameter in the URL of each link you place on your Site to an Amazon Site." §2(b) also: "Your Site may only show prices and availability if: (a) we serve the link in which that price and availability data are displayed, or (b) you obtain Product pricing and availability data via Creators API or PA API…" | Outbound links carry `?tag=shopnow047c-20`, which matches the `XXXXX-##` shape. Prices are **not** displayed on shop pages — consistent with (a)/(b) being unavailable to a static build. | 2026-11-20 |
| P3 | [Same document](https://affiliate-program.amazon.com/help/operating/policies) — Participation Requirements §2(t) | "You will not display or otherwise use any of our customer reviews or star ratings, in part or in whole, on your Site unless you have obtained a link to that customer review or star rating through Creators API or PA API…" | Star ratings are not displayed on shop pages (`ratingsOnShopPages: false`). Unchanged by this pass; the underlying open item is FLG-023. | 2026-11-20 |
| P4 | [Same document](https://affiliate-program.amazon.com/help/operating/policies) — Participation Requirements §3(e) | Requires disclosing "the use of cookies, pixels, and other technologies by you and third parties" through a privacy policy or otherwise. | The site uses no cookies, pixels or third-party scripts (`assets/app.js` has no network call while `events.endpoint` is empty). `about.html` and `methodology.html` say so. Unchanged. | 2026-11-20 |
| P5 | [Same document](https://affiliate-program.amazon.com/help/operating/policies) — Commission Income Statement §2(d) and §2(e) | Purchases referred "by a link that is generated or displayed on a search engine" (2(d)) and via a "Redirecting Link" (2(e)) are **disqualified**, not merely discouraged. | Relevant to the five submitted `link.amazon` short links: they are redirect-style. This is **not** a conclusion that they are non-compliant — see FLG-003, which stays open. The site's own outbound links go directly to `https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20`, so §2(d)/2(e) does not touch the links this site builds. | 2026-11-20 |

**Not re-read this session, and therefore not restated as verified today:** FTC *Disclosures 101 for Social Media Influencers*. The compliance page's FTC claims keep their 2026-11-19 provenance exactly as recorded in `COORDINATION.md`. I did not want a policy page to acquire a fresher date than its evidence.

---

## 2. Search-engine documentation this pass actually depended on

| # | Source (link for manual review) | What I read | How it changed the build | Date read |
|---|---|---|---|---|
| G1 | [Google Search Central — Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article) | Page states **"Last updated 2026-09-08 UTC"**. Article objects must be `Article`, `NewsArticle` or `BlogPosting`. Recommended properties: `author` (Person or Organization), `author.name`, `author.url`, `dateModified`, `datePublished`, `headline`, `image`. It says explicitly: *"There are no required properties; instead, add the properties that apply to your content."* Author guidance also says to use `type` and `url`/`sameAs` where possible. | The generator was emitting `Article` on **one** guide only, and that one lacked `image` and `mainEntityOfPage`. Now all ten published guides emit: `headline`, `url`, `mainEntityOfPage`, `datePublished`, `dateModified`, `inLanguage`, `author` (Organization + `url` to `about.html`), `publisher`, `image` (the guide's own 1200×630 card), `isPartOf`, `description`. | 2026-11-20 |
| G2 | [Google Search Central — Changes to HowTo and FAQ rich results](https://developers.google.com/search/blog/2023/08/howto-faq-changes) | Published **Tuesday, August 8, 2023**. States FAQ rich results "will only be shown for well-known, authoritative government and health websites. For all other sites, this rich result will no longer be shown regularly." Also: *"Structured data that's not being used does not cause problems for Search."* | Directly resolves the **open** question recorded on `flagged.html#FLG-036`, which had been written from secondary reporting because no official page had been read. The answer: keep the `FAQPage` blocks, remove any implication they earn a rich result. The site already sells nothing on FAQ rich results; FLG-036 is now **closed with an official citation** rather than left as hearsay. | 2026-11-20 |
| G3 | [Google Search Central — Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) | "Google uses the `<lastmod>` value if it's consistently and verifiably (for example by comparing to the last modification of the page) accurate." Also: use fully-qualified absolute URLs; list the canonical URLs you want shown; `priority`/`changefreq` are ignored. | Fixes the value stamped as `Article.dateModified`: it is now the build's content date, the **same** field the sitemap uses for `<lastmod>`, so the two signals cannot disagree about the same page. `datePublished` is the commit that first added the page, not the build date — a guide first published on the 19th no longer claims to have been published on the 20th. | 2026-11-20 |
| G4 | [Schema.org — Article](https://schema.org/Article) | Defines the `Article` type and its `image` / `mainEntityOfPage` properties in the vocabulary Google's guidance relies on. | Reference only; no claim beyond G1. | 2026-11-20 |

**What I deliberately did not claim.** G1 is explicit that Google *does not guarantee* rich results even for fully valid markup. So the site says the markup is present and describes the page; it does not say it wins anything. That distinction is the whole point of FLG-036 and it is not going to be lost again.

---

## 3. The five submitted products, against their own listings

Five listings opened today. Identification fields only — I did **not** re-score price or rating into the register, because those are volatile and the site does not publish them (`display.pricesOnShopPages: false`).

| Product | Intended ASIN | Listing opened | Title as served today | Identification verdict |
|---|---|---|---|---|
| P1 Chefman 6QT Dual-Basket | `B0CDY277D3` | [amazon.com/dp/B0CDY277D3](https://www.amazon.com/dp/B0CDY277D3) | "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black" | **Matches the register.** Brand, capacity (6 QT / 2×3 QT) and form all agree. |
| P2 Emeril Lagasse 26QT French-Door | `B09B7SB46R` | [amazon.com/dp/B09B7SB46R](https://www.amazon.com/dp/B09B7SB46R) | "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven \| Countertop Convection Cooker, 24 One-Touch Preset Options, Extra Large Interior, Six Cooking Accessories Included" | **Matches.** Note the register records *25 presets* in some prose; today's title says *24 One-Touch Preset Options*. **Not resolved here** — this is a listing-side number that the site quotes only as "per listing". Logged below as an irregularity, not silently changed. |
| P3 Chefman 8QT TurboFry | `B08DKYBTPH` | [amazon.com/dp/B08DKYBTPH](https://www.amazon.com/dp/B08DKYBTPH) | "Chefman Air Fryer 8 Qt \| TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results \| Bake, Dehydrate, Frozen \| XL Nonstick Dishwasher-Safe Basket \| Stainless Steel" | **Matches.** The 450°F Hi-Fry in the title against the 200–400°F bullets is already published as FLG-022; today's title still says 450°F. |
| P4 ThermoMaven 1-Sec Instant-Read | `B0DHZTCNR5` | [amazon.com/dp/B0DHZTCNR5](https://www.amazon.com/dp/B0DHZTCNR5) | "ThermoMaven 1 Sec Professional Digital Meat Thermometer, ±0.5℉ Accuracy \| NIST&NSF Certified, Auto-Rotate Bright LED Screen, IP67 Waterproof for Grill BBQ, Stocking Stuffers Gifts for Men, Black" | **Matches.** ±0.5°F and the NIST/NSF claim the site quotes are in the title. Dimensions still absent from the listing fields → stays blank (FLG-004). |
| P5 CHEF iQ Sense Wireless (3 probes) | `B0DZFD6R9Z` | [amazon.com/dp/B0DZFD6R9Z](https://www.amazon.com/dp/B0DZFD6R9Z) | "CHEF iQ Sense \| Smart Wireless Meat Thermometer \| 3 Ultra-Thin Probes \| WiFi Unlimited Range \| 1000°F Heat Safe \| 5 Sensors \| BBQ, Grill, Oven, Smoker, Air Fryer \| Gen3" | **Matches.** 3 probes and 5 sensors agree with the register. No ±°F tolerance figure appears → stays blank (Q-36/FLG-071). |

All five sit in the expected Amazon categories (Air Fryers `node=17659096011`; Meat Thermometers `node=289810`), which I read off the breadcrumb on each page.

**One field I could not confirm, so it stays blank:** packed versus unpacked dimensions for all five. The listings give one dimension triple with no indication of which it is. `FLG-073` already records that the data cannot distinguish "not captured" from "not applicable"; this pass adds nothing to that and does not pretend otherwise.

---

## 4. Defects found by reading, and what now stops them recurring

These are the reason this pass exists. Each was found by opening the published output, not by a gate — and each now has one.

| Defect | How it was found | Blast radius | Gate added |
|---|---|---|---|
| Ten of thirteen guides emitted no `Article` node | Parsed the JSON-LD on every generated page | Every guide was unidentifiable as an article | `check_meta.mjs` §8 — a published guide without `Article`, or with a missing `author`/`publisher`/`image`/dates/`mainEntityOfPage`/`url`, fails the build |
| `Article` on the one page that had it lacked `image` and `mainEntityOfPage` | Same parse | That page's markup was incomplete against G1 | Same §8 |
| All thirty pages shared one `og:image` | Compared `og:image` across pages | No share preview described the page it linked to | §8 fails when `og:image` and `Article.image` disagree, or when the named file is not in the repo |
| The product card's sentence ended at "…the button shows today's" | Read the live front page | Five pages, five times each | §9 — a sentence ending on a determiner, preposition, possessive or objectless transitive verb fails the build |
| The masthead labelled the page date as if it were the read date | Read the live issue bar | Thirty pages | Not gated; it is now two named dates, and the evidence date is the one the cards quote |

**The gate is only worth what it catches, so I planted the defects and re-ran it:**

1. Disabled the `Article` branch in the generator → 10 `FAIL` lines, one per published guide. Build blocked.
2. Restored the truncated price sentence verbatim → 13 `FAIL` lines across the shop pages. Build blocked.
3. Pointed `Article.image` at a card that does not exist → 10 `FAIL` lines. Build blocked.
4. Restored the correct tree → `0 warning(s), no blocking items`.

Test 2 initially passed, which was itself a defect: my first pattern looked for a literal `’` while the generator emits `&rsquo;`. The detector now decodes entities before matching, and the three-tell version (determiner / possessive / objectless verb) was tuned until it fired on the broken copy and stayed quiet on all 19 reader pages of the correct copy. A check that has never been seen to fail is not a check.

---

## 5. Irregularities logged rather than fixed

| Ref | What | Why it is not fixed here |
|---|---|---|
| FLG-088 | Ten guides had no `Article` markup; the one that did was incomplete | **Fixed and gated** in this pass. Recorded because the *class* of defect — valid HTML, present strings, no meaning — is the one this repo keeps producing. |
| FLG-089 | One shared social card for every page | **Fixed and gated.** Ten cards drawn from each guide's own title and description. |
| FLG-090 | Truncated sentence on the product card | **Fixed and gated.** |
| FLG-091 | Masthead printed the page date where the evidence date belongs | **Fixed.** Two fields, two labels. |
| P2 preset count (24 in today's title vs 25 recorded) | Listing-side change | The register's number is dated 2026-11-20 from an earlier read. I will not overwrite a dated observation from a different read without re-reading the field it came from; recorded here for the register's owner. |
| FLG-003 | Compliance status of the five `link.amazon` short links | **Unresolved and left unresolved.** Nothing in this pass tests it. The brief is explicit: do not claim the short links are invalid. P5 above is the closest the documentation comes, and it is about *disqualified purchases*, not about the links being forbidden. |
| FLG-001 / SG-53 | No Special Link click has ever been confirmed as attributed | Needs an Associates Central login. Cannot be closed from this sandbox. |
| FLG-004 / FLG-071 / Q-36 | Thermometer dimensions and the CHEF iQ tolerance figure are not on the listings | Leave blank. Never infer. |
| FLG-023 | Price/star display versus Participation Requirements §2 | Clause re-confirmed verbatim today (P2, P3). The site's choice — display neither — already satisfies it. Owner ratification still open. |
| FLG-039 / FLG-070 | Three builds on one host | Outside this session's scope. The open PR #37 carries the `robots.txt` half. |

---

## 6. Reproducing this pass

```
python3 build_site.py                    # 30 pages, 20 sitemap URLs, 4 consolidated
python3 scripts/make_og.py               # site card   -> assets/og-image.png
python3 scripts/make_og.py --cards       # 10 cards    -> assets/cards/*.png
node scripts/check_site.mjs              # 55 HTML files
node scripts/check_meta.mjs              # includes the new §8 and §9 checks
node scripts/check_style.mjs
node scripts/verify_structure.mjs
python3 counter-check/tools/check_site.py
```

All six pass on this branch. The rebuild is deterministic: a second `python3 build_site.py` produces no diff.

**Limits of this pass, stated plainly.** I read the pages; I did not *look* at them. No browser could be installed here in earlier sessions and none was attempted here. Structure, markup and prose are proven; layout and typography are not. The ten new cards I did look at as images, and two of them are reproduced against the risk that clipped them — the longest title wraps to three lines inside the safe area.

— session `arena/e0c70d8e-prod1`

---

## 7. Merge and renumbering (2026-11-20, after PR #44/#49/#51 landed)

`main` advanced four times while this branch was open. Rebasing onto `3e86d23` produced a genuine
collision of the kind the board warns about: **two sessions inventing the same numbers.** Main's
`FLG-074…081`, `SG-54…57` and `Q-38…41` are already published, so this pass moved its rows to
**FLG-088…087, SG-61/SG-62, Q-45** and left every one of main's records untouched. Caught by
`check_style.mjs`'s duplicate-id rule, which is exactly the gate that should catch it.

Two things worth recording rather than hiding:

- **A rebase pushed main's build into a failing state under my hands.** `build_site.py` refuses to
  write `decisions.html` while any board row is untriaged, and three of my new rows were. Main's own
  triage list already covered its rows; mine did not. SG-61, SG-62 and Q-45 are now triaged into the
  *Findability and one canonical site* theme, and the build is green again.
- **I very nearly rewrote another session's flags.** A bulk ID renumber briefly relabelled five of
  main's rows before I restored them verbatim from `3e86d23`. Every flag row is now verified to have
  `id` equal to its visible label, and no ID appears twice. The lesson is in the method: renumber by
  matching the row's *text*, never by a range substitution.

The prose gate I added (FLG-090) also had to survive a merge: main had independently repaired the
same truncated sentence I did, with better wording. Theirs is kept; my sentence is discarded. The
gate stays, because the gate is the part that stops it happening a third time.
