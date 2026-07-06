// Short-answer (flashcard) question screen: reveal the answer, then self-grade.
function reveal() {
  document.getElementById('reveal-box').style.display = 'block';
  document.getElementById('reveal-btn').style.display = 'none';
}
function setSelf(v) { document.getElementById('self_correct').value = v; }
window.reveal = reveal;
window.setSelf = setSelf;
