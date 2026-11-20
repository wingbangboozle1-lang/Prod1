#!/usr/bin/env python3
"""Contract self-test for analytics-endpoint/server.py — no network, no server started.

Confirms the endpoint accepts exactly the site's five defined events and the client
payload shape that assets/app.js sends, and that malformed input is rejected. Also
confirms the privacy property that counts survive with no per-event timestamps.
Run by scripts/check_measure.mjs in CI and by hand: python3 analytics-endpoint/selftest.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import server  # noqa: E402

FIVE = ["page_view", "outbound_click", "search", "chooser_complete", "guide_read"]
failures: list[str] = []


def check(ok: bool, label: str) -> None:
    print(("PASS " if ok else "FAIL ") + label)
    if not ok:
        failures.append(label)


# 1. The contract: EVENT_NAMES is exactly the five defined events.
check(sorted(server.EVENT_NAMES) == sorted(FIVE), "EVENT_NAMES == the five defined events")

# 2. The client envelope that assets/app.js sends validates for every event.
# `data` carries both the search query and the three chooser answers, because one fixture is
# used for all five events; the endpoint only reads the fields its event documents
# (analytics-endpoint/README.md), so extra keys are ignored rather than trusted.
client_envelope = {
    "event": "", "path": "/Prod1/guide-basket-vs-oven.html",
    "page": "/Prod1/guide-basket-vs-oven.html", "ts": "2026-11-20T00:00:00.000Z",
    "asin": "B0CDY277D3",
    "data": {"q": "capacity", "q1": "snacks", "q2": "compact", "q3": "budget"},
}
for name in FIVE:
    payload = dict(client_envelope, event=name)
    ok, reason = server.validate(payload)
    check(ok, f"client envelope validates for {name}" + (f" ({reason})" if reason else ""))

# 3. Malformed input is rejected.
cases = [
    ({"event": "guide_read_75", "path": "/Prod1/"}),                     # old vocabulary, gone
    ({"event": "conversion_signal", "path": "/Prod1/"}),                 # never a client event
    ({"event": "page_view", "path": "/Prod1/index.html?q=x"}),           # query not allowed in path
    ({"event": "page_view", "path": "Prod1/index.html"}),                # path must start with /
    ({"event": "page_view", "path": "/Prod1/", "asin": "not-an-asin"}),
    ({"event": "chooser_complete", "path": "/Prod1/", "data": {"q1": "snacks"}}),   # a partial answer set cannot be read as a decision
    ({"event": "search", "path": "/Prod1/", "data": {"q": "x" * 200}}),             # query length is bounded at the door
    ({"event": "outbound_click", "path": "/Prod1/", "data": {}}),                   # a click with no ASIN is unattributable
    ({"event": "page_view"}),
    ("page_view"),
]
for c in cases:
    ok, _ = server.validate(c)
    check(not ok, f"rejects {json.dumps(c)[:70]}")

# 4. record() writes daily counts and no per-event timestamps; ASINs bucket separately.
with tempfile.TemporaryDirectory() as td:
    counts = pathlib.Path(td) / "counts.json"
    server.record(counts, {"event": "outbound_click", "path": "/Prod1/air-fryers.html", "asin": "B0CDY277D3"}, today="2026-11-20")
    server.record(counts, {"event": "outbound_click", "path": "/Prod1/air-fryers.html", "asin": "B0CDY277D3"}, today="2026-11-20")
    server.record(counts, {"event": "page_view", "path": "/Prod1/", "data": {"q": "private words"}}, today="2026-11-20")
    data = json.loads(counts.read_text(encoding="utf-8"))
    day = data.get("2026-11-20", {})
    check(day.get("outbound_click", {}).get("/Prod1/air-fryers.html") == 2, "daily per-path counts recorded")
    check(day.get("outbound_click_asin", {}).get("B0CDY277D3") == 2, "outbound_click buckets by ASIN")
    raw = counts.read_text(encoding="utf-8")
    check("private words" not in raw, "no query text stored")
    check(not re.search(r'"ts"|timestamp', raw), "no per-event timestamps stored")

print(("\nSELFTEST FAILED: " + "; ".join(failures)) if failures else "\nSELFTEST PASSED")
sys.exit(1 if failures else 0)
