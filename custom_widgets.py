from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtWidgets import QLabel, QFrame, QPushButton
from PyQt5.QtGui import QPalette, QColor


class ClickLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, color):
        super().__init__()
        self.base_color = color
        self.setMinimumSize(self.sizeHint())
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        self.setAlignment(Qt.AlignCenter)
        self.set_background_color(color)
        font = self.font()
        font.setBold(True)
        font.setPointSize(20)
        self.setFont(font)

    def set_background_color(self, color):
        self.setStyleSheet('background-color:{};'.format(color))

    def set_font_color(self, color):
        self.setStyleSheet(self.styleSheet() + 'color:{}'.format(color))

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)

    def sizeHint(self):
        size = QSize()
        size.setHeight(50)
        size.setWidth(50)
        return size


class ControlButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        font = self.font()
        font.setBold(True)
        font.setPointSize(15)
        self.setFont(font)


class HLine(QFrame):
    def __init__(self, thickness):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(thickness)
