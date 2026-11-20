# Decision worksheet — what we know, what we do not, and what would settle it

Written 2026-11-20 for the owner of The Countertop Guide. It exists because the site has
accumulated a large register of suggestions (SG), questions (Q) and flags (FLG) across
several sessions, and a reader cannot tell from that pile *which* items actually change the
site and which merely tidy it.

This file is the short version: **eighteen decisions, grouped by what they unlock**, each one
stating four things —

1. **Question** — the decision in one line.
2. **What we know** — the evidence already in the repository or read from an official source.
3. **What we do not know** — the missing fact, stated as a gap rather than a guess.
4. **What would settle it** — the smallest real action that produces the missing fact, with
   who can do it.

Nothing here is implemented. Every row is a proposal until a reviewer marks it. The live
board is `suggestions.html`; the numbered registers are `S`=suggestion, `Q`=question,
`FLG`=irregularity.

---

## A. Decisions that change whether the site can earn anything

These four gate revenue. Everything else in this file is polish compared with them.

### A1. Is the Associates account actually earning on these links? — `SG-01`, `FLG-001`, `FLG-015`

- **Question.** Do the five links in the enrolled Associates account carry the tracking ID and
  register clicks in the Associates reports?
- **What we know.** Every outbound link on the site is
  `https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20` with `rel="sponsored nofollow
  noopener"`, and the build fails if a link to an Amazon host is missing the sponsored
  marking. The five ASINs all resolve to live listings whose titles match the register (see
  `review/3c99f15c/VERIFICATION.md`). That is a *destination* check.
- **What we do not know.** Whether a click registers in the Associates tracking report, and
  whether the account is approved for the `shopnow047c-20` tracking ID. Both live behind the
  Associates Central login. **No automated check can substitute.** The site currently makes
  no claim about this either way.
- **What would settle it.** One person, signed in to Associates Central: click one link per
  product from the live site, then open Reports → Tracking ID and confirm the clicks appear
  against `shopnow047c-20`. Record the date and the report screenshot reference in
  `COORDINATION.md`. Requires: Associates login. Cost: fifteen minutes.
- **Why it is first.** If the tag is wrong, every other hour spent on this site earns
  nothing, and nothing on the site would show the error.

### A2. Are the supplied short links acceptable to use? — `FLG-003`

- **Question.** Do the `link.amazon/…` short links comply with the Operating Agreement, or
  must they be replaced with full `amazon.com/dp/ASIN?tag=` links?
- **What we know.** The build already uses **full links with the tag on every page**. The
  short links appear only in the verification record, as the submitted artefact. So the
  reader-facing site does not depend on the answer.
- **What we do not know.** Their compliance status. It is unresolved, not proven invalid. The
  register must not claim either.
- **What would settle it.** Read the Operating Agreement's link-format section against the
  link, or ask Associates support for a written answer. Until then, keep the full links —
  which is what the site does — and keep the status "unresolved".

### A3. Where do the analytics events actually go? — `SG-03`, `FLG-008`

- **Question.** Host the self-hosted analytics endpoint, or drop measurement?
- **What we know.** `analytics-endpoint/server.py` is written, standard-library only, and
  contract-tested by `analytics-endpoint/selftest.py`, which runs inside the deploy gate. It
  accepts exactly five events (`page_view`, `outbound_click`, `search`, `chooser_complete`,
  `guide_read`), stores no client address, no user agent, no referrer, no cookie, and no
  query text. The site transmits **nothing** today because
  `body[data-analytics-endpoint]` is empty by design.
- **What we do not know.** Whether the owner will pay for and operate a host, and which one.
  This is a cost and maintenance decision, not an engineering one.
- **What would settle it.** A yes/no on hosting. If yes: deploy the endpoint, set
  `events.endpoint` in `data/editorial.json`, rebuild. If no: the browser-local counter stays,
  and the site keeps saying plainly that it measures nothing server-side.
- **Consequence of "no" being chosen.** No outbound-click data, therefore no evidence-based
  topic choice, therefore the topic calendar stays a stated plan. That is an honest
  position, but it should be chosen deliberately rather than by silence.

### A4. Does the site need a domain of its own? — `SG-02`, `Q-02`, `FLG-007`

- **Question.** Keep `https://wingbangboozle1-lang.github.io/Prod1/` as the canonical, or buy
  a domain?
- **What we know.** Every page self-canonicalises to its own absolute GitHub Pages URL, the
  sitemap lists exactly those URLs, and the feed and `og:image` use the same base. The build
  reads the base from one field, so a domain change is one edit plus a rebuild.
- **What we do not know.** Whether the owner wants the brand name in the URL badly enough to
  pay for and maintain a domain and its DNS.
- **What would settle it.** A yes/no. If yes: buy the domain, add a `CNAME`, set
  `baseUrl` in `data/editorial.json`, rebuild, and add the Search Console property.
- **Note.** Search Console verification is usually easier on a domain you own, which links
  this row to A5.

### A5. Is the site measurable in search? — `SG-27`…`SG-30`, `FLG-032`

- **Question.** Add a Search Console property so queries are visible?
- **What we know.** `sitemap.xml` (24 URLs) and `robots.txt` (declares the sitemap, keeps the
  three parallel builds out of the index) are generated and served. Every page has a unique
  title, a unique description, a self-referencing canonical and Open Graph tags. The RSS feed
  is valid RSS 2.0.
- **What we do not know.** Any actual query, impression or click figure. **None exists.** No
  page on this site claims a traffic number, a ranking or a search volume, and none should
  until this is done.
- **What would settle it.** Verify the property (DNS or HTML file), submit the sitemap, then
  export *Queries* after 28 days. That export is the input to the topic queue
  (`topics.html`) — replacing the current editorial hypotheses with measured ones.
- **Cost.** Free. Requires: a Google account and access to verify the property.

---

## B. Decisions that change what the site looks like

### B1. Which visual direction, and does the shelf settle it? — `SG-11`, `Q-21`, `Q-12`, `DI-1`…`DI-8`

- **Question.** Choose one design direction and delete the other brief, or keep both?
- **What we know.** Two design briefs exist (`DESIGN_PROMPT.md` and
  `design-brief.html` — also linked from `suggestions.html`). They overlap. The live site
  now implements one concrete thing: the warm cream / espresso / terracotta editorial
  palette with Fraunces display type and Inter body type, self-hosted, and the new
  front-page shelf (one card per product: capacity, counter depth, one reason, one caution,
  two bullets, one buy button). That is a real direction, already shipped and gated
  (`scripts/check_style.mjs` fails the build if a class has no rule).
- **What we do not know.** Whether the owner likes it. The gate can prove coverage; it
  cannot prove taste.
- **What would settle it.** Look at the live front page on a phone and on a desktop. Then
  either (a) accept the current direction and delete the losing brief, or (b) name the
  direction that replaces it. **Running both is the one option that guarantees the site
  looks generated.**

### B2. Product photography — licence, or keep drawings? — `SG-04`, `FLG-009`, `FLG-079`

- **Question.** Buy/licence photography, shoot it, or keep the current SVG drawings?
- **What we know.** Amazon's Program Content — including product images — is licensed to the
  Associates programme, not owned by us, and may not simply be copied onto the site. The
  site therefore ships **original SVG artwork only**: a stylised appliance drawing plus a
  to-scale counter-footprint diagram generated from the listing's own dimensions (with a
  12 × 12 in reference square, at one scale for all products so cards are comparable by
  eye). Each is labelled "our drawing … not a photograph".
- **What we do not know.** Whether the owner will fund original photography or a licence.
  Without that, images stay drawings.
- **What would settle it.** A yes/no plus a budget. If no photography: keep drawings and say
  so — they are honest, they cannot go stale, and they are the reason the cards look
  intentional rather than broken. If yes: real, consistently-lit kitchen photography, shot
  by the owner, with no implication of a hands-on test unless `SG-09` (a funded testing
  protocol) exists.
- **Do not** fill this gap with scraped listing images. That is the one option that turns a
  compliance problem into a termination risk.

### B3. Who is the author? — `SG-26`, `Q-33`

- **Question.** Publish under an editorial-desk byline, or name a real person with a bio?
- **What we know.** Every page currently names "The Countertop Guide editorial desk", and the
  structured data types the author as an Organisation. `about.html` states outright that no
  individual has a credential that can be shown, so none is invented. Articles carry
  `Article` structured data with `datePublished` and `dateModified`.
- **What we do not know.** Whether there is a real person willing to be the named author,
  and what their one-line credential is.
- **What would settle it.** A name plus one sentence of relevant experience plus a contact
  route. It is a single field in `data/editorial.json`; the build already reads it.

---

## C. Decisions that change what the site says

### C1. May shop pages display price and rating after all? — `SG-19`, `SG-20`, `FLG-023`, `FLG-032`

- **Question.** Keep prices and ratings off the shelf, or bring them back with a refresh
  mechanism?
- **What we know.** Amazon's Program Policies allow a site to show price and availability
  only when Amazon serves that data on the link, or when it comes from the Creators/PA API
  and is cached no longer than 24 hours. This site is a static build with no API refresh at
  publish time, so it displays **no** price, rating, rating count or badge on any
  reader-facing page. What it shows instead is a button that says "see today's price on
  Amazon", marked sponsored, and a dated observation in the verification register.
- **What we do not know.** Whether the owner has — or can get — Creators API eligibility and
  a refresh job. `FLG-026` records that eligibility was not read from Amazon.
- **What would settle it.** Confirm API eligibility in Associates Central. If eligible:
  build the refresh job, then turn on live figures. If not: the current link-only approach
  stays, and it is the compliant one.
- **Note.** A price on the page is the single biggest conversion lever a shop page has. The
  reason it is off is a policy constraint, not a design preference — so this is the row with
  the largest revenue upside in the whole file.

### C2. Which topics, chosen how? — `SG-32`, `FLG-078`, `FLG-085`

- **Question.** Keep publishing on editorial judgement, or wait for measured queries?
- **What we know.** Fifteen question-shaped topics are on the calendar: twelve published, three
  queued. This pass made those counts derive from the data after they had drifted out of step
  with the table that lists them (`FLG-085`). Nothing on the site claims any topic is popular
  or in demand.
- **What we do not know.** Which questions people actually type. That requires A5.
- **What would settle it.** Search Console queries after 28 days (A5), plus the analytics
  events from A3. Then the next four topics are chosen from what people searched for and did
  not find, not from instinct.
- **Interim rule the site already follows.** A new topic is published only if the guide can
  be built entirely from verified listing fields, is added to `sitemap.xml` and `feed.xml` at
  publish time, and does not restate an existing page.

### C3. Hands-on testing — ever? — `SG-09`

- **Question.** Fund a testing programme, or stay a spec-and-listing publication permanently?
- **What we know.** No page claims hands-on use. `about.html` has a table of "what we do not
  claim" and says plainly that nobody here has cooked in these machines. This is currently a
  *strength*: it is verifiable, and it is the opposite of the "we tested 12 air fryers" claim
  that competing pages make without evidence.
- **What we do not know.** Budget, and whether the owner wants to own that work.
- **What would settle it.** A budget and a written protocol — how many units, what measured,
  what photographed, how recorded. Until then the honest voice stays, and no guide should
  drift into testing language.

---

## D. Decisions that unblock the machinery

### D1. Which GitHub Pages build is the site? — `SG-51`, `Q-34`, `FLG-070`, `FLG-051`

- **Question.** Three builds are reachable on one host: the root publication, `docs/`, and
  `counter-check/site/`. Which is the site?
- **What we know.** The root publication is the only build with a sitemap, self-canonical
  URLs, noindex on its internal surfaces and a five-gate deploy pipeline. `robots.txt`
  disallows `/counter-check/`, `/docs/`, `/articles/`, `/review/` and `/analytics-endpoint/`,
  so search engines see one site even though files for the others still exist. The Pages
  build source is **legacy** (`main` branch, root directory), which is why the root files are
  the site and why the `deploy-pages` step is skipped rather than run.
- **What we do not know.** Whether the owner wants the other two builds kept at all.
- **What would settle it.** Either set Pages → Build source to **GitHub Actions** (then the
  gate blocks a bad publish outright, and the red-X-on-main ambiguity disappears), or keep
  legacy mode and accept that gates run on push rather than on publish. Separately: delete or
  relocate `docs/` and `counter-check/site/`.
- **Recommendation.** Switch to GitHub Actions build source. The workflow already supports
  it; today a gate failure is a red X rather than a blocked deploy.

### D2. Should the site keep the FAQ structured data? — `FLG-025`

- **Question.** Keep `FAQPage` structured data on guides, or remove it?
- **What we know.** It is emitted on guides that have a "Questions readers ask" block, and
  the questions are answered in the visible text — which is what Google's guidance requires.
- **What we do not know.** Whether it earns rich results for this site. Google has narrowed
  when FAQ rich results are shown.
- **What would settle it.** Search Console → Enhancements after 28 days (needs A5). Keep it
  until there is evidence it is inert; it is not a policy risk, it is a "does it help"
  question.

### D3. What is the review cadence for this board? — `Q-14`, `FLG-080`

- **Question.** Does a decision left unanswered for 28 days get its recommended default
  applied, or does it wait indefinitely?
- **What we know.** `data/decisions.json` proposes a 28-day default rule, marked as a
  proposal. Today nothing auto-applies: a silent board is still a silent board.
- **What we do not know.** Whether the owner wants defaults applied without them.
- **What would settle it.** Approve, amend or reject the rule. If rejected, the board needs
  another mechanism or the open items simply accumulate.

### D4. Register hygiene — `Q-02`, `Q-14`, `SG-33`, `SG-43`

- **Question.** Four register rows sit in two decision themes at once (`Q-02`, `Q-14`,
  `SG-33`, `SG-43`). Merge or separate them?
- **What we know.** The build does not enforce uniqueness, so a row appearing twice is
  currently allowed and is reported on `flagged.html` rather than silently fixed.
- **What would settle it.** A rule (one row, one theme) applied by the register owner.

---

## E. The information we simply do not have — a shopping list

The fastest way to unblock the rows above. Each line is one action, one owner, and what it
unlocks.

| # | Missing fact | How to obtain it | Unlocks |
|---|---|---|---|
| 1 | Do clicks register against `shopnow047c-20`? | Associates Central → Reports, after one click per product | A1, and the whole revenue question |
| 2 | Is the account approved for that tracking ID? | Associates Central → Account settings | A1 |
| 3 | Short-link compliance status | Associates support, written answer | A2 |
| 4 | Creators/PA API eligibility | Associates Central → Tools | C1 (largest conversion upside) |
| 5 | Which queries arrive, if any | Search Console after 28 days | A5, C2 |
| 6 | Which pages convert | Analytics endpoint hosted + a month of events | A3, C2 |
| 7 | Will the owner fund a host? | Owner decision | A3 |
| 8 | Will the owner fund photography / a domain / testing? | Owner budget decision | B2, A4, C3 |
| 9 | Who is the named author? | Owner supplies a name and one-line credential | B3 |
| 10 | Which visual brief wins? | Owner reviews the live front page | B1 |
| 11 | Existing brand assets, if any | Owner: logo, colours, fonts already in use | B1 |
| 12 | Are the two thermometer dimension sets obtainable? | Manufacturer manual linked from each listing | `FLG-004`, `FLG-072` |
| 13 | Emeril warranty term | The warranty PDF linked from the P2 listing | `FLG-005` |
| 14 | Actual sell-through / commission rate | Associates reports (first-party only) | The campaign ledger, currently empty by design |

## F. Suggestions for discovering what we are missing

The list above is finite because the questions are known. Unknown unknowns are the real risk,
and they are usually found by watching readers rather than by asking ourselves. Five
low-cost instruments, in order of value per hour:

1. **Read the query report out loud, monthly.** Every phrase that arrives and is *not*
   answered by an existing page is a topic. This is the only instrument that tells you what
   people want instead of what you assume.
2. **Watch the chooser exits.** The three-question chooser logs `chooser_complete`. If people
   start it and abandon it, the questions are wrong, not the products.
3. **Count outbound clicks per product.** The ledger starts empty. The first real
   `outbound_click` numbers tell you which of the five actually gets chosen — that is the
   product the site should lead with, and it may not be the one it leads with today.
4. **Ask one reader a month what they were trying to decide.** A single sentence from a real
   person beats a survey. The site already invites topic suggestions without collecting
   anything silently.
5. **Read the flagged page as a stranger.** Every open flag is a place where the site knows
   less than it appears to. A flag that has been open for months is either a decision nobody
   made or a question nobody needed — both worth knowing.

## G. What this session actually changed

For the record, so this worksheet is not mistaken for a plan that was executed:

- Front page rebuilt as a **shelf**: one card per product, no duplicated spec dumps
  (`FLG-086`).
- Topic calendar counts derived from the data they describe (`FLG-085`), after they had
  drifted to "twelve … five published" against a table of fifteen rows.
- Five product titles re-read against Amazon and confirmed; scope of the re-read recorded
  (`FLG-087`, and the verification record).

Nothing in sections A–D was implemented. Each needs the owner.
