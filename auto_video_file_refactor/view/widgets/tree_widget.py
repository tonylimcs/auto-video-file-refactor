from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from auto_video_file_refactor.common import ICONS_DIR

import auto_video_file_refactor.common as common
import os


class TreeWidget(QTreeWidget):
    def __init__(self):
        super().__init__()

        self.opened_folder_icon = QIcon(os.path.join(ICONS_DIR, "opened_folder_icon.png"))
        self.closed_folder_icon = QIcon(os.path.join(ICONS_DIR, "closed_folder_icon.png"))
        self.file_icon = QIcon(os.path.join(ICONS_DIR, "file_icon.png"))
        self.video_file_icon = QIcon(os.path.join(ICONS_DIR, "movie_icon.png"))

        headers = ["Name", "Type", "Directory"]
        self.setHeaderLabels(headers)
        self.setColumnCount(len(headers))

        self.itemExpanded.connect(self.item_expanded)
        self.itemCollapsed.connect(self.item_collapsed)

    def item_expanded(self, item: QTreeWidgetItem):
        if item.text(1) == common.FILE_FOLDER:
            item.setIcon(0, self.opened_folder_icon)

    def item_collapsed(self, item):
        if item.text(1) == common.FILE_FOLDER:
            item.setIcon(0, self.closed_folder_icon)

    def populate(self, data: list[dict[tuple, list[tuple] | list[dict[tuple, list[tuple]]]]]) -> None:
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

        def customize_item(item: QTreeWidgetItem):
            if item.text(1) == common.FILE_FOLDER:
                font = QFont()
                font.setItalic(True)
                item.setFont(0, font)
            elif item.text(1) in common.VIDEO_TYPES:
                item.setIcon(0, self.video_file_icon)
            else:
                item.setIcon(0, self.file_icon)

            return item

        def populate_item(subtree: dict):
            # Only one key per subtree
            key, values = list(subtree.items())[0]

            item = customize_item(QTreeWidgetItem(list(key)))

            if values:
                for value in values:
                    if isinstance(value, dict):
                        item.addChild(populate_item(value))
                    else:

                        item.addChild(customize_item(QTreeWidgetItem(list(value))))

            return item

        items = [populate_item(d) for d in data]

        self.clear()    # remove existing items in the tree
        self.insertTopLevelItems(0, items)

        self.expandAll()

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

        super().show()
