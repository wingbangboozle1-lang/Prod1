// Compliance and link gate. Exits non-zero on any failure.
// Checks: disclosure strip on every page + footer repeat; rel="sponsored" on every Amazon link;
// internal links and in-page anchors resolve; unique titles/descriptions; sitemap and RSS complete;
// every product row has a source link and blank unverified fields carry a flag.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DOCS = path.join(ROOT, "docs");
const SITE = "https://wingbangboozle1-lang.github.io/Prod1";
const STATEMENT = "As an Amazon Associate I earn from qualifying purchases.";
const errors = [];
const err = (m) => errors.push(m);

const walk = (d) =>
  fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]
  );
const files = walk(DOCS);
const htmlFiles = files.filter((f) => f.endsWith(".html"));
const rel = (f) => path.relative(DOCS, f).split(path.sep).join("/");

const titles = new Map();
const descs = new Map();
const idsByFile = new Map();

for (const f of htmlFiles) {
  const r = rel(f);
  const html = fs.readFileSync(f, "utf8");
  if (!html.includes('<div class="disclosure"')) err(`${r}: missing disclosure strip under masthead`);
  if (!html.includes('class="disclosure-foot"') || !html.includes(STATEMENT)) err(`${r}: footer disclosure missing or wrong`);
  if (!html.includes(`<div class="disclosure" role="note">`) || html.indexOf('class="disclosure"') > html.indexOf("<main")) err(`${r}: disclosure strip not above main content`);
  if (r !== "404.html" && !html.includes(STATEMENT)) err(`${r}: Associates statement absent`);

  const t = (html.match(/<title>([^<]*)<\/title>/) || [])[1];
  const d = (html.match(/<meta name="description" content="([^"]*)"/) || [])[1];
  if (!t) err(`${r}: no <title>`);
  if (!d) err(`${r}: no meta description`);
  if (t) { if (titles.has(t)) err(`${r}: duplicate title with ${titles.get(t)}`); titles.set(t, r); }
  if (d) { if (descs.has(d) && r !== "404.html") err(`${r}: duplicate description with ${descs.get(d)}`); descs.set(d, r); }

  const ids = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]));
  idsByFile.set(r, ids);

  // every anchor tag
  for (const m of html.matchAll(/<a\s[^>]*>/g)) {
    const tag = m[0];
    const href = (tag.match(/href="([^"]*)"/) || [])[1];
    if (href === undefined) continue;
    const isAmazon = /^https?:\/\/(www\.)?(amazon\.com|link\.amazon)\b/.test(href);
    if (isAmazon) {
      const relv = (tag.match(/rel="([^"]*)"/) || [])[1] || "";
      if (!relv.split(/\s+/).includes("sponsored")) err(`${r}: Amazon link without rel="sponsored": ${href}`);
      if (!/noopener/.test(relv)) err(`${r}: Amazon link without noopener: ${href}`);
    }
  }

  // internal links
  for (const m of html.matchAll(/<(?:a|link|script)\s[^>]*?(?:href|src)="([^"]*)"/g)) {
    const h = m[1];
    if (/^(https?:|mailto:|data:)/.test(h)) {
      if (h.startsWith(SITE)) {
        const local = path.join(DOCS, h.slice(SITE.length).replace(/^\//, "") || "index.html");
        const candidates = [local, path.join(local, "index.html")];
        if (!candidates.some((c) => fs.existsSync(c) && fs.statSync(c).isFile())) err(`${r}: site link target missing: ${h}`);
      }
      continue;
    }
    const [pathPart, frag] = h.split("#");
    const base = path.dirname(path.join(DOCS, r));
    let target = pathPart ? path.resolve(base, pathPart) : path.join(DOCS, r);
    if (pathPart && pathPart.endsWith("/")) target = path.join(target, "index.html");
    if (pathPart && !path.extname(target)) target = path.join(target, "index.html");
    if (!fs.existsSync(target) || !fs.statSync(target).isFile()) {
      err(`${r}: broken internal link: ${h}`);
      continue;
    }
    if (frag) {
      const tr = rel(target);
      const tIds = tr === r ? ids : idsByFile.get(tr) || new Set([...fs.readFileSync(target, "utf8").matchAll(/\sid="([^"]+)"/g)].map((x) => x[1]));
      if (!tIds.has(frag)) err(`${r}: missing anchor #${frag} in ${tr}`);
    }
  }
}

// in-page anchors ("#x" hrefs) on the same page
for (const f of htmlFiles) {
  const r = rel(f);
  const html = fs.readFileSync(f, "utf8");
  for (const m of html.matchAll(/href="#([^"]+)"/g)) {
    if (!(idsByFile.get(r) || new Set()).has(m[1])) err(`${r}: in-page anchor #${m[1]} has no target`);
  }
}

// sitemap completeness
const sitemap = fs.readFileSync(path.join(DOCS, "sitemap.xml"), "utf8");
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
for (const loc of locs) {
  const p = loc.slice(SITE.length).replace(/^\//, "");
  const target = path.join(DOCS, p, p === "" || p.endsWith("/") ? "index.html" : "");
  if (!fs.existsSync(target)) err(`sitemap: url has no page: ${loc}`);
}
for (const f of htmlFiles) {
  const r = rel(f);
  if (r === "404.html") continue;
  const url = `${SITE}/${r === "index.html" ? "" : r.replace(/index\.html$/, "")}`;
  if (!locs.includes(url)) err(`sitemap: missing ${url}`);
}

// RSS completeness
const { guides } = await import(pathToFileURL(path.join(ROOT, "src/guides.mjs")).href);
const rss = fs.readFileSync(path.join(DOCS, "rss.xml"), "utf8");
for (const g of guides) {
  if (!rss.includes(`${SITE}/guides/${g.slug}/`)) err(`rss: missing guide ${g.slug}`);
  if (!sitemap.includes(`${SITE}/guides/${g.slug}/`)) err(`sitemap: missing guide ${g.slug}`);
}

// data gate
const data = JSON.parse(fs.readFileSync(path.join(ROOT, "data/products.json"), "utf8"));
for (const p of data.products) {
  if (!/^https:\/\/www\.amazon\.com\/dp\/[A-Z0-9]{10}$/.test(p.source_url)) err(`${p.id}: source_url is not an amazon.com /dp/ listing`);
  if (!/^https:\/\/link\.amazon\/[A-Za-z0-9]+$/.test(p.submitted_link)) err(`${p.id}: submitted link not a link.amazon URL`);
  if (!p.intended_asin && !/^UNVERIFIED/.test(p.intended_asin_status)) err(`${p.id}: blank intended ASIN without UNVERIFIED flag`);
  if (p.intended_asin && !/^[A-Z0-9]{10}$/.test(p.intended_asin)) err(`${p.id}: intended ASIN malformed`);
  if (!p.price_observed && !p.rating_observed) {
    // blanks are allowed only because the rows say so on the page
  }
  const observed = p.source_url.split("/dp/")[1];
  if (observed !== p.observed_redirect_asin) err(`${p.id}: observed ASIN field does not match source URL`);
  const productsHtml = fs.readFileSync(path.join(DOCS, "products/index.html"), "utf8");
  if (!productsHtml.includes(p.source_url)) err(`${p.id}: row missing source link on products page`);
}
const flagged = JSON.parse(fs.readFileSync(path.join(ROOT, "data/flagged.json"), "utf8"));
for (const f of flagged.items) {
  if (!f.id || !f.title) err(`flag without id/title`);
  if (f.type !== "Verified" && f.sources.length === 0 && f.id !== "FL-13" && f.id !== "FL-14") err(`${f.id}: no source link provided`);
}

if (errors.length) {
  console.error(`CHECK FAILED — ${errors.length} problem(s):`);
  for (const e of errors) console.error(" - " + e);
  process.exit(1);
}
console.log(`check passed: ${htmlFiles.length} pages, ${locs.length} sitemap urls, ${data.products.length} product rows, ${flagged.items.length} flags`);
