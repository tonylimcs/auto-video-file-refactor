from dataclasses import dataclass, field

import auto_video_file_refactor.common as common
import os
import re


@dataclass
class FileMetadata:
    _path: str | bytes
    name: str = field(init=False)
    ext: str = field(init=False)
    type: str = field(init=False)
    dir: str = field(init=False)

    def __post_init__(self):
        self._path = os.path.normpath(self._path)
        self.ext = common.get_file_ext(self._path)
        self.name = common.get_file_title(self._path, self.ext)
        self.type = common.FILE_FOLDER if not self.ext else self.ext
        self.dir = os.path.dirname(self._path)

    @property
    def path(self) -> str:
        return self._path

    @property
    def basic(self) -> tuple:
        return self.name, self.type, self.dir


@dataclass
class VideoFileMetadata(FileMetadata):
    _root_dir: str
    _title: str
    season: str = field(default="", init=False)
    episode: str = field(default="", init=False)

    def __post_init__(self):
        super().__post_init__()

        m = re.search(r"\bS(?P<season>\d+)E(?P<episode>\d+)\b", common.normalize_filename(self.name))
        if m is not None:
            self.season = m.group('season')
            self.episode = m.group('episode')

    @property
    def root_dir(self) -> str:
        return os.path.normpath(self._root_dir)

    @property
    def title(self) -> str:
        return self._title


@dataclass
class Refactored:

    @dataclass
    class Path:
        title: str
        season: str
        file: str

    _raw: VideoFileMetadata
    name: str = field(init=False)
    path: Path = field(init=False)

    def __post_init__(self):
        self.name = self.refactor_name()
        self.path = self.refactor_path()

    def refactor_name(self) -> str:
        series = f" S{self._raw.season}E{self._raw.episode}" if self._raw.season and self._raw.episode else ""
        return f"{self._raw.title}{series}{self._raw.ext}"

    def refactor_path(self) -> Path:
        title_path = os.path.join(self._raw.root_dir, self._raw.title)

        season_name = f"Season {int(self._raw.season)}" if self._raw.season else ""
        season_path = os.path.join(title_path, season_name) if self._raw.season else ""

        file_path = os.path.join(title_path, season_name, self.name)

        return self.Path(title_path, season_path, file_path)

    @property
    def raw(self) -> VideoFileMetadata:
        return self._raw
