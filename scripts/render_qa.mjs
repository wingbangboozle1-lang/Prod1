// Rendered-page QA (session 1d3cc97c, T-1D3-A).
//
// What it checks, for every root *.html page, at desktop (1366px) and mobile (390px):
//   - horizontal overflow (document wider than the viewport)
//   - elements whose box extends past the right edge of the viewport
//     (ignores elements inside a horizontally scrollable container)
//   - images that never loaded (after scrolling the page, so lazy images are triggered)
//   - web fonts declared in CSS that did not load
//   - console errors and page errors
//   - network requests that were not served from the checkout
//
// Why it looks the way it does: the pages reference their stylesheet, fonts and art by
// absolute URL (https://wingbangboozle1-lang.github.io/Prod1/...). The harness serves those
// URLs from the working tree, so the render matches what the live site ships, without
// needing outbound access to github.io.
//
// Not a visual-taste review. It proves the page renders without the defects above; a
// human still judges the look. Screenshots are written to OUT_DIR (default /tmp/render-qa),
// outside the repository, and are never committed.
//
// Run (browser is not installed by the repo; see review/1d3cc97c/RENDER-QA.md):
//   node scripts/render_qa.mjs --deps /tmp/chr [--only index.html,guides.html]
// where --deps is a directory containing node_modules with puppeteer-core and
// @sparticuz/chromium. Set LD_LIBRARY_PATH to the extracted al2023 libs if the
// browser reports a missing shared library (see the RENDER-QA record).

import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PREFIX = 'https://wingbangboozle1-lang.github.io/Prod1/';
const OUT_DIR = process.env.OUT_DIR || '/tmp/render-qa';
const args = process.argv.slice(2);
const argOf = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null; };
const deps = argOf('--deps');
const only = argOf('--only');
const require = createRequire(deps ? path.join(path.resolve(deps), 'x.js') : import.meta.url);
const puppeteer = require('puppeteer-core');
const chromium = require('@sparticuz/chromium');

const MIME = { '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.js': 'application/javascript', '.woff2': 'font/woff2', '.html': 'text/html', '.xml': 'application/xml',
  '.json': 'application/json', '.txt': 'text/plain' };

const pages = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html')).sort()
  .filter((f) => !only || only.split(',').includes(f));
const VIEWPORTS = [
  ['desktop', { width: 1366, height: 900 }],
  ['mobile', { width: 390, height: 844, isMobile: true, hasTouch: true, deviceScaleFactor: 1 }],
];

const browser = await puppeteer.launch({ executablePath: await chromium.executablePath(), args: chromium.args, headless: true });
fs.mkdirSync(OUT_DIR, { recursive: true });

const results = [];
for (const file of pages) {
  for (const [vname, vp] of VIEWPORTS) {
    const page = await browser.newPage();
    const issues = { overflowPx: 0, offRight: [], brokenImages: [], fontsFailed: [], consoleErrors: [], pageErrors: [], unservedRequests: [] };
    page.on('console', (m) => { if (m.type() === 'error') issues.consoleErrors.push(m.text().slice(0, 160)); });
    page.on('pageerror', (e) => issues.pageErrors.push(String(e.message || e).slice(0, 160)));
    await page.setRequestInterception(true);
    page.on('request', (req) => {
      const u = req.url();
      if (u.startsWith(PREFIX)) {
        const rel = u.slice(PREFIX.length).split('?')[0] || 'index.html';
        const f = path.join(ROOT, rel);
        if (f.startsWith(ROOT) && fs.existsSync(f) && fs.statSync(f).isFile()) {
          return req.respond({ status: 200, contentType: MIME[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) });
        }
        issues.unservedRequests.push(u.slice(PREFIX.length).slice(0, 120));
        return req.respond({ status: 404, body: 'not found in checkout' });
      }
      if (u.startsWith('data:') || u.startsWith('file:')) return req.continue();
      issues.unservedRequests.push(u.slice(0, 120));
      return req.abort();
    });
    await page.setViewport(vp);
    await page.goto(PREFIX + file, { waitUntil: 'networkidle0', timeout: 45000 });
    // Scroll through the page so lazy images and reveal-on-scroll content load before measuring.
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); }
      window.scrollTo(0, 0);
    });
    await new Promise((r) => setTimeout(r, 300));
    const m = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const overflowPx = Math.max(0, document.documentElement.scrollWidth - vw);
      const offRight = [];
      for (const el of document.querySelectorAll('body *')) {
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) continue;
        if (r.right > vw + 1) {
          let p = el.parentElement, scrollable = false;
          while (p && p !== document.body) {
            const ox = getComputedStyle(p).overflowX;
            if (ox === 'auto' || ox === 'scroll' || ox === 'hidden' || ox === 'clip') { scrollable = true; break; }
            p = p.parentElement;
          }
          if (!scrollable) offRight.push(el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '') + ` right=${Math.round(r.right)}`);
        }
      }
      const brokenImages = [...document.images].filter((i) => i.complete && i.naturalWidth === 0).map((i) => (i.getAttribute('src') || '').slice(0, 120));
      const fontsFailed = [...document.fonts].filter((f) => f.status === 'error').map((f) => f.family);
      return { overflowPx, offRight: offRight.slice(0, 8), brokenImages, fontsFailed, loadedFonts: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family) };
    });
    Object.assign(issues, m);
    issues.unservedRequests = [...new Set(issues.unservedRequests)];
    issues.consoleErrors = issues.consoleErrors.slice(0, 5);
    const shot = path.join(OUT_DIR, `${file.replace(/\.html$/, '')}-${vname}.png`);
    await page.screenshot({ path: shot, fullPage: false });
    results.push({ file, viewport: vname, ...issues, loadedFonts: m.loadedFonts });
    await page.close();
  }
}
await browser.close();

const bad = results.filter((r) => r.overflowPx > 0 || r.offRight.length || r.brokenImages.length || r.fontsFailed.length || r.pageErrors.length || r.unservedRequests.length || r.consoleErrors.length);
console.log(JSON.stringify({ pages: pages.length, runs: results.length, runsWithIssues: bad.length, results }, null, 1));
// Exit non-zero only with --strict so the script can be used as a gate later without changing today's behaviour.
if (args.includes('--strict') && bad.length) process.exit(1);
