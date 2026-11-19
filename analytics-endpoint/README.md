# Self-hosted measurement endpoint

`server.py` is a standard-library Python service that counts the five site events per day, per event and per path.

- Accepts only: `page_view`, `outbound_click`, `guide_read_75`, `category_click`, `feed_click`.
- Stores daily counts only. It does not log request addresses, user agents, referrers or cookies.
- CORS is limited to one origin (`--origin` or `KBD_ALLOWED_ORIGIN`).

## Run

```bash
python3 analytics-endpoint/server.py --port 8787 --origin https://wingbangboozle1-lang.github.io
curl -s http://localhost:8787/health   # ok
```

## Connect the site

Set `window.KBD_ENDPOINT = "https://<your-host>/event";` before `assets/measure.js` loads (for example in `scripts/build.mjs`). Until this is set, the site sends nothing.

## Status

Code only. Not hosted. GitHub Pages serves static files, so the endpoint must run elsewhere. Hosting is an open decision (SUG-03, FLAG-06).
