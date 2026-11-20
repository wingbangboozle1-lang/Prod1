#!/usr/bin/env python3
"""Contract test: the events the site fires are the events the endpoint accepts.

Why this exists: the site documents exactly five events (data/editorial.json -> events.five),
the browser client in assets/app.js fires them, and analytics-endpoint/server.py validates
them. Three places, one agreement - and an earlier session found the client and the endpoint
disagreeing on names, which no reader would ever see but which would silently discard every
count on the day measurement was switched on. This script makes that disagreement a build
failure instead of a discovery.

It runs offline, imports no third-party packages, and transmits nothing.

Usage: python3 scripts/test_event_contract.py
"""
from __future__ import annotations

import ast
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analytics-endpoint"))
import server  # noqa: E402  (the module under test)

fails: list[str] = []


def check(ok: bool, label: str) -> None:
    print(("  ok   " if ok else "  FAIL ") + label)
    if not ok:
        fails.append(label)


edit = json.loads((ROOT / "data" / "editorial.json").read_text(encoding="utf-8"))
documented = [e["name"] for e in edit["events"]["five"]]
client_js = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")
fired = sorted(set(re.findall(r'track\("([a-z_]+)"', client_js)))
declared = sorted(set(ast.literal_eval(re.search(r"var EVENTS = (\[[^\]]+\])", client_js).group(1))))

print("event names")
check(sorted(documented) == declared, f"client EVENTS array matches the documented five: {declared}")
check(fired == sorted(documented), f"app.js fires exactly the documented five: {fired}")
check(set(documented) == set(server.EVENT_NAMES), f"endpoint EVENT_NAMES matches the documented five: {sorted(server.EVENT_NAMES)}")

print("payloads the client actually builds")
# The client sends location.pathname: no query string, no fragment. Paths below follow that.
P, C, G = "/guide-price-check.html", "/index.html", "/air-fryers.html"
cases = [
    (True, "page_view", {"event": "page_view", "path": G, "page": G, "ts": "2026-11-20T00:00:00.000Z", "data": {}}),
    (True, "outbound_click", {"event": "outbound_click", "path": G, "asin": "B0CDY277D3", "data": {"asin": "B0CDY277D3"}}),
    (True, "search", {"event": "search", "path": P, "data": {"q": "dual basket air fryer"}}),
    (True, "chooser_complete", {"event": "chooser_complete", "path": P,
                                "data": {"q1": "family", "q2": "standard", "q3": "mid"}}),
    (True, "guide_read", {"event": "guide_read", "path": P, "data": {"page": P}}),
    (False, "outbound_click without an asin", {"event": "outbound_click", "path": G, "data": {}}),
    (False, "outbound_click with a 9-character code", {"event": "outbound_click", "path": G, "asin": "B04G1MEwY", "data": {}}),
    (False, "search with an empty query", {"event": "search", "path": P, "data": {"q": ""}}),
    (False, "search with an 81-character query", {"event": "search", "path": P, "data": {"q": "x" * 81}}),
    (False, "chooser_complete with an invented answer", {"event": "chooser_complete", "path": P, "data": {"q1": "cheap", "q2": "standard", "q3": "mid"}}),
    (False, "a sixth event", {"event": "purchase", "path": P, "data": {}}),
    (False, "an old endpoint-only name (guide_read_75)", {"event": "guide_read_75", "path": P, "data": {}}),
    (False, "no path", {"event": "page_view", "data": {}}),
    (False, "path with a query string", {"event": "page_view", "path": "/x.html?a=1", "data": {}}),
    (False, "path with a fragment", {"event": "outbound_click", "path": "/x.html#P1", "asin": "B0CDY277D3", "data": {}}),
    (False, "a non-object body", ["page_view"]),
]
for want, label, payload in cases:
    ok, reason = server.validate(payload)
    check(ok == want, f"{label}: {'accepted' if want else 'refused'}" + (f" ({reason})" if reason and not want else ""))

print("retention and privacy shape")
src = (ROOT / "analytics-endpoint" / "server.py").read_text(encoding="utf-8")
check("request.log_message" not in src and "def log_message" in src, "the handler overrides log_message, so no request line is written")
check(all(k not in src for k in ("headers.get(\"User-Agent", "X-Forwarded-For")), "no user-agent or forwarded-for value is read")
body = json.dumps({"event": "page_view", "path": G, "page": G, "ts": "2026-11-20T00:00:00.000Z", "data": {}}, separators=(",", ":"))
check(len(body.encode()) <= server.MAX_BODY, f"the largest client payload fits MAX_BODY ({len(body)} of {server.MAX_BODY} bytes)")
check(edit["events"]["endpoint"] == "", f'endpoint stays unset in this build ({edit["events"]["endpoint"]!r}): the site sends nothing')

if fails:
    print(f"\nFAILED: {len(fails)} item(s). The client and the endpoint do not agree; do not host the endpoint until this passes.\n")
    sys.exit(1)
print("\nPASS: the documented five, the client and the endpoint agree; every payload is bounded.\n")
