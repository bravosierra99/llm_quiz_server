// Theme handling. Loaded SYNCHRONOUSLY in <head> (no defer) on purpose: the
// saved theme must be applied before first paint or the page flashes
// light/dark. No value stored => fall back to the OS preference (CSS handles it).
(function () {
  try {
    var t = localStorage.getItem('theme');
    if (t === 'light' || t === 'dark') document.documentElement.setAttribute('data-theme', t);
  } catch (e) {}
})();

// Theme toggle: flip the explicit choice and remember it. With nothing stored we
// follow the OS, so the first toggle picks the opposite of whatever is showing.
function toggleTheme() {
  var root = document.documentElement;
  var cur = root.getAttribute('data-theme');
  if (!cur) {
    cur = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  var next = cur === 'dark' ? 'light' : 'dark';
  root.setAttribute('data-theme', next);
  try { localStorage.setItem('theme', next); } catch (e) {}
}
window.toggleTheme = toggleTheme;
