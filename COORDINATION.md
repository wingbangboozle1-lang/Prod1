# Coordination board

This checkout is the active Arena branch `arena/cba9af3f-prod1` (base `86bb372dc76781a50966966c39481c5b242a9ea4`). No other task claims were present when work began.

| Task | Status | Owner/session | Scope |
|---|---|---|---|
| Build the publication-style affiliate website, decision/suggestions review area, research register, and supporting editorial/SEO assets | done | `cba9af3f` | `index.html`, `styles.css`, `guides/`, `review/`, `feed.xml`, `sitemap.xml`, `robots.txt`, `.nojekyll`, `scripts/check_site.py`, `README.md`, `COORDINATION.md` |

## Verification and source notes

- Initial repository review: the checkout contained only a seven-byte `README.md`; no prior site, tests, coordination board, or product register existed. Authenticated GitHub API inspection confirmed public repository `wingbangboozle1-lang/Prod1`, default branch `main`, and Pages configured for `main` at `/` (legacy source), URL `https://wingbangboozle1-lang.github.io/Prod1/`.
- Product claims: not verified. Five user-supplied shortened URLs are preserved as submitted, without claiming they are invalid or valid, without resolving redirects, and without inferring titles/ASINs, prices, specifications, reviews, availability, commissions, or tracking attribution. Intended ASIN, official listing, date/source, and observed redirect are separate blank fields.
- Applicable review references supplied in the user request: [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement), [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies), [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers), and [FTC Endorsement Guides](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews). They are included as references for human review; external hosts are outside this session's outbound network allowlist, so the current source text was not independently fetched or confirmed.
- Analytics, campaign reports, product intent confirmations, Search Console, and Amazon API access: not provided. No analytics or conversions are fabricated; review pages document the evidence and gates required before activation.
- Checks run: `python3 scripts/check_site.py` (8 HTML pages, unique titles/descriptions, canonical URLs, disclosure strips and footer statements, local links/fragments, sponsored product link markup, XML sitemap and RSS) and `git diff --check`; both passed. These are structural checks, not product/policy verification.

## Irregularities / needs review

- All five submitted short links have unresolved destinations, listing URLs, intended ASINs, source/confirmation evidence, and tracking status. See the site's Flagged for Review register.
- GitHub Pages is configured on `main` as a legacy branch-root deployment; its post-merge build must still be checked. There is no analytics backend/database, custom domain, or Search Console verification.
