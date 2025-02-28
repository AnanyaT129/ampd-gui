from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QLabel
)

from view.LeftLayout import LayoutLeft
from view.RightLayout import RightLayout

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, experiment):
      super().__init__()
      self.experiment = experiment

      self.setWindowTitle("Widgets App")

      layoutMain = QHBoxLayout()
      layoutLeft = LayoutLeft(self.experiment)
      layoutRight = RightLayout(self.experiment)
      
      layoutRight.addWidget(QLabel("Right label"))

      layoutMain.addLayout(layoutLeft)
      layoutMain.addLayout(layoutRight)

      widget = QWidget()
      widget.setLayout(layoutMain)
      self.setCentralWidget(widget)