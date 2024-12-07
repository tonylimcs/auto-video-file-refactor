from auto_video_file_refactor.common import normalize_filename

import os
import re


def compare(a: list[str], b: list[str]) -> str:
    similar_ls = []
    for i, token in enumerate(a):
        if token == b[i]:
            similar_ls.append(token)
        else:
            break

    return ' '.join(similar_ls)


def sort_score_index(score_index: dict[str, int | float]) -> dict[str, int | float]:
    # Sort dictionary by values in descending order, i.e. highest score first
    return dict(sorted(score_index.items(), key=lambda x: x[1], reverse=True))


def max_score_key(score_index: dict[str, int | float]) -> str:
    return list(score_index.keys())[0]


def max_score_value(score_index: dict[str, int | float]) -> int | float:
    return list(score_index.values())[0]


def similarity(strings: list[str], threshold: float = 0.6) -> tuple:
    """
    Assumption: Files in the same folder most likely contain the title of the same video.
    """

    tokens_ls = [normalize_filename(string).split(' ') for string in strings]
    score_index = {}
    for i, tokens in enumerate(tokens_ls):
        if i + 1 >= len(tokens_ls):
            break

        similar = compare(tokens, tokens_ls[i + 1])
        if similar:
            score_index.setdefault(similar, 1)
            score_index[similar] += 1

    if score_index:
        score_index = sort_score_index(score_index)
        score = list(score_index.values())[0] / len(strings)
        if score >= threshold:
            return max_score_key(score_index).title(), score

    return "", 0


def autosuggest_movie_title(path: str) -> str:
    filename = os.path.basename(path)
    m = re.search(r".+\s\(\d+\)", normalize_filename(filename))
    return m.group(0).title() if m else filename


def autosuggest_video_title(paths: str | list[str]) -> str:
    if isinstance(paths, str):
        paths = [paths]

    score_index = {}
    for path in paths:
        files_ls = []
        for root, dirs, files in os.walk(path):
            files_ls.extend(files)

        similar, score = similarity(files_ls)
        if similar:
            score_index.setdefault(similar, 0)
            score_index[similar] += score

    if score_index:
        score_index = sort_score_index(score_index)
        import json
        print("similarity score index:", json.dumps(score_index, indent=2), "\n")
        return list(score_index.keys())[0].title()

    if len(paths) == 1:
        return autosuggest_movie_title(paths[0])

    return ""
