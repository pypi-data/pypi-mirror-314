## 2.0.0 2024-12-11
* New: web UI for offline sync
* New: edit lyrics in metadata editor
* New: support for time-synced lyrics in metadata (LRC format)
* Improve: performance impact of resizing music player
* Fix: clicking on playlist checkbox labels to toggle checkbox
* Fix: fresh database creation
* Fix: album cover missing in offline mode
* Fix: lyrics setting not being saved when toggled by clicking album cover image
* Remove: profiler (will be added back later)
* Technical: rewrite using aiohttp instead of Flask and requests. This opens up the ability to use websockets in the future, without needing many worker threads. Performance should also be a bit better.
* Technical: added many tests, migrate to pytest
* Technical: many tweaks to improve performance

## 1.5.0 2024-11-23

Source code is now hosted on Codeberg. To change the Git remote, use: `git remote set-url origin https://codeberg.org/raphson/music-server.git`

The offline music player should now be installed using the `raphson_mp[offline]` package instead of the bare `raphson_mp`.

* New: theming support
* New: Windows 95 theme
* Improve: layout of forms for small screens
* Improve: player layout
* Improve: many small styling updates
* Improve: home page now adapts to wider screens
* Improve: refresh authentication cookie so it does not expire during use
* Improve: remove 'today' from last chosen chart
* Fix: PWA installation button
* Fix: volume slider is now unfocused after usage to avoid hijacking hotkeys
* Fix: Spotify artist matching was case sensitive
* Technical: add command line option to enable performance profiling
* Technical: frontend errors are now reported to the backend so bugs can be more easily identified
* Technical: API clients can now provide an authentication token via the Authorization header, and skip CSRF checks

## 1.4.0 2024-11-12
* New: compare playlist with Spotify playlist
* New: support for H264 music videos
* New: fetch lyrics from LyricFind
* Improve: music video layout
* Improve: do not show "[Instrumental]" lyrics
* Improve: layout of several forms
* Improve: last chosen chart is now per playlist
* Improve: artist similarity heatmap is no longer halved and now shows relative values
* Improve: extrapolate current position in activity
* Fix: several bugs related to music videos
* Fix: adding track without metadata to queue
* Fix: too many newlines for lyrics downloaded before v1.2.0 in offline mode
* Fix: outdated lyrics showing when page was not visible while switching tracks
* Technical: database connection is now closed properly
* Technical: added tests
* Technical: many code improvements
* Meta: repository has been moved to https://github.com/Derkades/raphson-music-player

## 1.3.0 2024-11-05
* New: playlist selection in guessing game
* New: experimental music video support
* New: setting to enable or disable lyrics
* New: download data export in account settings
* Improve: highlight current lyrics line
* Improve: automatically reload if browser loads outdated player from cache
* Improve: better sizing of cover image and lyrics box, will now take up as much screen space as possible
* Improve: remove BeautifulSoup and lxml dependency
* Improve: reduce memory usage and startup time in offline mode by only importing necessary modules
* Improve: add description to settings
* Improve: login box design
* Fix: missing play button for first track
* Fix: restore missing settings button in offline mode
* Fix: copy button missing if source playlist is not writable (source doesn't need to be writable)
* Fix: broken box shadows in music player

## 1.2.1 2024-10-26
* Improve: MusicBrainz search is more likely to find the correct cover image
* Fix: album cover from cache always being low quality
* Fix: time-synced lyrics are now available in offline-mode
* Fix: language and privacy account settings were applied for all users

## 1.2.0 2024-10-22
* New: time-synced lyrics
* New: automatic metadata lookup using AcoustID and MusicBrainz
* Fix: untranslated strings

## 1.1.0 2024-10-16

* New: add track to queue from web URL
* New: hotkey to open search
* New: artist similarity heatmap in statistics
* Improve: autofocus search field
* Improve: search UI
* Improve: switch search from trigram to unicode61 tokenizer. Misspellings are no longer tolerated, but returned results are a better match.
* Improve: restore home button to offline music player
* Improve: fixed height for queue so buttons don't jump around
* Fix: missing translations in package
* Fix: broken copy button for virtual tracks (like news)

## 1.0.1 2024-10-14

* Improve: tags UI
* Fix: lyrics extraction
* Fix: null albums in search
* Fix: missing dependencies in pypi package

## 1.0.0 2024-10-13

First release
