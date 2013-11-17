// to be called whenever you update links
function targetBlank() {
  $('a[href^="http://"], a[href^="https://"]').attr('target', '_blank');
}

// things to run after updating the DOM
function loadHook() {
  targetBlank();
  bindEnqueue();
}

$(function() {
  $(document).pjax('a[href^="/"]:not([download])', '#content');
  targetBlank();
  $('#content').bind('pjax:end', loadHook);
});
