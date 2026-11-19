/* Static-host-safe measurement: no cookies, identifiers, or network transmission. Counts stay in this browser only. */
document.addEventListener('click', function (event) {
  const link = event.target.closest('a');
  if (!link || !/^https?:/.test(link.href)) return;
  try {
    const key = 'cc_local_outbound_clicks';
    const count = Number(localStorage.getItem(key) || 0) + 1;
    localStorage.setItem(key, String(count));
  } catch (_) { /* Storage may be disabled. */ }
});
