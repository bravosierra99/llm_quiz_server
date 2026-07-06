// Tutor thread page. Server values arrive via data attributes:
//   #tutor-form[data-question-id]  — the question this thread belongs to
//   #tutor-seed[data-mode/-session/-intent] — present only when auto-seeding
//
// CONTRACT NOTE: the payload shapes here (URLSearchParams bodies, Accept:
// application/json, and the reply keys read back — data.reply / data.skipped)
// are pinned on BOTH sides: tests/js/tutor.test.js asserts what is sent, and
// tests/test_tutor_contract.py feeds the same shapes to the real routes.
// Change one side only and a test goes red.

// Progressive enhancement: when JS is on, send the follow-up with fetch and swap
// the reply into the thread in place — no full-page reload. The plain <form> POST
// is the no-JS fallback (it 303s back to this page), so this only takes over
// when scripting is available.
(function () {
  var form = document.getElementById('tutor-form');
  if (!form || !window.fetch) return;
  var questionId = form.dataset.questionId;
  var thread = document.getElementById('tutor-thread');
  var empty = document.querySelector('.tutor-empty');
  var textarea = form.querySelector('textarea');
  var button = form.querySelector('button');

  function bubble(role, text) {
    var wrap = document.createElement('div');
    wrap.className = 'tutor-msg tutor-' + role;
    var who = document.createElement('span');
    who.className = 'tutor-who';
    who.textContent = role === 'user' ? 'You' : 'Tutor';
    var p = document.createElement('p');
    p.className = 'tutor-text';
    p.textContent = text;
    wrap.appendChild(who);
    wrap.appendChild(p);
    thread.appendChild(wrap);
    wrap.scrollIntoView({block: 'nearest'});
    return p; // so callers can update the text later (the thinking placeholder)
  }

  form.addEventListener('submit', function (e) {
    var msg = textarea.value.trim();
    if (!msg) return; // let the browser's required-validation handle it
    e.preventDefault();
    if (empty) empty.hidden = true;
    button.disabled = true;
    button.textContent = 'Thinking…';
    textarea.value = '';

    bubble('user', msg);
    var pending = bubble('assistant', 'Thinking…');
    pending.classList.add('tutor-pending');

    var body = new URLSearchParams();
    body.set('message', msg);
    body.set('back', form.querySelector('input[name=back]').value);

    fetch(form.getAttribute('action'), {
      method: 'POST',
      headers: {'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'},
      body: body.toString()
    }).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.json();
    }).then(function (data) {
      pending.textContent = data.reply || '(The tutor didn’t say anything — try again.)';
      pending.classList.remove('tutor-pending');
    }).catch(function () {
      pending.textContent = 'I couldn’t reach the tutor right now. Please try again in a moment.';
      pending.classList.remove('tutor-pending');
    }).then(function () {
      button.disabled = false;
      button.textContent = 'Ask →';
      pending.scrollIntoView({block: 'nearest'});
      textarea.focus();
    });
  });

  // Auto-seed an empty thread that arrived with ?seed=<mode>. Same fetch+swap as a
  // follow-up, but the request runs the canned intro. We echo the 'You' bubble so a
  // mid-flight reload (the server stores the reply regardless) renders the same shape.
  var seed = document.getElementById('tutor-seed');
  if (seed) {
    var backVal = form.querySelector('input[name=back]').value;
    // Drop ?seed/?session_id from the address bar so a manual reload won't re-fire.
    try {
      history.replaceState(null, '',
        '/tutor/' + questionId + (backVal ? '?back=' + encodeURIComponent(backVal) : ''));
    } catch (e) {}

    if (empty) empty.hidden = true;
    bubble('user', seed.dataset.intent);
    var seeding = bubble('assistant', 'Thinking…');
    seeding.classList.add('tutor-pending');

    var sbody = new URLSearchParams();
    sbody.set('mode', seed.dataset.mode);
    if (seed.dataset.session) sbody.set('session_id', seed.dataset.session);
    sbody.set('back', backVal);

    fetch('/questions/' + questionId + '/tutor', {
      method: 'POST',
      headers: {'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'},
      body: sbody.toString()
    }).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.json();
    }).then(function (data) {
      if (data.skipped) { window.location.reload(); return; } // raced — show real thread
      seeding.textContent = data.reply || '(The tutor didn’t say anything — try again.)';
      seeding.classList.remove('tutor-pending');
      seeding.scrollIntoView({block: 'nearest'});
    }).catch(function () {
      seeding.textContent = 'I couldn’t reach the tutor right now. Please reload to try again.';
      seeding.classList.remove('tutor-pending');
    });
  }
})();
