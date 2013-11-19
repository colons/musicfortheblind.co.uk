var csrftoken;

// to be called whenever you update links
function targetBlank() {
  $('a[href^="http://"], a[href^="https://"]').attr('target', '_blank');
}

// things to run after updating the DOM
function loadHook() {
  targetBlank();
  bindEnqueue();
}

function loadCsrf() {
  csrftoken = $.cookie('csrftoken');
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  $.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
}

function notify(message) {
  $('#notify').remove();
  $('#controls p').append('<span id="notify"></span>');
  var tab = $('#notify');
  tab.text(message);
  tab.slideDown().animate({opacity: 1}, 3000).slideUp();
}

$(function() {
  $(document).pjax('a[href^="/"]:not([download])', '#content');
  $.pjax.defaults.timeout = 3000;
  targetBlank();
  loadCsrf();
  $('#content').bind('pjax:end', loadHook);
});
