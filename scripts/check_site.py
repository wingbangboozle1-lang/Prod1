#!/usr/bin/env python3
"""Dependency-free sanity checks for the static Counterwise publication."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PRODUCTS = [
    "https://link.amazon/B04G1MEwY",
    "https://link.amazon/B02NbDxp3",
    "https://link.amazon/B00hJ57DV",
    "https://link.amazon/B0c8moW59",
    "https://link.amazon/B0f3GKalj",
]
BASE = "https://wingbangboozle1-lang.github.io/Prod1/"


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.title_open = False
        self.disclosure_depth = 0
        self.disclosure_text = ""
        self.sponsored_links: set[str] = set()
        self.footer_statement = False
        self._footer_text = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if a.get("href"):
            href = a["href"] or ""
            self.links.append(href)
            if "sponsored" in (a.get("rel") or "").split():
                self.sponsored_links.add(href)
        if a.get("id"):
            self.ids.add(a["id"] or "")
        if tag == "title":
            self.title_open = True
        if tag == "meta" and a.get("name") == "description":
            self.description = a.get("content") or ""
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href") or ""
        if tag == "div" and "disclosure" in (a.get("class") or "").split():
            self.disclosure_depth += 1
        if tag == "footer":
            self._footer_text = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title_open = False
        if tag == "div" and self.disclosure_depth:
            self.disclosure_depth -= 1
        if tag == "footer":
            self._footer_text = False

    def handle_data(self, data: str) -> None:
        if self.title_open:
            self.title += data
        if self.disclosure_depth:
            self.disclosure_text += data
        if self._footer_text and "As an Amazon Associate I earn from qualifying purchases." in data:
            self.footer_statement = True


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    pages = sorted(ROOT.rglob("*.html"))
    page_records: dict[Path, Page] = {}
    titles: set[str] = set()
    descriptions: set[str] = set()
    for path in pages:
        rel = path.relative_to(ROOT)
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        page_records[path] = page
        if not page.title.strip():
            fail(f"{rel}: missing title", errors)
        if page.title in titles:
            fail(f"{rel}: duplicate title: {page.title}", errors)
        titles.add(page.title)
        if len(page.description.strip()) < 30:
            fail(f"{rel}: missing or short meta description", errors)
        if page.description in descriptions:
            fail(f"{rel}: duplicate meta description", errors)
        descriptions.add(page.description)
        if not page.canonical.startswith(BASE):
            fail(f"{rel}: missing or unexpected canonical URL: {page.canonical}", errors)
        if "Affiliate disclosure:" not in page.disclosure_text:
            fail(f"{rel}: disclosure strip is absent", errors)
        if not page.footer_statement:
            fail(f"{rel}: Associates disclosure statement is absent from footer", errors)
        for href in page.links:
            parsed = urlparse(href)
            if parsed.scheme or href.startswith("//") or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                fail(f"{rel}: broken local link {href}", errors)
            elif parsed.fragment and target.suffix == ".html":
                destination = Page()
                destination.feed(target.read_text(encoding="utf-8"))
                if unquote(parsed.fragment) not in destination.ids:
                    fail(f"{rel}: missing fragment target in {href}", errors)

    home = page_records.get(ROOT / "index.html")
    if home:
        for product in EXPECTED_PRODUCTS:
            if product not in home.sponsored_links:
                fail(f"Homepage product link is missing sponsored rel: {product}", errors)

    # Keep machine-readable discovery files syntactically valid and tied to this site.
    try:
        sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        listed = {node.text for node in sitemap.findall("s:url/s:loc", ns)}
        for page_path in pages:
            rel = page_path.relative_to(ROOT).as_posix()
            if rel == "index.html":
                suffix = ""
            elif rel == "guides/index.html":
                suffix = "guides/"
            elif rel == "review/index.html":
                suffix = "review/"
            else:
                suffix = rel
            expected = BASE + suffix
            if expected not in listed:
                fail(f"sitemap.xml: missing {expected}", errors)
    except (ET.ParseError, OSError) as exc:
        fail(f"sitemap.xml: invalid XML ({exc})", errors)

    try:
        feed = ET.parse(ROOT / "feed.xml").getroot()
        if feed.findtext("channel/link") != BASE:
            fail("feed.xml: channel link does not match site base", errors)
        if not feed.findall("channel/item"):
            fail("feed.xml: no guide entries", errors)
    except (ET.ParseError, OSError) as exc:
        fail(f"feed.xml: invalid XML ({exc})", errors)

    if errors:
        print("Site checks failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"PASS: {len(pages)} HTML pages; unique titles/descriptions; canonical URLs; disclosures; local links/fragments; sponsored product links; sitemap; RSS feed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
