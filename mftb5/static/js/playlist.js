var playlistTemplate;
var state;
var currentSound;

var $playlist;
var $controls;
var $pauseButton;
var $nextButton;
var $prevButton;

function getState() {
  state = {
    'playing': "16"  // could also be null
  };
}

function playlist() {
  return $('#playlist li');
}

function drawPlaylist() {
  $.getJSON(playlistUrl, function(data) {
    var element = $('#playlist ul');
    element.html('');
    $.each(data, function(i, track) {
      element.append(playlistTemplate(track));
    });

    $('#playlist .playable a[href]').off('click');

    $('#playlist ul').sortable({
      scroll: false,
      axis: "x",
      update: function() {
        positionPlaylist(true);
      }
    });

    bindPlayable();
    bindControls();
    targetBlank();
    selectTrack(playlist().first());  // XXX respect state
  });
}

function selectNextTrack() {
  var next = $('#playlist .selected').next();
  if (next.length) {
    selectTrack(next);
  } else {
    selectTrack(playlist().first());
  }
}

function selectPrevTrack() {
  var prev = $('#playlist .selected').prev();
  if (prev.length) {
    selectTrack(prev);
  } else {
    selectTrack(playlist().last());
  }
}

function bindPlayable() {
  playlist().on('click', function(e) {
    if (!$(this).hasClass('selected')) {
      e.preventDefault();
      e.stopPropagation();
      selectTrack($(this));
      play();
    }
  });
}

function paused() {
  return currentSound && currentSound.isPaused();
}

function bindControls() {
  $controls = $('#controls');
  $pauseButton = $controls.find('.pp');
  $nextButton = $controls.find('.next');
  $prevButton = $controls.find('.prev');

  $pauseButton.click(function() {
    var wasPaused = paused();
    currentSound.togglePlay();
    if (wasPaused) {
      play();
    } else {
      pause();
    }
  });

  $nextButton.click(function() {
    var wasPaused = paused();
    selectNextTrack();
    if (!wasPaused) {play();}
  });

  $prevButton.click(function() {
    var wasPaused = paused();
    selectPrevTrack();
    if (!wasPaused) {play();}
  });
}

function getOffset() {
  var reference = $('#controls :first-child');
  return reference.position().left - $('#playlist .selected').position().left;
}

function selectTrack(track) {
  track.siblings().removeClass('selected').addClass('playable');
  track.addClass('selected').removeClass('playable');

  buzz.all().stop();
  currentSound = new buzz.sound(track.attr('data-mp3'), {
    autoplay: false
  });
  currentSound.bindOnce("ended", function() {
    selectNextTrack();
    play();
  });
  positionPlaylist(true);
}

function play() {
  $('#playlist').addClass('playing');
  currentSound.play();
  $pauseButton.removeClass('fa-play').addClass('fa-pause');
}

function pause() {
  $('#playlist').removeClass('playing');
  currentSound.pause();
  $pauseButton.removeClass('fa-pause').addClass('fa-play');
}

function positionPlaylist(animate) {
  var ul = $('#playlist ul');
  var dest = {'left': getOffset()};
  if (!animate) {
    ul.css(dest);
  } else {
    ul.animate(dest);
  }
}

$(function() {
  sounds = {};
  $playlist = $('#playlist');
  playlistTemplate = Handlebars.compile($('#playlist-template').html());
  getState();
  drawPlaylist();
  $(window).resize(function() {
    positionPlaylist(false);
  });
});
