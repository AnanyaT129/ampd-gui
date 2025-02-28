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

from model.Server import Server
from view.components.Logs import Logs
from model.DeviceStatus import DeviceStatus

class ExperimentMonitor(QWidget):
  def __init__(self):
    super().__init__()
    self.setAutoFillBackground(True)

    # Experiment logs
    self.logs = Logs(self)

    # Experiment server
    self.server = Server(log_callback=self.logs.appendLog)

    palette = self.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor("White"))
    self.setPalette(palette)

    # Experiment status labels 
    labelConnect = QLabel("Device Status")
    labelConnect.setStyleSheet("color: black; font-weight: bold")

    self.status = DeviceStatus.DISCONNECTED
    self.labelStatus = QLabel(self.status.value)
    self.labelStatus.setStyleSheet("color: black;")

    statusLayout = QHBoxLayout()
    statusLayout.addWidget(labelConnect)
    statusLayout.addWidget(self.labelStatus)

    # Start server experiment button
    self.startStopServerButton = QPushButton(self)
    self.startStopServerButton.setText("Start Server")
    self.startStopServerButton.setStyleSheet("color: black;")
    self.startStopServerButton.clicked.connect(self.start_stop_server)

    # Start data collection button
    self.startStopExperimentButton = QPushButton(self)
    self.startStopExperimentButton.setText("Start Experiment")
    self.startStopExperimentButton.setStyleSheet("color: black;")
    self.startStopExperimentButton.clicked.connect(self.start_stop_experiment)

    # Layout
    layoutStartStop = QHBoxLayout()
    layoutStartStop.addWidget(self.startStopServerButton)
    layoutStartStop.addWidget(self.startStopExperimentButton)
    
    layout = QVBoxLayout()
    layout.addLayout(statusLayout)
    layout.addLayout(layoutStartStop)
    layout.addWidget(self.logs)
    
    self.setLayout(layout)
  
  def change_status(self, new_status: DeviceStatus):
    self.status = new_status
    self.labelStatus.setText(self.status.value)
    self.logs.appendLog("Experiment Status: " + self.status.value)

  def start_stop_server(self):
    if self.status == DeviceStatus.DISCONNECTED:
       if self.server.start_server():
          self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)
          self.startStopServerButton.setText("Stop Server")
    elif self.status == DeviceStatus.RUNNING_EXPERIMENT:
      self.logs.appendLog("Cannot stop server while experiment is running")
    else:
      stop = self.stopConfirmation()
      if stop:
        self.server.close_server()
        self.change_status(DeviceStatus.DISCONNECTED)
        self.startStopServerButton.setText("Start Server")
  
  def start_stop_experiment(self):
    if self.status == DeviceStatus.READY_TO_START_EXPERIMENT:
      self.change_status(DeviceStatus.RUNNING_EXPERIMENT)
      self.startStopExperimentButton.setText("Stop Experiment")
      data = self.server.start_data_collection(5)

      # after data collection is complete
      self.logs.appendLog(f"Data collected: {data[:10]}")
      self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)
      self.startStopExperimentButton.setText("Start Experiment")
    elif self.status == DeviceStatus.RUNNING_EXPERIMENT:
      stop = self.stopConfirmation()
      if stop:
        self.logs.appendLog("Experiment Stopped")
        self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)
        self.startStopExperimentButton.setText("Start Experiment")
    else:
      self.logs.appendLog("Cannot change experiment status in current state")

  def stopConfirmation(self):
    reply = QMessageBox.question(self, 'Confirmation',
                                  "Are you sure you want to stop process?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                  QMessageBox.StandardButton.No)
  
    return reply