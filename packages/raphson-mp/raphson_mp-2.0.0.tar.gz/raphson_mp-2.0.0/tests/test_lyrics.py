from raphson_mp import lyrics
from raphson_mp.lyrics import LyricsLine, PlainLyrics, TimeSyncedLyrics


def test_lrc_convert():
    lrc = """
[00:09.59] Tumble outta bed and I stumble to the kitchen
[00:12.08] Pour myself a cup of ambition
[00:14.16] And yawn and stretch and try to come to life
[00:19.09] Jump in the shower and the blood starts pumpin'
[00:21.75] Out on the street, the traffic starts jumpin'
[00:23.73] The folks like me on the job from 9 to 5
[00:27.82] Workin' 9 to 5, what a way to make a livin'
[00:32.69] Barely gettin' by, it's all takin' and no givin'
[00:37.57] They just use your mind
[00:40.34] And they never give you credit
[00:42.06] It's enough to drive you crazy if you let it
[00:46.85] 9 to 5, for service and devotion
[00:51.34] You would think that I
[00:53.80] Would deserve a fair promotion
[00:56.07] Want to move ahead
[00:58.42] But the boss won't seem to let me
[01:00.77] I swear sometimes that man is out to get me
[01:05.44] Mmm
[01:10.79] They let you dream just to watch 'em shatter
[01:12.41] You're just a step on the boss-man's ladder
[01:14.94] But you got dreams he'll never take away
[01:18.92] You're in the same boat with a lot of your friends
[01:21.82] Waitin' for the day your ship'll come in
[01:24.06] And the tide's gonna turn
[01:25.56] And it's all gonna roll your way
[01:28.26] Workin' 9 to 5, what a way to make a livin'
[01:33.31]
"""
    lyrics = TimeSyncedLyrics.from_lrc("", lrc)
    lrc2 = lyrics.to_lrc()
    assert lrc.strip() == lrc2.strip()


def test_synced_to_plain():
    lyrics = TimeSyncedLyrics("", [LyricsLine(0, "hello"), LyricsLine(1, "world")])
    plain = lyrics.to_plain().text
    assert plain.splitlines()[0] == "hello"


def test_from_text():
    assert lyrics.from_text("", None) is None

    lrc = """
[00:09.59] Tumble outta bed and I stumble to the kitchen
[00:12.08] Pour myself a cup of ambition
[00:14.16] And yawn and stretch and try to come to life
[00:19.09] Jump in the shower and the blood starts pumpin'
[00:21.75] Out on the street, the traffic starts jumpin'
"""
    assert isinstance(lyrics.from_text("", lrc), TimeSyncedLyrics)

    plain = """
Tumble outta bed and I stumble to the kitchen
Pour myself a cup of ambition
And yawn and stretch and try to come to life
Jump in the shower and the blood starts pumpin'
Out on the street, the traffic starts jumpin'
"""
    assert isinstance(lyrics.from_text("", plain), PlainLyrics)
