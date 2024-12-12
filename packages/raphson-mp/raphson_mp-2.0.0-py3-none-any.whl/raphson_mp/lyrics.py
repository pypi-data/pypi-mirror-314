import html
import json
import logging
import re
import time
import traceback
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Final, override

import aiohttp

from raphson_mp import cache, settings, util

log = logging.getLogger(__name__)


@dataclass
class LyricsLine:
    start_time: float
    text: str


class Lyrics(ABC):
    source: str


@dataclass
class TimeSyncedLyrics(Lyrics):
    source: str
    text: list[LyricsLine]

    def to_lrc(self) -> str:
        lrc = ''
        for line in self.text:
            minutes, seconds = divmod(line.start_time, 60)
            lrc += f'[{int(minutes):02d}:{seconds:05.2f}] {line.text}\n'
        return lrc

    def to_plain(self) -> 'PlainLyrics':
        text = '\n'.join([line.text for line in self.text])
        return PlainLyrics(self.source, text)

    @classmethod
    def from_lrc(cls, source: str, lrc: str):
        lines: list[LyricsLine] = []
        for line in lrc.splitlines():
            matches = re.findall(r'\[(\d{2}):(\d{2})\.(\d{2})\](?: (.*))?', line)
            if matches:
                minutes, seconds, centiseconds, text = matches[0]
                lines.append(LyricsLine(int(minutes) * 60 + int(seconds) + int(centiseconds) / 100, text))
        return cls(source, lines)


@dataclass
class PlainLyrics(Lyrics):
    source: str
    text: str


def from_text(source: str, text: str | None):
    if text is None:
        return None
    synced = TimeSyncedLyrics.from_lrc(source, text)
    # TimeSyncedLyrics matcher skips lines that don't match the regex
    # if the line count is significantly lower than expected, the text is probably not in LRC format
    if len(synced.text) * 2 > text.count('\n'):
        return synced
    return PlainLyrics(source, text)


class LyricsFetcher(ABC):
    name: str
    supports_synced: bool

    @abstractmethod
    async def find(self, title: str, artist: str, album: str | None, duration: int | None) -> Lyrics | None:
        pass


class LrcLibFetcher(LyricsFetcher):
    name: str = 'lrclib.net'
    supports_synced: bool = True

    def _json_to_lyrics(self, json: Any) -> Lyrics | None:
        if json['syncedLyrics']:
            return TimeSyncedLyrics.from_lrc('LRCLIB ' + str(json['id']), json['syncedLyrics'])

        if json['plainLyrics']:
            return PlainLyrics('LRCLIB ' + str(json['id']), json['plainLyrics'])

    @override
    async def find(self, title: str, artist: str, album: str | None, duration: int | None) -> Lyrics | None:
        params: dict[str, str] = {'track_name': title, 'artist_name': artist}
        if album is not None:
            params['album_name'] = album
        if duration is not None:
            params['duration'] = str(duration)
        async with aiohttp.ClientSession("https://lrclib.net", headers={'User-Agent': settings.user_agent}) as session:
            async with session.get('/api/get', params=params) as response:
                if response.status != 404:
                    response.raise_for_status()
                    return self._json_to_lyrics(await response.json())

            log.info('lrclib: no results for direct get, trying search')
            async with session.get('/api/search', params={'artist_name': artist, 'track_name': title}, raise_for_status=True) as response:
                json = await response.json()
                if len(json) == 0:
                    return None
                json = json[0]

                # Sanity check on title and artist
                if not util.str_match(artist, json['artistName']):
                    return None
                if not util.str_match(title, json['trackName']):
                    return None

                return self._json_to_lyrics(json)


class MusixMatchFetcher(LyricsFetcher):
    """
    Based on (but heavily modified):
    https://gitlab.com/ronie/script.cu.lrclyrics/-/blob/master/lib/culrcscrapers/musixmatchlrc/lyricsScraper.py

    MIT License

    Copyright (c) 2022 Momo

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    name: str = 'MusixMatch'
    supports_synced: bool = True

    _cached_token: str | None = None
    _cached_token_expiration_time: int = 0

    async def get_token(self, session: aiohttp.ClientSession) -> str:
        if self._cached_token and int(time.time()) < self._cached_token_expiration_time:
            return self._cached_token

        async with session.get('token.get', params={'user_language': 'en', 'app_id': 'web-desktop-app-v1.0', 't': int(time.time())}) as response:
            result = await response.json(content_type="text/plain")  # MusixMatch uses wrong Content-Type for JSON
            if 'message' in result and 'body' in result["message"] and 'user_token' in result["message"]["body"]:
                token = result["message"]["body"]["user_token"]
                self._cached_token = token
                self._cached_token_expiration_time = int(time.time()) + 600
                return token

        raise ValueError('could not obtain token', result)

    async def get_lyrics_from_list(self, session: aiohttp.ClientSession, track_id: str) -> str | None:
        async with session.get('track.subtitle.get', params={'track_id': track_id, 'subtitle_format': 'lrc', 'app_id': 'web-desktop-app-v1.0', 'usertoken': await self.get_token(session), 't': str(int(time.time()))}) as response:
            try:
                result = await response.json(content_type="text/plain")  # MusixMatch uses wrong Content-Type for JSON
            except json.JSONDecodeError:
                log.warning('MusixMatch: failed to decode json: %s', response.text)
                return None

        if 'message' in result and 'body' in result["message"] and 'subtitle' in result["message"]["body"] and 'subtitle_body' in result["message"]["body"]["subtitle"]:
            lyrics = result["message"]["body"]["subtitle"]["subtitle_body"]
            return lyrics

        log.warning('unexpected response: %s', result)
        return None

    @override
    async def find(self, title: str, artist: str, album: str | None, duration: int | None):
        async with aiohttp.ClientSession("https://apic-desktop.musixmatch.com/ws/1.1/", headers={"authority": "apic-desktop.musixmatch.com",
                                     "cookie": "AWSELBCORS=0; AWSELB=0",
                                     "User-Agent": settings.webscraping_user_agent}, raise_for_status=True) as session:
            async with session.get("track.search", params={'q': title + ' ' + artist, 'page_size': 5, 'page': 1, 'app_id': 'web-desktop-app-v1.0', 'usertoken': await self.get_token(session), 't': int(time.time())}) as response:
                try:
                    result = await response.json(content_type="text/plain")  # MusixMatch uses wrong Content-Type for JSON
                except json.JSONDecodeError:
                    log.warning('MusixMatch: failed to decode json: %s', response.text)
                    return None

            if 'message' in result and 'body' in result["message"] and 'track_list' in result["message"]["body"] and result["message"]["body"]["track_list"]:
                for item in result["message"]["body"]["track_list"]:
                    found_artist = item['track']['artist_name']
                    found_title = item['track']['track_name']
                    found_track_id = item['track']['track_id']
                    log.info('musixmatch: search result: %s: %s - %s', found_track_id, found_artist, found_title)
                    if not util.str_match(title, found_title) and util.str_match(artist, found_artist):
                        continue

                    lyrics = await self.get_lyrics_from_list(session, found_track_id)
                    if lyrics is None or lyrics == '':
                        # when this happens, the website shows "Unfortunately we're not authorized to show these lyrics..."
                        log.info('musixmatch: lyrics are empty')
                        continue

                    return TimeSyncedLyrics.from_lrc('MusixMatch', lyrics)

            return None


class AZLyricsFetcher(LyricsFetcher):
    """
    Adapted from: https://gitlab.com/ronie/script.cu.lrclyrics/-/blob/master/lib/culrcscrapers/azlyrics/lyricsScraper.py
    Licensed under GPL v2
    """
    name: str = 'AZLyrics'
    supports_synced: bool = False

    @override
    async def find(self, title: str, artist: str, album: str | None, duration: int | None) -> PlainLyrics | None:
        artist = re.sub("[^a-zA-Z0-9]+", "", artist).lower().lstrip('the ')
        title = re.sub("[^a-zA-Z0-9]+", "", title).lower()
        async with aiohttp.ClientSession("https://www.azlyrics.com", headers={'User-Agent': settings.webscraping_user_agent}) as session:
            async with session.get(f'/lyrics/{artist}/{title}.html') as response:
                if response.status == 404:
                    return None
                response.raise_for_status()
                text = await response.text()
                lyricscode = text.split('t. -->')[1].split('</div')[0]
                lyricstext = html.unescape(lyricscode).replace('<br />', '\n')
                lyrics = re.sub('<[^<]+?>', '', lyricstext)
                return PlainLyrics(str(response.url), lyrics)


class GeniusFetcher(LyricsFetcher):
    name: str = 'Genius'
    supports_synced: bool = False

    @override
    async def find(self, title: str, artist: str, album: str | None, duration: int | None) -> PlainLyrics | None:
        async with aiohttp.ClientSession(headers={'User-Agent': settings.webscraping_user_agent}, raise_for_status=True) as session:
            url = await self._search(session, title, artist)
            if url is None:
                return None

            lyrics = await self._extract_lyrics(session, url)
            if lyrics is None:
                return None

            return PlainLyrics(url, lyrics)


    async def _search(self, session: aiohttp.ClientSession, title: str, artist: str) -> str | None:
        """
        Returns: URL of genius lyrics page, or None if no page was found.
        """
        async with session.get("https://genius.com/api/search/multi", params={"per_page": "1", "q": title + ' ' + artist}) as response:
            search_json = await response.json()
            for section in search_json["response"]["sections"]:
                if section['type'] == 'top_hit':
                    for hit in section['hits']:
                        if hit['index'] == 'song':
                            if util.str_match(title, hit['result']['title']):
                                return hit['result']['url']
                    break

            return None

    def _html_to_lyrics(self, html: str) -> str:
        # Extract text from HTML tags
        # Source HTML contains <p>, <b>, <i>, <a> etc. with lyrics inside.
        class Parser(HTMLParser):
            text: str = ''

            def __init__(self):
                HTMLParser.__init__(self)

            @override
            def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
                if tag == 'br':
                    self.text += "\n"

            @override
            def handle_data(self, data: str):
                self.text += data.strip()

        parser = Parser()
        parser.feed(html)
        return parser.text

    async def _extract_lyrics(self, session: aiohttp.ClientSession, genius_url: str) -> str | None:
        """
        Extract lyrics from the supplied Genius lyrics page
        Parameters:
            genius_url: Lyrics page URL
        Returns: A list where each element is one lyrics line.
        """
        # Firstly, a request is made to download the standard Genius lyrics page. Inside this HTML is
        # a bit of inline javascript.
        async with session.get(genius_url) as response:
            text = await response.text()

        # Find the important bit of javascript using known parts of the code
        text = util.substr_keyword(text, "window.__PRELOADED_STATE__ = JSON.parse('", "');")

        # Inside the javascript bit that has now been extracted, is a string. This string contains
        # JSON data. Because it is in a string, some characters are escaped. These need to be
        # un-escaped first.
        text = text \
            .replace('\\"', "\"") \
            .replace("\\'", "'") \
            .replace('\\\\', '\\') \
            .replace('\\$', '$') \
            .replace('\\`', '`')

        # Now, the JSON object is ready to be parsed.
        try:
            info_json = json.loads(text)
        except json.decoder.JSONDecodeError as ex:
            log.info('Error retrieving lyrics: json decode error at %s', ex.pos)
            log.info('Neighbouring text: "%s"', text[ex.pos-20:ex.pos+20])
            raise ex

        # For some reason, the JSON object happens to contain lyrics HTML. This HTML is parsed.
        lyrics_html = info_json['songPage']['lyricsData']['body']['html']
        lyrics_text = self._html_to_lyrics(lyrics_html)
        if lyrics_text.lower() in {'instrumental', '[instrumental]', '[instrument]', '(instrumental)', '♫ instrumental ♫', '*instrumental*'}:
            return None
        return lyrics_text


class LyricFindFetcher(LyricsFetcher):
    # https://lyrics.lyricfind.com/openapi.spec.json
    name: str = 'LyricFind'
    supports_synced: bool = False

    @override
    async def find(self, title: str, artist: str, album: str | None, duration: int | None) -> PlainLyrics | None:
        async with aiohttp.ClientSession("https://lyrics.lyricfind.com", headers={'User-Agent': settings.webscraping_user_agent}, raise_for_status=True) as session:
            async for slug in self._search(session, title, artist, duration):
                try:
                    return await self._get(session, slug)
                except:
                    traceback.print_exc()
                    continue
            return None

    async def _search(self, session: aiohttp.ClientSession, title: str, artist: str, duration: int | None) -> AsyncIterator[str]:
        async with session.get('/api/v1/search',
        params={'reqtype': 'default',
                                    'territory': 'NL',
                                    'searchtype': 'track',
                                    'track': title,
                                    'artist': artist,
                                    'limit': 10,
                                    'output': 'json',
                                    'useragent': settings.webscraping_user_agent}) as response:

            for track in (await response.json())['tracks']:
                if not util.str_match(title, track['title']):
                    continue

                if not util.str_match(artist, track['artist']['name']) and artist not in [artist['name'] for artist in track['artists']]:
                    continue

                log.info('found result: %s - %s', track['artist']['name'], track['title'])

                if duration and 'duration' in track:
                    duration_str = track['duration']
                    duration_int = int(duration_str.split(':')[0]) * 60 + int(duration_str.split(':')[1])

                    if abs(duration - duration_int) > 5:
                        log.info('duration not close enough')
                        continue

                yield track['slug']

    async def _get(self, session: aiohttp.ClientSession, slug: str) -> PlainLyrics | None:
        # 'https://lyrics.lyricfind.com/api/v1/lyric' exists but seems to always return unauthorized
        # use a web scraper instead :-)

        url = '/lyrics/' + slug
        log.info('LyricFind: downloading from: %s', url)
        async with session.get(url) as response:
            response_html = await response.text()
            response_json = util.substr_keyword(response_html, '<script id="__NEXT_DATA__" type="application/json">', '</script>')
            track_json = json.loads(response_json)['props']['pageProps']['songData']['track']
            if 'lyrics' in track_json:
                return PlainLyrics(url, track_json['lyrics'])
            else:
                # Instrumental
                return None

if settings.offline_mode:
    # set fetchers to an empty list, as an additional safety measure to ensure no data is used in offline mode
    FETCHERS: Final[list[LyricsFetcher]] = []
else:
    FETCHERS: Final[list[LyricsFetcher]] = [  # pyright: ignore[reportConstantRedefinition,reportGeneralTypeIssues]
        #                      ratelimit   time-synced   exact search  duration
        LrcLibFetcher(),     # none        yes           yes           yes
        MusixMatchFetcher(), # bad         yes           no            no
        LyricFindFetcher(),  # unknown     no            yes           yes
        GeniusFetcher(),     # good        no            no            no
        AZLyricsFetcher(),   # unknown     no            yes           no
    ]


async def _find(title: str, artist: str, album: str | None, duration: int | None) -> Lyrics | None:
    assert title is not None and artist is not None, "title and artist are required"

    log.info('fetching lyrics for: %s - %s', artist, title)

    plain_match: Lyrics | None = None

    for fetcher in FETCHERS:
        if plain_match is not None and not fetcher.supports_synced:
            # if we already have plain lyrics, we do not need to try any fetchers that only support plain lyrics
            continue

        try:
            lyrics = await fetcher.find(title, artist, album, duration)
        except:
            log.exception('%s: encountered an error', fetcher.name)
            continue

        if lyrics is None:
            log.info('%s: no lyrics found, continuing search', fetcher.name)
            continue

        if isinstance(lyrics, TimeSyncedLyrics):
            log.info('%s: found time-synced lyrics', fetcher.name)
            return lyrics

        if plain_match:
            log.info('%s, no time-synced lyrics found, continuing search', fetcher.name)
            continue

        if isinstance(lyrics, PlainLyrics):
            log.info('%s: found plain lyrics, continuing search', fetcher.name)
            plain_match = lyrics
            continue

        raise ValueError(lyrics)

    if plain_match is not None:
        log.info('Returning plain lyrics')
        return plain_match

    log.info('No lyrics found')
    return None


def to_dict(lyrics: Lyrics | None) -> dict[str, Any]:
    if lyrics is None:
        return {'type': 'none'}
    elif isinstance(lyrics, TimeSyncedLyrics):
        text = [{'start_time': line.start_time, 'text': line.text} for line in lyrics.text]
        return {'type': 'synced', 'source': lyrics.source, 'text': text}
    elif isinstance(lyrics, PlainLyrics):
        return {'type': 'plain', 'source': lyrics.source, 'text': lyrics.text}
    else:
        raise ValueError(lyrics)


def from_dict(dict: dict[str, Any]) -> Lyrics | None:
    if dict['type'] == 'none':
        return None

    if dict['type'] == 'synced':
        lines = [LyricsLine(line['start_time'], line['text']) for line in dict['text']]
        return TimeSyncedLyrics(dict['source'], lines)

    if dict['type'] == 'plain':
        return PlainLyrics(dict['source'], dict['text'])

    raise ValueError(dict['type'])


async def find(title: str, artist: str, album: str | None, duration: int | None) -> Lyrics | None:
    assert title is not None and artist is not None, "title and artist are required"

    cache_key = f'lyrics{artist}{title}{album}{duration}'

    cached_dict = await cache.retrieve_json(cache_key)
    if cached_dict is not None:
        log.info('returning lyrics from cache')
        return from_dict(cached_dict)

    lyrics = await _find(title, artist, album, duration)

    cached_dict = to_dict(lyrics)
    if lyrics is None:
        duration = cache.MONTH
    else:
        duration = cache.YEAR

    await cache.store_json(cache_key, cached_dict, duration)

    return lyrics
