from PySide6.QtWidgets import QMessageBox, QCheckBox, QPushButton
from PySide6.QtGui import QIcon
from auto_video_refactor.common import ICONS_DIR

import enum
import os


class MessageBoxWidget(QMessageBox):

    class Type(enum.Enum):
        Information = 1
        Warning = 2
        Error = 3
        Question = 4
        Success = 5

    Information: Type = Type.Information
    Warning: Type = Type.Warning
    Error: Type = Type.Error
    Question: Type = Type.Question
    Success: Type = Type.Success

    def __init__(self, type_: Type, message: str, show_checkbox: bool = False):
        super().__init__()

        self.setText(message)

        if type_ == self.Type.Information:
            self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, 'information_icon.png')))
            self.setWindowTitle("Information")
            self.setIcon(QMessageBox.Information)
            self.setStandardButtons(QMessageBox.Ok)
        elif type_ == self.Type.Warning:
            self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, 'warning_icon.png')))
            self.setWindowTitle("Warning")
            self.setIcon(QMessageBox.Warning)
            self.setStandardButtons(QMessageBox.Ok)
        elif type_ == self.Type.Error:
            self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, 'error_icon.png')))
            self.setWindowTitle("Error")
            self.setIcon(QMessageBox.Critical)
            self.setStandardButtons(QMessageBox.Ok)
        elif type_ == self.Type.Question:
            self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, 'question_icon.png')))
            self.setWindowTitle("Query")
            self.setIcon(QMessageBox.Question)
            self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        elif type_ == self.Type.Success:
            self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, 'success_icon.png')))
            self.setWindowTitle("Success")
            self.setIcon(QMessageBox.Information)
            self.setStandardButtons(QMessageBox.Ok)
            # self.addButton(
            #     QPushButton(text="OK", icon=QIcon(os.path.join(ICONS_DIR, 'tick_icon.png'))),
            #     QMessageBox.YesRole
            # )

        self.show_msgbox = True

        if show_checkbox:
            self.checkbox = QCheckBox("Don't show this again.")
            self.checkbox.stateChanged.connect(self.checkbox_state_changed)
            self.setCheckBox(self.checkbox)

    def checkbox_state_changed(self):
        self.show_msgbox = not self.checkbox.isChecked()

    def show(self) -> int | None:
        if self.show_msgbox:
            return self.exec()

        return None
