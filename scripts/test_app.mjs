#!/usr/bin/env node
// Small dependency-free browser-DOM harness for the publication's client interactions.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync(new URL('../assets/app.js', import.meta.url), 'utf8');

function makeHarness(storage = new Map(), endpoint = "") {
  const documentListeners = {};
  const domListeners = {};
  const stored = storage;
  const makeButton = () => ({ listeners: {}, addEventListener(name, fn) { this.listeners[name] = fn; }, click() { this.listeners.click?.({ preventDefault() {} }); } });
  const makeSelect = (id) => ({
    id,
    value: '',
    listeners: {},
    getAttribute(name) { return name === 'data-decision-id' ? id : null; },
    addEventListener(name, fn) { this.listeners[name] = fn; },
    change(value) { this.value = value; this.listeners.change?.(); }
  });
  const selects = [makeSelect('SG-01'), makeSelect('SG-02')];
  const status = { textContent: '' };
  const chooserOutput = { innerHTML: '', scrolled: false, scrollIntoView() { this.scrolled = true; } };
  const chooserValues = {
    'input[name="q1"]:checked': { value: 'meat' },
    'input[name="q2"]:checked': { value: 'standard' },
    'input[name="q3"]:checked': { value: 'mid' }
  };
  const chooserForm = {
    listeners: {},
    addEventListener(name, fn) { this.listeners[name] = fn; },
    querySelector(selector) { return chooserValues[selector] || null; },
    submit() { this.listeners.submit?.({ preventDefault() {} }); }
  };
  const downloadButton = makeButton();
  const clearButton = makeButton();
  const searchInput = { value: 'query that should stay local' };
  const searchForm = {
    listeners: {},
    addEventListener(name, fn) { this.listeners[name] = fn; },
    submit() { this.listeners.submit?.({ preventDefault() {} }); }
  };
  const downloadAnchor = { href: '', download: '', click() { this.clicked = true; }, remove() {} };
  const body = {
    getAttribute(name) { return name === 'data-analytics-endpoint' ? endpoint : ''; },
    classList: { contains() { return false; } },
    appendChild() {}
  };
  const elements = {
    'chooser-form': chooserForm,
    'chooser-result': chooserOutput,
    'site-search-form': searchForm,
    'site-search-input': searchInput,
    'decision-save-status': status,
    'download-decision-record': downloadButton,
    'clear-decision-record': clearButton
  };
  const document = {
    body,
    addEventListener(name, fn) { documentListeners[name] = fn; },
    querySelectorAll(selector) { return selector === 'select[data-decision-id]' ? selects : []; },
    getElementById(id) { return elements[id] || null; },
    createElement(name) { assert.equal(name, 'a'); return downloadAnchor; }
  };
  const window = {
    location: { hostname: 'wingbangboozle1-lang.github.io', pathname: '/Prod1/suggestions.html', search: '', href: 'https://wingbangboozle1-lang.github.io/Prod1/suggestions.html' },
    addEventListener(name, fn) { domListeners[name] = fn; },
    setTimeout(fn) { fn(); }
  };
  const localStorage = {
    getItem(key) { return stored.has(key) ? stored.get(key) : null; },
    setItem(key, value) { stored.set(key, value); },
    removeItem(key) { stored.delete(key); }
  };
  const URLClass = class extends URL {
    static createObjectURL() { return 'blob:test'; }
    static revokeObjectURL() {}
  };
  const beacons = [];
  const context = vm.createContext({
    document, window, localStorage,
    navigator: { sendBeacon(url, body) { beacons.push({ url, payload: JSON.parse(body) }); return true; } },
    URL: URLClass, URLSearchParams, Blob, console,
    fetch() { throw new Error('search is not invoked in this harness'); }
  });
  vm.runInContext(source, context, { filename: 'assets/app.js' });
  documentListeners.DOMContentLoaded();
  return { stored, selects, status, chooserOutput, chooserForm, searchForm, searchInput, downloadButton, clearButton, downloadAnchor, documentListeners, domListeners, beacons, window };
}

const storage = new Map();
let app = makeHarness(storage, 'https://metrics.example/event');
assert.deepEqual(app.beacons[0], {
  url: 'https://metrics.example/event',
  payload: { event: 'page_view', path: '/Prod1/suggestions.html' }
});

// The chooser produces sponsored, measurable links and an anonymous aggregate event.
app.chooserForm.submit();
assert.match(app.chooserOutput.innerHTML, /rel="sponsored nofollow noopener"/);
assert.match(app.chooserOutput.innerHTML, /data-ctg-outbound data-asin="B0DHZTCNR5"/);
assert.equal(app.chooserOutput.scrolled, true);
assert.deepEqual(app.beacons[1], {
  url: 'https://metrics.example/event',
  payload: { event: 'chooser_complete', path: '/Prod1/suggestions.html' }
});
let counts = JSON.parse(storage.get('ctg_counts_v1'));
const today = new Date().toISOString().slice(0, 10);
assert.equal(counts[today].page_view, 1);
assert.equal(counts[today].chooser_complete, 1);

// Sponsored outbound clicks save only an event count locally when the endpoint is blank.
const clickHandler = app.documentListeners.click;
clickHandler({ target: { closest() { return { getAttribute(name) { return name === 'data-asin' ? 'B0CDY277D3' : null; } }; } } });
counts = JSON.parse(storage.get('ctg_counts_v1'));
assert.equal(counts[today].outbound_click, 1);
assert.deepEqual(app.beacons[2], {
  url: 'https://metrics.example/event',
  payload: { event: 'outbound_click', path: '/Prod1/suggestions.html', asin: 'B0CDY277D3' }
});

// Search records the event but keeps the query out of the event payload.
app.searchForm.submit();
counts = JSON.parse(storage.get('ctg_counts_v1'));
assert.equal(counts[today].search, 1);
assert.deepEqual(app.beacons[3], {
  url: 'https://metrics.example/event',
  payload: { event: 'search', path: '/Prod1/suggestions.html' }
});
assert.match(app.window.location.href, /search\.html\?q=query%20that%20should%20stay%20local/);

// Reviewer choices are saved locally, restored on reload, exportable, and clearable.
app.selects[0].change('approve');
assert.equal(app.status.textContent, 'Choices saved in this browser only. They are not sent to the site.');
const saved = JSON.parse(storage.get('ctg_decisions_v1'));
assert.deepEqual(Object.keys(saved), ['SG-01']);
assert.equal(saved['SG-01'], 'approve');
app.downloadButton.click();
assert.equal(app.downloadAnchor.download, 'countertop-guide-decisions.json');
assert.equal(app.downloadAnchor.clicked, true);

app = makeHarness(storage);
assert.equal(app.selects[0].value, 'approve');
assert.match(app.status.textContent, /loaded from this browser/);
app.clearButton.click();
assert.equal(storage.has('ctg_decisions_v1'), false);
assert.equal(app.selects[0].value, '');
assert.match(app.status.textContent, /cleared/);

console.log('Client checks passed: five-event local tracking, sponsored shortlist links, and local suggestions-board save/export/clear/restore.');
