# Executive summary — Countertop Check (working name)

Date: 2026-11-19 · Branch: `arena/9b748801-prod1` · Published site: https://wingbangboozle1-lang.github.io/Prod1/ (the root site built by other sessions). This session's parallel build was NOT published; see `README.md` in this folder.

## What was built (prototype, not published)
- A static, sponsored-link site for the five Amazon links you submitted: three air fryers/ovens and two meat thermometers.
- Front page (products first), two category pages, a products table, five question-shaped guides, and dashboards for Analysis, Verification, Campaign ledger, Measurement, Suggestions, Open questions, **Flagged for Review**, Executive summary, and Disclosure & policy.
- Disclosure strip under the masthead of every page, repeated in the footer. Wording is the Operating Agreement §5 statement.
- Every Amazon link carries `rel="sponsored noopener noreferrer"` (Google's guidance for paid/affiliate links).
- Sitemap, RSS feed of guides, `robots.txt`, unique titles and descriptions per page.
- Note: the live site on `main` already covers this scope; the review-relevant parts were merged into it as FLG-013 to FLG-020.
- Build and gate scripts (`npm run build`, `npm run check`). The check fails the build on a missing disclosure, a non-sponsored Amazon link, a broken internal link, a missing sitemap/RSS entry, or a product row without a source.

## What is verified (sources on each page)
- All five submitted links open to amazon.com listings. Observed ASINs: B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5, B0DZFD6R9Z.
- Titles and breadcrumbs were read from those listings. Capacity and accuracy values come only from the titles.
- Disclosure wording: Associates Operating Agreement §5 (official).
- Link attribute: Google Search Central, qualify outbound links (official).

## What is not verified (left blank and flagged)
- **Intended ASIN** — blank for all five. The submitted codes are 9 characters; the 10-character ASIN rule is only from third-party sites (FL-01, FL-02, FL-03).
- **Tracking attribution** — none of the five redirect URLs carries `tag=shopnow047c-20` (FL-04).
- **Special Link status** — the short links are not claimed invalid; their status is unresolved and needs a one-link test in the Associates workflow (FL-05).
- **Price, rating, dimensions, commission** — not in the fetched text for the main products, so blank (FL-06, FL-08, FL-16).

## Main risks
1. Attribution to the selected tracking ID is unconfirmed (FL-04). Revenue cannot be attributed until a Special Link test is done.
2. Short-link compliance is unresolved (FL-05). The Operating Agreement requires tagged Special Links.
3. Several reader-facing choices are still open: brand, byline, cadence, analytics endpoint, imagery, price display (Suggestions S-02 to S-08).

## Decisions requested (Suggestions page)
- **S-01** Test one Special Link per product in Associates before scaling (recommended by the brief's own rule).
- **S-02/S-03** Brand name and byline.
- **S-04** Publishing cadence.
- **S-05** Where the analytics endpoint runs (GitHub Pages cannot host it).
- **S-06** Imagery policy. No photos are used.
- **S-07** Which guide to publish first.
- **S-08** Whether to show prices.
- **S-09** Confirm the five measurement events (the brief did not list them).

## What cannot be done from this environment
- Logging in to Associates or Search Console (manual).
- Running a self-hosted analytics endpoint on static hosting.
- Reviewing the external source register in Zone3/Zone4 (not in this repo; FL-12).

## Sources
- Associates Program Operating Agreement — https://affiliate-program.amazon.com/help/operating/agreement
- Associates Program Policies — https://affiliate-program.amazon.com/help/operating/policies
- Google Search Central, qualify outbound links — https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
- FTC, Disclosures 101 for social media influencers — https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers (not retrieved; FL-10)
- Amazon listings — https://www.amazon.com/dp/B0CDY277D3 · https://www.amazon.com/dp/B09B7SB46R · https://www.amazon.com/dp/B08DKYBTPH · https://www.amazon.com/dp/B0DHZTCNR5 · https://www.amazon.com/dp/B0DZFD6R9Z
