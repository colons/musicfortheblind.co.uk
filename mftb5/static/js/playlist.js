var playlistTemplate;
var canPlayMP3;
var canPlayVorbis;
var currentAudio;
var timeouts = {};

var $controls;
var $pauseButton;
var $nextButton;
var $prevButton;
var $np;

function saveState() {
  var serial = $('#playlist ul').sortable('serialize', {key: 'id'});
  var selected = $('#playlist .selected').attr('data-pk');

  $.post(playlistUrl, serial + '&' + $.param({
    selected: selected,
    stranger: $('body.stranger').length.toString()
  }));
}

function queueTracks(tracks) {
  var targetWidth = $('#playlist .selected').css('max-width');
  var triedToAddSelectedTrack = false;
  var playlistUl = $('#playlist ul');

  $('#playlist li').each(function() {
    $(this).addClass('present-at-start');
  });

  $.each(tracks, function(i, track) {
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
    rendered.addClass('manually-appended');
    rendered.css({'max-width': 0}).addClass('animating');
    
    if (anchorTrack) {
      anchorTrack.after(rendered);
    } else {
      playlistUl.append(rendered);
    }
  });

  $('#playlist .animating').animate({'max-width': targetWidth}, function() {
    $(this).css({'max-width': ''});
    $(this).removeClass('animating');
  });

  $('.present-at-start').removeClass('present-at-start');
  playlistChangeHook();

  if (currentAudio.paused) {
    if (!triedToAddSelectedTrack) {
      selectTrack(nextTrack());
    }
    play();
    notify('Now playing');
  } else if (triedToAddSelectedTrack && tracks.length === 1) {
    notify('Already playing');
  } else {
    notify('Added to playlist');
  }
}

function bindEnqueue() {
  $('.enqueue').off('click');
  $('.enqueue').on('click', function(e) {
    e.preventDefault();

    // just in case this is a stranger clicking the feature
    $('body').removeClass('stranger');

    animateUpwards($(this).parent());
    var jsonString = decodeURIComponent($(this).attr('data-json'));
    queueTracks($.parseJSON(jsonString));
  });
}

function bindNp() {
  $np = $('#np');
  $np.click(function() {
    $('html, body').animate({
      scrollTop: 0
    });
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
    'opacity': 1,
    'width': element.width()
  });

  dupe.animate({
    'top': targetPos.top - 100,
    'opacity': 0
  }, 1000, function() {
    dupe.remove();
  });
}

function flashPlaylist() {
  $('#playlist').stop().css({'background-color': '#c52'}).animate({'background-color': ''});
  $('#playlist .selected').stop().css({'opacity': '0'}).animate({'opacity': '1'}, function() {
    $(this).css({'opacity': ''});
  });
}

function bindShuffle() {
  $controls.find('.shuffle').click(function(e) {
    e.preventDefault();
    $('#playlist li').shuffle();
    flashPlaylist();
    positionPlaylistAnimated();
    notify('Playlist shuffled');
    defer('shufflehook', playlistChangeHook);
  });
}

function getPlaylist() {
  var embeddedPlaylist = $('[data-feature]');
  var playlist = [];
  var selected = null;

  var focalEnqueue = $('.focal .enqueue');
  if (focalEnqueue.length && $('body.stranger').length) {
    // this is a page for a piece of content we can be confident our user is probably interested in
    $('body').removeClass('stranger');
    var focalJsonString = decodeURIComponent(focalEnqueue.attr('data-json'));
    playlist = $.parseJSON(focalJsonString);
    selected = playlist[0].pk;
  }

  if ($('body.stranger').length && embeddedPlaylist.length) {
    var featureJsonString = decodeURIComponent(embeddedPlaylist.attr('data-feature'));
    $.merge(playlist, $.parseJSON(featureJsonString));
    drawPlaylist(playlist, playlist[0].pk);
  } else {
    $.getJSON(playlistUrl, function(data) {
      $.merge(playlist, data.playlist);
      drawPlaylist(playlist, (selected || data.selected));
    }).fail(giveUp);
  }
}

function drawPlaylist(playlist, selected) {
  var element = $('#playlist ul');
  element.html('');
  $.each(playlist, function(i, track) {
    if (!$('#playlist li[data-pk="' + track.pk.toString() + '"]').length) {
      // this isn't a dupe, we can add it
      element.append(playlistTemplate(track));
    }
  });

  $('#playlist ul').sortable({
    scroll: false,
    axis: "x",
    update: function() {
      playlistChangeHook();
      positionPlaylistAnimated();
    }
  });

  playlistChangeHook();
  bindControls();
  loadHook();
  selectTrack($('#playlist li[data-pk="' + selected.toString() + '"]'));
}

function nextTrack() {
  var next = relativeTrack('next');
  if (next && next.length) {
    return next;
  } else {
    return $('#playlist li').first();
  }
}

function prevTrack() {
  var prev = relativeTrack('prev');
  if (prev && prev.length) {
    return prev;
  } else {
    return $('#playlist li').last();
  }
}

function relativeTrack(attr) {
  var selected = $('#playlist .selected');
  if (selected.length) {
    return selected[attr]();
  }
}

// things to run when the state of the playlist changes
function playlistChangeHook() {
  saveState();
  bindPlayable();
  bindRemove();
  bindIndexButtons();
}

// if it's not urgent and you don't know how many times you might call it unnecessarily, wrap it with this
function defer(name, func) {
  if (name in timeouts) {
    clearTimeout(timeouts[name]);
  }
  timeouts[name] = setTimeout(func, 200);
}

function bindAudioEvents() {
  currentAudio.addEventListener('ended', handleEndedTrack);
  var states = {
    'waiting': 'loading',
    'error': 'error',
    'loadstart': 'loading',
    'playing': 'okay',
    'ended': 'okay',
    'canplaythrough': 'okay',
    'abort': 'okay'
  };

  $.each(states, function(state, stateAttr) {
    currentAudio.addEventListener(state, function() {
      $controls.attr('data-state', stateAttr);
    });
  });
  $controls.attr('data-state', 'okay');
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
    selectTrack(nextTrack());
    if (!wasPaused) {play();}
  });

  $prevButton.click(function() {
    var wasPaused = currentAudio.paused;
    selectTrack(prevTrack());
    if (!wasPaused) {play();}
  });

  bindAudioEvents();
  bindShuffle();

  $controls.find('.inner p').animate({'bottom': 0}, 300);
}

function makeSpinner() {
  new Spinner({
    radius: 3,
    length: 3,
    width: 2,
    lines: 9,
    color: '#fafafa'
  }).spin(document.getElementById('spinner'));
}

function destroySpinner() {
  $('#spinner').html('');
}

function bindIndexButtons() {
  bindAnything();
  $('#watfk').attr('href', $('#playlist .selected a.track').attr('href'));
}

function bindAnything() {
  var anything = $('#anything');

  anything.off('click');
  anything.on('click', function(e) {
    // If they're a stranger, we're not showing the playlist, and the playlist
    // can only be populated with the feature. It'll be quicker and less abusive
    // of their bandwidth to play the track we already selected.
    if (!$('body.stranger').length) {
      flashPlaylist();  // hide all the gross shit that's about to happen

      $('#playlist li').remove();

      var jsonString = decodeURIComponent($(this).attr('data-feature'));
      var tracks = $.parseJSON(jsonString);
      var element = $('#playlist ul');

      $.each(tracks, function(i, track) {
        element.append(playlistTemplate(track));
      });

      notify('Playlist reset');
    }

    selectTrack($('#playlist li').first(), true);
    playlistChangeHook();
    positionPlaylist();
    play();
  });
}

function getOffset() {
  var reference = $('main :first-child');
  return reference.offset().left - $('#playlist .selected').position().left;
}

function assignTrack(audio, track) {
  var attr;
  if (canPlayMP3) {attr = 'data-mp3';} else {attr = 'data-ogg';}
  $(audio).attr('src', track.attr(attr));
  $(audio).attr('data-pk', track.attr('data-pk'));
}

function selectTrack(track, skipAnimation) {
  track.siblings().removeClass('selected');
  track.siblings().removeClass('manually-appended');
  track.addClass('selected');
  $np.text(track.attr('data-name'));
  assignTrack(currentAudio, track);
  playlistChangeHook();
  positionPlaylist(!skipAnimation);
}

function play() {
  currentAudio.play();
  if (!currentAudio.paused) {
    $pauseButton.removeClass('fa-play').addClass('fa-pause');
    $('body').addClass('playing');
  }
}

function remove(item) {
  item.addClass('animating');
  item.animate({width: 0}, function() {
    item.remove();
    defer('removeHook', playlistChangeHook);
    defer('removeAnimate', positionPlaylistAnimated);
  });
}

function pause() {
  $('body').removeClass('playing');
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

function positionPlaylistAnimated() { positionPlaylist(true); }

function canPlayFormat(format) {
  return !!(currentAudio.canPlayType && currentAudio.canPlayType(format).replace(/no/, ''));
}

function giveUp() {
  // our magic is useless here, let us pretend we do not exist
  $('body').removeClass('audio');
}

function handleEndedTrack(e) {
  selectTrack(nextTrack());
  play();
}

$(function() {
  $('body').append(
    '<audio id="deck-a" preload="auto"></audio>'
  );
  currentAudio = document.getElementById('deck-a');
  canPlayMP3 = canPlayFormat('audio/mpeg;');
  canPlayVorbis = canPlayFormat('audio/ogg; codecs="vorbis"');

  if (!canPlayMP3 && !canPlayVorbis) {
    giveUp();
    return;
  }

  bindNp();
  playlistTemplate = Handlebars.compile($('#playlist-template').html());
  getPlaylist();
  bindEnqueue();
  bindIndexButtons();
  makeSpinner();
  $(window).resize(function() {
    positionPlaylist();
  });
});
