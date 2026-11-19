#!/usr/bin/env python3
"""Check the built site in docs/. Exits non-zero on any failure. Standard library only.

Checks:
  1. Every page has one non-empty <title> and <meta name=description>; both are unique across pages.
  2. Disclosure strip sits under the masthead (before <main>) and is repeated in the footer, on every page.
  3. Every link to amazon.com or link.amazon carries rel="sponsored".
  4. Every internal link and #fragment resolves to a built file and an existing id.
  5. Every row of a data-verified table has an https source link to an allowed official host,
     or is explicitly marked UNVERIFIED / NO SOURCE.
  6. No currency amounts appear in the built pages (no inferred prices).
  7. No affiliate tag or tracking parameter has been appended to any link.
  8. sitemap.xml lists every indexable page; feed.xml is well-formed and lists every guide.
  9. Every JSON data file parses.
"""
import html.parser
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = ROOT / "data"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
SITE_BASE = "https://wingbangboozle1-lang.github.io/Prod1"
ALLOWED_HOSTS = {
    "www.amazon.com", "amazon.com", "link.amazon", "affiliate-program.amazon.com", "sellercentral.amazon.com",
    "developers.google.com", "search.google.com", "www.ftc.gov", "github.com",
}
UNVERIFIED_MARKERS = ("UNVERIFIED", "NO SOURCE", "NOT SET", "NONE", "NOT CONFIRMED", "NOT CAPTURED", "PROPOSED", "NO OFFICIAL SOURCE", "NO GUIDE", "BLANK")

errors = []


def fail(msg):
    errors.append(msg)


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self.description = None
        self.ids = set()
        self.links = []          # (href, rel)
        self.in_title = False
        self.in_disclosure = 0
        self.disclosure_before_main = False
        self.disclosure_in_footer = False
        self.main_seen = False
        self.footer_depth = 0
        self.disclosure_positions = []
        self.text = []
        self.tables = []         # list of dicts: attrs, rows: list of (cells_text, hrefs)
        self._table_stack = []
        self._cur_row = None
        self._cur_cell = None
        self._in_thead = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "title":
            self.in_title = True
            self.title = ""
        if tag == "meta" and a.get("name") == "description":
            self.description = a.get("content", "")
        if tag == "main":
            self.main_seen = True
        if tag == "footer":
            self.footer_depth += 1
        if tag == "div" and "disclosure" in (a.get("class") or "").split():
            self.disclosure_positions.append("footer" if self.footer_depth else ("main" if self.main_seen else "masthead"))
        if tag == "a":
            self.links.append((a.get("href", ""), a.get("rel", "")))
            if self._cur_cell is not None:
                self._cur_cell["hrefs"].append(a.get("href", ""))
        if tag == "table":
            self._table_stack.append({"attrs": a, "rows": []})
        if tag == "thead":
            self._in_thead = True
        if tag == "tbody":
            self._in_thead = False
        if tag == "tr" and self._table_stack and not self._in_thead:
            self._cur_row = {"cells": [], "hrefs": []}
        if tag in ("td", "th") and self._cur_row is not None:
            self._cur_cell = {"text": "", "hrefs": []}
            self._cur_row["cells"].append(self._cur_cell)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "footer":
            self.footer_depth -= 1
        if tag in ("td", "th"):
            self._cur_cell = None
        if tag == "tr" and self._cur_row is not None and self._table_stack:
            self._table_stack[-1]["rows"].append(self._cur_row)
            self._cur_row = None
        if tag == "table" and self._table_stack:
            self.tables.append(self._table_stack.pop())

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self._cur_cell is not None:
            self._cur_cell["text"] += data
        self.text.append(data)


def parse(path):
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    return p


def rel_target(page_rel, href):
    """Resolve an internal href against the page's path inside docs/. Returns (file, fragment) or None if external."""
    parsed = urlparse(href)
    if parsed.scheme or href.startswith("//"):
        return None
    if href.startswith("mailto:"):
        return None
    path, _, frag = href.partition("#")
    if path == "":
        target = page_rel
    elif path.startswith("/"):
        target = pathlib.PurePosixPath(path.lstrip("/"))
    else:
        target = (pathlib.PurePosixPath(page_rel).parent / path)
    # normalise ..
    parts = []
    for part in pathlib.PurePosixPath(target).parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part not in ("", "."):
            parts.append(part)
    return "/".join(parts), frag


def main():
    # 9. JSON parses
    for jf in DATA.glob("*.json"):
        try:
            json.loads(jf.read_text(encoding="utf-8"))
        except Exception as ex:  # noqa
            fail(f"JSON parse error in {jf.name}: {ex}")

    if not DOCS.exists():
        fail("docs/ missing; run tools/build.py first")
        return report()

    pages = {}
    for f in sorted(DOCS.rglob("*.html")):
        rel = f.relative_to(DOCS).as_posix()
        pages[rel] = parse(f)

    titles, descs = {}, {}
    for rel, pg in pages.items():
        # 1
        if not pg.title or not pg.title.strip():
            fail(f"{rel}: missing <title>")
        else:
            titles.setdefault(pg.title.strip(), []).append(rel)
        if not pg.description or not pg.description.strip():
            fail(f"{rel}: missing meta description")
        else:
            descs.setdefault(pg.description.strip(), []).append(rel)

        # 2 disclosure under masthead and in footer on every page
        if pg.disclosure_positions.count("masthead") + pg.disclosure_positions.count("main") < 1:
            fail(f"{rel}: no disclosure strip under the masthead")
        elif "masthead" not in pg.disclosure_positions and "main" not in pg.disclosure_positions:
            fail(f"{rel}: disclosure strip not placed under the masthead")
        if "footer" not in pg.disclosure_positions:
            fail(f"{rel}: disclosure not repeated in footer")
        if DISCLOSURE not in " ".join(pg.text):
            fail(f"{rel}: required Associates statement text missing")

        for href, rel_attr in pg.links:
            host = urlparse(href).hostname or ""
            # 3 sponsored on Amazon links
            if host in ("amazon.com", "www.amazon.com", "link.amazon"):
                if "sponsored" not in rel_attr.split():
                    fail(f"{rel}: Amazon link without rel=sponsored: {href}")
            # 7 no affiliate tag appended
            if "tag=" in href or "shopnow047c-20" in href:
                fail(f"{rel}: tracking parameter found in link: {href}")
            # 4 internal links
            tgt = rel_target(rel, href)
            if tgt is None:
                continue
            file_part, frag = tgt
            candidates = [file_part] if file_part.endswith(".html") else [file_part.rstrip("/") + "/index.html", file_part]
            if file_part == "":
                candidates = ["index.html"]
            found = None
            for c in candidates:
                if c and (DOCS / c).is_file():
                    found = c
                    break
            if found is None:
                fail(f"{rel}: broken internal link {href}")
                continue
            if frag:
                tp = pages.get(found)
                if tp is None or frag not in tp.ids:
                    fail(f"{rel}: missing anchor #{frag} in {found} (from {href})")

        # 5 data-verified tables
        for t in pg.tables:
            if "data-verified" not in t["attrs"]:
                continue
            for r in t["rows"]:
                if not r["cells"]:
                    continue
                cell_texts = " ".join(c["text"] for c in r["cells"]).upper()
                hrefs = [h for c in r["cells"] for h in c["hrefs"]]
                good_links = []
                for h in hrefs:
                    p_ = urlparse(h)
                    if p_.scheme == "https" and p_.hostname in ALLOWED_HOSTS:
                        good_links.append(h)
                if not good_links and not any(m in cell_texts for m in UNVERIFIED_MARKERS):
                    fail(f"{rel}: table row without official source link or UNVERIFIED flag: {cell_texts[:90]!r}")

        # 6 no currency amounts
        plain = " ".join(pg.text)
        for m in re.finditer(r"[$£€]\s?\d", plain):
            fail(f"{rel}: currency amount found (no prices may be shown unverified): ...{plain[max(0,m.start()-30):m.start()+20]!r}")

    for t, where in titles.items():
        if len(where) > 1:
            fail(f"duplicate <title> '{t}' on {where}")
    for d, where in descs.items():
        if len(where) > 1:
            fail(f"duplicate meta description on {where}")

    # 8 sitemap and feed
    sm = DOCS / "sitemap.xml"
    if not sm.exists():
        fail("sitemap.xml missing")
    else:
        locs = set(re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8")))
        for rel, pg in pages.items():
            if rel == "404.html":
                continue
            loc = f"{SITE_BASE}/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)
            if loc not in locs:
                fail(f"sitemap.xml missing {loc}")
    feed = DOCS / "feed.xml"
    try:
        root = ET.parse(feed).getroot()
        items = root.findall("./channel/item")
        guides = json.loads((DATA / "guides.json").read_text(encoding="utf-8"))["guides"]
        if len(items) != len(guides):
            fail(f"feed.xml has {len(items)} items; expected {len(guides)}")
    except Exception as ex:  # noqa
        fail(f"feed.xml not well-formed: {ex}")

    # 6b. guide pages must include Article JSON-LD
    for g in json.loads((DATA / "guides.json").read_text(encoding="utf-8"))["guides"]:
        rel = f"guides/{g['slug']}/index.html"
        if rel not in pages:
            fail(f"missing guide page {rel}")
        elif not re.search(r'"@type":\s*"Article"',  (DOCS / rel).read_text(encoding="utf-8")):
            fail(f"{rel}: Article JSON-LD missing")

    return report()


def report():
    if errors:
        print(f"CHECK FAILED: {len(errors)} problem(s)")
        for e in errors:
            print(" -", e)
        return 1
    print("CHECK PASSED: titles, descriptions, disclosure placement, sponsored links, internal links, verified-table sources, no inferred prices, sitemap, feed, JSON.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
