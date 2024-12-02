from dataclasses import dataclass, field

import auto_video_refactor.common as common
import os
import re


@dataclass
class FileMetadata:
    __path: str | bytes
    name: str = field(init=False)
    ext: str = field(init=False)
    type: str = field(init=False)
    dir: str = field(init=False)

    def __post_init__(self):
        self.__path = os.path.normpath(self.__path)
        self.ext = common.get_file_ext(self.__path)
        self.name = common.get_file_title(self.__path, self.ext)
        self.type = common.FILE_FOLDER if not self.ext else self.ext
        self.dir = os.path.dirname(self.__path)

    @property
    def path(self) -> str:
        return self.__path

    @property
    def basic(self) -> tuple:
        return self.name, self.type, self.dir


@dataclass
class VideoFileMetadata(FileMetadata):
    __root_dir: str
    __title: str
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
        return os.path.normpath(self.__root_dir)

    @property
    def title(self) -> str:
        return self.__title


@dataclass
class Refactored:

    @dataclass
    class Path:
        title: str
        season: str
        file: str

    __raw: VideoFileMetadata
    name: str = field(init=False)
    path: Path = field(init=False)

    def __post_init__(self):
        self.name = self.refactor_name()
        self.path = self.refactor_path()

    def refactor_name(self) -> str:
        series = f" S{self.__raw.season}E{self.__raw.episode}" if self.__raw.season and self.__raw.episode else ""
        return f"{self.__raw.title}{series}{self.__raw.ext}"

    def refactor_path(self) -> Path:
        title_path = os.path.join(self.__raw.root_dir, self.__raw.title)

        season_name = f"Season {int(self.__raw.season)}" if self.__raw.season else ""
        season_path = os.path.join(title_path, season_name) if self.__raw.season else ""

        file_path = os.path.join(title_path, season_name, self.name)

        return self.Path(title_path, season_path, file_path)

    @property
    def raw(self) -> VideoFileMetadata:
        return self.__raw
