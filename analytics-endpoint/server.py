"""Self-hosted, privacy-preserving event counter for The Countertop Guide.

Accepts exactly the five events this site documents (data/editorial.json -> events.five):
page_view, outbound_click, search, chooser_complete, guide_read. Each arrives as JSON POST
to /event and is counted per day, per event and per path. It never stores or logs client
addresses, user agents, referrers, cookies or per-event timestamps, and it has no database.

The event names and payload shape are a contract with assets/app.js. scripts/
test_event_contract.py imports this module, feeds validate() the payloads the client actually
builds, and fails the build if either side drifts - which is how the earlier mismatch
(endpoint expecting guide_read_75 / category_click / feed_click while the client emitted
search / chooser_complete / guide_read) got closed instead of being re-litigated.

Run:      python3 analytics-endpoint/server.py --port 8787 --origin https://wingbangboozle1-lang.github.io
Health:   GET /health
Site:     set data-editorial.json -> events.endpoint (which the build writes into
          body[data-analytics-endpoint]) to the hosted /event URL. While it is empty, as it
          is today, the site sends no request at all.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

EVENT_NAMES = frozenset({"page_view", "outbound_click", "search", "chooser_complete", "guide_read"})
# Fields a payload must carry to be useful later, per event. Kept tiny on purpose: every
# extra field is something a reader would have to trust us with.
CHOOSERS = frozenset({"snacks", "family", "meat", "compact", "standard", "plenty", "budget", "mid", "premium"})
MAX_Q = 80
PATH_RE = re.compile(r"^/[A-Za-z0-9._~/\-]{0,200}$")   # a site path only: no query, no fragment, no spaces
ASIN_RE = re.compile(r"^B[0-9A-Z]{9}$")                 # Amazon ASIN format
MAX_BODY = 1024   # the client sends {event, path, asin?, data}; 1 KB bounds a search query at MAX_Q
DEFAULT_ORIGIN = "https://wingbangboozle1-lang.github.io"
_lock = threading.Lock()


def validate(payload: object) -> tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "body must be a JSON object"
    event = payload.get("event")
    if event not in EVENT_NAMES:
        return False, "unknown event"
    path = payload.get("path")
    if not isinstance(path, str) or not PATH_RE.match(path):
        return False, "invalid path"
    asin = payload.get("asin", "")
    if asin not in ("", None) and (not isinstance(asin, str) or not ASIN_RE.match(asin)):
        return False, "invalid asin"
    if event == "outbound_click" and not (isinstance(asin, str) and ASIN_RE.match(asin)):
        # A click without an ASIN cannot ever be reconciled against an Associates report,
        # so it is refused rather than stored as an unattributable count.
        return False, "outbound_click requires a valid asin"
    data = payload.get("data", {})
    if data and not isinstance(data, dict):
        return False, "data must be an object"
    if event == "search":
        q = data.get("q")
        if not isinstance(q, str) or not 0 < len(q) <= MAX_Q:
            return False, f"search needs q between 1 and {MAX_Q} characters"
        if any(ord(ch) < 32 for ch in q):
            return False, "search q contains control characters"
    if event == "chooser_complete":
        answers = [data.get(k) for k in ("q1", "q2", "q3")]
        if any(a not in CHOOSERS for a in answers):
            return False, "chooser_complete needs q1, q2 and q3 from the known answer set"
    return True, ""


def record(counts_file: pathlib.Path, payload: dict, today: str | None = None) -> None:
    day = today or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    with _lock:
        data = {}
        if counts_file.exists():
            data = json.loads(counts_file.read_text(encoding="utf-8"))
        bucket = data.setdefault(day, {})
        by_path = bucket.setdefault(payload["event"], {})
        by_path[payload["path"]] = by_path.get(payload["path"], 0) + 1
        asin = payload.get("asin") or ""
        if payload["event"] == "outbound_click" and asin:
            by_asin = bucket.setdefault("outbound_click_asin", {})
            by_asin[asin] = by_asin.get(asin, 0) + 1
        counts_file.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=str(counts_file.parent), prefix=".counts-")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
        os.replace(tmp, counts_file)


def make_handler(counts_file: pathlib.Path, allowed_origin: str):
    class Handler(BaseHTTPRequestHandler):
        server_version = "kbd-measure"
        sys_version = ""

        def log_message(self, format, *args):  # no request log: it would record client addresses
            return

        def _cors(self) -> None:
            origin = self.headers.get("Origin", "")
            if origin and origin == allowed_origin:
                self.send_header("Access-Control-Allow-Origin", origin)
                self.send_header("Vary", "Origin")
                self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")

        def _send(self, code: int) -> None:
            self.send_response(code)
            self._cors()
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_OPTIONS(self):
            self._send(204 if self.path == "/event" else 404)

        def do_GET(self):
            if self.path == "/health":
                body = b"ok"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            self._send(404)

        def do_POST(self):
            if self.path != "/event":
                self._send(404)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._send(400)
                return
            if length <= 0 or length > MAX_BODY:
                self._send(413 if length > MAX_BODY else 400)
                return
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send(400)
                return
            ok, _reason = validate(payload)
            if not ok:
                self._send(400)
                return
            record(counts_file, payload)
            self._send(204)

    return Handler


def main() -> None:
    here = pathlib.Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--counts", default=str(here / "counts.json"))
    ap.add_argument("--origin", default=os.environ.get("KBD_ALLOWED_ORIGIN", DEFAULT_ORIGIN))
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), make_handler(pathlib.Path(args.counts), args.origin))
    print(f"listening on {args.host}:{args.port}; origin {args.origin}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
