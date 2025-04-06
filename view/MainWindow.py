from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QMessageBox,
    QVBoxLayout,
    QPushButton
)

from view.LeftLayout import LayoutLeft
from view.RightLayout import RightLayout
from model.Experiment import Experiment

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.experiment = Experiment()

        self.setWindowTitle("Widgets App")

        # data clear button
        self.refreshButton = QPushButton()
        self.refreshButton.setText("Clear Data and Refresh")
        self.refreshButton.clicked.connect(self.refresh)
        self.refreshButton.setEnabled(False)

        layoutMain = QHBoxLayout()
        self.layoutLeft = LayoutLeft(self.experiment, self.refreshButton)
        self.layoutRight = RightLayout(self.experiment)

        layoutMain.addLayout(self.layoutLeft)
        layoutMain.addLayout(self.layoutRight)

        layout = QVBoxLayout()
        layout.addLayout(layoutMain)
        layout.addWidget(self.refreshButton)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)
    
    def refresh(self):
        if self.stopConfirmation():
            self.experiment = Experiment()

            layoutMain = QHBoxLayout()
            self.layoutLeft = LayoutLeft(self.experiment, self.refreshButton)
            self.layoutRight = RightLayout(self.experiment)

            layoutMain.addLayout(self.layoutLeft)
            layoutMain.addLayout(self.layoutRight)

            layout = QVBoxLayout()
            layout.addLayout(layoutMain)
            layout.addWidget(self.refreshButton)
            
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

    def stopConfirmation(self):
        reply = QMessageBox.question(self, 'Confirmation',
                                  "Are you sure you want to clear all data and start a new experiment?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                  QMessageBox.StandardButton.No)
  
        return reply