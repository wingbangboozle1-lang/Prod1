/* The Countertop Guide - the one client script this site loads.
   Five defined events (see methodology.html), counted in this browser only.
   No cookies, no fingerprints, no identifiers, and no network call while
   body[data-analytics-endpoint] is empty, which is how the site ships.
   Privacy-preserving by construction, not by promise. */
(function () {
  "use strict";
  var BODY = document.body || {};
  var ENDPOINT = BODY.getAttribute && BODY.getAttribute("data-analytics-endpoint") || "";
  var EVENTS = ["page_view", "outbound_click", "search", "chooser_complete", "guide_read"];
  var KEY = "ctg_counts";
  function store(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: stay silent */ } }
  function load(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function track(name, data) {
    if (EVENTS.indexOf(name) === -1) return;              // contract: these five names only
    data = data || {};
    var counts = load(KEY, {});
    counts[name] = (counts[name] || 0) + 1;
    store(KEY, counts);
    if (!ENDPOINT) return;                                  // gate: nothing leaves the device until a host exists
    try {
      /* Shape chosen to be accepted as-is by the endpoint in analytics-endpoint/server.py,
         which validates a top-level "event", a site "path" and an optional "asin". The two
         extra keys are ignored there and are what a future store would want. Names the
         endpoint does not know yet (search, chooser_complete, guide_read) are listed as an
         open request in COORDINATION.md rather than silently renamed here. */
      var payload = JSON.stringify({
        event: name,
        path: location.pathname,
        page: location.pathname,
        ts: new Date().toISOString(),
        asin: data.asin || undefined,
        data: data
      });
      if (navigator.sendBeacon) navigator.sendBeacon(ENDPOINT, payload);
    } catch (e) { /* measurement must never break the page */ }
  }
  window.ctgTrack = track;

  var TAG = (BODY.getAttribute && BODY.getAttribute("data-tag")) || "";
  /* ---- the chooser: spec-based shortlist, no claims we cannot source ---- */
  var PICKS = {
    dual:    { name: "Chefman 6QT Dual-Basket", asin: "B0CDY277D3", why: "two independent 3-quart baskets with Sync Finish, so two dishes land together - narrowest at 11.81 in wide" },
    oven:    { name: "Emeril Lagasse 26QT French-Door", asin: "B09B7SB46R", why: "the biggest cavity here - rotisserie and a 12-inch pizza per the listing, and the deepest at 16.9 in" },
    basket:  { name: "Chefman 8QT TurboFry", asin: "B08DKYBTPH", why: "one large basket in the shallowest footprint (12.75 in deep), basket and tray top-rack dishwasher safe per bullets" },
    instant: { name: "ThermoMaven 1-Second Instant-Read", asin: "B0DHZTCNR5", why: "the listing states a 1-second thermocouple read and a +/-0.5F tolerance with NIST and NSF certification named" },
    wireless:{ name: "CHEF iQ Sense Wireless, 3 probes", asin: "B0DZFD6R9Z", why: "three probes plus a hub, app alerts over WiFi, and 1000F heat-safe probes per the listing" }
  };
  function recommend(q1, q2, q3) {
    if (q1 === "meat") return q3 === "budget" ? [PICKS.instant, PICKS.wireless] : [PICKS.instant, PICKS.wireless];
    if (q1 === "family") return q2 === "compact" ? [PICKS.basket, PICKS.dual] : [PICKS.oven, PICKS.basket];
    if (q2 === "compact") return [PICKS.basket, PICKS.dual];
    return [PICKS.dual, PICKS.basket];
  }
  function link(p) {
    /* Every outbound product link on this site is sponsored - including the ones this
       script builds. rel + label + the click attribute, same as the static markup. */
    var u = 'https://www.amazon.com/dp/' + p.asin + (TAG ? '?tag=' + TAG : '');
    return '<a href="' + u + '" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="' + p.asin + '">' + p.name + '</a>';
  }

  document.addEventListener("DOMContentLoaded", function () {
    track("page_view", {});
    Array.prototype.forEach.call(document.querySelectorAll("a[data-ctg-outbound]"), function (a) {
      a.addEventListener("click", function () { track("outbound_click", { asin: a.getAttribute("data-asin") || "" }); });
    });

    var form = document.getElementById("chooser-form");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var q1 = form.querySelector('input[name="q1"]:checked');
        var q2 = form.querySelector('input[name="q2"]:checked');
        var q3 = form.querySelector('input[name="q3"]:checked');
        var out = document.getElementById("chooser-result");
        if (!q1 || !q2 || !q3) { out.innerHTML = '<p>Answer all three and you get a shortlist built from the listings.</p>'; return; }
        var picks = recommend(q1.value, q2.value, q3.value);
        out.innerHTML = '<div class="result"><strong>Your shortlist, from the specs</strong>' +
          '<ul>' + picks.map(function (p) { return "<li>" + link(p) + " <span class=\"fine\">- sponsored, opens Amazon - " + p.why + "</span></li>"; }).join("") + "</ul>" +
          '<p class="fine">Built from listing fields only - nobody has cooked in these. Today&rsquo;s price, current stock and the return window live on Amazon: ' +
          '<a href="compare.html">compare all five</a> or read <a href="verification.html">what we checked</a>.</p></div>';
        track("chooser_complete", { q1: q1.value, q2: q2.value, q3: q3.value });
        out.scrollIntoView({ behavior: "smooth", block: "nearest" });
      });
    }

    if (BODY.classList && BODY.classList.contains("guide-page")) {
      var fired = false;
      window.addEventListener("scroll", function () {
        if (fired) return;
        var h = document.documentElement;
        if ((h.scrollTop + h.clientHeight) / h.scrollHeight >= 0.75) { fired = true; track("guide_read", { page: location.pathname }); }
      }, { passive: true });
    }

    function bindSearch(formId, inputId) {
      var f = document.getElementById(formId);
      if (!f) return;
      f.addEventListener("submit", function (e) {
        e.preventDefault();
        var q = document.getElementById(inputId).value.trim();
        if (q) track("search", { q: q });
        location.href = "search.html?q=" + encodeURIComponent(q);
      });
    }
    bindSearch("site-search-form", "site-search-input");
    bindSearch("search-page-form", "search-input");

    var results = document.getElementById("search-results");
    if (results) {
      var q = (new URLSearchParams(location.search).get("q") || "").toLowerCase();
      var input = document.getElementById("search-input");
      if (input) input.value = q;
      fetch("data/search-index.json").then(function (r) { return r.json(); }).then(function (idx) {
        var hits = idx.filter(function (x) { return !q || (x.title + " " + x.text).toLowerCase().indexOf(q) > -1; });
        results.innerHTML = hits.length
          ? "<ul>" + hits.map(function (h) { return '<li><a href="' + h.url + '">' + h.title + "</a><br><span class=\"fine\">" + h.text + "</span></li>"; }).join("") + "</ul>"
          : "<p>Nothing matches &ldquo;" + q.replace(/[<>&]/g, "") + "&rdquo;. Try <em>depth</em>, <em>capacity</em>, <em>wireless</em> or <em>gift</em> - and if the answer you wanted is missing, that is a topic request: <a href=\"suggestions.html\">add it to the desk</a>.</p>";
      }).catch(function () { results.innerHTML = "<p>The search index did not load. <a href=\"guides.html\">Start with the guides</a>.</p>"; });
    }

    /* Where a reader can see what we counted, and wipe it. Honest, local, no server. */
    var meter = document.getElementById("local-meter");
    if (meter) {
      var c = load(KEY, {});
      meter.innerHTML = "<p class=\"fine\">Your browser has locally recorded: " +
        (EVENTS.map(function (k) { return k + " " + (c[k] || 0); }).join(" &middot; ")) +
        ' &middot; <button type="button" id="local-meter-clear" class="link-quiet" style="border:0;background:none;cursor:pointer;text-decoration:underline">clear</button></p>';
      var clear = document.getElementById("local-meter-clear");
      if (clear) clear.addEventListener("click", function () { store(KEY, {}); meter.innerHTML = "<p class=\"fine\">Local counts cleared. Nothing was ever sent anywhere.</p>"; });
    }
  });
})();
