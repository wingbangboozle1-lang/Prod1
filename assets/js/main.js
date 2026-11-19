/* ShopNow Buying Guides — front-page behaviour
   Populates the submitted-product grid from data/products.json and wires the
   three-question chooser (S-19). No values are inferred; blanks stay blank. */

(function () {
  'use strict';

  var container = document.getElementById('product-listing');
  var heroTitle = document.getElementById('hero-product-title');
  var heroPrice = document.getElementById('hero-product-price');
  var heroLink = document.getElementById('hero-product-link');
  var heroThumb = document.querySelector('#hero-product .thumb');

  function esc(text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function statusLine(label, status) {
    return '<p class="tag" style="font-size:12px;"><b>' + esc(label) + ':</b> <span class="unverified" style="font-size:12px;">' + esc(status) + '</span></p>';
  }

  function render(products) {
    if (!container) return;
    container.innerHTML = '';
    products.forEach(function (p) {
      var card = document.createElement('article');
      card.className = 'card';
      card.dataset.category = esc(p.category || 'uncategorized');
      var imageHtml = p.imageUrl
        ? '<img src="' + esc(p.imageUrl) + '" alt="' + esc(p.title || 'Product image') + '" class="thumb" style="height:150px;object-fit:cover;border-radius:8px;border:1px solid var(--border);">'
        : '<div class="thumb">No real photography available &mdash; decision pending (IR-02)</div>';
      var linkHtml = p.submittedLink
        ? '<a class="btn" href="' + esc(p.submittedLink) + '" rel="sponsored" target="_blank" rel="noopener noreferrer">View on Amazon</a>'
        : '<button class="btn" disabled>No link on file</button>';
      card.innerHTML =
        imageHtml +
        '<h3>' + esc(p.title || 'Product ' + p.id.slice(-1) + ' &mdash; title unverified') + '</h3>' +
        '<p class="price">Price <b>' + esc(p.price || 'unverified') + '</b></p>' +
        statusLine('Intended ASIN', p.intendedAsinStatus || 'unverified') +
        statusLine('Official listing URL', p.officialListingUrlStatus || 'blank') +
        statusLine('Confirmation date', p.confirmationDateStatus || 'blank') +
        statusLine('Source', p.source || 'user-submitted affiliate link') +
        statusLine('Redirect target (separate field)', p.redirectTargetStatus || 'blank') +
        '<div class="product-actions" style="margin-top:auto;">' + linkHtml +
        '<a class="btn secondary" href="dashboard.html">Findings &rarr;</a></div>';
      container.appendChild(card);
    });
  }

  function load() {
    fetch('data/products.json')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        var products = data.products || [];
        render(products);
        // Hero uses the first product as the lead product (leads with the products).
        if (products[0]) {
          var first = products[0];
          if (heroTitle) heroTitle.textContent = first.title || 'Product 1 &mdash; pending verification';
          if (heroPrice) heroPrice.textContent = first.price || 'unverified';
          if (heroLink) heroLink.href = first.submittedLink || '#';
          if (heroThumb) heroThumb.innerHTML = first.imageUrl
            ? '<img src="' + esc(first.imageUrl) + '" alt="Lead product" style="width:100%;height:150px;object-fit:cover;border-radius:8px;border:1px solid var(--border);">'
            : 'No real photography available &mdash; decision pending (IR-02)';
        }
      })
      .catch(function (err) {
        console.error('Failed to load products.json', err);
        if (container) container.innerHTML = '<p class="blank">Could not load product register.</p>';
      });
  }

  // Chooser: clicking a button filters the product grid by category hint.
  var chooserButtons = document.querySelectorAll('.chooser button');
  chooserButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var label = btn.textContent.trim();
      var cards = document.querySelectorAll('#product-listing .card');
      cards.forEach(function (card) {
        card.style.display = 'none';
      });
      // Very loose keyword mapping &mdash; a working surface, not a claim.
      var showAll = label.indexOf('family') !== -1;
      var count = 0;
      cards.forEach(function (card) {
        if (showAll || label.indexOf('tight') !== -1 || label.indexOf('one or two') !== -1) {
          card.style.display = '';
          count++;
        }
      });
    });
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', load);
  } else {
    load();
  }
})();
