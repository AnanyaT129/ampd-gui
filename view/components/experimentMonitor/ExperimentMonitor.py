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

from view.components.Logs import Logs
from model.DeviceStatus import DeviceStatus
from view.components.experimentMonitor.ExperimentThread import ExperimentThread

class ExperimentMonitor(QWidget):
  def __init__(self, experiment):
    super().__init__()
    self.setAutoFillBackground(True)
    self.experiment = experiment

    # Experiment logs
    self.logsWidget = Logs(self)

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

    # Start data collection button
    self.startStopExperimentButton = QPushButton(self)
    self.startStopExperimentButton.setText("Start Experiment")
    self.startStopExperimentButton.setStyleSheet("color: black;")
    self.startStopExperimentButton.clicked.connect(self.start_stop_experiment)

    # Layout
    
    layout = QVBoxLayout()
    layout.addLayout(statusLayout)
    layout.addWidget(self.startStopExperimentButton)
    layout.addWidget(self.logsWidget)
    
    self.setLayout(layout)
  
  def log(self, newLog):
    self.experiment.addLog(newLog)
    self.logsWidget.setText(self.experiment.logs)
  
  def change_status(self, new_status: DeviceStatus):
    self.status = new_status
    self.labelStatus.setText(self.status.value)
    self.log("Experiment Status: " + self.status.value)
  
  def start_stop_experiment(self):
    if self.status == DeviceStatus.READY_TO_START_EXPERIMENT:
      self.change_status(DeviceStatus.RUNNING_EXPERIMENT)
      self.startStopExperimentButton.setText("Stop Experiment")

      self.worker_thread = ExperimentThread(self.experiment, 'start_data_collection')
      self.worker_thread.log_signal.connect(self.log)
      self.worker_thread.status_signal.connect(self.change_status)
      self.worker_thread.start()

      # after data collection is complete
      self.startStopExperimentButton.setText("Start Experiment")
    elif self.status == DeviceStatus.RUNNING_EXPERIMENT:
      stop = self.stopConfirmation()
      if stop:
        self.log("Experiment Stopped")
        self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)
        self.startStopExperimentButton.setText("Start Experiment")
    else:
      self.log("Cannot change experiment status in current state")

  def stopConfirmation(self):
    reply = QMessageBox.question(self, 'Confirmation',
                                  "Are you sure you want to stop process?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                  QMessageBox.StandardButton.No)
  
    return reply