#!/usr/bin/env python3
"""Small, self-hosted aggregate event counter for The Countertop Guide.

Accepts the same five event names as assets/app.js. POST /event accepts only
{event, path} and, for outbound_click only, {event, path, asin}. It retains daily
counts by event/path and outbound ASIN for a configurable period. It does not log
request addresses, user agents, referrers, cookies, full URLs, or per-event timestamps.

Run:      python3 analytics-endpoint/server.py --port 8787 --origin https://wingbangboozle1-lang.github.io
Health:   GET /health
Connect:  configure the deployed site's data-analytics-endpoint only after HTTPS,
          retention, privacy, and host-log decisions are reviewed. It is blank today.
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
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

EVENT_NAMES = frozenset({"page_view", "outbound_click", "search", "chooser_complete", "guide_read"})
PATH_CHAR_RE = re.compile(r"^/[A-Za-z0-9._~/-]{0,200}$")
SEGMENT_RE = re.compile(r"^[A-Za-z0-9_~-][A-Za-z0-9._~-]*$")
ASIN_RE = re.compile(r"^B[A-Z0-9]{9}$")
MAX_BODY = 512
DEFAULT_ORIGIN = "https://wingbangboozle1-lang.github.io"
DEFAULT_RETENTION_DAYS = 90
CLEANUP_INTERVAL_SECONDS = 24 * 60 * 60
_lock = threading.Lock()


def valid_path(path: object) -> bool:
    if not isinstance(path, str) or not PATH_CHAR_RE.fullmatch(path):
        return False
    if "?" in path or "#" in path:
        return False
    if path == "/":
        return True
    parts = path.split("/")[1:]
    if parts and parts[-1] == "":
        parts.pop()
    return bool(parts) and all(part not in {".", ".."} and SEGMENT_RE.fullmatch(part) for part in parts)


def validate(payload: object) -> tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "body must be a JSON object"
    event = payload.get("event")
    if event not in EVENT_NAMES:
        return False, "unknown event"
    if not valid_path(payload.get("path")):
        return False, "invalid path"
    allowed_keys = {"event", "path", "asin"} if event == "outbound_click" else {"event", "path"}
    if set(payload) != allowed_keys:
        return False, "unexpected or missing fields"
    if event == "outbound_click" and (not isinstance(payload.get("asin"), str) or not ASIN_RE.fullmatch(payload["asin"])):
        return False, "invalid asin"
    return True, ""


def _read_counts(counts_file: pathlib.Path) -> dict:
    if not counts_file.exists():
        return {}
    try:
        data = json.loads(counts_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_counts(counts_file: pathlib.Path, data: dict) -> None:
    counts_file.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=str(counts_file.parent), prefix=".counts-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as output:
            json.dump(data, output, indent=2, sort_keys=True)
            output.write("\n")
        os.replace(temporary, counts_file)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def _trim(data: dict, today: dt.date, retention_days: int) -> dict:
    trimmed = {}
    for day_text, counts in data.items():
        try:
            day = dt.date.fromisoformat(day_text)
        except (TypeError, ValueError):
            continue
        age = (today - day).days
        if 0 <= age < retention_days and isinstance(counts, dict):
            trimmed[day_text] = counts
    return trimmed


def prune(counts_file: pathlib.Path, retention_days: int = DEFAULT_RETENTION_DAYS,
          today: str | dt.date | None = None) -> None:
    if retention_days < 1:
        raise ValueError("retention_days must be at least 1")
    current_day = dt.date.fromisoformat(today) if isinstance(today, str) else today or dt.datetime.now(dt.timezone.utc).date()
    with _lock:
        data = _trim(_read_counts(counts_file), current_day, retention_days)
        _write_counts(counts_file, data)


def record(counts_file: pathlib.Path, payload: dict, today: str | None = None,
           retention_days: int = DEFAULT_RETENTION_DAYS) -> None:
    ok, reason = validate(payload)
    if not ok:
        raise ValueError(reason)
    if retention_days < 1:
        raise ValueError("retention_days must be at least 1")
    day = today or dt.datetime.now(dt.timezone.utc).date().isoformat()
    current_day = dt.date.fromisoformat(day)
    with _lock:
        data = _trim(_read_counts(counts_file), current_day, retention_days)
        bucket = data.setdefault(day, {})
        by_path = bucket.setdefault(payload["event"], {})
        path = payload["path"]
        by_path[path] = by_path.get(path, 0) + 1
        if payload["event"] == "outbound_click":
            by_asin = bucket.setdefault("outbound_click_asin", {})
            asin = payload["asin"]
            by_asin[asin] = by_asin.get(asin, 0) + 1
        _write_counts(counts_file, data)


def _cleanup_loop(counts_file: pathlib.Path, retention_days: int) -> None:
    while True:
        time.sleep(CLEANUP_INTERVAL_SECONDS)
        try:
            prune(counts_file, retention_days)
        except Exception:
            # No request or personal data is written to logs; a later cycle retries.
            continue


def make_handler(counts_file: pathlib.Path, allowed_origin: str,
                 retention_days: int = DEFAULT_RETENTION_DAYS):
    class Handler(BaseHTTPRequestHandler):
        server_version = "ctg-aggregate-measurement"
        sys_version = ""

        def log_message(self, format, *args):
            # The standard HTTP log contains client addresses; intentionally disabled.
            return

        def _origin_allowed(self) -> bool:
            return self.headers.get("Origin", "") == allowed_origin

        def _cors(self) -> None:
            self.send_header("Access-Control-Allow-Origin", allowed_origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")

        def _send(self, code: int, include_cors: bool = False) -> None:
            self.send_response(code)
            if include_cors:
                self._cors()
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_OPTIONS(self):
            if self.path != "/event":
                self._send(404)
            elif not self._origin_allowed():
                self._send(403)
            else:
                self._send(204, include_cors=True)

        def do_GET(self):
            if self.path == "/health":
                body = b"ok"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self._send(404)

        def do_POST(self):
            if self.path != "/event":
                self._send(404)
                return
            if not self._origin_allowed():
                self._send(403)
                return
            content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if content_type != "text/plain":
                self._send(415, include_cors=True)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._send(400, include_cors=True)
                return
            if length <= 0 or length > MAX_BODY:
                self._send(413 if length > MAX_BODY else 400, include_cors=True)
                return
            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send(400, include_cors=True)
                return
            ok, _reason = validate(payload)
            if not ok:
                self._send(400, include_cors=True)
                return
            try:
                record(counts_file, payload, retention_days=retention_days)
            except (OSError, ValueError):
                self._send(500, include_cors=True)
                return
            self._send(204, include_cors=True)

    return Handler


class ThreadingServer(ThreadingHTTPServer):
    daemon_threads = True


def _validate_origin(origin: str) -> None:
    parsed = urlsplit(origin)
    if parsed.scheme != "https" or not parsed.netloc or parsed.path or parsed.query or parsed.fragment:
        raise SystemExit("--origin must be an HTTPS origin with no path, query, or fragment")


def main() -> None:
    here = pathlib.Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--counts", default=str(here / "counts.json"))
    parser.add_argument("--origin", default=os.environ.get("CTG_ALLOWED_ORIGIN", DEFAULT_ORIGIN))
    parser.add_argument("--retention-days", type=int, default=DEFAULT_RETENTION_DAYS)
    args = parser.parse_args()
    if args.retention_days < 1:
        parser.error("--retention-days must be at least 1")
    _validate_origin(args.origin)

    counts_file = pathlib.Path(args.counts)
    prune(counts_file, args.retention_days)
    cleaner = threading.Thread(target=_cleanup_loop, args=(counts_file, args.retention_days), daemon=True)
    cleaner.start()
    server = ThreadingServer((args.host, args.port), make_handler(counts_file, args.origin, args.retention_days))
    print(f"listening on {args.host}:{args.port}; allowed origin {args.origin}; retention {args.retention_days} days", flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
