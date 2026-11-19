// The Countertop Guide — client JS (no tracking by default; privacy-preserving local counts only)
(function(){
  "use strict";
  var ENDPOINT = document.body && document.body.getAttribute("data-analytics-endpoint") || "";
  var EVENTS = ["page_view","outbound_click","search","chooser_complete","guide_read"];
  function store(k,v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){} }
  function load(k,d){ try{ var v=localStorage.getItem(k); return v?JSON.parse(v):d; }catch(e){ return d; } }
  function track(name, data){
    data = data || {};
    if(EVENTS.indexOf(name)===-1) return;
    var counts = load("ctg_counts", {});
    counts[name] = (counts[name]||0)+1;
    store("ctg_counts", counts);
    if(ENDPOINT){
      try{
        var payload = JSON.stringify({event:name, page:location.pathname, ts:new Date().toISOString(), data:data});
        if(navigator.sendBeacon){ navigator.sendBeacon(ENDPOINT, payload); }
      }catch(e){}
    }
  }
  window.ctgTrack = track;
  document.addEventListener("DOMContentLoaded", function(){
    track("page_view", {});
    // Outbound sponsored clicks
    document.querySelectorAll('a[data-ctg-outbound]').forEach(function(a){
      a.addEventListener("click", function(){ track("outbound_click", {asin:a.getAttribute("data-asin")||"", href:a.href}); });
    });
    // Guide read: 75% scroll on guide pages
    if(document.body.classList.contains("guide-page")){
      var fired=false;
      window.addEventListener("scroll", function(){
        if(fired) return;
        var h=document.documentElement;
        var pct=(h.scrollTop+h.clientHeight)/h.scrollHeight;
        if(pct>=0.75){ fired=true; track("guide_read", {}); }
      }, {passive:true});
    }
    // Chooser
    var form=document.getElementById("chooser-form");
    if(form){
      form.addEventListener("submit", function(e){
        e.preventDefault();
        var q1=form.querySelector('input[name="q1"]:checked');
        var q2=form.querySelector('input[name="q2"]:checked');
        var q3=form.querySelector('input[name="q3"]:checked');
        var out=document.getElementById("chooser-result");
        if(!q1||!q2||!q3){ out.innerHTML="<p>Answer all three questions to see a spec-based shortlist.</p>"; return; }
        var pick = recommend(q1.value, q2.value, q3.value);
        out.innerHTML = '<div class="result"><strong>Your shortlist (spec-based, not hands-on tested):</strong><ul>'+
          pick.map(function(p){ return '<li><a href="'+p.href+'">'+p.name+'</a> — '+p.why+'</li>'; }).join("")+
          '</ul><p class="small">Prices are snapshots from '+document.body.getAttribute("data-verified-date")+'. Always confirm price and fit on Amazon before buying. See <a href="compare.html">full comparison</a>.</p></div>';
        track("chooser_complete", {q1:q1.value,q2:q2.value,q3:q3.value});
        out.scrollIntoView({behavior:"smooth", block:"nearest"});
      });
    }
    // Search
    function bindSearch(formId, inputId){
      var f=document.getElementById(formId);
      if(!f) return;
      f.addEventListener("submit", function(e){
        e.preventDefault();
        var q=document.getElementById(inputId).value.trim();
        if(q) track("search", {q:q});
        location.href="search.html?q="+encodeURIComponent(q);
      });
    }
    bindSearch("site-search-form","site-search-input");
    bindSearch("search-page-form","search-input");
    var results=document.getElementById("search-results");
    if(results){
      var params=new URLSearchParams(location.search);
      var q=(params.get("q")||"").toLowerCase();
      var input=document.getElementById("search-input");
      if(input) input.value=q;
      fetch("data/search-index.json").then(function(r){return r.json();}).then(function(idx){
        var hits = q ? idx.filter(function(x){ return (x.title+" "+x.text).toLowerCase().indexOf(q)>-1; }) : idx;
        results.innerHTML = hits.length ? "<ul>"+hits.map(function(h){return '<li><a href="'+h.url+'">'+h.title+'</a> — '+h.text+'</li>';}).join("")+"</ul>" : "<p>No matches. Try “air fryer”, “thermometer”, “capacity” or “cleanup”.</p>";
      }).catch(function(){ results.innerHTML="<p>Search index unavailable.</p>"; });
    }
    // Sticky compare bar: show cheapest air fryer price snapshot link
    var bar=document.getElementById("sticky-bar");
    if(bar){ bar.style.display="flex"; }
  });
  function recommend(q1,q2,q3){
    // q1: snacks|family|meat ; q2: compact|standard|plenty ; q3: budget|mid|premium
    var P={
      dual:{name:"Chefman 6QT Dual-Basket (B0CDY277D3)", href:"https://www.amazon.com/dp/B0CDY277D3?tag=shopnow047c-20", why:"two independent baskets, Sync Finish, smallest depth of the three fryers (13.38\")"},
      oven:{name:"Emeril Lagasse 26QT French-Door Oven (B09B7SB46R)", href:"https://www.amazon.com/dp/B09B7SB46R?tag=shopnow047c-20", why:"largest capacity (26QT), rotisserie + 12-inch pizza per listing; needs the most counter depth (16.9\")"},
      basket:{name:"Chefman 8QT TurboFry Basket (B08DKYBTPH)", href:"https://www.amazon.com/dp/B08DKYBTPH?tag=shopnow047c-20", why:"single large basket, 450°F Hi-Fry, top-rack dishwasher-safe basket"},
      instant:{name:"ThermoMaven 1-Second Instant-Read (B0DHZTCNR5)", href:"https://www.amazon.com/dp/B0DHZTCNR5?tag=shopnow047c-20", why:"±0.5°F NIST accuracy, 1-second read, waterproof"},
      wireless:{name:"CHEF iQ Sense Wireless, 3 probes (B0DZFD6R9Z)", href:"https://www.amazon.com/dp/B0DZFD6R9Z?tag=shopnow047c-20", why:"WiFi monitoring, 3 probes at once, 1000°F heat-safe probes"}
    };
    if(q1==="meat") return q3==="premium" ? [P.wireless, P.instant] : [P.instant, P.wireless];
    if(q1==="family") return q2==="compact" ? [P.basket, P.dual] : [P.oven, P.basket];
    // snacks
    if(q2==="compact") return [P.dual, P.basket];
    if(q3==="budget") return [P.basket, P.dual];
    return [P.dual, P.basket];
  }
})();
