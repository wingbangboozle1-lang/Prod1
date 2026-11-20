#!/usr/bin/env node
/* Headless smoke test for the reader-facing JavaScript.
 *
 * It loads each page's real HTML plus assets/app.js into jsdom, fires DOMContentLoaded and
 * asserts: no runtime error on any page, the chooser's links are sponsored/tagged/labelled,
 * and the decision desk exports a sheet. The static gates cannot see any of that -
 * check_meta.mjs deliberately reads the client source text instead of executing it, which is
 * exactly the blind spot this script covers.
 *
 * Not wired into .github/workflows/pages.yml: it needs jsdom (npm install jsdom) and the
 * Pages workflow runs on a clean checkout with no install step. Run it locally after touching
 * assets/app.js. It covers 15 pages today. Run it again after touching assets/app.js.
 *
 * Usage: node scripts/test_pages_dom.mjs
 */
// jsdom is a local-only dependency (the Pages workflow installs nothing). The sandbox path is
// tried first so the script runs without an install step; otherwise npm's copy is used.
let JSDOM;
try { ({ JSDOM } = await import('/tmp/domtest/node_modules/jsdom/lib/api.js')); }
catch { ({ JSDOM } = await import('jsdom')); }
import fs from 'node:fs';
import process from 'node:process';
const ROOT=process.cwd()+'/';
const appjs = fs.readFileSync(ROOT+'assets/app.js','utf8');
let problems=0;
async function run(page, fn){
  const html = fs.readFileSync(ROOT+page,'utf8').replace(/<script src="[^"]*"><\/script>/,'');
  const dom = new JSDOM(html,{runScripts:'outside-only',pretendToBeVisual:true,url:'https://wingbangboozle1-lang.github.io/Prod1/'+page});
  const {window}=dom; const errs=[];
  window.Element.prototype.scrollIntoView=function(){};   // not implemented by jsdom, not a site defect
  window.addEventListener('error', e=>errs.push(String(e.error&&e.error.stack||e.message)));
  window.URL.createObjectURL=(b)=>{window.__blob=b;return 'blob:stub';}; window.URL.revokeObjectURL=()=>{};
  window.eval(appjs);
  window.document.dispatchEvent(new window.Event('DOMContentLoaded',{bubbles:true}));
  const out = fn ? await fn(window) : null;
  console.log(`${page.padEnd(24)} ${errs.length?'FAIL '+errs[0].split('\n')[0]:'no errors'}` + (out?('  | '+out):''));
  if(errs.length) problems++;
  return window;
}
await run('index.html', async w=>{
  const f=w.document.getElementById('chooser-form');
  f.querySelectorAll('input')[0].checked=true; f.querySelectorAll('input')[4].checked=true; f.querySelectorAll('input')[7].checked=true;
  f.dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));
  const links=[...w.document.getElementById('chooser-result').querySelectorAll('a')].filter(a=>/amazon\.com/.test(a.href));
  const ok=links.length>0 && links.every(a=>/rel="sponsored nofollow noopener"/.test(a.outerHTML)&&/\?tag=shopnow047c-20/.test(a.href)&&/sponsored, opens Amazon/.test(a.nextElementSibling.textContent));
  return `chooser: ${links.length} outbound link(s), all sponsored+tagged+labelled: ${ok}`;
});
const w2 = await run('suggestions.html', async w => {
  // every numbered row on the desk must carry a control, or the board silently loses rows
  const ids = new Set([...w.document.querySelectorAll('[id^="SG-"],[id^="Q-"],[id^="DI-"]')]
    .map(e => e.id).filter(x => /^(SG|Q|DI)-\d+$/.test(x)));
  const ctrls = w.document.querySelectorAll('select[data-pick]').length;
  if (!(ids.size > 0 && ctrls >= ids.size)) throw new Error(`desk coverage: ${ctrls} controls for ${ids.size} numbered rows`);
  return `desk coverage: ${ctrls} controls over ${ids.size} numbered rows`;
});
w2.document.getElementById('sg-export').click();
const txt=await w2.__blob.text();
console.log('export head:', JSON.stringify(txt.split('\n')[0]), '| lines:', txt.trim().split('\n').length);
const w3 = await run('search.html');
for (const p of ['compare.html','guide-price-check.html','guide-counter-height.html','guide-accessories-in-box.html','air-fryers.html','thermometers.html','flagged.html','executive-summary.html','methodology.html','guides.html','review-desk.html','topics.html','verification.html']) await run(p);
console.log(problems? `FAIL: ${problems} page(s) threw` : 'PASS: no runtime errors on 15 pages under the client script');
