// Minimal first-party event collector for Counter Notes.
// Stores DAILY COUNTS ONLY, keyed by day, event name, page path and (for outbound clicks) product ID.
// It does not store IP addresses, user agents, cookies, or query strings.
// Not deployed: GitHub Pages cannot run this. Run it on a server you control (see analytics page, SG-01).
//
// Usage:  PORT=8787 ALLOWED_ORIGIN=https://wingbangboozle1-lang.github.io node endpoint/server.js
// Then set the page meta tag analytics-endpoint to https://<your-host>/collect in tools/build.py (TRACKER_ENDPOINT)
// and rebuild.

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = Number(process.env.PORT || 8787);
const ORIGIN = process.env.ALLOWED_ORIGIN || 'https://wingbangboozle1-lang.github.io';
const FILE = process.env.COUNTS_FILE || path.join(__dirname, 'counts.json');
const EVENTS = new Set(['page_view', 'outbound_click', 'guide_scroll_75', 'table_filter', 'feed_subscribe_click']);
const SAFE_ID = /^[a-z0-9-]{1,60}$/;

let counts = {};
try { counts = JSON.parse(fs.readFileSync(FILE, 'utf8')); } catch (_) { counts = {}; }

let saveTimer = null;
function scheduleSave() {
  if (saveTimer) return;
  saveTimer = setTimeout(() => {
    saveTimer = null;
    fs.writeFile(FILE, JSON.stringify(counts, null, 2), () => {});
  }, 500);
}

function cors(res) {
  res.setHeader('Access-Control-Allow-Origin', ORIGIN);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'content-type');
  res.setHeader('Vary', 'Origin');
}

const server = http.createServer((req, res) => {
  cors(res);
  const url = (req.url || '').split('?')[0];
  if (req.method === 'OPTIONS') { res.writeHead(204); return res.end(); }
  if (req.method !== 'POST' || url !== '/collect') { res.writeHead(404); return res.end(); }

  const chunks = [];
  let size = 0;
  let tooBig = false;
  req.on('data', (c) => {
    size += c.length;
    if (size > 1024) { tooBig = true; return; }
    chunks.push(c);
  });
  req.on('end', () => {
    if (tooBig) { res.writeHead(413); return res.end(); }
    let body;
    try { body = JSON.parse(Buffer.concat(chunks).toString('utf8')); } catch (_) { res.writeHead(400); return res.end(); }
    if (!body || !EVENTS.has(body.e)) { res.writeHead(400); return res.end(); }
    const day = new Date().toISOString().slice(0, 10);
    const page = typeof body.p === 'string' && body.p.length <= 120 ? body.p : '/';
    const product = body.d && typeof body.d.product === 'string' && SAFE_ID.test(body.d.product) ? body.d.product : '';
    const key = [day, body.e, page, product].join('|');
    counts[key] = (counts[key] || 0) + 1;
    scheduleSave();
    res.writeHead(204);
    res.end();
  });
});

server.listen(PORT, '0.0.0.0', () => console.log(`collector listening on ${PORT}, origin ${ORIGIN}`));
