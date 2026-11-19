#!/usr/bin/env python3
"""Self-hosted, privacy-preserving event counter for the Kitchen Buyer's Desk site.

Accepts exactly five events (page_view, outbound_click, guide_read_75, category_click,
feed_click) as JSON POST to /event. Keeps daily counts per event and path. It never
stores or logs client addresses, user agents, referrers, cookies or timestamps per event.
Standard library only.

Run:      python3 analytics-endpoint/server.py --port 8787 --origin https://wingbangboozle1-lang.github.io
Health:   GET /health
Site:     set window.KBD_ENDPOINT = "https://<your-host>/event" before assets/measure.js loads.
          The site sends nothing until that is set. (Not set in this build; see FLAG-06.)
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

EVENT_NAMES = frozenset({"page_view", "outbound_click", "guide_read_75", "category_click", "feed_click"})
PATH_RE = re.compile(r"^/[A-Za-z0-9._~/\-]{0,200}$")   # a site path only: no query, no fragment, no spaces
ASIN_RE = re.compile(r"^B[0-9A-Z]{9}$")                 # Amazon ASIN format
MAX_BODY = 512
DEFAULT_ORIGIN = "https://wingbangboozle1-lang.github.io"
_lock = threading.Lock()


def validate(payload: object) -> tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "body must be a JSON object"
    if payload.get("event") not in EVENT_NAMES:
        return False, "unknown event"
    path = payload.get("path")
    if not isinstance(path, str) or not PATH_RE.match(path):
        return False, "invalid path"
    asin = payload.get("asin", "")
    if asin not in ("", None) and (not isinstance(asin, str) or not ASIN_RE.match(asin)):
        return False, "invalid asin"
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
