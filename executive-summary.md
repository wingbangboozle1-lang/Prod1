# Executive summary — ShopNow Buying Guides

**Site:** ShopNow Buying Guides  
**Branch:** `arena/9969fd0c-prod1`  
**Tracking ID:** `shopnow047c-20`  
**Status:** Live candidate (GitHub Pages)  
**Date:** 2026-11-19

## What was built

A clean, publication-style Amazon affiliate marketing site for kitchen appliances, built from an empty repository.
The landing page leads with the five submitted products (not with the verification process). Every page carries an
affiliate disclosure strip above the fold and repeats it in the footer. All outbound product links are marked
`rel="sponsored"`.

## Product register

Five submitted `link.amazon/…` affiliate links are recorded in `data/products.json` and `data/confirmations.json`.
No product value (title, price, category, image, official listing URL, confirmation date) has been confirmed from an
official source. Every such field is left blank and flagged unverified — nothing is inferred.

## Verification rule

Every table row carries a source link to an official site. If a value can't be confirmed from an official source,
it's left blank and flagged unverified. Official sources referenced:

- Amazon ASIN definition (affiliate program help) — ASINs are exactly 10 alphanumeric characters
- Amazon Associates Operating Agreement — Program Content includes data, images and text (Section 1); Participation Requirements 6(v) and 6(w)
- Amazon Associates Program Policies
- Google Search Central — qualifying outbound links (`rel="sponsored"`), unique descriptions per page, helpful/people-first content
- FTC — Disclosures 101; Endorsements & Influencers

## Flagged irregularities

| ID | Issue | Status |
|----|-------|--------|
| IR-01 | All five submitted `link.amazon` tokens are 9 characters; Amazon ASINs are exactly 10 characters. Destinations cannot be confirmed (link.amazon / amazon.com not reachable from this environment). | Open |
| IR-02 | No real product photography available. Generated or copied photography is not permitted (Amazon OA §1); a decision is pending. | Open — needs decision |

These are published on the **Flagged for review** page (`flagged.html`) and do not block the site going live.

## Measurement

A privacy-preserving, self-hosted analytics capture (`assets/js/analytics.js`) records five defined events:
page_view, outbound_click, affiliate_redirect, guide_view, conversion_signal. No cookies, no personal data, no
third-party scripts. Events are held in browser localStorage and can be posted to a self-hosted beacon endpoint
(`/api/analytics/collect`) once a backend is deployed — the endpoint is a gate, automation stops there by design.
Real conversion measurement requires the Amazon Associates reporting gateway (authorized first-party reports only).
No conversion score or revenue forecast is presented.

## SEO / publication polish

- Unique title + meta description on every page (S-04)
- `rel="sponsored"` on outbound links (S-05)
- sitemap.xml, robots.txt, RSS feed (feed.xml) — each new guide is added to both
- JSON-LD structured data (Organization, WebSite, Article) and Open Graph / Twitter cards (S-09, partly implemented)
- Single navigation group; every dashboard surface reachable from the footer (S-24 internal linking)
- Question-shaped working-title guides (S-07, S-13)
- Mobile-first CSS with `clamp()` type scale (S-20, partly implemented)

## Decision gate

Proposed changes live on the **Suggestions** page (`suggestions.html`). Nothing is implemented until someone reviews
it and chooses the best path. Verified values are recorded in COORDINATION.md before a task is marked done.

## Next steps

1. Enable GitHub Pages for this repository and confirm the build has no broken links.
2. Review IR-01 and IR-02 (flagged page); supply real product photography or confirm the decision to omit it.
3. Resolve the `link.amazon` destination/compliance question (++FLG-003++) through the enrolled Associates workflow.
4. Wire the self-hosted analytics beacon endpoint when a backend is available.
5. Publish question-shaped guides on a cadence; add each to sitemap.xml and feed.xml.
