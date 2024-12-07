from auto_video_file_refactor.model.file_metadata import FileMetadata

import os


def generate(root_paths: str | list[str]) -> list:
    """
    data = [
        {Title1: [
            {Season1: [Episode1, Episode2, ... ]},
            {Season2: [...]},
            {...},
        ]},
        {Title2: [Title2.mkv, Title2.srt]},
        {...},
    ]
    """

    if isinstance(root_paths, str):
        root_paths = [root_paths]

    data = []
    for path in root_paths:
        tree = {}
        index: dict = {}
        for root, dirs, files in os.walk(path):
            root_md: tuple = FileMetadata(root).basic
            children = [FileMetadata(os.path.join(root, file)).basic for file in files]
            children.sort()

            if root == path:
                tree[root_md] = children
            else:
                parent_md = FileMetadata(os.path.dirname(root)).basic
                subtree, insert_at = index[parent_md]
                subtree.insert(insert_at, {root_md: children})  # put folders in front of files

                index[parent_md][1] += 1    # update position of the subsequent folder to insert into the list

            index[root_md] = [children, 0]   # initialize whenever a directory is traversed

        data.append(tree)

    return data
