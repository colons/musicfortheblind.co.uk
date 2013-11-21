# Tests for Music for the Blind 5

Because I can't be bothered to automate them but this thing is complex enough
that I'm scared of it breaking.

- Visit the site in porn mode. No playlist should be visible.

- Reload the page. The playlist should still not show.

- Click the big orange button. The track indicated by its [href] should
  *immediately* start playing (because it should already have started loading).

- Hit the back button. You should be on the homepage, only with the playlist
  now visible.
  
  - Behaviour is a little undefined here. At time of writing, the button says
    'Play me something else' but just starts the same track over. Might be
    worth doing something about.

- Go forward again and click the headphone next to the song title. It should
  float upwards and the text 'Already playing' should be shown. When hovering
  over the headphone, the text 'Listen' should appear next to it. Nothing else
  should happen.

- Find another track. Click the headphone link. It should be queued up after
  the currently playing track and the text 'Added to playlist' should be shown.

- Find an album and do the same. It should be queued up after the track you
  just queued up.

- Click a track in the playlist. It should slide into position above the
  controls and start playing, after the play/pause button is replaced by a
  spinner for a short time.

- Pause the track by clicking the pause button in the controls. Skip forward
  and back a few times and make sure the spinner does not appear, but that when
  you wait for a moment on one track and click play, it has loaded enough to
  start playing immediately.

- Scroll down a big page. The controls should stick to the top of the screen
  and a box should appear to their right advertising the title of the currently
  playing song. Clicking that title should scroll the page back to the top.

- Skip back from the first track and forward from the last. The playlist should
  wrap.

- Drag tracks around the playlist and ensure they stay where they are put.

- Queue up a track while the current one is paused. It should appear after the
  current one and start playing.

- Queue up an album containing (but not beginning with) the currently selected
  track. Ensure the playlist rearranges itself into album order but with the
  selected track pulled out and put at the front, regardless of if it was
  currently playling.

  - A rationalisation, perhaps, but I'd rather not play someone a track twice
    when it can be easily avoided, even if they aren't listening to it *right
    now*.

- Click the big black X to the right of a track in the playlist. It should go
  away.

- Click the title and album title of the selected track. They should take you
  to its track and album pages, respectively.

- Click the shuffle button. The playlist should flash orange and as it fades up
  should be scrolling to the new position of the selected track. The playlist
  should be in a new, random order.

- Find the Neko Desu jingle and play it. At the end of the track, whatever's
  next in the playlist should load and start playing. Move the Neko Desu jingle
  to the end of the playlist and do this again, and the first track in the
  playlist should load and start playing.

- Add a bunch of stuff to the playlist and then hammer on the shuffle button.
  There should be no lag to the flash or the animation. A playlist update
  should only be sent if you stop for a fifth of a second.

- Add Music for the Blind to the playlist. There should be no lag as the title
  floats towards the playlist, and only one playlist update should be sent.

- Reload the page. The playlist should retain its state.

- Remove most of the tracks from the playlist, and add a few that are not
  featured.  Go to the homepage and click the big orange button again. The
  playlist should contain nothing but featured items and playback should be
  interrupted to start playing one of them. The text 'Playlist reset' should
  briefly be shown.

- Click an external link. It should open in a new window or tab.

- Disconnect from the internet and ensure the play/pause button becomes a
  warning triangle.
