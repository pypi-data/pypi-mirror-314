from unittest import TestCase

from raphson_mp import metadata


def test_split():
    assert metadata.split_meta_list("hello;hello2 ; hello3") == ["hello", "hello2", "hello3"]


def test_ad():
    assert metadata._has_advertisement("djsoundtop.com")
    assert not metadata._has_advertisement("hello")


def test_sort():
    assert metadata.sort_artists(["A", "B"], "B") == ["B", "A"]
