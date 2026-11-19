// The Countertop Guide — search, shortlist, privacy-preserving local metrics, and reviewer controls.
(function () {
  "use strict";

  var ENDPOINT = document.body && document.body.getAttribute("data-analytics-endpoint") || "";
  var EVENTS = ["page_view", "outbound_click", "search", "chooser_complete", "guide_read"];
  var LOCAL_RETENTION_DAYS = 30;
  var COUNTS_KEY = "ctg_counts_v1";
  var DECISIONS_KEY = "ctg_decisions_v1";
  var ASIN_RE = /^[A-Z0-9]{10}$/;

  function load(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function store(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      return false;
    }
  }

  function todayUtc() {
    return new Date().toISOString().slice(0, 10);
  }

  function recordLocal(name) {
    var today = todayUtc();
    var counts = load(COUNTS_KEY, {});
    if (!counts || typeof counts !== "object" || Array.isArray(counts)) counts = {};

    Object.keys(counts).forEach(function (day) {
      var age = (Date.parse(today + "T00:00:00Z") - Date.parse(day + "T00:00:00Z")) / 86400000;
      if (!Number.isFinite(age) || age < 0 || age >= LOCAL_RETENTION_DAYS) delete counts[day];
    });
    if (!counts[today] || typeof counts[today] !== "object" || Array.isArray(counts[today])) counts[today] = {};
    counts[today][name] = (Number(counts[today][name]) || 0) + 1;
    store(COUNTS_KEY, counts);
  }

  function sendAggregate(name, details) {
    if (!ENDPOINT) return;
    try {
      var endpointUrl = new URL(ENDPOINT, window.location.href);
      var localDevelopment = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
      if (endpointUrl.protocol !== "https:" && !localDevelopment) return;

      // Deliberately allow only a page path and (for outbound clicks) an ASIN.
      // Search terms, full links, choices, referrers, and client identifiers are never sent.
      var payload = { event: name, path: window.location.pathname };
      if (name === "outbound_click") {
        if (!details || typeof details.asin !== "string" || !ASIN_RE.test(details.asin)) return;
        payload.asin = details.asin;
      }
      var body = JSON.stringify(payload);
      if (navigator.sendBeacon) {
        navigator.sendBeacon(endpointUrl.href, body);
      } else if (window.fetch) {
        fetch(endpointUrl.href, {
          method: "POST",
          mode: "cors",
          credentials: "omit",
          headers: { "Content-Type": "text/plain;charset=UTF-8" },
          body: body,
          keepalive: true
        }).catch(function () {});
      }
    } catch (error) {
      // Analytics must never interrupt navigation or page interaction.
    }
  }

  function track(name, details) {
    if (EVENTS.indexOf(name) === -1) return;
    recordLocal(name);
    sendAggregate(name, details || {});
  }
  window.ctgTrack = track;

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (character) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[character];
    });
  }

  function bindSearch(formId, inputId) {
    var form = document.getElementById(formId);
    var input = document.getElementById(inputId);
    if (!form || !input) return;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var query = input.value.trim();
      if (query) track("search");
      window.location.href = "search.html?q=" + encodeURIComponent(query);
    });
  }

  function bindChooser() {
    var form = document.getElementById("chooser-form");
    if (!form) return;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var q1 = form.querySelector('input[name="q1"]:checked');
      var q2 = form.querySelector('input[name="q2"]:checked');
      var q3 = form.querySelector('input[name="q3"]:checked');
      var output = document.getElementById("chooser-result");
      if (!output) return;
      if (!q1 || !q2 || !q3) {
        output.innerHTML = "<p>Answer all three questions to see a spec-based shortlist.</p>";
        return;
      }
      var picks = recommend(q1.value, q2.value, q3.value);
      output.innerHTML = '<div class="result"><strong>Spec-based shortlist — not a hands-on recommendation:</strong><ul>' +
        picks.map(function (product) {
          return '<li><a href="' + product.href + '" rel="sponsored nofollow noopener" target="_blank" data-ctg-outbound data-asin="' + product.asin + '">' +
            escapeHtml(product.name) + '</a> — ' + escapeHtml(product.why) + '</li>';
        }).join("") +
        '</ul><p class="small">Prices and details are historical listing snapshots. Confirm the current listing and variant before buying. See the <a href="compare.html">full comparison</a>.</p></div>';
      track("chooser_complete");
      output.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }

  function recommend(q1, q2, q3) {
    var products = {
      dual: {
        name: "Chefman 6QT Dual-Basket (B0CDY277D3)",
        asin: "B0CDY277D3",
        href: "https://www.amazon.com/dp/B0CDY277D3?tag=shopnow047c-20",
        why: "The captured listing describes two 3-quart baskets and Sync Finish; cooking results have not been tested."
      },
      oven: {
        name: "Emeril Lagasse 26QT French-Door Oven (B09B7SB46R)",
        asin: "B09B7SB46R",
        href: "https://www.amazon.com/dp/B09B7SB46R?tag=shopnow047c-20",
        why: "The captured title says 26QT; compare the listed dimensions and verify clearance in the current manual."
      },
      basket: {
        name: "Chefman 8QT TurboFry Basket (B08DKYBTPH)",
        asin: "B08DKYBTPH",
        href: "https://www.amazon.com/dp/B08DKYBTPH?tag=shopnow047c-20",
        why: "The captured listing describes one 8-quart basket; its stated depth is 12.75 inches."
      },
      instant: {
        name: "ThermoMaven Instant-Read (B0DHZTCNR5)",
        asin: "B0DHZTCNR5",
        href: "https://www.amazon.com/dp/B0DHZTCNR5?tag=shopnow047c-20",
        why: "The listing capture states ±0.5°F and a one-second read; neither claim was independently tested."
      },
      wireless: {
        name: "CHEF iQ Sense Wireless, 3 probes (B0DZFD6R9Z)",
        asin: "B0DZFD6R9Z",
        href: "https://www.amazon.com/dp/B0DZFD6R9Z?tag=shopnow047c-20",
        why: "The listing describes three probes and app connectivity; real-world connection has not been tested."
      }
    };

    if (q1 === "meat") return q3 === "premium" ? [products.wireless, products.instant] : [products.instant, products.wireless];
    if (q1 === "family" && q2 !== "compact" && q3 === "premium") return [products.oven, products.dual];
    if (q1 === "family" && q2 !== "compact") return [products.dual, products.basket];
    if (q3 === "budget" || q2 === "compact") return [products.basket, products.dual];
    return [products.dual, products.basket];
  }

  function bindOutboundClicks() {
    document.addEventListener("click", function (event) {
      var link = event.target && event.target.closest ? event.target.closest("a[data-ctg-outbound]") : null;
      if (!link) return;
      track("outbound_click", { asin: link.getAttribute("data-asin") || "" });
    });
  }

  function bindGuideRead() {
    if (!document.body.classList.contains("guide-page")) return;
    var fired = false;
    window.addEventListener("scroll", function () {
      if (fired) return;
      var root = document.documentElement;
      var percentage = (root.scrollTop + root.clientHeight) / Math.max(root.scrollHeight, 1);
      if (percentage >= 0.75) {
        fired = true;
        track("guide_read");
      }
    }, { passive: true });
  }

  function bindSearchResults() {
    var results = document.getElementById("search-results");
    if (!results) return;
    var params = new URLSearchParams(window.location.search);
    var query = (params.get("q") || "").toLowerCase();
    var input = document.getElementById("search-input");
    if (input) input.value = params.get("q") || "";
    fetch("data/search-index.json")
      .then(function (response) { if (!response.ok) throw new Error("Search index unavailable"); return response.json(); })
      .then(function (index) {
        var hits = query ? index.filter(function (entry) {
          return (entry.title + " " + entry.text).toLowerCase().indexOf(query) !== -1;
        }) : index;
        if (!hits.length) {
          results.innerHTML = "<p>No matches. Try “air fryer”, “thermometer”, “capacity”, or “cleanup”.</p>";
          return;
        }
        results.innerHTML = "<ul>" + hits.map(function (entry) {
          return '<li><a href="' + escapeHtml(entry.url) + '">' + escapeHtml(entry.title) + '</a> — ' + escapeHtml(entry.text) + '</li>';
        }).join("") + "</ul>";
      })
      .catch(function () { results.innerHTML = "<p>Search index unavailable.</p>"; });
  }

  function bindDecisionBoard() {
    var controls = Array.prototype.slice.call(document.querySelectorAll("select[data-decision-id]"));
    if (!controls.length) return;
    var status = document.getElementById("decision-save-status");
    var download = document.getElementById("download-decision-record");
    var clear = document.getElementById("clear-decision-record");
    var decisions = load(DECISIONS_KEY, {});
    if (!decisions || typeof decisions !== "object" || Array.isArray(decisions)) decisions = {};
    var allowed = ["approve", "defer", "reject"];

    controls.forEach(function (select) {
      var id = select.getAttribute("data-decision-id");
      if (allowed.indexOf(decisions[id]) !== -1) select.value = decisions[id];
      select.addEventListener("change", function () {
        if (allowed.indexOf(select.value) === -1) delete decisions[id];
        else decisions[id] = select.value;
        if (store(DECISIONS_KEY, decisions)) {
          if (status) status.textContent = "Choices saved in this browser only. They are not sent to the site.";
        } else if (status) {
          status.textContent = "This browser could not save local choices. Use Download decision record to keep a copy.";
        }
      });
    });

    if (download) download.addEventListener("click", function () {
      var record = {
        title: "The Countertop Guide — local suggestion decisions",
        generatedAt: new Date().toISOString(),
        note: "Selections are reviewer notes only; they are not submitted to the site.",
        decisions: decisions
      };
      var blob = new Blob([JSON.stringify(record, null, 2)], { type: "application/json" });
      var url = URL.createObjectURL(blob);
      var link = document.createElement("a");
      link.href = url;
      link.download = "countertop-guide-decisions.json";
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    });

    if (clear) clear.addEventListener("click", function () {
      try { localStorage.removeItem(DECISIONS_KEY); } catch (error) {}
      decisions = {};
      controls.forEach(function (select) { select.value = ""; });
      if (status) status.textContent = "Local choices cleared from this browser.";
    });

    if (status && Object.keys(decisions).length) status.textContent = "Saved choices loaded from this browser. They are not sent to the site.";
  }

  document.addEventListener("DOMContentLoaded", function () {
    track("page_view");
    bindOutboundClicks();
    bindGuideRead();
    bindChooser();
    bindSearch("site-search-form", "site-search-input");
    bindSearch("search-page-form", "search-input");
    bindSearchResults();
    bindDecisionBoard();
    var stickyBar = document.getElementById("sticky-bar");
    if (stickyBar) stickyBar.style.display = "flex";
  });
})();
