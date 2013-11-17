var playlistTemplate;
var state;
var currentSound;

var $playlist;
var $controls;
var $pauseButton;
var $nextButton;
var $prevButton;

function bindEnqueue() {
  $('.enqueue').off('click');
  $('.enqueue').on('click', function(e) {
    e.preventDefault();
    var targetWidth = $('#playlist .selected').width();

    $('#playlist li').each(function() {
      $(this).addClass('present-at-start');
    });

    $.getJSON($(this).attr('data-json-url'), function(data) {
      var triedToAddSelectedTrack = false;

      console.log('writing to playlist');
      $.each(data, function(i, track) {
        // if we're already playing this track, don't bother adding it
        if ($('.present-at-start#playlist-item-' + track.pk + '.selected').length) {
          triedToAddSelectedTrack = true;
          return true;
        }

        // remove any tracks that were here when we started and are duplicates of this one
        var stale = $('.present-at-start#playlist-item-' + track.pk);
        stale.animate({width: 0}, function() {
          stale.remove();
        });

        var anchorTrack;
        var manuallyAppendedTracks = $('#playlist .manually-appended');
        if (manuallyAppendedTracks.length) {
          anchorTrack = manuallyAppendedTracks.last();
        } else {
          anchorTrack = $('#playlist .selected');
        }

        var rendered = $(playlistTemplate(track));
        rendered.addClass('manually-appended').addClass('animating');

        rendered.css({width: 0});
        anchorTrack.after(rendered);

        rendered.animate({width: targetWidth}, function() {
          rendered.css({width: ''});
          rendered.removeClass('animating');
        });
      });

      $('.present-at-start').removeClass('present-at-start');
      playlistChangeHook();

      if (paused()) {
        if (!triedToAddSelectedTrack) {
          selectNextTrack();
        }
        play();
      }
    });
  });
}

function bindShuffle() {
  $('#controls .shuffle').click(function(e) {
    e.preventDefault();
    $('#playlist li').shuffle();
    positionPlaylist(false);
  });
}

function drawPlaylist() {
  $.getJSON(playlistUrl, function(data) {
    var element = $('#playlist ul');
    element.html('');
    $.each(data, function(i, track) {
      element.append(playlistTemplate(track));
    });

    $('#playlist ul').sortable({
      scroll: false,
      axis: "x",
      update: function() {
        positionPlaylist(true);
      }
    });

    playlistChangeHook();
    bindControls();
    loadHook();
    selectTrack($('#playlist li').first());
  });
}

function selectNextTrack() {
  var next = $('#playlist .selected').next();
  if (next.length) {
    selectTrack(next);
  } else {
    selectTrack($('#playlist li').first());
  }
}

function selectPrevTrack() {
  var prev = $('#playlist .selected').prev();
  if (prev.length) {
    selectTrack(prev);
  } else {
    selectTrack($('#playlist li').last());
  }
}

// things to run when the state of the playlist changes
function playlistChangeHook() {
  bindPlayable();
}

function bindPlayable() {
  $('#playlist li').on('click', function(e) {
    if (!$(this).hasClass('selected')) {
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
  $controls.sticky();
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
  var reference = $('#controls .inner :first-child');
  return reference.position().left - $('#playlist .selected').position().left;
}

function selectTrack(track) {
  track.siblings().removeClass('selected');
  track.siblings().removeClass('manually-appended');
  track.addClass('selected');

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
    ul.clearQueue();
    ul.animate(dest);
  }
}

$(function() {
  sounds = {};
  $playlist = $('#playlist');
  playlistTemplate = Handlebars.compile($('#playlist-template').html());
  drawPlaylist();
  bindShuffle();
  bindEnqueue();
  $(window).resize(function() {
    positionPlaylist(false);
  });
});
