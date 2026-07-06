// "Select all" checkbox for a collection: mirror its state onto every enabled
// chapter checkbox belonging to that collection.
function toggleColl(box, cid) {
  document.querySelectorAll('input[name="chapter_ids"][data-coll="' + cid + '"]:not([disabled])')
    .forEach(function (cb) { cb.checked = box.checked; });
}
window.toggleColl = toggleColl;
