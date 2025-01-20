from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel
)
from PyQt6.QtGui import QFont

class AmpdTitle(QLabel):
    def __init__(self):
        super().__init__()

        font = QFont()
        font.setPointSize(40)

        self.setText("AMP'D")
        self.setFont(font)
        self.setTextFormat