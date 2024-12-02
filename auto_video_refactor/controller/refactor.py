from auto_video_refactor.model.file_metadata import FileMetadata, VideoFileMetadata, Refactored
from auto_video_refactor.common import (
    normalize_filename,
    normalize_title,
    create_directory,
    rename_file
)

import os


def refactor_single(path: str, title: str, forced: bool = False) -> dict:
    title_norm = normalize_title(title)

    dict_ = {}
    for root, dirs, files in os.walk(path):
        for file in files:
            filename_norm = normalize_filename(file)

            if title_norm in filename_norm or forced:
                rf = Refactored(VideoFileMetadata(
                    os.path.join(str(root), file),
                    os.path.dirname(path),
                    title
                ))

                dict_.setdefault(FileMetadata(rf.path.title).basic, {}).setdefault(
                    FileMetadata(rf.path.season).basic if rf.path.season else "", []
                ).append(rf)

    return dict_


def refactor(root_paths: str | list[str], title: str, forced: bool = False):
    if isinstance(root_paths, str):
        root_paths = [root_paths]

    def update(a, b):
        if isinstance(a, dict) and isinstance(b, dict):
            for key in b:
                if key not in a:
                    a[key] = b[key]
                elif isinstance(a[key], list) and isinstance(b[key], list):
                    a[key].extend(b[key])
                else:
                    update(a[key], b[key])

    dict_ = {}
    for path in root_paths:
        update(dict_, refactor_single(path, title, forced))

    return dict_


def preview(rf_struct: dict):
    data = []
    for title_md in rf_struct:
        title_dict = {}
        for season_md in rf_struct[title_md]:
            children = [FileMetadata(rf.path.file).basic for rf in rf_struct[title_md][season_md]]
            children.sort()

            if season_md:
                children = [{season_md: children}]

            title_dict.setdefault(title_md, []).extend(children)

        data.append(title_dict)

    # data.sort(key=lambda x: list(x.keys())[0])    # sort by season folder
    return data


def exec_refactoring(rf_struct: dict):
    if not rf_struct:
        raise Exception('Nothing to refactor.')

    for title_md in rf_struct:
        for season_md in rf_struct[title_md]:
            for rf in rf_struct[title_md][season_md]:
                create_directory(rf.path.title)
                create_directory(rf.path.season)
                rename_file(rf.raw.path, rf.path.file)
