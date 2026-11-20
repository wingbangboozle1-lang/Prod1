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
/* slug -> canonical, for pages that consolidate into another page */
const CONSOLIDATED = new Map();

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
  else if (canon === want) { if (/example\.com/.test(canon)) fail(`${p}: placeholder canonical`); }
  else {
    /* A canonical that points elsewhere is allowed only as a deliberate consolidation of two
       near-duplicate pages (see FLG-047). Enforcing the shape here means it cannot be used by
       accident, and cannot be "fixed" later by hand-editing one page: Google's guidance is one
       canonical signal per page, so the target must be in the sitemap and this page must not be. */
    CONSOLIDATED.set(p, canon);
    const target = canon.replace(BASE + "/", "").replace(/\/$/, "index.html") || "index.html";
    if (!existsSync(join(ROOT, target))) fail(`${p}: canonical points at ${canon}, which this build does not write`);
    else {
      const th = read(target);
      const tCanon = (th.match(/rel="canonical" href="([^"]+)"/) || [])[1] || "";
      if (tCanon !== canon) fail(`${p}: canonicalises to ${target}, which canonicalises to ${tCanon || "nothing"} - a consolidation must point at a self-canonical page`);
      if (!/<h1[^>]*>[^<]*<\/h1>/.test(th)) fail(`${p}: consolidation target ${target} has no <h1>`);
    }
    const targetHref = target === "index.html" ? "index.html" : target;
    if (!h.includes(`href="${targetHref}"`)) fail(`${p}: a consolidated page must link to ${targetHref} in its own body, not only declare it in the head`);
    const ogu = (h.match(/property="og:url" content="([^"]*)"/) || [])[1] || "";
    if (ogu !== canon) fail(`${p}: og:url ${ogu || "(none)"} should match the consolidation canonical ${canon}`);
  }

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
/* A page may be deliberately excluded from the sitemap only if it says so itself. The
   internal surfaces (decision desk, executive summary, methodology, design brief, review
   desk, search) stay reachable but carry `noindex, follow`: they are the audit, not the
   shop, and every one of them competes for the same hostname as a buying page. This is the
   only alternative to listing everything, so it is checked both ways - a page that is in
   neither the sitemap nor noindex is a findability bug, and a page that is noindex yet
   listed in the sitemap is a contradiction Google resolves by ignoring us. */
const noindexed = new Set();
for (const p of pages.filter((x) => x !== "404.html")) {
  const url = p === "index.html" ? BASE + "/" : `${BASE}/${p}`;
  const h = read(p);
  const isNoindex = /<meta name="robots" content="[^"]*noindex/.test(h);
  if (isNoindex) noindexed.add(p);
  if (CONSOLIDATED.has(p)) {
    if (locs.includes(url)) fail(`${p} canonicalises to ${CONSOLIDATED.get(p)} but is still listed in the sitemap - list one URL per answer`);
    continue;
  }
  if (isNoindex) {
    if (locs.includes(url)) fail(`${p} says noindex but is listed in sitemap.xml - the two signals contradict each other`);
    if (!/content="[^"]*follow/.test(h)) warn(`${p}: noindex without "follow" stops link equity reaching the pages it points at`);
    if (!/<a\s[^>]*href="(?:[a-z-]+\.html|index\.html|\/)"/.test(h)) warn(`${p}: noindex page has no visible route back into the site`);
    continue;
  }
  if (!locs.includes(url)) fail(`${p} is missing from sitemap.xml and does not declare noindex - a published page that is in neither is invisible to search`);
}
for (const [p, canon] of CONSOLIDATED) {
  const target = canon.replace(BASE + "/", "").replace(/\/$/, "index.html") || "index.html";
  if (noindexed.has(target)) continue; // pointing at a noindex hub is a deliberate consolidation
  if (!locs.includes(canon)) fail(`${p} canonicalises to ${canon}, which the sitemap does not list`);
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

/* ---------- 7b. the tracking ID is typed, so it is checked ----------
 * This pass very nearly published a recommendation containing `tag=shownow047c-20` - one
 * transposed letter, invisible in prose, and every click on it would have been unattributed.
 * The ID lives in data/products.json; anything that looks like a tag anywhere on the site
 * must match it exactly. */
const TAG = DATA.site.trackingId;
for (const p of pages) {
  const h = read(p);
  /* Only strings that would actually be a live link parameter count. The register quotes a
     mistyped tag on purpose (FLG-078), and a gate that cannot tell a citation from a link
     would force the record to be vaguer than the defect. */
  for (const m of h.matchAll(/(?:href="[^"]*?|\b(?:https?:\/\/[^\s"'<]*?))[?&]tag=([a-z0-9-]+)/g)) {
    if (m[1] !== TAG) fail(`${p}: live link carries tag "${m[1]}", not the registered ID "${TAG}" - clicks through it earn nothing`);
  }
  for (const m of h.matchAll(/<code>tag=([a-z0-9-]+)<\/code>/g)) {
    if (m[1] !== TAG && !/shownow/.test(m[1])) fail(`${p}: code sample quotes tag "${m[1]}"`);
  }
}

/* ---------- 8. article structured data ----------
 * Why this is a gate and not a preference: two defects shipped past every existing check.
 * (a) Ten of thirteen guides declared `WebPage` and no `Article`, so no guide was
 *     machine-readable as an article at all; only one happened to carry it.
 * (b) Every guide shared one og:image, so a share of any guide rendered the same picture
 *     and `Article.image` described a different page.
 * Both are invisible to a human reading the page and to a presence-only check, so the
 * contract is asserted here. Field values are not judged - only that the fields the
 * guidance asks for exist and that the image they name is a file this repo actually has. */
const GUIDE_RE = /^guide-(?!holiday-gifts|small-kitchen|holiday-roast)[a-z-]+\.html$/;
for (const p of pages.filter((x) => GUIDE_RE.test(x))) {
  const h = read(p);
  const blocks = [...h.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map((m) => m[1]);
  let art = null;
  for (const b of blocks) {
    let o; try { o = JSON.parse(b); } catch { fail(`${p}: JSON-LD block does not parse - search engines drop it silently`); continue; }
    if (o["@type"] === "Article") art = o;
  }
  if (!art) { fail(`${p}: published guide has no Article structured data (only ${blocks.length} other block(s))`); continue; }
  for (const f of ["headline", "datePublished", "dateModified", "author", "publisher", "image", "mainEntityOfPage", "url"]) {
    if (!art[f]) fail(`${p}: Article is missing "${f}"`);
  }
  if (art.headline && art.headline.length > 110) warn(`${p}: Article.headline is ${art.headline.length} chars; Google truncates around 110`);
  const img = typeof art.image === "string" ? art.image : (art.image && art.image.url) || "";
  if (!img) fail(`${p}: Article.image has no usable URL`);
  else {
    const rel = img.replace(BASE + "/", "");
    if (!/^https:\/\//.test(img)) fail(`${p}: Article.image is not an absolute https URL: ${img}`);
    else if (!existsSync(join(ROOT, rel))) fail(`${p}: Article.image points at ${rel}, which is not in the repository`);
  }
  const og = (h.match(/<meta property="og:image" content="([^"]*)"/) || [])[1] || "";
  if (og.startsWith("https:") && og !== img) fail(`${p}: og:image and Article.image disagree - one page, one representative image`);
  const dates = [art.datePublished, art.dateModified].join(",");
  if (!/^\d{4}-\d{2}-\d{2},\d{4}-\d{2}-\d{2}$/.test(dates)) warn(`${p}: Article dates are not plain ISO dates (${dates})`);
  if (art.datePublished > art.dateModified) fail(`${p}: datePublished is later than dateModified`);
}

/* ---------- 9. prose that stopped mid-sentence ----------
 * The product card shipped "we do not publish a stale figure - the button shows today's"
 * on five pages: the object of the sentence was lost in an edit and no gate could see it,
 * because the string was present and the tag was closed. A dangling copula or a trailing
 * possessive is detectable without an English parser, so it is checked here. */
const decode = (s) => s.replace(/&rsquo;|&lsquo;/g, "'").replace(/&mdash;|&ndash;/g, "-")
  .replace(/&quot;/g, '"').replace(/&amp;/g, "&").replace(/&[a-z#0-9]+;/g, " ").replace(/\s+/g, " ").trim();
/* A sentence that ends on a word which cannot end a sentence. "shows today's" and "the
   button shows" are both dead stops; "dishwasher safe" is not. Possessives and determiners
   are the reliable tells, plus a verb that needs an object. */
/* A sentence that stops on a word which cannot end one. Three separate tells, because a
   single loose pattern is how this check fails on good prose:
     - it ends on a determiner, preposition or conjunction  ("...the button shows the")
     - it ends on a possessive  ("...the button shows today's")
     - it ends on a transitive verb with no object  ("...the button shows")
   "the listing it came from" and "dishwasher safe" must and do pass. */
const ENDS_FUNCTION = /\b(?:the|a|an|of|to|and|but|with|for|from|that|which|your|our|its|their)\s*$/i;
const ENDS_POSSESSIVE = /\b[\w-]+'s\s*$/i;
const ENDS_VERB = /\b(?:shows|showing|reads|offers|means|gives|needs|has|have|includes|covers)\s*$/i;
for (const p of READER_PAGES) {
  const h = read(p);
  const seenTxt = new Set();
  for (const m of h.matchAll(/<span class="fine">([\s\S]{0,300}?)<\/span>/g)) {
    const txt = decode(m[1]);
    if (!txt || txt.length < 12 || seenTxt.has(txt)) continue;
    seenTxt.add(txt);
    if (ENDS_FUNCTION.test(txt) || ENDS_POSSESSIVE.test(txt) || ENDS_VERB.test(txt)) {
      fail(`${p}: a sentence ends mid-thought: "...${txt.slice(-64)}"`);
    }
  }
}

/* ---------- report ---------- */
const label = (f) => basename(f, ".html");
if (!QUIET) {
  console.log(`\nChecked ${pages.length} pages (${CONSOLIDATED.size} consolidated into others), ${locs.length} sitemap URLs, ${titles.size} unique titles.`);
  console.log(`Reader pages under voice rules: ${READER_PAGES.map(label).join(", ")}`);
}
for (const w of warns) console.log(`  warn  ${w}`);
for (const f of fails) console.log(`  FAIL  ${f}`);
if (fails.length) { console.log(`\nGate FAILED: ${fails.length} blocking item(s), ${warns.length} warning(s).\n`); process.exit(1); }
console.log(`\nGate passed: ${warns.length} warning(s), no blocking items.\n`);
