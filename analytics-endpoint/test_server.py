from __future__ import annotations

import datetime as dt
import json
import pathlib
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import server


SITE_ORIGIN = "https://wingbangboozle1-lang.github.io"


class ContractValidationTests(unittest.TestCase):
    def test_accepts_only_client_contract(self):
        good = [
            {"event": "page_view", "path": "/Prod1/"},
            {"event": "outbound_click", "path": "/Prod1/compare.html", "asin": "B0CDY277D3"},
            {"event": "search", "path": "/Prod1/search.html"},
            {"event": "chooser_complete", "path": "/Prod1/compare.html"},
            {"event": "guide_read", "path": "/Prod1/guide-capacity-checklist.html"},
        ]
        for payload in good:
            with self.subTest(event=payload["event"]):
                self.assertEqual(server.validate(payload), (True, ""))

    def test_rejects_unknown_fields_events_and_unsafe_paths(self):
        bad = [
            {"event": "unknown", "path": "/Prod1/"},
            {"event": "page_view", "path": "/Prod1/", "query": "private search"},
            {"event": "page_view", "path": "/Prod1/", "asin": "B0CDY277D3"},
            {"event": "outbound_click", "path": "/Prod1/", "asin": "bad"},
            {"event": "outbound_click", "path": "/Prod1/"},
            {"event": "page_view", "path": "/Prod1/?q=private"},
            {"event": "page_view", "path": "/Prod1/../secret"},
            {"event": "page_view", "path": "/Prod1/%2Fsecret"},
            [],
            None,
        ]
        for payload in bad:
            with self.subTest(payload=payload):
                self.assertFalse(server.validate(payload)[0])

    def test_path_validation_accepts_published_paths_only(self):
        for path in ("/", "/Prod1/", "/Prod1/index.html", "/Prod1/guide-capacity-checklist.html"):
            with self.subTest(path=path):
                self.assertTrue(server.valid_path(path))
        for path in ("", "//", "/Prod1//guide.html", "/.", "/..", "/has space", "/x?y", "/x#y"):
            with self.subTest(path=path):
                self.assertFalse(server.valid_path(path))


class RetentionTests(unittest.TestCase):
    def test_prune_removes_old_future_and_malformed_days(self):
        with tempfile.TemporaryDirectory() as folder:
            counts = pathlib.Path(folder) / "counts.json"
            counts.write_text(json.dumps({
                "2026-01-01": {"page_view": {"/": 1}},
                "2026-04-01": {"page_view": {"/": 2}},
                "2026-04-02": {"page_view": {"/": 3}},
                "not-a-date": {"page_view": {"/": 4}},
            }), encoding="utf-8")
            server.prune(counts, retention_days=90, today="2026-06-30")
            result = json.loads(counts.read_text(encoding="utf-8"))
            self.assertEqual(set(result), {"2026-04-02"})

    def test_record_aggregates_and_applies_retention(self):
        with tempfile.TemporaryDirectory() as folder:
            counts = pathlib.Path(folder) / "counts.json"
            counts.write_text(json.dumps({"2026-01-01": {"page_view": {"/": 9}}}), encoding="utf-8")
            payload = {"event": "outbound_click", "path": "/Prod1/compare.html", "asin": "B0CDY277D3"}
            server.record(counts, payload, today="2026-06-30", retention_days=90)
            server.record(counts, payload, today="2026-06-30", retention_days=90)
            result = json.loads(counts.read_text(encoding="utf-8"))
            self.assertEqual(set(result), {"2026-06-30"})
            day = result["2026-06-30"]
            self.assertEqual(day["outbound_click"]["/Prod1/compare.html"], 2)
            self.assertEqual(day["outbound_click_asin"]["B0CDY277D3"], 2)
            self.assertNotIn("ip", json.dumps(result).lower())
            self.assertNotIn("user-agent", json.dumps(result).lower())


class HttpContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.counts = pathlib.Path(self.temp.name) / "counts.json"
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.make_handler(self.counts, SITE_ORIGIN, 90))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        self.temp.cleanup()

    def post(self, payload, origin=SITE_ORIGIN, raw=None, content_type="text/plain;charset=UTF-8"):
        body = raw if raw is not None else json.dumps(payload).encode("utf-8")
        headers = {"Origin": origin, "Content-Type": content_type}
        request = Request(self.url + "/event", data=body, headers=headers, method="POST")
        try:
            response = urlopen(request, timeout=3)
            return response.status, response.headers
        except HTTPError as error:
            return error.code, error.headers

    def test_posts_client_events_and_returns_cors(self):
        payloads = [
            {"event": "page_view", "path": "/Prod1/"},
            {"event": "outbound_click", "path": "/Prod1/compare.html", "asin": "B0CDY277D3"},
            {"event": "search", "path": "/Prod1/search.html"},
            {"event": "chooser_complete", "path": "/Prod1/compare.html"},
            {"event": "guide_read", "path": "/Prod1/guide-capacity-checklist.html"},
        ]
        for payload in payloads:
            with self.subTest(event=payload["event"]):
                status, headers = self.post(payload)
                self.assertEqual(status, 204)
                self.assertEqual(headers.get("Access-Control-Allow-Origin"), SITE_ORIGIN)
        saved = json.loads(self.counts.read_text(encoding="utf-8"))
        today = dt.datetime.now(dt.timezone.utc).date().isoformat()
        self.assertEqual(set(saved[today]), {"page_view", "outbound_click", "outbound_click_asin", "search", "chooser_complete", "guide_read"})

    def test_rejects_bad_origin_payload_content_type_and_oversize_body(self):
        status, headers = self.post({"event": "page_view", "path": "/"}, origin="https://example.invalid")
        self.assertEqual(status, 403)
        self.assertIsNone(headers.get("Access-Control-Allow-Origin"))

        status, _ = self.post({"event": "page_view", "path": "/", "query": "private"})
        self.assertEqual(status, 400)
        status, _ = self.post({"event": "page_view", "path": "/"}, content_type="application/json")
        self.assertEqual(status, 415)
        status, _ = self.post(None, raw=b"x" * (server.MAX_BODY + 1))
        self.assertEqual(status, 413)
        self.assertFalse(self.counts.exists())

    def test_health_and_unknown_route(self):
        self.assertEqual(urlopen(self.url + "/health", timeout=3).read(), b"ok")
        with self.assertRaises(HTTPError) as error:
            urlopen(self.url + "/missing", timeout=3)
        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
