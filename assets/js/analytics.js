/* ShopNow Buying Guides — privacy-preserving analytics
   Self-hosted analytics endpoint + outbound-click counter.
   Records five defined events. No cookies, no personal data, no third-party scripts.
   Stores events in localStorage; can POST to a self-hosted beacon endpoint once one
   is deployed (the endpoint is a gate: automation stops there until a backend exists). */

(function () {
  'use strict';

  var ENDPOINT = '/api/analytics/collect'; // self-hosted beacon (gate: not wired until backend deployed)
  var STORAGE_KEY = 'shopnow_events';
  var MAX_EVENTS = 500;

  // The five defined events.
  var EVENTS = {
    page_view: 'page_view',
    outbound_click: 'outbound_click',
    affiliate_redirect: 'affiliate_redirect',
    guide_view: 'guide_view',
    conversion_signal: 'conversion_signal'
  };

  function readStorage() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) {
      return [];
    }
  }
  function writeStorage(events) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(events.slice(-MAX_EVENTS)));
    } catch (e) {
      // storage unavailable — events are still handled in-memory for this session
    }
  }
  function record(eventType, payload) {
    var event = {
      id: crypto && crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(36).slice(2),
      ts: new Date().toISOString(),
      event: eventType,
      page: location.pathname + location.search + location.hash,
      referrer: document.referrer || null,
      payload: payload || null
    };
    var events = readStorage();
    events.push(event);
    writeStorage(events);
    // Best-effort beacon to self-hosted endpoint. Fails silently if no backend.
    try {
      var beacon = new Blob([JSON.stringify(event)], { type: 'application/json' });
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, beacon);
      }
    } catch (e) {
      // beacon not supported — ignore
    }
    return event;
  }

  function init() {
    // 1. page_view on load
    record(EVENTS.page_view);

    // 2. outbound_click + affiliate_redirect on affiliate / outbound links
    document.addEventListener('click', function (ev) {
      var a = ev.target.closest && ev.target.closest('a[href]');
      if (!a) return;
      var href = a.getAttribute('href') || '';
      var isOutbound = href.indexOf('http') === 0 && href.indexOf(location.origin) !== 0;
      var isAffiliate = a.getAttribute('rel') && a.getAttribute('rel').indexOf('sponsored') !== -1;
      if (isOutbound) {
        record(EVENTS.outbound_click, { target: href, sponsored: isAffiliate });
        if (isAffiliate && href.indexOf('amazon') !== -1 || href.indexOf('link.amazon') !== -1) {
          record(EVENTS.affiliate_redirect, { target: href });
        }
      }
    }, true);

    // 3. guide_view when a question-shaped guide page loads is handled by page_view on that page;
    // explicit recording is exposed for pages that want it:
    window.shopnowAnalytics = { record: record, EVENTS: EVENTS };
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
