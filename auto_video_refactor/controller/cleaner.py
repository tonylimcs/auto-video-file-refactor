from auto_video_refactor.common import remove_dir

import os


def clean(rf_struct: dict):
    def collect_dirs(dict_: dict, dirs: set):
        for key, values in dict_.items():
            if isinstance(values, dict):
                dirs = collect_dirs(values, dirs)
            elif isinstance(values, list):
                for value in values:
                    dirs.add(value.raw.dir)

        return dirs

    dirs_set: set = collect_dirs(rf_struct, set())

    for dir_ in dirs_set:
        sub_dir = dir_
        while sub_dir:
            try:
                remove_dir(sub_dir)
                sub_dir = os.path.dirname(sub_dir)
            except OSError:
                break
