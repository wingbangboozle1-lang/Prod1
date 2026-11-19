#!/usr/bin/env python3
"""Validate the curated artifact that the GitHub Pages workflow will upload."""
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE = "https://wingbangboozle1-lang.github.io/Prod1/"
EXPECTED_HTML = {
    "index.html", "air-fryers.html", "thermometers.html", "compare.html", "guides.html",
    "guide-basket-vs-oven.html", "guide-capacity-checklist.html", "guide-cleanup-counter-space.html",
    "guide-multifunction-questions.html", "guide-thermometer-accuracy.html", "executive-summary.html",
    "suggestions.html", "verification.html", "flagged.html", "compliance.html", "methodology.html", "search.html",
}
INDEXABLE = {"index.html", "air-fryers.html", "thermometers.html", "compare.html", "guides.html"}
NOINDEX = {"search.html", "executive-summary.html", "suggestions.html", "verification.html", "flagged.html", "compliance.html", "methodology.html"}
XML_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.canonicals = []
        self.og_urls = []
        self.robots = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag.lower() == "head":
            self.in_head = True
        if not self.in_head:
            return
        if tag.lower() == "link" and values.get("rel", "").lower() == "canonical":
            self.canonicals.append(values.get("href", ""))
        if tag.lower() == "meta" and values.get("property", "").lower() == "og:url":
            self.og_urls.append(values.get("content", ""))
        if tag.lower() == "meta" and values.get("name", "").lower() == "robots":
            self.robots.append(values.get("content", ""))

    def handle_endtag(self, tag):
        if tag.lower() == "head":
            self.in_head = False


class TablesParser(HTMLParser):
    """Collect table rows and whether each row cites a direct Amazon product page."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self.table_depth = 0
        self.current_table = None
        self.current_row = None
        self.current_cell = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)
        if tag == "table":
            if self.table_depth == 0:
                self.current_table = []
            self.table_depth += 1
        elif tag == "tr" and self.table_depth and self.current_row is None:
            self.current_row = {"cells": [], "has_source": False, "header": False}
        elif tag in ("td", "th") and self.current_row is not None:
            self.current_cell = ""
            if tag == "th":
                self.current_row["header"] = True
        elif tag == "a" and self.current_row is not None:
            href = attrs.get("href", "")
            if href.startswith("https://www.amazon.com/dp/"):
                self.current_row["has_source"] = True

    def handle_data(self, data):
        if self.current_cell is not None:
            self.current_cell += data

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("td", "th") and self.current_row is not None and self.current_cell is not None:
            self.current_row["cells"].append(self.current_cell.strip())
            self.current_cell = None
        elif tag == "tr" and self.current_table is not None and self.current_row is not None:
            self.current_table.append(self.current_row)
            self.current_row = None
        elif tag == "table" and self.table_depth:
            self.table_depth -= 1
            if self.table_depth == 0 and self.current_table is not None:
                self.tables.append(self.current_table)
                self.current_table = None


def fail(message: str) -> None:
    raise SystemExit("publication artifact check failed: " + message)


def canonical_for(name: str) -> str:
    return BASE if name == "index.html" else BASE + name


def get_tables(path: Path):
    parser = TablesParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.tables


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="_site", help="curated Pages artifact directory")
    parser.add_argument("--manifest", default=str(PROJECT_ROOT / "data" / "guides.json"))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    guides = manifest.get("guides", [])
    guide_paths = [item.get("path", "") for item in guides]
    if len(guide_paths) != len(set(guide_paths)):
        fail("guide manifest contains duplicate feed paths")

    if not root.is_dir():
        fail(f"artifact directory does not exist: {root}")
    found_html = {path.name for path in root.glob("*.html")}
    if found_html != EXPECTED_HTML:
        fail(f"artifact HTML set differs; missing={sorted(EXPECTED_HTML - found_html)}, extra={sorted(found_html - EXPECTED_HTML)}")
    if any((root / name).exists() for name in ("docs", "articles", "counter-check")):
        fail("secondary publication output was included in the primary artifact")
    for directory in ("assets", "data"):
        if not (root / directory).is_dir():
            fail(f"missing artifact directory: {directory}")
    for name in ("assets/app.js", "assets/style.css", "assets/og-image.svg", "data/search-index.json", "sitemap.xml", "feed.xml", "robots.txt", ".nojekyll"):
        if not (root / name).is_file():
            fail(f"missing publication file: {name}")

    canonical_urls = set()
    for name in sorted(EXPECTED_HTML):
        page_text = (root / name).read_text(encoding="utf-8")
        if "{source_links(" in page_text or "{VERIFIED}" in page_text:
            fail(f"{name}: unresolved publication template token")
        head = HeadParser()
        head.feed(page_text)
        expected = canonical_for(name)
        if head.canonicals != [expected]:
            fail(f"{name}: expected one self-canonical {expected!r}; found {head.canonicals!r}")
        if head.og_urls != [expected]:
            fail(f"{name}: expected one matching og:url; found {head.og_urls!r}")
        if expected in canonical_urls:
            fail(f"duplicate canonical URL: {expected}")
        canonical_urls.add(expected)
        if name in NOINDEX:
            if head.robots != ["noindex,follow"]:
                fail(f"{name}: expected robots noindex,follow")
        elif head.robots:
            fail(f"{name}: indexable page has an unexpected robots directive {head.robots!r}")

    sitemap = ET.parse(root / "sitemap.xml").getroot()
    sitemap_urls = [element.text or "" for element in sitemap.findall("sm:url/sm:loc", XML_NS)]
    expected_sitemap = {canonical_for(name) for name in INDEXABLE}
    expected_sitemap.update(BASE + path for path in guide_paths)
    if len(sitemap_urls) != len(set(sitemap_urls)) or set(sitemap_urls) != expected_sitemap:
        fail(f"sitemap URLs differ from the buyer-facing page set; found={sorted(sitemap_urls)}")

    rss = ET.parse(root / "feed.xml").getroot()
    channel = rss.find("channel")
    if channel is None:
        fail("RSS feed has no channel")
    feed_items = channel.findall("item")
    feed_links = [item.findtext("link", default="") for item in feed_items]
    expected_feed = [BASE + path for path in guide_paths]
    if feed_links != expected_feed:
        fail(f"RSS item order/URLs do not match data/guides.json: {feed_links!r}")
    for item, guide in zip(feed_items, guides):
        if item.findtext("title") != guide["title"] or not item.findtext("description"):
            fail(f"RSS metadata differs for {guide['path']}")

    robots_text = (root / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {BASE}sitemap.xml" not in robots_text:
        fail("robots.txt does not point at the root sitemap")

    product_table_pages = {
        "air-fryers.html", "thermometers.html", "compare.html", "executive-summary.html",
        "guide-basket-vs-oven.html", "guide-capacity-checklist.html", "guide-cleanup-counter-space.html",
        "guide-multifunction-questions.html",
    }
    for name in product_table_pages:
        tables = get_tables(root / name)
        if not tables:
            fail(f"{name}: expected source-backed product table")
        for table_number, rows in enumerate(tables, 1):
            for row_number, row in enumerate(rows, 1):
                if row["header"]:
                    continue
                if not row["has_source"]:
                    fail(f"{name}: product-table row {table_number}.{row_number} lacks a direct listing source")

    verification_tables = get_tables(root / "verification.html")
    if len(verification_tables) < 5:
        fail("verification register must contain five product source tables")
    non_product_fields = {
        "Submitted short link", "Intended ASIN", "Official listing URL for intended product",
        "Intent confirmation date", "Intent confirmation source",
    }
    for table_number, rows in enumerate(verification_tables[:5], 1):
        for row_number, row in enumerate(rows, 1):
            if row["header"] or (row["cells"] and row["cells"][0] in non_product_fields):
                continue
            if not row["has_source"]:
                fail(f"verification.html: factual product record row {table_number}.{row_number} lacks its listing source")

    flagged_rows = {}
    for row in get_tables(root / "flagged.html")[0]:
        if row["cells"]:
            flagged_rows[row["cells"][0]] = row
    for flag_id in ("FLG-002", "FLG-004", "FLG-005", "FLG-006", "FLG-012", "FLG-016", "FLG-020"):
        row = flagged_rows.get(flag_id)
        if not row or not row["has_source"]:
            fail(f"flagged.html: {flag_id} product note lacks a direct listing source")

    js = (root / "assets" / "app.js").read_text(encoding="utf-8")
    endpoint = (PROJECT_ROOT / "analytics-endpoint" / "server.py").read_text(encoding="utf-8")
    events = ("page_view", "outbound_click", "search", "chooser_complete", "guide_read")
    for event in events:
        if event not in js or event not in endpoint:
            fail(f"client/server analytics event is missing: {event}")
    if 'rel="sponsored nofollow noopener"' not in js or "data-ctg-outbound" not in js:
        fail("dynamic shortlist links are missing sponsored-link analytics attributes")
    if 'data-analytics-endpoint=""' not in (root / "index.html").read_text(encoding="utf-8"):
        fail("analytics endpoint must remain disabled until hosting/privacy review")

    print(f"Publication artifact passed: {len(EXPECTED_HTML)} pages, {len(expected_sitemap)} sitemap URLs, {len(guide_paths)} RSS items; secondary publications excluded.")


if __name__ == "__main__":
    main()
