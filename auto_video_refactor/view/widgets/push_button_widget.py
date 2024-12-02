from auto_video_refactor.view.widgets.message_box_widget import MessageBoxWidget
from auto_video_refactor.controller.refactor import exec_refactoring
# from auto_video_refactor.controller.validator import validate
from auto_video_refactor.controller.cleaner import clean
from auto_video_refactor.common import ICONS_DIR
from PySide6.QtWidgets import QPushButton, QMessageBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

import traceback
import os


class PushButtonWidget(QPushButton):
    def __init__(self, icon: QIcon | None = None, text: str = ""):
        super().__init__()

        self.line_edit_widget = None
        self.checkbox_widget = None
        self.left_tree_widget = None
        self.right_tree_widget = None
        self.confirm_message_box = MessageBoxWidget(
            MessageBoxWidget.Question,
            "Confirm?",
            show_checkbox=True
        )
        self.success_message_box = MessageBoxWidget(
            MessageBoxWidget.Success,
            "Files refactored.",
            show_checkbox=True
        )

        self.setText(text)

        if icon is not None:
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))

        self.clicked.connect(self.button_clicked)

        self.refactored_struct = {}

    def reset(self):
        self.line_edit_widget.clear()
        self.checkbox_widget.setChecked(False)
        self.left_tree_widget.clear()
        self.right_tree_widget.clear()

    def button_clicked(self):
        try:
            result = self.confirm_message_box.show()

            if result is None or result == QMessageBox.Ok:
                self.setEnabled(False)
                # validate(self.refactored_struct)
                exec_refactoring(self.refactored_struct)
                clean(self.refactored_struct)
                self.success_message_box.show()
                self.reset()
            elif result == QMessageBox.Cancel:
                MessageBoxWidget(
                    MessageBoxWidget.Information,
                    "No changes were made."
                ).show()
        except Exception as e:
            print(traceback.format_exc())
            MessageBoxWidget(
                MessageBoxWidget.Error,
                str(e)
            ).show()
            self.reset()
