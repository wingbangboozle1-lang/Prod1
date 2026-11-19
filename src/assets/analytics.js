// Privacy-preserving event counter. No cookies, no localStorage, no fingerprinting.
// Events are kept in memory. They are sent only when the page sets
// <meta name="analytics-endpoint" content="https://..."> to an endpoint you control.
// The event list is a PROPOSAL (see Flagged FL-13) and is not confirmed.
(function () {
  var EVENTS = ["page_view", "outbound_click", "category_open", "guide_view", "flagged_view"];
  var meta = document.querySelector('meta[name="analytics-endpoint"]');
  var endpoint = (meta && meta.content) || "";
  var queue = [];

  function record(name, props) {
    if (EVENTS.indexOf(name) < 0) return;
    var evt = { event: name, path: location.pathname, ts: new Date().toISOString(), props: props || {} };
    queue.push(evt);
    if (endpoint && navigator.sendBeacon) {
      try { navigator.sendBeacon(endpoint, new Blob([JSON.stringify(evt)], { type: "application/json" })); } catch (e) {}
    }
  }
  window.SiteEvents = { record: record, queue: queue, endpointSet: !!endpoint };

  var p = location.pathname;
  record("page_view");
  if (/\/categories\/[^/]+\/?$/.test(p)) record("category_open", { category: p.split("/").filter(Boolean).pop() });
  if (/\/guides\/[^/]+\/?$/.test(p)) record("guide_view", { guide: p.split("/").filter(Boolean).pop() });
  if (/\/flagged\/?$/.test(p)) record("flagged_view");

  document.addEventListener("click", function (ev) {
    var a = ev.target && ev.target.closest && ev.target.closest("a[data-outbound]");
    if (a) record("outbound_click", { product: a.getAttribute("data-outbound") });
  }, true);
})();
