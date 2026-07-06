// Site-wide behaviors, loaded at the end of <body> on every page.

// Don't let a second action fire while one is still working: when any form inside
// an action row submits, disable every button in that row (the submit itself still
// goes through). Stops e.g. firing two tutor calls from the feedback screen.
// Deferred one tick on purpose: a submit button that's disabled *during* the submit
// event is dropped from the form data (native) and we don't want to race htmx's
// serialization either — so we let the request capture its params first (incl. the
// submitter, e.g. name="dont_know"), then lock the buttons before any human could
// click again.
document.addEventListener('submit', function (e) {
  var box = e.target.closest('.feedback-actions, .row-actions, .actions');
  if (box) setTimeout(function () {
    box.querySelectorAll('button').forEach(function (b) { b.disabled = true; });
  }, 0);
}, true);

// Quiz keyboard ergonomics. The quiz flow swaps #quiz-stage in place (htmx), which
// drops focus back to <body> after every question — so the keyboard does nothing
// until you click in. Re-focus the first answer control after each render so the
// whole quiz is drivable from the keyboard: Tab / ↑↓ move between options, Space
// selects, Enter submits; number keys 1–9 jump straight to an option.
function focusQuizStage() {
  var stage = document.getElementById('quiz-stage');
  if (!stage) return;
  var first = stage.querySelector('.choice-list input[type=radio], textarea[name=answer]');
  if (first) { try { first.focus({ preventScroll: false }); } catch (e) {} }
}
document.addEventListener('DOMContentLoaded', focusQuizStage);
// htmx settles the swapped-in content; re-focus then so navigation lands in the form.
document.addEventListener('htmx:afterSettle', focusQuizStage);

document.addEventListener('keydown', function (e) {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  var stage = document.getElementById('quiz-stage');
  if (!stage) return;
  // Number keys pick the Nth choice — but never while typing a short answer.
  var typing = e.target.tagName === 'TEXTAREA' ||
               (e.target.tagName === 'INPUT' && e.target.type !== 'radio');
  if (!typing && e.key >= '1' && e.key <= '9') {
    var radios = stage.querySelectorAll('.choice-list input[type=radio]');
    var pick = radios[parseInt(e.key, 10) - 1];
    if (pick) { pick.checked = true; pick.focus(); e.preventDefault(); }
  }
}, false);
window.focusQuizStage = focusQuizStage;
