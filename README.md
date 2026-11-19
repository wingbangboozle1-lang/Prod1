# Counterwise

A publication-style Amazon Associates starter site for buyer-first kitchen-appliance guides, a transparent submitted-link shortlist, and an evidence/review desk. The project intentionally distinguishes editorial guidance from product facts: **no submitted product has been identified or recommended yet.**

## Executive summary

- The landing page leads with useful buyer questions, an editorial guide cluster, and the five product links as submitted—not with audit machinery.
- Four human-sounding question-led guides cover format, capacity, cleanup/counter space, and multi-function trade-offs. They provide decision frameworks, not product reviews or claims of testing/search popularity.
- The site repeats an Associates disclosure beneath the masthead and in every footer. All five outbound submitted product links carry `rel="sponsored nofollow"`.
- The research desk lays out known/unknown questions, an editable suggestions queue, a blank campaign ledger, and a separate Flagged for Review register.
- Sitemap, RSS feed, robots.txt, unique titles/descriptions, canonical URLs, and a small WebSite JSON-LD block are included.
- This is static GitHub Pages. It does **not** contain an active self-hosted analytics service, verified Search Console property, Amazon API integration, or conversion reports. No such infrastructure can be represented as live without a host, permissions, credentials, and evidence.

## Product evidence status

The only product inputs are the following user-supplied short URLs:

- `https://link.amazon/B04G1MEwY`
- `https://link.amazon/B02NbDxp3`
- `https://link.amazon/B00hJ57DV`
- `https://link.amazon/B0c8moW59`
- `https://link.amazon/B0f3GKalj`

Their exact destinations and compliance status are unresolved; this project does not claim that any is invalid. No official product listing, intended ASIN, title, price, image, specification, review, commission, or product-to-link match has been confirmed. The supplied tracking ID `shopnow047c-20` is recorded as user input but has not been checked in Associates Central. Product-intent records keep intended ASIN, official listing URL, confirmation date/source, and observed redirect target as separate fields.

## Review pages

- [Research desk and decision suggestions](review/index.html)
- [Flagged for Review](review/flagged.html)
- [Question-led guides](guides/index.html)
- [Sitemap](sitemap.xml) · [RSS feed](feed.xml)

## Preview locally

No build step or package dependencies are required. Serve the repository root with any static-file server, for example:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000/`. Run the repository checks from a clean checkout with:

```sh
python3 scripts/check_site.py
```

## Publishing and measurement gates

The repository's GitHub Pages site was observed via the authenticated GitHub API to be enabled from `main` at `/` (legacy Pages source) at the time of this work. The planned public URL is `https://wingbangboozle1-lang.github.io/Prod1/`. A successful source change does not by itself prove that a particular deployment has completed; check the Pages build status after merge.

Before enabling measurement, choose and configure a first-party endpoint and persistent store, establish consent/privacy/retention controls, and test event receipt. The static site alone cannot provide durable click counts or conversions. See the research desk for the proposed five-event vocabulary and decision gates. Search Console access and Associates reports must likewise come from authorized first-party accounts.

## Official review references

These are links for a human to review, not a claim that their current content was fetched or that the project has completed legal/compliance review:

- [Amazon Associates Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement)
- [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies)
- [FTC Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
- [FTC Endorsement Guides](https://www.ftc.gov/business-guidance/advertising-marketing/endorsements-influencers-reviews)

## Coordination

See [COORDINATION.md](COORDINATION.md) for scope, verification boundaries, and flagged irregularities.
