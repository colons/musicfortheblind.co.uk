var playlistTemplate;
var state;
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
  $.post(playlistUrl, serial + '&selected=' + selected);
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
  } else if (triedToAddSelectedTrack && data.length === 1) {
    notify('Already playing');
  } else {
    notify('Added to playlist');
  }
}

function bindEnqueue() {
  $('.enqueue').off('click');
  $('.enqueue').on('click', function(e) {
    e.preventDefault();
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
  $('#playlist .selected').stop().css({'opacity': '0'}).animate({'opacity': '1'});
}

function bindShuffle() {
  $('#controls .shuffle').click(function(e) {
    e.preventDefault();
    $('#playlist li').shuffle();
    flashPlaylist();
    positionPlaylistAnimated();
    notify('Playlist shuffled');
    defer('shufflehook', playlistChangeHook);
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
        playlistChangeHook();
        positionPlaylistAnimated();
      }
    });

    playlistChangeHook();
    bindControls();
    loadHook();
    selectTrack($('#playlist li[data-pk="' + data.selected.toString() + '"]'));
  }).fail(giveUp);
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
}

// if it's not urgent and you don't know how many times you might call it unnecessarily, wrap it with this
function defer(name, func) {
  if (name in timeouts) {
    clearTimeout(timeouts[name]);
  }
  timeouts[name] = setTimeout(func, 200);
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

  $controls.find('.inner p').animate({'bottom': 0}, 300);
}

function bindAnything() {
  $('#anything').off('click');
  $('#anything').on('click', function() {
    flashPlaylist();  // hide all the gross shit that's about to happen

    $('#playlist li').remove();

    var jsonString = decodeURIComponent($(this).attr('data-feature'));
    var tracks = $.parseJSON(jsonString);
    var element = $('#playlist ul');

    $.each(tracks, function(i, track) {
      element.append(playlistTemplate(track));
    });

    $('#playlist li').shuffle();
    selectTrack($('#playlist li').first());
    playlistChangeHook();
    positionPlaylist();
    play();
  });
}

function getOffset() {
  var reference = $('#controls .inner p > :first-child');
  return reference.offset().left - $('#playlist .selected').position().left;
}

function assignTrack(audio, track) {
  var attr;
  if (canPlayMP3) {attr = 'data-mp3';} else {attr = 'data-ogg';}
  $(audio).attr('src', track.attr(attr));
  $(audio).attr('data-pk', track.attr('data-pk'));
}

function selectTrack(track) {
  track.siblings().removeClass('selected');
  track.siblings().removeClass('manually-appended');
  track.addClass('selected');
  $np.text(track.attr('data-name'));
  assignTrack(currentAudio, track);
  playlistChangeHook();
  positionPlaylistAnimated();
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
    defer('removeHook', playlistChangeHook);
    defer('removeAnimate', positionPlaylistAnimated);
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
  currentAudio.addEventListener('ended', handleEndedTrack);

  canPlayMP3 = canPlayFormat('audio/mpeg;');
  canPlayVorbis = canPlayFormat('audio/ogg; codecs="vorbis"');

  if (!canPlayMP3 && !canPlayVorbis) {
    giveUp();
    return;
  }

  playlistTemplate = Handlebars.compile($('#playlist-template').html());
  drawPlaylist();
  bindShuffle();
  bindEnqueue();
  bindNp();
  bindAnything();
  $(window).resize(function() {
    positionPlaylist();
  });
});
