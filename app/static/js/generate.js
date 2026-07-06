// Generate form: show the source picker only in "from source material" mode.
function syncMode() {
  var source = document.querySelector('input[name=mode][value=source]').checked;
  document.getElementById('source-field').style.display = source ? '' : 'none';
  document.getElementById('topic-field').style.display = source ? 'none' : '';
}
window.syncMode = syncMode;
syncMode();
