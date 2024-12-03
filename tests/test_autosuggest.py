from auto_video_refactor.controller.autosuggest import similarity, autosuggest_movie_title

import pytest


@pytest.mark.parametrize("filenames, expected", [
    (["This is a TV Series S01E01", "This is a TV Series S01E02", "This is a TV Series S01E03"], "This Is A Tv Series"),
    (["This-is-a-TV-Series S01E01", "This-is-a-TV-Series S01E02", "This-is-a-TV-Series S01E02"], "This Is A Tv Series"),
    (["This is a TV Series S01E01", "This is a TV Series S01E02", "This TV Series S01E03"], "This Is A Tv Series"),
    (["This is a TV Series S01E01", "This TV Series S01E02", "A TV Series S01E03"], "This")
])
def test_similarity_positive(filenames, expected):
    assert similarity(filenames)[0] == expected


@pytest.mark.xfail(reason="known case sensitive issue")
@pytest.mark.parametrize("filenames, expected", [
    (["This is a TV Series S01E01", "This is a TV Series S01E02", "This is a TV Series S01E02"], "'This is a TV Series")
])
def test_similarity_fail(filenames, expected):
    assert similarity(filenames)[0] == expected


def test_autosuggest_video_title_with_year(tmp_path):
    d = tmp_path / "This.is.a.Movie.(2024).blah.blah.blah"
    d.mkdir()
    p = d / "This.is.a.Movie.(2024).blah.blah.blah.mkv"
    p.write_text("")
    assert autosuggest_movie_title(str(d)) == "This Is A Movie (2024)"


def test_autosuggest_video_title_without_year(tmp_path):
    d = tmp_path / "This.is.a.Movie.blah.blah.blah"
    d.mkdir()
    p = d / "This.is.a.Movie.blah.blah.blah.mkv"
    p.write_text("")
    assert autosuggest_movie_title(str(d)) == "This.is.a.Movie.blah.blah.blah"
