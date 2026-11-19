# Analytics integration review

**Checked:** 2026-11-19 against `origin/main` at `2351ed4`; PR #10 was open at the time. This is a read-only review of the existing analytics paths, not a deployed tracker or a compliance certification.

## Executive finding

The live GitHub Pages site has no production analytics endpoint configured. More importantly, the current page client and the optional self-hosted Python endpoint do not share an event contract. Turning on the existing endpoint without aligning them would not record the root site's events. A separate, unused client file and an open parallel implementation add further schema ambiguity. Do not report click totals, conversions, orders, or revenue from these files until one client/server pair is selected, connected, and tested.

## Verified code findings

1. **The current root-site client defines one five-event set.** `assets/app.js` lists `page_view`, `outbound_click`, `search`, `chooser_complete`, and `guide_read`. It reads `data-analytics-endpoint` from `<body>`; that attribute is empty in the checked root HTML pages. When enabled, the request body uses the fields `event`, `page`, `ts`, and `data`.

2. **The existing Python endpoint defines a different five-event set and payload.** `analytics-endpoint/server.py` accepts `page_view`, `outbound_click`, `guide_read_75`, `category_click`, and `feed_click`; its validator requires `path` and optionally a top-level `asin`. Therefore a root `page_view` from `assets/app.js` fails the endpoint's required-path check (`page` is not `path`), and the root `search`, `chooser_complete`, and `guide_read` names are not in its allowlist. The server is not currently configured on the root pages, so this is a latent integration defect, not evidence that production events were lost.

3. **The endpoint README names a client file not present in the checked root tree.** `analytics-endpoint/README.md` says to set `window.KBD_ENDPOINT` before `assets/measure.js` loads. No `assets/measure.js` file is tracked on `origin/main`; the visible root client uses `data-analytics-endpoint` instead.

4. **A third, unreferenced tracker remains in the repository.** `assets/js/analytics.js` defines `page_view`, `outbound_click`, `affiliate_redirect`, `guide_view`, and `conversion_signal`, and was not referenced by the checked HTML. Its localStorage records include a timestamp, `location.search`/hash, `document.referrer`, and outbound `target` URL. Its comment says it records no personal data; do not activate it without reviewing/removing those fields and settling the site's actual data policy.

5. **The Python endpoint needs an owner review before production.** Its `record()` function retains daily buckets without pruning. Its `_cors()` method adds response headers only for the configured origin; `do_POST()` does not itself reject a mismatched `Origin` before recording. This review does not claim a browser exploit; it requests explicit origin and retention decisions before hosting.

6. **GitHub Pages cannot host the server process.** GitHub documents Pages as static HTML/CSS/JavaScript hosting and documents platform IP logging for security. A separate runtime would be required, and the platform's own logging is outside the custom collector's control.

## Decision and discovery requests

- Choose a single five-event taxonomy and source of truth. A working option for the current root pages is to keep the names already emitted by `assets/app.js`, then update the selected backend contract and add passing client/server contract tests.
- Minimize the browser payload to the event name, path (without query or fragment), and an allowlisted product reference for product clicks. Do not persist raw search terms, full outbound URLs, referrers, per-event IDs, or client timestamps in the privacy-preserving aggregate counter.
- Choose an HTTPS host, durable storage, access policy, retention period, and privacy-notice language before setting a production endpoint. GitHub Pages alone cannot run the collector.
- Keep the campaign ledger empty until authorized first-party Associates reports supply dated source/channel, eligible-session, click, and order values. A local outbound-click event is not an Amazon report click or conversion.
- Request to the owners of the root pages and endpoint: update the existing Flagged for Review entry (analytics is already flagged) with the client/server schema mismatch and stale README reference. Do not activate either parallel tracker until the chosen contract is wired and tested.

## Official references checked

- [GitHub Pages — What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages): static hosting and GitHub's documented security logging for Pages visits.
- [Amazon Associates Program Operating Agreement](https://affiliate-program.amazon.com/help/operating/agreement): Special Link and Associates disclosure framework.
- [Amazon Associates Program Policies](https://affiliate-program.amazon.com/help/operating/policies): Special Link requirements; the site still needs its separate enrolled-workflow test.
- [Google Search Console — Get started](https://developers.google.com/search/docs/monitor-debug/search-console-start): ownership verification and query/page performance reporting; no Search Console property or report was checked in this review.
