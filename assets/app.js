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
      /* The contract, enforced by scripts/test_event_contract.py in CI: a top-level "event"
         from EVENTS, a site "path", an optional "asin" for clicks, and the small "data"
         object each event documents. The endpoint refuses an outbound_click with no asin, a
         search with no query, and a chooser result whose answers are not the ones it offers.
         Nothing here is sent until body[data-analytics-endpoint] names a host, and the site
         ships with that attribute empty. */
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
    basket:  { name: "Chefman 8QT TurboFry", asin: "B08DKYBTPH", why: "one large basket, and the shallowest of the three at 12.75 in deep (footprint area is not the same claim); basket and tray top-rack dishwasher safe per bullets" },
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
        if (q) track("search", { q: q.slice(0, 80) });   // 80 chars is the endpoint limit; longer input is a paste, not a query
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
      /* Guarded, because a context with no fetch (an older engine, a file:// open, a
         stripped CSP) throws synchronously and a promise catch cannot see a ReferenceError. */
      if (typeof fetch !== "function") {
        results.innerHTML = "<p>Search needs <code>fetch</code>, which this browser context did not provide. <a href=\"guides.html\">Start with the guides</a>.</p>";
      } else {
      fetch("data/search-index.json").then(function (r) { return r.json(); }).then(function (idx) {
        var hits = idx.filter(function (x) { return !q || (x.title + " " + x.text).toLowerCase().indexOf(q) > -1; });
        results.innerHTML = hits.length
          ? "<ul>" + hits.map(function (h) { return '<li><a href="' + h.url + '">' + h.title + "</a><br><span class=\"fine\">" + h.text + "</span></li>"; }).join("") + "</ul>"
          : "<p>Nothing matches &ldquo;" + q.replace(/[<>&]/g, "") + "&rdquo;. Try <em>depth</em>, <em>capacity</em>, <em>wireless</em> or <em>gift</em> - and if the answer you wanted is missing, that is a topic request: <a href=\"suggestions.html\">add it to the desk</a>.</p>";
      }).catch(function () { results.innerHTML = "<p>The search index did not load. <a href=\"guides.html\">Start with the guides</a>.</p>"; });
      }
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

// Suggestions decision desk - a reviewer picks a path per item, keeps it in this browser,
// and exports a review sheet to paste into docs/decisions.md. Static hosting only: nothing
// is sent anywhere, and no pick is recorded as a decision until an owner writes it down.
(function(){
  "use strict";
  var KEY = "ctg_suggestion_picks";
  var board = document.getElementById("suggestion-board");
  if(!document.querySelector) return;
  /* The page keeps its panels in separate containers (the path picker is a div of its own),
     so the controls are scoped to the document, not to one box. Restricting the sweep to
     ids that look like board rows is what keeps it from touching anything else. */
  function rows(){ return document.querySelectorAll('tr[id^="SG-"], tr[id^="Q-"], tr[id^="DI-"], article.sg[id]'); }
  function allSelects(){ return document.querySelectorAll("select[data-pick]"); }
  var OPTIONS = [["approve", "Approve - build it"], ["defer", "Defer - park it with a date"], ["reject", "Reject - and why on the flag list"]];

  function load(){ try{ return JSON.parse(localStorage.getItem(KEY) || "{}"); }catch(e){ return {}; } }
  function save(picks){ try{ localStorage.setItem(KEY, JSON.stringify(picks)); }catch(e){} }
  function title(row){
    var h = row.querySelector("h3") || row.querySelector("td:nth-child(2)");
    return h ? h.textContent.replace(/\s+/g, " ").trim().slice(0, 140) : "";
  }
  function sel(id, current){
    var el = document.createElement("select");
    el.setAttribute("data-pick", id);
    el.setAttribute("aria-label", "Your pick for " + id);
    var opts = [["", "Not picked yet"]].concat(OPTIONS);
    opts.forEach(function(o){
      var op = document.createElement("option");
      op.value = o[0]; op.textContent = o[1];
      if (o[0] === current) op.selected = true;
      el.appendChild(op);
    });
    return el;
  }
  /* Every numbered row on the board gets a control, including rows other passes add later.
     Rows that already ship a select (the path cards) are left exactly as they are. */
  var seen = {};
  Array.prototype.forEach.call(rows(), function(row){
    var id = row.getAttribute("id");
    if(!/^(SG|Q|DI)-/.test(id) || seen[id]) return;
    seen[id] = row;
    var picks = load();
    if (row.tagName === "TR") {
      if (row.querySelector("select[data-pick]")) return;
      var td = document.createElement("td");
      td.appendChild(sel(id, picks[id] || ""));
      var note = document.createElement("p");
      note.className = "pick-status";
      td.appendChild(note);
      row.appendChild(td);
    } else {
      var host = document.createElement("p");
      host.className = "review-state";
      host.appendChild(sel(id, picks[id] || ""));
      var n2 = document.createElement("span");
      n2.className = "pick-status";
      host.appendChild(n2);
      row.appendChild(host);
    }
  });
  Array.prototype.forEach.call(document.querySelectorAll("table"), function(t){
    var head = t.querySelector("tr");
    if (!head || !head.querySelector("th")) return;
    var count = 0;
    Array.prototype.forEach.call(t.querySelectorAll("tr[id]"), function(r){ if (r.querySelector("select[data-pick]")) count++; });
    if (count && !/Your pick/.test(head.textContent)) {
      var th = document.createElement("th");
      th.textContent = "Your pick";
      th.setAttribute("scope", "col");
      head.appendChild(th);
    }
  });
  function refreshStatus(){
    Array.prototype.forEach.call(allSelects(), function(el){
      var row = el.closest("tr") || el.closest("article");
      if(!row) return;
      var note = row.querySelector(".pick-status");
      if(note){ note.textContent = el.value === "" ? "" : el.value; }
    });
    var meter = document.getElementById("pick-meter");
    if (meter) {
      var all = allSelects().length;
      var n = Object.keys(load()).length;
      meter.textContent = n + " of " + all + " numbered rows picked in this browser. Nothing has been sent; a pick becomes a decision when it is written into docs/decisions.md.";
    }
  }
  Array.prototype.forEach.call(allSelects(), function(el){
    el.addEventListener("change", function(){
      var p = load();
      var id = el.getAttribute("data-pick");
      if(el.value){ p[id] = el.value; } else { delete p[id]; }
      save(p);
      refreshStatus();
    });
  });
  refreshStatus();

  function sheet(){
    var picks = load(), out = [];
    Object.keys(picks).sort().forEach(function(id){
      out.push("- " + id + ": " + picks[id] + (seen[id] && title(seen[id]) ? " - " + title(rows[id]) : ""));
    });
    return "# Decision sheet - The Countertop Guide board\n\nExported " + new Date().toISOString() +
      "\n\nPicks recorded in this browser (they are not a decision until an owner writes them into docs/decisions.md or COORDINATION.md):\n\n" +
      (out.length ? out.join("\n") : "- none yet") + "\n";
  }
  var exp = document.getElementById("sg-export");
  if(exp){
    exp.addEventListener("click", function(){
      var blob = new Blob([sheet()], {type:"text/markdown"});
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "countertop-guide-decisions.md";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(a.href);
    });
  }
  var pr = document.getElementById("sg-print");
  if(pr){ pr.addEventListener("click", function(){ window.print(); }); }
  var rs = document.getElementById("sg-reset");
  if(rs){
    rs.addEventListener("click", function(){
      if(!window.confirm("Clear all picks on this page?")) return;
      try{ localStorage.removeItem(KEY); }catch(e){}
      Array.prototype.forEach.call(allSelects(), function(el){ el.value = ""; });
      refreshStatus();
    });
  }
})();
