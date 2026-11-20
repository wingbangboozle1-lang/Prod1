# Self-hosted measurement endpoint

`server.py` is a standard-library Python service that counts the five documented site events per day, per event and per path. It is code only: nothing here is hosted, and the site sends no request at all until a host is chosen (see `events.endpoint` in `data/editorial.json`).

## The contract

Accepts exactly the five names in `data/editorial.json` → `events.five`:

| Event | Required fields | What it answers |
|---|---|---|
| `page_view` | `path` | which pages get traffic at all |
| `outbound_click` | `path`, `asin` (10-char Amazon ASIN format) | which product cards earn clicks, reconcilable against an Associates report |
| `search` | `path`, `data.q` (1–80 chars) | which questions the site has not answered |
| `chooser_complete` | `path`, `data.q1/q2/q3` from the answer set the chooser offers | whether the decision aid is used |
| `guide_read` | `path` | which guides hold a reader to 75% |

`path` is a site path only: no query string, no fragment, no spaces (the client sends `location.pathname`). Anything else is refused with 400, and the request is not counted.

The mismatch this closes: an earlier session found the endpoint expecting `guide_read_75`, `category_click` and `feed_click` while the site emitted `search`, `chooser_complete` and `guide_read` - a live endpoint would have answered 200 to nothing and thrown away every event. `scripts/test_event_contract.py` now fails the build if either side drifts, and it is a step in `.github/workflows/pages.yml`.

## What is stored

One JSON file: `{"YYYY-MM-DD": {"event": {"/path": count}}}`, plus `outbound_click_asin` counts per ASIN. Daily aggregates only.

- No request log: the handler overrides `log_message`, so addresses never reach disk.
- No user agent, referrer, cookie, fingerprint, or per-event timestamp is read or stored.
- No database, no retention job: the file is small and dated, and deletion is a file operation.
- Body limit 1 KB, which bounds a search query at 80 characters.
- Conversion and revenue are **not** measurable here, deliberately. Order counts come only from authorized Associates reports into the campaign ledger (`methodology.html`).

## Run and check

```bash
python3 analytics-endpoint/server.py --port 8787 --origin https://wingbangboozle1-lang.github.io
curl -s localhost:8787/health                                            # ok
curl -s -X POST localhost:8787/event -H 'Content-Type: application/json' \
     --data '{"event":"page_view","path":"/index.html","data":{}}' -i | head -1   # 204 No Content
python3 scripts/test_event_contract.py                                   # the contract, offline
```

CORS is limited to one origin (`--origin`, or `KBD_ALLOWED_ORIGIN`); a request from any other origin gets no `Access-Control-Allow-Origin` header.

## Connect the site

Set `events.endpoint` in `data/editorial.json` to `https://<host>/event`, rebuild, and the build writes it into `body[data-analytics-endpoint]`, which is the only thing `assets/app.js` reads. Leave it empty and the client counts in the browser and transmits nothing.

## Still open before this goes live

Owner decisions, all listed on `suggestions.html` (SG-03) and `flagged.html`: a host with HTTPS, how long counts are kept, and the privacy sentence on `about.html` that tells a reader this exists. Verified working in the sandbox on 2026-11-20 (five accepted, six planted defects refused, per-ASIN bucket written, foreign Origin unanswered) - **not** deployed, and no production data has been collected.
