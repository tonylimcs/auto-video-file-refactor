from auto_video_refactor.controller.refactor import refactor, preview
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont


class LineEditWidget(QLineEdit):
    def __init__(self, placeholder):
        super().__init__()

        self.paths = []
        self.forced = False
        self.file_system_tree_widget = None
        self.confirm_button_widget = None
        self.__checkbox_widget = None

        font = QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.setFont(font)

        self.setPlaceholderText(placeholder)
        self.textEdited.connect(self.text_edited)
        self.returnPressed.connect(self.return_pressed)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.text_changed)

    @property
    def checkbox_widget(self):
        return self.__checkbox_widget

    @checkbox_widget.setter
    def checkbox_widget(self, value):
        self.__checkbox_widget = value
        self.__checkbox_widget.stateChanged.connect(self.checkbox_state_changed)

    def text_edited(self):
        self.timer.start(500)  # wait for user input for 0.5 sec

    def return_pressed(self):
        self.setText(self.text())
        self.text_changed()

    def text_changed(self):
        if self.text().strip():
            refactored_struct = refactor(self.paths, self.text(), self.forced)
            prev = preview(refactored_struct)
            self.file_system_tree_widget.populate(prev)

            if refactored_struct:
                self.confirm_button_widget.setEnabled(True)
                self.confirm_button_widget.refactored_struct = refactored_struct
            else:
                self.confirm_button_widget.setEnabled(False)

    def checkbox_state_changed(self):
        self.forced = self.checkbox_widget.isChecked()
        self.text_changed()
