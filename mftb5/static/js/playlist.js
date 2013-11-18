var playlistTemplate;
var state;
var canPlayMP3;
var canPlayVorbis;

var $playlist;
var $controls;
var $pauseButton;
var $nextButton;
var $prevButton;
var $currentAudio;

function saveState() {
  var serial = $('#playlist ul').sortable('serialize', {key: 'id'});
  var selected = $('#playlist .selected').attr('data-pk');
  $.post(playlistUrl, serial + '&selected=' + selected);
}

function bindEnqueue() {
  $('.enqueue').off('click');
  $('.enqueue').on('click', function(e) {
    e.preventDefault();
    animateUpwards($(this).parent());

    var targetWidth = $('#playlist .selected').width();

    $('#playlist li').each(function() {
      $(this).addClass('present-at-start');
    });

    var jsonString = decodeURIComponent($(this).attr('data-json'));
    var data = $.parseJSON(jsonString);

    var triedToAddSelectedTrack = false;

    $.each(data, function(i, track) {
      // if we're already playing this track, don't bother adding it
      if ($('.present-at-start#playlist-item-' + track.pk + '.selected').length) {
        triedToAddSelectedTrack = true;
        return true;
      }

      // remove any tracks that were here when we started and are duplicates of this one
      var stale = $('.present-at-start#playlist-item-' + track.pk);
      remove(stale);

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

    if (currentAudio.paused) {
      if (!triedToAddSelectedTrack) {
        selectNextTrack();
      }
      play();
      notify('Now playing');
    } else {
      notify('Added to playlist');
    }
  });
}

function animateUpwards(element) {
  element.after(element.clone());
  var dupe = element.next();
  targetPos = element.position();
  dupe.css({
    'position': 'absolute',
    'left': targetPos.left,
    'top': targetPos.top,
    'pointer-events': 'none',
    'opacity': 0.5,
    'width': element.width()
  });

  dupe.animate({
    'top': targetPos.top - 100,
    'opacity': 0
  }, 1000, function() {
    dupe.remove();
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
    $.each(data.playlist, function(i, track) {
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
    selectTrack($('#playlist li[data-pk="' + data.selected.toString() + '"]'));
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
  bindRemove();
  saveState();
}

function bindPlayable() {
  var elements = $('#playlist li');
  elements.off('click');
  elements.on('click', function(e) {
    if (!$(this).hasClass('selected')) {
      selectTrack($(this));
      play();
    }
  });
}

function bindRemove() {
  var elements = $('#playlist li .remove');
  elements.off('click');
  elements.on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    var removeButton = $(this);
    removeButton.animate({opacity: 0}, 100);
    remove(removeButton.closest('li'));
  });
}

function bindControls() {
  $controls = $('#controls');
  $controls.sticky();
  $pauseButton = $controls.find('.pp');
  $nextButton = $controls.find('.next');
  $prevButton = $controls.find('.prev');

  $pauseButton.click(function() {
    var wasPaused = currentAudio.paused;
    if (wasPaused) {
      play();
    } else {
      pause();
    }
  });

  $nextButton.click(function() {
    var wasPaused = currentAudio.paused;
    selectNextTrack();
    if (!wasPaused) {play();}
  });

  $prevButton.click(function() {
    var wasPaused = currentAudio.paused;
    selectPrevTrack();
    if (!wasPaused) {play();}
  });

  $controls.find('.inner').animate({'bottom': 0}, 300);
}

function getOffset() {
  var reference = $('#controls .inner > :first-child');
  return reference.offset().left - $('#playlist .selected').position().left;
}

function selectTrack(track) {
  track.siblings().removeClass('selected');
  track.siblings().removeClass('manually-appended');
  track.addClass('selected');

  var attr;
  if (canPlayMP3) {attr = 'data-mp3';} else {attr = 'data-ogg';}
  $(currentAudio).attr('src', track.attr(attr));
  playlistChangeHook();
  positionPlaylist(true);
}

function play() {
  currentAudio.play();
  if (!currentAudio.paused) {
    $pauseButton.removeClass('fa-play').addClass('fa-pause');
    $('#playlist').addClass('playing');
  }
}

function remove(item) {
  item.addClass('animating');
  item.animate({width: 0}, function() {
    item.remove();
    playlistChangeHook();
    positionPlaylist(true);
  });
}

function pause() {
  $('#playlist').removeClass('playing');
  currentAudio.pause();
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

function canPlayFormat(format) {
  return !!(currentAudio.canPlayType && currentAudio.canPlayType(format).replace(/no/, ''));
}

function giveUp() {
  // our magic is useless here, let us pretend we do not exist
  $('body').removeClass('audio');
}

$(function() {
  $('body').append(
    '<audio id="current-audio" preload="auto"></audio>'
  );
  currentAudio = document.getElementById('current-audio');
  currentAudio.addEventListener('ended', function(e) {
    selectNextTrack();
    play();
  });

  canPlayMP3 = canPlayFormat('audio/mpeg;');
  canPlayVorbis = canPlayFormat('audio/ogg; codecs="vorbis"');

  if (!canPlayMP3 && !canPlayVorbis) {
    giveUp();
    return;
  }

  $playlist = $('#playlist');
  playlistTemplate = Handlebars.compile($('#playlist-template').html());
  drawPlaylist();
  bindShuffle();
  bindEnqueue();
  $(window).resize(function() {
    positionPlaylist(false);
  });
});
