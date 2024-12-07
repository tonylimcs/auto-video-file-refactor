import shutil
import re
import os

FILE_FOLDER = "File folder"
VIDEO_TYPES = [".mkv", ".mp4", ".avi"]
ICONS_DIR = os.path.join(os.path.dirname(__file__), "view", "icons")


def normalize_filename(filename):
    filename = filename.replace('.', ' ').replace('-', ' ').upper()
    filename = re.sub(r'\s+', ' ', filename)
    return filename


def normalize_title(title):
    title_norm = re.sub(r"\s\(\d+\)$", "", title)  # remove year of series in the title
    title_norm = title_norm.upper()
    return title_norm


def create_directory(dir_path):
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Directory", f"'{dir_path}'", "created")


def rename_file(old_path, new_path):
    if old_path != new_path:
        os.rename(old_path, new_path)
        print("Renamed", f"'{old_path}'", "to", f"'{new_path}'")


def remove_dir(dir_path):
    os.rmdir(dir_path)
    print("Directory", f"'{dir_path}'", "Removed")


def force_remove_dir(dir_path):
    shutil.rmtree(dir_path)
    print("Directory", f"'{dir_path}'", "Removed")


def get_file_ext(path: str) -> str:
    ext = os.path.splitext(path)[-1]

    if os.path.exists(path):
        return ext if os.path.isfile(path) else ""  # folders have no extension

    return ext


def get_file_title(path: str, ext: str) -> str:
    return re.sub(rf"{ext}$", "", os.path.basename(path))
