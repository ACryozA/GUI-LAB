import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget

BASE_DIR = Path(__file__).resolve().parent


class PngWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)

        image = QPixmap(str(BASE_DIR / "beeee.png"))
        if image.isNull():
            raise FileNotFoundError("Не найден файл shape.png")

        self.resize(image.size())
        self.image_label = QLabel(self)
        self.image_label.setGeometry(0, 0, image.width(), image.height())
        self.image_label.setPixmap(image)
        self.image_label.mousePressEvent = self.close_on_click

    def close_on_click(self, event):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа №1")
        self.setFixedSize(500, 340)

        self.label = QLabel("Выполнил Маслюк А.С.", self)
        self.label.setGeometry(85, 45, 330, 165)
        self.label.setAlignment(Qt.AlignCenter)

        self.button1 = QPushButton("Кнопка 1", self)
        self.button1.setGeometry(100, 245, 130, 45)
        self.button1.clicked.connect(self.show_image)

        self.button2 = QPushButton("Кнопка 2", self)
        self.button2.setGeometry(270, 245, 130, 45)
        self.button2.clicked.connect(self.open_png_window)

        self.png_window = None

    def show_image(self):
        image = QPixmap(str(BASE_DIR / "image.png"))
        if image.isNull():
            self.label.setText("Не найден файл image.png")
            return
        image = image.scaled(
            self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.label.setPixmap(image)

    def open_png_window(self):
        self.png_window = PngWindow()
        self.png_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
