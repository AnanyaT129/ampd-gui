from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QColor, QPalette

from components.Logs import Logs
from model.DeviceStatus import DeviceStatus

class ExperimentMonitor(QWidget):
  def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("White"))
        self.setPalette(palette)

        # Experiment status labels 
        labelConnect = QLabel("Device Status")
        labelConnect.setStyleSheet("color: black; font-weight: bold")

        self.status = DeviceStatus.READY_TO_START_EXPERIMENT
        self.labelStatus = QLabel(self.status.value)
        self.labelStatus.setStyleSheet("color: black;")

        statusLayout = QHBoxLayout()
        statusLayout.addWidget(labelConnect)
        statusLayout.addWidget(self.labelStatus)

        # Start/Stop experiment button
        self.startStopButton = QPushButton(self)
        self.startStopButton.setText("Start Experiment")
        self.startStopButton.setStyleSheet("color: black;")
        self.startStopButton.clicked.connect(self.changeButtonStatus)

        # Experiment logs
        self.logs = Logs(self)

        layout = QVBoxLayout()
        layout.addLayout(statusLayout)
        layout.addWidget(self.startStopButton)
        layout.addWidget(self.logs)
        
        self.setLayout(layout)
  
  def change_status(self, new_status: DeviceStatus):
      self.status = new_status
      self.labelStatus.setText(self.status.value)
    
  def changeButtonStatus(self):
      if (self.status == DeviceStatus.READY_TO_START_EXPERIMENT):
          self.change_status(DeviceStatus.RUNNING_EXPERIMENT)
          self.startStopButton.setText("Stop Experiment")
          self.logs.appendLog("Experiment Started")
      else:
          reply = QMessageBox.question(self, 'Confirmation',
                                     "Are you sure you want to quit?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
          if reply == QMessageBox.StandardButton.Yes:
            self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)
            self.startStopButton.setText("Start Experiment")
            self.logs.appendLog("Experiment Stopped")
    
      self.logs.appendLog("Experiment Status: " + self.status.value)