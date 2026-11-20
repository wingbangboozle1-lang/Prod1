# Self-hosted measurement endpoint — The Countertop Guide

`server.py` is a standard-library Python service that counts the site's **five defined
events** per day, per event and per path. It is the server half of one contract; the
client half is `assets/app.js`, the data half is `data/editorial.json` (`events.five`),
and `scripts/check_measure.mjs` fails the deploy if the three ever disagree.

- Accepts exactly: `page_view`, `outbound_click`, `search`, `chooser_complete`, `guide_read`.
- POST JSON to `/event` with `event`, `path` (site path, no query/fragment) and, for
  `outbound_click`, an `asin` (`B0XXXXXXXX`). Extra envelope keys (`page`, `ts`, `data`)
  are tolerated but **not stored**.
- Stores daily aggregate counts only. It does not log request addresses, user agents,
  referrers, cookies, per-event timestamps or search query text.
- CORS is limited to one origin (`--origin` or `CTG_ALLOWED_ORIGIN`).

## Run

```bash
python3 analytics-endpoint/server.py --port 8787 --origin https://wingbangboozle1-lang.github.io
curl -s http://localhost:8787/health   # ok
```

Self-test (no network, no server started; also run in CI):

```bash
python3 analytics-endpoint/selftest.py
```

## Connect the site

The generator writes `data-analytics-endpoint` on `<body>` from
`data/editorial.json` → `events.endpoint`. Set that field to
`https://<your-host>/event`, rebuild, and `assets/app.js` will beacon the five events
there with `navigator.sendBeacon`. Until that field is set the site sends **nothing** —
counts stay in the visitor's own browser (visible and clearable on the methodology page).

## Status

Code complete and contract-tested. **Not hosted.** GitHub Pages serves static files, so
the endpoint must run elsewhere (any small HTTPS box the owner controls). Hosting is an
open owner decision: SG-03 on the suggestion board, Q-08 on the missing-information map.
Until it is hosted, no data leaves any visitor's device and the campaign ledger stays
empty — conversions and orders are recorded only from authorized first-party reports
(Associates Central), never from client-side events.
