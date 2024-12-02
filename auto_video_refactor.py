from PySide6.QtWidgets import QApplication
from auto_video_refactor.view.widgets.main_window_widget import MainWindow


if __name__ == "__main__":
    window = MainWindow(QApplication())
    window.start_app()
