#!/usr/bin/env node
/* The Countertop Guide - publishing gate.
 *
 * Why this exists: a rule that is not checked is a preference. This script runs in the
 * Pages workflow before the artifact is uploaded, so a page that breaks the disclosure,
 * the sponsored marking, the metadata, the voice rules or the price policy cannot deploy.
 *
 * Zero dependencies on purpose - the workflow must run on a clean checkout with no install.
 * It parses with regular expressions, not a DOM, so it is a gate on patterns, not a proof
 * of structure. Known blind spots are listed at the bottom of this header:
 *   - it does not execute JavaScript, so it checks the client source text instead;
 *   - it does not render CSS, so visual regressions still need a human.
 *
 * Usage: node scripts/check_meta.mjs [--root DIR] [--quiet]
 */
import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join, basename } from "node:path";

const args = process.argv.slice(2);
const ROOT = args.includes("--root") ? args[args.indexOf("--root") + 1] : process.cwd();
const QUIET = args.includes("--quiet");
const BASE = JSON.parse(readFileSync(join(ROOT, "data/editorial.json"), "utf8")).baseUrl.replace(/\/$/, "");
const DATA = JSON.parse(readFileSync(join(ROOT, "data/products.json"), "utf8"));
const EDIT = JSON.parse(readFileSync(join(ROOT, "data/editorial.json"), "utf8"));
const REQUIRED_DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases.";
const SHOP_PAGES = ["index.html", "air-fryers.html", "thermometers.html", "compare.html", "about.html"];
const READER_PAGES = [...SHOP_PAGES, ...readdirSync(ROOT).filter((f) => /^guide[-a-z]*\.html$/.test(f))];

let fails = [], warns = [], checkedPages = [];

const read = (f) => readFileSync(join(ROOT, f), "utf8");
const stripTags = (h) => h.replace(/<script[\s\S]*?<\/script>/g, " ").replace(/<style[\s\S]*?<\/style>/g, " ")
  .replace(/<[^>]+>/g, " ").replace(/&mdash;|&ndash;/g, "-").replace(/&[a-z#0-9]+;/g, " ").replace(/\s+/g, " ");
/* A marketing claim can hide in an attribute - the search snippet and alt text are exactly
   where slop survives - so the voice check sees body text AND those values. */
const textOf = (h) => {
  const attrs = [
    ...[...h.matchAll(/<meta[^>]*(?:name|property)="(?:description|og:description|og:title|twitter:title|twitter:description|article:[a-z_]+)"[^>]*content="([^"]{4,})"/g)].map((m) => m[1]),
    ...[...h.matchAll(/\b(?:alt|title)="([^"]{4,})"/g)].map((m) => m[1]),
  ].join(" ");
  return stripTags(h) + " " + stripTags(attrs);
};
const fail = (m) => fails.push(m);
const warn = (m) => warns.push(m);

/* ---------- which files are ours ---------- */
const pages = readdirSync(ROOT).filter((f) => f.endsWith(".html") && existsSync(join(ROOT, f)) && statSync(join(ROOT, f)).isFile());
checkedPages = pages;
if (!pages.length) fail("no HTML pages found - did the build run?");

/* ---------- 1. head metadata ---------- */
const titles = new Map(), descs = new Map();
for (const p of pages) {
  const h = read(p);
  const t = (h.match(/<title>([^<]*)<\/title>/) || [])[1] || "";
  const d = (h.match(/<meta name="description" content="([^"]*)"/) || [])[1] || "";
  if (!t) fail(`${p}: no <title>`);
  if (t.length > 68) warn(`${p}: title is ${t.length} chars; search results truncate near 60`);
  if (!d) fail(`${p}: no meta description`);
  if (d && (d.length < 60 || d.length > 165)) warn(`${p}: description is ${d.length} chars (aim 70-160)`);
  if (titles.has(t)) fail(`duplicate <title> shared by ${titles.get(t)} and ${p} - every page needs its own`);
  titles.set(t, p);
  if (descs.has(d)) fail(`duplicate meta description on ${p}`);
  descs.set(d, p);

  const canon = (h.match(/rel="canonical" href="([^"]+)"/) || [])[1] || "";
  const want = p === "index.html" ? BASE + "/" : `${BASE}/${p}`;
  if (!canon) fail(`${p}: no canonical link`);
  else if (canon !== want) fail(`${p}: canonical is ${canon}, expected ${want} (self-referential, absolute)`);
  else if (/example\.com/.test(canon)) fail(`${p}: placeholder canonical`);

  for (const prop of ["og:title", "og:description", "og:url", "og:image"]) {
    const v = (h.match(new RegExp(`property="${prop}" content="([^"]*)"`)) || [])[1] || "";
    if (!v) fail(`${p}: missing ${prop}`);
    else if ((prop === "og:url" || prop === "og:image") && !/^https?:\/\//.test(v)) fail(`${p}: ${prop} must be absolute for social crawlers, got ${v}`);
  }
  const img = (h.match(/property="og:image" content="([^"]*)"/) || [])[1] || "";
  if (img) {
    if (/\.(svg|gif)$/i.test(img)) fail(`${p}: og:image is ${img.split(".").pop()}; share crawlers need a raster (png/jpg)`);
    const local = img.replace(BASE + "/", "");
    if (local.startsWith("assets") && !existsSync(join(ROOT, local))) fail(`${p}: og:image file missing on disk (${local})`);
  }
  if (!/name="viewport"/.test(h)) fail(`${p}: no viewport meta`);
  if (!/application\/ld\+json/.test(h)) fail(`${p}: no structured data block`);
  for (const bad of ["example.com", "TODO", "FIXME", "Lorem ipsum"]) if (h.includes(bad)) fail(`${p}: contains ${bad}`);
}

/* ---------- 2. disclosure + sponsored marking ---------- */
for (const p of pages) {
  const h = read(p);
  const body = h.slice(h.indexOf("<body"), h.indexOf("</body>"));
  if (!body.includes(REQUIRED_DISCLOSURE)) fail(`${p}: the Operating Agreement sentence is missing verbatim (Section 5)`);
  const stripAt = body.indexOf("disclosure-strip");
  const mainAt = body.indexOf("</main>");
  if (stripAt === -1) fail(`${p}: no disclosure strip found`);
  else if (mainAt > -1 && stripAt > mainAt) fail(`${p}: disclosure is not above the fold (it appears after </main>)`);
  if (!/<footer[\s\S]*?disclosure-strip/.test(body)) fail(`${p}: disclosure is not repeated in the footer`);

  const amazon = [...h.matchAll(/<a\s[^>]*href="(https:\/\/www\.amazon\.com[^"]*)"[^>]*>/g)];
  amazon.forEach((m, i) => {
    const tag = m[0];
    if (!/rel="[^"]*sponsored/.test(tag)) fail(`${p}: amazon link #${i + 1} lacks rel="sponsored" -> ${m[1].slice(0, 70)}`);
    if (!/nofollow/.test(tag)) warn(`${p}: amazon link #${i + 1} lacks nofollow`);
    if (!/noopener/.test(tag)) warn(`${p}: amazon link #${i + 1} lacks noopener`);
  });
  // the label a reader can see, not only the attribute a crawler reads
  const shop = SHOP_PAGES.concat("guides.html");
  if (shop.includes(p) && amazon.length && !/sponsored/i.test(stripTags(body))) fail(`${p}: has ${amazon.length} amazon links but never says "sponsored" in text`);

  const dp = amazon.filter((m) => /\/dp\/[A-Z0-9]{10}/.test(m[1])).length;
  if (amazon.length && dp !== amazon.length) warn(`${p}: ${amazon.length - dp} amazon link(s) are not /dp/ASIN form - check they are intended`);
}

/* ---------- 3. the client must mark the links it builds ---------- */
const client = read("assets/app.js");
if (!/rel="sponsored nofollow noopener"/.test(client) && !/rel=\\"sponsored/.test(client)) {
  fail("assets/app.js builds outbound links without rel=\"sponsored\"");
}
if (/tag=[A-Za-z0-9-]{4,}/.test(client)) fail("assets/app.js hardcodes a tracking id; it must read data-tag from the page");
for (const p of pages) {
  const tag = (read(p).match(/data-tag="([^"]*)"/) || [])[1];
  if (tag === undefined) warn(`${p}: no data-tag attribute on <body>`);
  else if (tag !== DATA.site.trackingId) fail(`${p}: data-tag "${tag}" does not match data/products.json "${DATA.site.trackingId}"`);
}

/* ---------- 4. volatile Program Content policy ---------- */
const priceAllowed = !!EDIT.display.pricesOnShopPages;
for (const p of SHOP_PAGES.filter((x) => x !== "about.html")) {
  if (!existsSync(join(ROOT, p))) continue;
  const text = textOf(read(p));
  if (!priceAllowed) {
    const money = text.match(/\$\s?\d+(?:[.,]\d{2})?/g) || [];
    if (money.length) fail(`${p}: shows price figures (${money.slice(0, 4).join(", ")}) while display.pricesOnShopPages is false - the policy read in FLG-021 forbids stale prices on shop pages`);
    const rating = text.match(/\b[1-5]\.\d\s*\(\s*[\d,]{3,}\s*(?:ratings)?/g) || [];
    if (rating.length) fail(`${p}: shows a rating figure (${rating[0]}) - volatile Program Content, keep it in the register only`);
    if (/bought in past month/i.test(text)) fail(`${p}: quotes "bought in past month", which is Amazon listing content that expires`);
  }
  if (/as an amazon associate, the/.test(text)) warn(`${p}: variant disclosure wording detected; the Agreement asks for the exact sentence`);
}
/* the register may keep dated observations - that is its whole purpose */

/* ---------- 5. voice rules on reader-facing pages ---------- */
for (const p of READER_PAGES) {
  if (!existsSync(join(ROOT, p))) continue;
  const text = textOf(read(p)).toLowerCase();
  for (const b of EDIT.voice.bannedPhrases) {
    if (text.includes(b.toLowerCase())) fail(`${p}: banned phrase "${b}" - a claim we cannot source (see data/editorial.json voice rules)`);
  }
  if (/\btrending\b/.test(text) && !/dated snapshot/.test(text)) fail(`${p}: says "trending" without the dated-snapshot rule beside it`);
  if (/\bguarantee[ds]?\b/.test(text) && !/not/.test(text)) warn(`${p}: check that "guarantee" is not a promise about outcomes`);
  const em = (read(p).match(/ — /g) || []).length;
  if (em > 12) warn(`${p}: ${em} spaced em-dashes - the rhythm reads as generated; vary the sentence lengths instead`);
}

/* ---------- 6. links, anchors, sitemap and feed ---------- */
const all = pages.map((p) => [p, read(p)]);
for (const [p, h] of all) {
  for (const m of h.matchAll(/<a\s[^>]*href="([^"#]+)(#[^"]*)?"/g)) {
    const href = m[1];
    if (/^(https?:|mailto:|tel:)/.test(href)) continue;
    const file = href.split("/").pop() || "index.html";
    if (!existsSync(join(ROOT, file))) fail(`${p}: broken internal link -> ${href}`);
    else if (m[2] && file.endsWith(".html") && !new RegExp(`id="${m[2].slice(1)}"`).test(readFileSync(join(ROOT, file), "utf8"))) {
      fail(`${p}: anchor ${m[2]} does not exist in ${file}`);
    }
  }
}
const sitemap = read("sitemap.xml");
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
if (!locs.length) fail("sitemap.xml has no URLs");
for (const loc of locs) {
  const rel = loc.replace(BASE + "/", "").replace(/^$/, "index.html") || "index.html";
  if (!existsSync(join(ROOT, rel))) fail(`sitemap lists ${loc}, which the build did not write`);
  if (!/^[a-z][a-z0-9+.-]*:\/\/[^\s<]+$/.test(loc)) fail(`sitemap entry is not an absolute URL: ${loc}`);
  if (/index\.html$/.test(loc) && loc !== BASE + "/index.html") fail(`sitemap uses /index.html while pages self-canonicalise without it: ${loc}`);
}
for (const p of pages.filter((x) => x !== "404.html")) {
  const url = p === "index.html" ? BASE + "/" : `${BASE}/${p}`;
  if (!locs.includes(url)) fail(`${p} is missing from sitemap.xml - a published page that is not in the sitemap is a findability bug`);
}
if (!/Sitemap:\s/.test(read("robots.txt"))) fail("robots.txt does not declare the sitemap");
if (new RegExp(`${BASE}/sitemap\\.xml`).test(read("robots.txt")) === false) warn("robots.txt sitemap line does not point at the deployed base URL");

const feed = read("feed.xml");
for (const m of feed.matchAll(/<link>(https?:[^<]+)<\/link>/g)) {
  const rel = m[1].replace(BASE + "/", "");
  if (rel && rel !== "" && !existsSync(join(ROOT, rel))) fail(`feed item points at a missing page: ${m[1]}`);
}
const RFC822 = /^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s+\d{2}\s+\w{3}\s+\d{4}\s+\d{2}:\d{2}:\d{2}\s+(?:GMT|UTC|[+-]\d{4})\s*$/;
if (/<lastBuildDate>([^<]*)<\/lastBuildDate>/.test(feed)) {
  const v = feed.match(/<lastBuildDate>([^<]*)<\/lastBuildDate>/)[1];
  if (!RFC822.test(v)) fail(`feed lastBuildDate "${v}" is not an RFC-822 date - readers and Google both reject it`);
} else fail("feed has no lastBuildDate");
for (const m of feed.matchAll(/<pubDate>([^<]*)<\/pubDate>/g)) {
  if (!RFC822.test(m[1])) fail(`feed pubDate "${m[1]}" is not RFC-822`);
}
if (/<title>\s*<\/title>|<description>\s*<\/description>/.test(feed)) fail("feed has an empty title or description");
if (/datetime\.now|new Date\(\)/.test(read("build_site.py"))) fail("build_site.py stamps a build time; that makes every rebuild dirty and the feed undeterministic");

/* ---------- 7. editorial data integrity ---------- */
for (const prod of DATA.products) {
  for (const f of ["asin", "officialListingUrl", "confirmationDate", "confirmationSource"]) {
    if (!prod[f]) warn(`product ${prod.id}: ${f} is blank (correct if unverified; flag it, never infer it)`);
  }
  if (prod.asin && prod.officialListingUrl && !prod.officialListingUrl.includes(prod.asin)) fail(`product ${prod.id}: listing URL does not contain the ASIN`);
}
const seenEvents = new Set([...client.matchAll(/track\("([a-z_]+)"/g)].map((m) => m[1]));
for (const e of EDIT.events.five) if (!seenEvents.has(e.name)) fail(`event "${e.name}" is documented on methodology.html but never fired by assets/app.js`);
if ([...seenEvents].some((e) => !EDIT.events.five.some((x) => x.name === e))) fail("app.js fires an event outside the documented five");

/* ---------- report ---------- */
const label = (f) => basename(f, ".html");
if (!QUIET) {
  console.log(`\nChecked ${pages.length} pages, ${locs.length} sitemap URLs, ${titles.size} unique titles.`);
  console.log(`Reader pages under voice rules: ${READER_PAGES.map(label).join(", ")}`);
}
for (const w of warns) console.log(`  warn  ${w}`);
for (const f of fails) console.log(`  FAIL  ${f}`);
if (fails.length) { console.log(`\nGate FAILED: ${fails.length} blocking item(s), ${warns.length} warning(s).\n`); process.exit(1); }
console.log(`\nGate passed: ${warns.length} warning(s), no blocking items.\n`);
