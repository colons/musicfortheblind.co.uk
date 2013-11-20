var csrftoken;

// to be called whenever you update links
function targetBlank() {
  $('a[href^="http://"], a[href^="https://"]').attr('target', '_blank');
}

// things to run after updating the DOM
function loadHook() {
  targetBlank();
  bindEnqueue();
  bindIndexButtons();
}

// things to run after loading a main
function pageLoadHook() {
  $('body').removeClass('stranger');
  loadHook();
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
  $('#dropdowns').append('<span id="notify"></span>');
  var tab = $('#notify');
  tab.text(message);
  tab.slideDown().animate({opacity: 1}, 3000).slideUp();
}

$(function() {
  FastClick.attach(document.body);
  $(document).pjax('a[href^="/"]:not([download])', 'main');
  $.pjax.defaults.timeout = 3000;
  targetBlank();
  loadCsrf();
  $('main').bind('pjax:end', pageLoadHook);
});
