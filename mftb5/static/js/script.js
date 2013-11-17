// to be called whenever you update links
function targetBlank() {
  $('a[href^="http://"], a[href^="https://"]').attr('target', '_blank');
}

$(function() {
  $(document).pjax('a', '#content');
  targetBlank();
});
