# Questions, information and answers — what has to be settled before a decision can be made

This file is the working form of the Q/I/A register published on
[`suggestions.html`](https://wingbangboozle1-lang.github.io/Prod1/suggestions.html).
It exists because "what should we do next?" cannot be answered until it is clear which
facts are in hand, which are missing, and who can obtain each missing fact.

Written 2026-11-20. Every "known" row links to where the evidence lives. Every "missing"
row names the route to obtain it. Nothing here is filled in by inference.

---

## A. The seven questions that actually block a decision

| # | The decision cannot be made until… | Known today | Missing | Who can get it | Route |
|---|---|---|---|---|---|
| A1 | …we know the tagged links are credited to **shopnow047c-20** | Outbound format is `https://www.amazon.com/dp/ASIN?tag=shopnow047c-20` on all five products; the supplied `link.amazon` short links carry **no** `tag=` parameter (FLG-015) | Whether a click on our tagged link appears in the Associates tracking report, per product | **Owner** — requires an Associates Central login | Click one link per product from a clean browser; open Reports → Tracking IDs; record the date and the result. Screenshot optional; a dated note is enough |
| A2 | …we know whether the supplied short links are compliant Special Links | Their redirects resolve to the five ASINs (2026-11-20, `review/1187e20d`) but carry no tag (FLG-015); their exact status is unresolved (**FLG-001**) | An authoritative answer from Amazon, or the owner's written decision to stop using them | **Owner** (+ Amazon Associates support if a written answer is wanted) | We do not use them as buttons today, so this is a records question, not a live risk. Either retire them in the register or ask support for a ruling |
| A3 | …we have measured search demand | Nothing. No Search Console property, no query data, no volume estimate anywhere on the site | Property verification; 28 days of queries | **Owner** — needs the GitHub/host account | Settings → Pages → confirm the canonical host → Search Console → add property → verify → submit `sitemap.xml` |
| A4 | …we know where analytics may send data | Five privacy-preserving events are defined and fire into `localStorage` only; the endpoint is unset (`data/editorial.json → events.endpoint`), so nothing leaves the browser (**FLG-008**) | A host, a retention period, and a privacy note | **Owner** | Either host `analytics-endpoint/server.py` somewhere that accepts POSTs, or keep the site local-only and say so (it does say so) |
| A5 | …we know what imagery we may use | No product photography anywhere; the only image is our own drawn card (**FLG-041**) | A licence (own photos) or manufacturer permission | **Owner** | Cheapest: photograph the products yourself if you own them. Otherwise request permission in writing and keep the reply |
| A6 | …we know who is accountable for the writing | The byline is the desk, not a person; the site says so on `about.html` and in every article's structured data | A named author with a real bio and contact route, or a deliberate decision to stay anonymous | **Owner** | Decide; if named, add the bio page and the `author` field in `data/editorial.json` |
| A7 | …we know whether a failed check can block a release | The workflow gates every push, but Pages publishes from the branch, so a green check is not a gate on the live site (**FLG-051**) | One settings change | **Owner** | Settings → Pages → Build source → GitHub Actions. Then a failing gate blocks the publish instead of merely marking the commit red |

---

## B. Questions about the product register — answered, with the limits stated

| # | Question | Answer | Evidence | Limit |
|---|---|---|---|---|
| B1 | Which products are being promoted? | Five ASINs: B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z | `data/products.json`; `verification.html` | — |
| B2 | How did each short link resolve? | To the five ASINs above, with no `tag=` on the redirect | `review/1187e20d/VERIFICATION-2026-11-20.md` | A redirect is not proof of the submitter's intent — hence the separate intended-ASIN field, which is blank (**FLG-045**) |
| B3 | Are the listed dimensions and capacities trustworthy? | They are quoted from each listing, dated 2026-11-19, with the listing linked per row | `verification.html` | Not re-read on 2026-11-20 by this session. Treat the page date as the shelf life |
| B4 | Where the listing contradicts itself, what is shown? | Both values, side by side, with a flag — never a silent pick | FLG-002 (presets/capacity), FLG-021 (accessory count), FLG-022 (Chefman 8QT wattage) | This is a deliberate choice: a resolved guess would be worse than a visible conflict |
| B5 | Why are there no prices or star ratings on the shop pages? | Amazon's Program Policies allow price/availability only where Amazon serves the link or the data comes via the Creators/PA API within a 24-hour cache; a static build does neither | FLG-032; policy re-read 2026-11-20 in `review/1035d1e2/VERIFICATION.md` | Whether a *dated* figure belongs even in the audit register is an open interpretation (**FLG-033**) |
| B6 | What is genuinely missing from the data? | Thermometer dimensions (both), the Emeril warranty term, the CHEF iQ accuracy figure | FLG-004, FLG-005 | All four are blank on the pages rather than guessed |

---

## C. Information that does not exist yet, and cannot be manufactured

These are the numbers a pitch deck would normally invent. They are listed here so nobody
mistakes their absence for an oversight.

| # | Thing | Why it is absent | What would produce it |
|---|---|---|---|
| C1 | Search volume for any topic | Never measured; the topic calendar is labelled a set of editorial hypotheses | Search Console query data after A3 |
| C2 | Traffic, click-through rate, conversion rate | No analytics endpoint is hosted (A4) | Hosted endpoint + time |
| C3 | Commission earned | No authorised first-party report has been recorded | Associates reports, entered in the campaign ledger with a date |
| C4 | Which product "converts best" | Same as C3 — and it would be a claim from measurement, not from reading listings | C3 over several weeks |
| C5 | Whether the copy improves sales | No A/B test has run and none can run without traffic | Traffic + a test plan |
| C6 | Rank positions | No Search Console property | A3 |

The campaign ledger on `methodology.html` is deliberately empty. An empty ledger with a
schema is honest; a filled one with invented numbers is the thing this project is trying
not to be.

---

## D. Decisions already taken (so they are not relitigated by accident)

| Decision | What was chosen | Where it is recorded |
|---|---|---|
| Disclosure wording | The Operating Agreement's exact sentence, every page, above the fold and in the footer | `data/products.json → site.disclosure`; FLG-042 |
| Prices on shop pages | Off. Buttons carry the price action; the register keeps dated observations | `data/editorial.json → display`; FLG-032 |
| Outbound link marking | `rel="sponsored nofollow noopener"`, visible label, `target="_blank"`, including script-built links | `compliance.html`; gate rule 2 |
| Duplicate seasonal guides | Three near-duplicate pages consolidated into three survivors, with the older URLs kept live, self-explained, excluded from the sitemap and canonicalised to the survivor | FLG-047 |
| Register numbering | Gaps (FLG-023…031) are retired numbers, not missing rows; nothing is renumbered retroactively | FLG-056 |
| Reader suggestions | Public GitHub issue with the `reader-suggestion` label; the count on the desk reads from data and is 0 | FLG-055 |

---

## E. How to answer A1 and A3 in fifteen minutes

The two decisions that unlock the most are also the two that need nothing from this
repository.

**A1 — the Special Link test.**
1. Sign in to Associates Central with the account that owns `shopnow047c-20`.
2. Open one product page, e.g. `https://www.amazon.com/dp/B0CDY277D3`.
3. Click the tagged link `https://www.amazon.com/dp/B0CDY277D3?tag=shopnow047c-20` (or use SiteStripe's Text link).
4. In Associates Central → Reports → Tracking ID report, look for a click today against `shopnow047c-20`.
5. Repeat for the other four ASINs. Record the date and pass/fail per product.
6. Mark `SG-01` approved and `FLG-001` accordingly. No code changes are needed either way.

**A3 — Search Console.**
1. Confirm which host is canonical. Today it is `https://wingbangboozle1-lang.github.io/Prod1/` (FLG-007). A custom domain changes every canonical, so decide that first.
2. Add the property in Search Console and verify it (the GitHub Pages host verifies by HTML file or DNS depending on the domain chosen).
3. Submit `sitemap.xml`. It already lists exactly the 25 pages the build writes.
4. Wait 28 days. Then choose the next guide from the queries that arrived, not from the calendar's guesses.

---

## F. What this file is not

It is not a forecast, a traffic estimate, or a revenue model. It contains no popularity
claim, no ranking claim and no claim that any product is better than another beyond what
its own listing states. Where a fact is missing it says so, names who can supply it, and
leaves the field empty.
