from auto_video_refactor.controller.autosuggest import similarity

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
