/*
 * Privacy-preserving event tracker.
 * - Disabled unless <meta name="analytics-endpoint" content="https://..."> is set to a real endpoint.
 * - No cookies, no localStorage, no fingerprinting. Sends only: event name, page path (no query string), optional short detail.
 * - Five events (proposed, pending owner approval, see analytics page):
 *   page_view, outbound_click, guide_scroll_75, table_filter, feed_subscribe_click
 * - Also provides a client-side filter for tables marked data-filter-table.
 */
(function () {
  "use strict";
  var meta = document.querySelector('meta[name="analytics-endpoint"]');
  var endpoint = meta && meta.getAttribute("content");
  var ALLOWED = { page_view: 1, outbound_click: 1, guide_scroll_75: 1, table_filter: 1, feed_subscribe_click: 1 };

  function send(name, detail) {
    if (!endpoint || !ALLOWED[name]) return;
    var body = JSON.stringify({ e: name, p: location.pathname, d: detail || null });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(endpoint, new Blob([body], { type: "application/json" }));
      } else {
        fetch(endpoint, { method: "POST", body: body, keepalive: true, headers: { "content-type": "application/json" } });
      }
    } catch (err) { /* analytics must never break the page */ }
  }

  send("page_view");

  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[data-event]");
    if (!a) return;
    var name = a.getAttribute("data-event");
    if (name === "outbound_click") send(name, { product: a.getAttribute("data-product") || null });
    if (name === "feed_subscribe_click") send(name, null);
  });

  var sentinel = document.querySelector("[data-scroll-sentinel]");
  if (sentinel && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { send("guide_scroll_75"); io.disconnect(); }
      });
    }, { threshold: 0.1 });
    io.observe(sentinel);
  }

  var input = document.querySelector("input[data-filter-for]");
  if (input) {
    var table = document.getElementById(input.getAttribute("data-filter-for"));
    var counter = document.querySelector("[data-filter-count]");
    var sentFilter = false;
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var rows = table.tBodies[0].rows, shown = 0;
      for (var i = 0; i < rows.length; i++) {
        var match = !q || rows[i].textContent.toLowerCase().indexOf(q) !== -1;
        rows[i].hidden = !match;
        if (match) shown++;
      }
      if (counter) counter.textContent = shown + " of " + rows.length + " rows shown";
      if (q && !sentFilter) { sentFilter = true; send("table_filter"); }
    });
  }
})();
