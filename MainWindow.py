from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel
)

from LeftLayout import LayoutLeft

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
      super().__init__()

      self.setWindowTitle("Widgets App")

      layoutMain = QHBoxLayout()
      layoutLeft = LayoutLeft()
      layoutRight = QVBoxLayout()
      
      layoutRight.addWidget(QLabel("Right label"))

      layoutMain.addLayout(layoutLeft)
      layoutMain.addLayout(layoutRight)

      widget = QWidget()
      widget.setLayout(layoutMain)
      self.setCentralWidget(widget)