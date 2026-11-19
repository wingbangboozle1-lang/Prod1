/* Kitchen Buyer's Desk: first-party measurement, five events.
 * Counts are stored in this browser only (localStorage key kbd_counts_v1). No cookies,
 * no third-party scripts, no timestamps, no identifiers. Nothing is sent over the network
 * unless window.KBD_ENDPOINT is set to a self-hosted endpoint (not set in this build).
 * Events: page_view, outbound_click, guide_read_75, category_click, feed_click.
 */
(function () {
  'use strict';
  var KEY = 'kbd_counts_v1';
  var EVENTS = ['page_view', 'outbound_click', 'guide_read_75', 'category_click', 'feed_click'];

  function load() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || '{}');
      return v && typeof v === 'object' ? v : {};
    } catch (e) { return {}; }
  }
  function save(counts) {
    try { localStorage.setItem(KEY, JSON.stringify(counts)); } catch (e) { /* storage unavailable */ }
  }
  function sitePath() {
    var parts = window.location.pathname.split('/').filter(Boolean);
    if (parts[0] === 'Prod1') parts.shift();
    var p = '/' + parts.join('/');
    return p.replace(/\/index\.html$/, '/') || '/';
  }
  function record(event, asin) {
    if (EVENTS.indexOf(event) < 0) return;
    var path = sitePath();
    var counts = load();
    counts[event] = counts[event] || {};
    counts[event][path] = (counts[event][path] || 0) + 1;
    save(counts);
    if (window.KBD_ENDPOINT && navigator.sendBeacon) {
      var body = JSON.stringify({ event: event, path: path, asin: asin || '' });
      try { navigator.sendBeacon(window.KBD_ENDPOINT, new Blob([body], { type: 'application/json' })); } catch (e) { /* ignore */ }
    }
    render();
  }
  function total(counts, event) {
    var by = counts[event] || {}; var n = 0;
    Object.keys(by).forEach(function (k) { n += by[k]; });
    return n;
  }
  function render() {
    var table = document.getElementById('local-counts');
    if (!table) return;
    var counts = load();
    var html = '';
    EVENTS.forEach(function (ev) {
      html += '<tr><td><code>' + ev + '</code></td><td>' + total(counts, ev) + '</td></tr>';
    });
    table.querySelector('tbody').innerHTML = html;
    var st = document.getElementById('local-status');
    if (st) st.textContent = window.KBD_ENDPOINT
      ? 'Endpoint configured: events are also sent to it.'
      : 'No endpoint configured. Nothing is sent. Counts are on this device only.';
  }

  document.addEventListener('click', function (ev) {
    var el = ev.target && ev.target.closest ? ev.target.closest('[data-track]') : null;
    if (!el) return;
    var kind = el.getAttribute('data-track');
    if (kind === 'outbound') record('outbound_click', el.getAttribute('data-asin'));
    else if (kind === 'category') record('category_click');
    else if (kind === 'feed') record('feed_click');
  }, false);

  // guide_read_75: once per guide page, when 75% of the page has been scrolled past.
  if (/\/guides\/[^/]+\.html$/.test(window.location.pathname)) {
    var fired = false;
    window.addEventListener('scroll', function () {
      if (fired) return;
      var h = document.documentElement;
      var seen = (window.scrollY + window.innerHeight) / Math.max(h.scrollHeight, 1);
      if (seen >= 0.75) { fired = true; record('guide_read_75'); }
    }, { passive: true });
  }

  record('page_view');
  render();
})();
