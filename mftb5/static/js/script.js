var csrftoken;

// to be called whenever you update links
function targetBlank() {
  $('a[href^="http://"], a[href^="https://"], a[href^="mailto:"]').attr('target', '_blank');
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
  bindTouchFeedback('main a');
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

function bindTouchFeedback(selector) {
  // pjax and/or fastclick prevents clicks from looking like anything has happened.
  // I repeatedly found myself tapping over and over again on some links on my phone,
  // so we have to provide some other feedback mechanism for links. Dumb, I know.
  $(selector).css({opacity: ''}).on('touchend', function(e) {
    var currentOpacity = $(this).css('opacity');
    $(this).css({opacity: '0'}).animate({opacity: currentOpacity}, function() {
      $(this).css({opacity: ''});
    });
  });
}

$(function() {
  document.body.classList.add('js');
  document.body.classList.add('audio');
  $('body').removeClass('first-load');
  FastClick.attach(document.body);
  $(document).pjax('a[href^="/"]:not([download])', 'main');
  $.pjax.defaults.timeout = 10000;
  targetBlank();
  loadCsrf();
  bindTouchFeedback('main a');
  $('main').bind('pjax:end', pageLoadHook);
});
