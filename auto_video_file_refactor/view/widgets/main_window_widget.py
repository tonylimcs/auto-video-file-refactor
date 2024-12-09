from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QCheckBox,
)
from auto_video_file_refactor.view.widgets.push_button_widget import PushButtonWidget
from auto_video_file_refactor.controller.autosuggest import autosuggest_video_title
from auto_video_file_refactor.view.widgets.line_edit_widget import LineEditWidget
from auto_video_file_refactor.model.file_system_tree import FileSystemTree
from auto_video_file_refactor.view.widgets.tree_widget import TreeWidget
from auto_video_file_refactor.common import ICONS_DIR
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon

import sys
import os

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'auto-video-file-refactor'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

basedir = os.path.dirname(__file__)


class MainWindow(QMainWindow):
    def __init__(self, app):
        QMainWindow.__init__(self)
        self.app = app
        self.setWindowTitle("Auto Video File Refactor")
        self.setMinimumSize(QSize(1000, 500))
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "film_roll_icon.png")))

        layout_v = QVBoxLayout()
        layout_h1 = QHBoxLayout()
        layout_h2 = QHBoxLayout()

        self.force_checkbox = QCheckBox("Force")
        self.line_edit_video_title = LineEditWidget("Enter title of video")
        self.line_edit_video_title.checkbox_widget = self.force_checkbox
        layout_h2.addWidget(self.line_edit_video_title)
        layout_h2.addWidget(self.force_checkbox)

        layout_v.addLayout(layout_h2)

        self.left_tree = TreeWidget()
        self.right_tree = TreeWidget()
        layout_h1.addWidget(self.left_tree)
        layout_h1.addWidget(self.right_tree)

        layout_v.addLayout(layout_h1)

        self.confirm_button = PushButtonWidget(QIcon(os.path.join(ICONS_DIR, 'fantasy_icon.png')))
        self.confirm_button.setEnabled(False)
        self.confirm_button.line_edit_widget = self.line_edit_video_title
        self.confirm_button.checkbox_widget = self.force_checkbox
        self.confirm_button.left_tree_widget = self.left_tree
        self.confirm_button.right_tree_widget = self.right_tree
        layout_v.addWidget(self.confirm_button)

        central_widget = QWidget()
        central_widget.setLayout(layout_v)
        self.setCentralWidget(central_widget)

    # The following four methods set up dragging and dropping for the app
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Drag and drop files directly into the widget."""

        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()

            paths = [str(url.toLocalFile()) for url in event.mimeData().urls()]

            tree: list = FileSystemTree(paths)
            self.left_tree.populate(tree)

            self.line_edit_video_title.clear()
            self.force_checkbox.setChecked(False)
            self.right_tree.clear()
            self.confirm_button.setEnabled(False)

            self.line_edit_video_title.paths = paths
            self.line_edit_video_title.file_system_tree_widget = self.right_tree
            self.line_edit_video_title.confirm_button_widget = self.confirm_button
            self.line_edit_video_title.setText(autosuggest_video_title(paths))
            self.line_edit_video_title.text_changed()

        else:
            event.ignore()

    def start_app(self):
        self.show()
        sys.exit(self.app.exec())

    @staticmethod
    def exit_app():
        QApplication.quit()


if __name__ == "__main__":
    window = MainWindow(QApplication())
    window.start_app()
