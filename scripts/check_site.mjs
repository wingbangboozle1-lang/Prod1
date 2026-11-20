#!/usr/bin/env node
// Publishing gate for the static site. Reads the HTML that GitHub Pages will serve
// (every *.html in the repository, excluding docs of other tools) and checks it.
// It does not modify any file. Exit code 1 means at least one check failed.
//
// Checks:
//  1. Disclosure strip above <main> and an Associates disclosure repeated in <footer>.
//     The exact Operating Agreement Section 5 sentence passes. A variant that names the site
//     instead of "I" is reported as a WARNING for owner review (it is not failed automatically).
//  2. Every link to an Amazon host carries rel="sponsored".
//  3. Every internal href resolves to a file (anchors and query strings ignored).
//  4. Same-page anchor links (#id) resolve to an id that exists on that page, and a link whose
//     visible text is an ID (FLG-012, SG-034, Q-005) points at that same ID. Cross-references
//     between the flag register and the suggestion desk are how a reviewer navigates the site;
//     a label that disagrees with its target sends them to the wrong record.
//     Added 2026-11-20 after four links labelled FLG-070 resolved to #FLG-069 and one labelled
//     FLG-060 resolved to #FLG-067 in the published HTML.
//  5. Every page has a non-empty, unique <title> and meta description.
//  5. No banned claim words in visible text ("bestseller", "top rated", "#1", "guaranteed", "most popular").
//     Words inside quotation marks are ignored (they quote a rule). "trending" is a WARNING, not a failure.
//
// Usage: node scripts/check_site.mjs [--root <dir>]
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = (() => {
  const i = process.argv.indexOf('--root');
  return i > 0 ? path.resolve(process.argv[i + 1]) : path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
})();
const DISCLOSURE = 'As an Amazon Associate I earn from qualifying purchases.';
const BANNED = /\b(best[- ]?sellers?|#1|top[- ]rated|most popular|guaranteed)\b/i;
const WARN_WORDS = /\b(trending)\b/i;
const VARIANT_DISCLOSURE = /As an Amazon Associate,? [^.<]{0,80}earns? from qualifying purchases\./;
const warnings = [];
const SKIP_DIRS = new Set(['.git', 'node_modules', '.github']);

function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('.') && e.name !== '.') { if (SKIP_DIRS.has(e.name) || e.isDirectory()) continue; }
    const p = path.join(dir, e.name);
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) walk(p, out); }
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

const files = walk(ROOT).sort();
const failures = [];
const seenTitle = new Map();
const seenDesc = new Map();

for (const file of files) {
  const rel = path.relative(ROOT, file);
  const h = fs.readFileSync(file, 'utf8');
  const low = h.toLowerCase();

  // 1. disclosure above main and repeated in footer
  const mainAt = low.indexOf('<main');
  const discAt = h.indexOf(DISCLOSURE);
  const variantAt = h.search(VARIANT_DISCLOSURE);
  const anyAt = discAt >= 0 ? discAt : variantAt;
  if (anyAt < 0) failures.push(`${rel}: no Associates disclosure found`);
  else if (mainAt >= 0 && anyAt > mainAt) failures.push(`${rel}: disclosure appears below <main> (not above the fold)`);
  if (discAt < 0 && variantAt >= 0) warnings.push(`${rel}: disclosure is a variant of the Section 5 wording; owner to confirm it is 'substantially similar': "${h.match(VARIANT_DISCLOSURE)[0]}"`);
  const footAt = low.indexOf('<footer');
  const footHas = footAt >= 0 && (h.indexOf(DISCLOSURE, footAt) >= 0 || VARIANT_DISCLOSURE.test(h.slice(footAt)));
  if (!footHas) failures.push(`${rel}: disclosure not repeated in <footer>`);

  // 2. Amazon links marked sponsored
  for (const m of h.matchAll(/<a\b([^>]*)>/gi)) {
    const attrs = m[1];
    const href = (attrs.match(/href="([^"]*)"/i) || [])[1] || '';
    if (/^https?:\/\/(www\.)?(amazon\.com|link\.amazon)\b/i.test(href)) {
      const rel2 = (attrs.match(/rel="([^"]*)"/i) || [])[1] || '';
      if (!/\bsponsored\b/i.test(rel2)) failures.push(`${rel}: Amazon link without rel="sponsored": ${href.slice(0, 90)}`);
    }
  }

  // 3. internal links resolve
  for (const m of h.matchAll(/\s(?:href|src)="([^"]+)"/gi)) {
    let href = m[1];
    if (/^(https?:|mailto:|tel:|data:|javascript:|#)/i.test(href)) continue;
    href = href.split('#')[0].split('?')[0];
    if (!href) continue;
    const target = href.startsWith('/') ? path.join(ROOT, href) : path.join(path.dirname(file), href);
    let ok = fs.existsSync(target);
    if (!ok && fs.existsSync(target) === false && fs.existsSync(path.join(target, 'index.html'))) ok = true;
    if (!ok) failures.push(`${rel}: broken internal link: ${href}`);
  }

  // 4. anchors resolve, and an ID-shaped link label names its own target
  const ids = new Set();
  for (const m of h.matchAll(/\sid="([^"]+)"/g)) ids.add(m[1]);
  for (const m of h.matchAll(/<a\s[^>]*href="([^"]*#[^"]+)"[^>]*>([\s\S]*?)<\/a>/gi)) {
    const href = m[1];
    const target = href.split('#')[0];
    const anchor = href.slice(href.indexOf('#') + 1);
    if (!anchor) continue;
    // same-page anchor (href="#x" or "thisfile.html#x") must have a matching id here
    const samePage = target === '' || target === rel || target === path.basename(rel);
    if (samePage && !ids.has(anchor)) {
      failures.push(`${rel}: anchor #${anchor} has no matching id on this page`);
    }
    // a label like "FLG-070" or "SG-034" must name the anchor it points at
    const label = m[2].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    if (/^(?:FLG|SG|Q)-\d+$/.test(label) && label !== anchor) {
      failures.push(`${rel}: link labelled ${label} points at #${anchor}`);
    }
  }

  // 5. title and description
  const title = (h.match(/<title>([^<]*)<\/title>/i) || [])[1]?.trim() || '';
  const desc = (h.match(/<meta\s+name="description"\s+content="([^"]*)"/i) || [])[1]?.trim() || '';
  if (!title) failures.push(`${rel}: missing <title>`);
  if (!desc) failures.push(`${rel}: missing meta description`);
  if (title && seenTitle.has(title)) failures.push(`${rel}: duplicate title with ${seenTitle.get(title)}`);
  if (desc && seenDesc.has(desc)) failures.push(`${rel}: duplicate description with ${seenDesc.get(desc)}`);
  if (title) seenTitle.set(title, rel);
  if (desc) seenDesc.set(desc, rel);

  // 6. banned claim wording in visible text
  const visible = h.replace(/<script[\s\S]*?<\/script>/gi, '').replace(/<style[\s\S]*?<\/style>/gi, '').replace(/<[^>]+>/g, ' ')
    .replace(/&quot;[^&]*&quot;/g, ' ').replace(/"[^"]*"/g, ' ').replace(/&#39;[^&]*&#39;/g, ' ');
  const hit = visible.match(BANNED);
  if (hit) failures.push(`${rel}: banned claim wording "${hit[0]}"`);
  const w = visible.match(WARN_WORDS);
  if (w) warnings.push(`${rel}: word "${w[0]}" used outside quotes; confirm it is not a claim`);
}

for (const w of warnings) console.warn('WARN: ' + w);
if (failures.length) {
  console.error(`CHECK FAILED: ${failures.length} issue(s) across ${files.length} HTML files`);
  for (const f of failures) console.error(' - ' + f);
  process.exit(1);
}
console.log(`CHECK PASSED: ${files.length} HTML files. Disclosure, sponsored links, internal links, anchors and link labels, titles and descriptions, claim wording.`);
