// Question editor: the choices box only applies to MCQ.
function syncType() {
  var t = document.getElementById('qtype').value;
  document.getElementById('choices-field').style.display = (t === 'mcq') ? '' : 'none';
}
window.syncType = syncType;
syncType();
