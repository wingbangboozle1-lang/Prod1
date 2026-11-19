# Aggregate measurement endpoint

`server.py` is an optional standard-library Python service. It is **not hosted** and the public site's `data-analytics-endpoint` remains blank. Do not enable it until an HTTPS host, privacy notice, provider-log policy, and retention/deletion owner are selected.

## Client/server contract

The client (`assets/app.js`) and service share exactly these event names:

| Event | Request JSON | What is counted |
|---|---|---|
| `page_view` | `{"event":"page_view","path":"/Prod1/"}` | Daily count by event and path |
| `outbound_click` | `{"event":"outbound_click","path":"/Prod1/compare.html","asin":"B0CDY277D3"}` | Daily count by event/path and separately by observed ASIN |
| `search` | `{"event":"search","path":"/Prod1/search.html"}` | Daily count by event and path; **no query text** |
| `chooser_complete` | `{"event":"chooser_complete","path":"/Prod1/compare.html"}` | Daily count by event and path; **no answers** |
| `guide_read` | `{"event":"guide_read","path":"/Prod1/guide-capacity-checklist.html"}` | Daily count by event and path |

Only `event`, `path`, and (for `outbound_click` only) `asin` are accepted. Query strings, fragments, full outbound URLs, search terms, chooser answers, cookies, referrers, user-agent strings, client IDs, and event timestamps are not accepted or stored. The browser keeps event totals in local storage for up to 30 days. This on-device counter is separate from the endpoint and can be cleared by the reader through browser storage controls.

The endpoint expects a JSON body sent as `text/plain`, an exact matching `Origin` header, and a single configured site origin. It does not write HTTP request logs. Aggregate files are pruned at startup, after each event, and daily; the default retention is 90 days (`--retention-days` can change it). A host or reverse proxy can still create its own logs; review and configure those separately. CORS and an Origin check are not an authentication or abuse-prevention system, so hosting/rate-limit decisions remain necessary before production use.

## Run locally

```sh
python3 analytics-endpoint/server.py \
  --port 8787 \
  --origin https://wingbangboozle1-lang.github.io \
  --retention-days 90
curl -s http://127.0.0.1:8787/health   # ok
```

A contract smoke test (the public client setting must remain blank unless using a local test page):

```sh
curl -i http://127.0.0.1:8787/event \
  -H 'Origin: https://wingbangboozle1-lang.github.io' \
  -H 'Content-Type: text/plain;charset=UTF-8' \
  --data '{"event":"page_view","path":"/Prod1/"}'
```

Run unit/HTTP contract tests with:

```sh
python3 -m unittest discover -s analytics-endpoint -p 'test_*.py' -v
node --check assets/app.js
node scripts/test_app.mjs
```

## Hosting gate

GitHub Pages is static and cannot run this Python service. The site therefore sends no network events today; only local browser counts run. Before setting `data-analytics-endpoint`, select a separate HTTPS host, exact allowed origin, persistence, retention, provider-log policy, deletion owner, and privacy notice. Affiliate orders and commissions are not client events; use authorized Associates reports only.
