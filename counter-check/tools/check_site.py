#!/usr/bin/env python3
"""Publishing gate for counter-check/site/. Exits non-zero if any check fails.

Checks:
  1. Disclosure strip under the masthead and repeated in the footer, on every page.
  2. Every link to amazon.com or link.amazon is rel="sponsored".
  3. Every buy link to an amazon.com product page carries tag=shopnow047c-20.
  4. Each product table row links to an amazon.com listing.
  5. No internal link is broken; fragment anchors on flagged/questions pages exist.
  6. Every page is listed in sitemap.xml; each page has a unique title and meta description.
  7. No currency amounts or star ratings appear on product or guide pages.
  8. Every flag ID referenced in data exists in flags.json.
Run after tools/build_site.py.
"""
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "site")
DATA = os.path.join(ROOT, "data")
BASE = "https://wingbangboozle1-lang.github.io/Prod1/counter-check/site/"
TAG = "shopnow047c-20"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
BUY_PAGES = {"index.html", "shop/air-fryers.html", "shop/kitchen-thermometers.html"}
CONTENT_PAGES_NO_PRICE = BUY_PAGES | {"guides/index.html"} | {
    f"guides/{f}" for f in os.listdir(os.path.join(DOCS, "guides")) if f.endswith(".html") and f != "index.html"}

errors = []


def fail(msg):
    errors.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors = []      # (href, rel, in_table_row, cls)
        self.ids = set()
        self.title = ""
        self.meta_desc = ""
        self._in_title = False
        self._tr_depth = 0
        self._in_table_tbody = 0
        self.rows_with_listing = 0
        self.table_rows = 0
        self._row_has_listing = False
        self._in_row = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "title":
            self._in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.meta_desc = a.get("content", "")
        if tag == "tbody":
            self._in_table_tbody += 1
        if tag == "tr" and self._in_table_tbody:
            self._in_row = True
            self._row_has_listing = False
            self.table_rows += 1
        if tag == "a" and "href" in a:
            self.anchors.append((a["href"], a.get("rel", ""), self._in_row, a.get("class", "")))
            if self._in_row and "amazon.com/dp/" in a["href"]:
                self._row_has_listing = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "tbody":
            self._in_table_tbody -= 1
        if tag == "tr" and self._in_row:
            if self._row_has_listing:
                self.rows_with_listing += 1
            self._in_row = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def pages():
    out = []
    for dp, _, files in os.walk(DOCS):
        for f in files:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dp, f), DOCS).replace(os.sep, "/"))
    return sorted(out)


def main():
    flags = {f["id"] for f in json.load(open(os.path.join(DATA, "flags.json")))["flags"]}
    products = json.load(open(os.path.join(DATA, "products.json")))["products"]
    sitemap = open(os.path.join(DOCS, "sitemap.xml"), encoding="utf-8").read()
    sitemap_urls = set(re.findall(r"<loc>(.*?)</loc>", sitemap))

    all_pages = pages()
    parsed = {}
    titles, descs = {}, {}
    for rel_path in all_pages:
        raw = open(os.path.join(DOCS, rel_path), encoding="utf-8").read()
        p = Page()
        p.feed(raw)
        parsed[rel_path] = (p, raw)

        # 1. disclosure strip under masthead and in footer
        strip = re.search(r'<div class="disclosure-strip"[^>]*>(.*?)</div>\s*</div>', raw, re.S)
        footer = raw.split("<footer", 1)[-1] if "<footer" in raw else ""
        if not strip or DISCLOSURE not in strip.group(1):
            fail(f"{rel_path}: disclosure missing from the strip under the masthead")
        if "<main" in raw and raw.index("disclosure-strip") > raw.index("<main"):
            fail(f"{rel_path}: disclosure strip is not above main content")
        if DISCLOSURE not in footer:
            fail(f"{rel_path}: disclosure missing from the footer")

        # 2 and 3. Amazon links sponsored, product buy links tagged
        for href, rel_attr, _, cls in p.anchors:
            host = urlparse(href).netloc.lower()
            if host.endswith("amazon.com") or host == "link.amazon":
                if "sponsored" not in rel_attr.split():
                    fail(f"{rel_path}: Amazon link not rel=sponsored: {href[:80]}")
            if rel_path in BUY_PAGES and host.endswith("amazon.com") and "/dp/" in href and "cite" not in cls.split():
                if f"tag={TAG}" not in href:
                    fail(f"{rel_path}: buy link without tag: {href[:80]}")

        # 4. table rows sourced
        if rel_path.startswith("shop/"):
            expected = sum(1 for x in products if rel_path.startswith("shop/") and (
                ("air-fryers" in rel_path and x["category"] == "air-fryers") or
                ("thermometers" in rel_path and x["category"] == "kitchen-thermometers")))
            if p.table_rows and p.rows_with_listing != p.table_rows:
                fail(f"{rel_path}: {p.table_rows - p.rows_with_listing} table row(s) lack an amazon.com listing source link")
            if expected and p.table_rows and p.table_rows != expected:
                fail(f"{rel_path}: expected {expected} product rows, found {p.table_rows}")

        titles[rel_path] = p.title.strip()
        descs[rel_path] = p.meta_desc.strip()
        if not p.title.strip():
            fail(f"{rel_path}: missing title")
        if not p.meta_desc.strip():
            fail(f"{rel_path}: missing meta description")

        # 7. no prices or ratings on product/guide pages
        if rel_path in CONTENT_PAGES_NO_PRICE:
            text = re.sub(r"<[^>]+>", " ", raw)
            if re.search(r"[$£€]\s?\d", text):
                fail(f"{rel_path}: currency amount found (prices are withheld by policy)")
            if re.search(r"\b\d(\.\d)?\s*(out of 5|stars?)\b", text, re.I):
                fail(f"{rel_path}: star rating found (ratings are withheld by policy)")

    # 5. internal links and fragments
    for rel_path, (p, _) in parsed.items():
        here = os.path.dirname(rel_path)
        for href, _, _, _ in p.anchors:
            if href.startswith(("http://", "https://", "mailto:", "#")) or not href:
                continue
            target, _, frag = href.partition("#")
            target_path = os.path.normpath(os.path.join(here, target)).replace(os.sep, "/")
            if target_path not in parsed and not os.path.exists(os.path.join(DOCS, target_path)):
                fail(f"{rel_path}: broken internal link -> {href}")
                continue
            if frag and target_path in parsed and frag not in parsed[target_path][0].ids:
                fail(f"{rel_path}: missing anchor #{frag} in {target_path}")

    # 6. sitemap coverage and unique titles/descriptions
    for rel_path in all_pages:
        if rel_path == "index.html":
            url = BASE
        else:
            url = BASE + rel_path
        if url not in sitemap_urls:
            fail(f"{rel_path}: not listed in sitemap.xml")
    if len(set(titles.values())) != len(titles):
        fail("duplicate page titles")
    if len(set(descs.values())) != len(descs):
        fail("duplicate meta descriptions")

    # 8. flag references
    refs = set()
    for name in ("products.json", "questions.json"):
        raw = open(os.path.join(DATA, name), encoding="utf-8").read()
        refs |= set(re.findall(r"\b(P-\d{2})\b", raw))
    missing = refs - flags
    if missing:
        fail(f"flag IDs referenced but not defined: {sorted(missing)}")

    # 9. tagged URLs in data
    for x in products:
        if f"tag={TAG}" not in x["tagged_outbound_url"]:
            fail(f"{x['id']}: tagged_outbound_url lacks tag={TAG}")

    print(f"Checked {len(all_pages)} pages, {len(products)} products, {len(flags)} flags.")
    if errors:
        print(f"FAILED: {len(errors)} problem(s)")
        for e in errors:
            print(" - " + e)
        return 1
    print("PASSED: disclosure, sponsored links, tags, sources, links, sitemap, metadata, policy checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
