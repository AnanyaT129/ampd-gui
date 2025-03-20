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

    # Start data collection buttons
    self.startStopImpedanceButton = QPushButton(self)
    self.startStopImpedanceButton.setText("Start Impedance Measurement")
    self.startStopImpedanceButton.setStyleSheet("color: black;")
    self.startStopImpedanceButton.clicked.connect(self.start_stop_impedance)

    self.startStopCameraButton = QPushButton(self)
    self.startStopCameraButton.setText("Start Camera Capture")
    self.startStopCameraButton.setStyleSheet("color: black; background-color: red")
    self.startStopCameraButton.clicked.connect(self.start_stop_camera)
    self.startStopCameraButton.setEnabled(False)

    # data clear button
    self.clearButton = QPushButton()
    self.clearButton.setText("Clear Data")
    self.clearButton.setStyleSheet("color: black")
    self.clearButton.clicked.connect(self.experiment.clear)

    # data collection layout
    self.dataCollectionLayout = QHBoxLayout()
    self.dataCollectionLayout.addWidget(self.startStopImpedanceButton)
    self.dataCollectionLayout.addWidget(self.startStopCameraButton)

    # Layout
    layout = QVBoxLayout()
    layout.addLayout(statusLayout)
    layout.addLayout(self.dataCollectionLayout)
    layout.addWidget(self.clearButton)
    layout.addWidget(self.logsWidget)
    
    self.setLayout(layout)
  
  def log(self, newLog):
    self.experiment.addLog(newLog)
    self.logsWidget.setText(self.experiment.logs)
  
  def change_status(self, new_status: DeviceStatus):
    self.status = new_status
    self.labelStatus.setText(self.status.value)
    self.log("Experiment Status: " + self.status.value)
  
  def enable_camera_capture(self, enable):
    if enable:
      self.startStopCameraButton.setEnabled(True)
      self.startStopCameraButton.setStyleSheet("color: black; background-color: green")
    else:
      self.startStopCameraButton.setEnabled(False)
      self.startStopCameraButton.setStyleSheet("color: black; background-color: red")
  
  def start_stop_impedance(self):
    if self.status == DeviceStatus.READY_TO_START_EXPERIMENT:
      self.change_status(DeviceStatus.RUNNING_EXPERIMENT)
      self.startStopImpedanceButton.setText("Stop Impedance Measrement")

      self.impedance_thread = ExperimentThread(self.experiment, 'start_data_collection')
      self.impedance_thread.log_signal.connect(self.log)
      self.impedance_thread.status_signal.connect(self.change_status)
      self.impedance_thread.enable_signal.connect(self.enable_camera_capture)

      self.impedance_thread.start()

      # after data collection is complete
      self.startStopImpedanceButton.setText("Start Impedance Measurement")
    elif self.status == DeviceStatus.RUNNING_EXPERIMENT:
      stop = self.stopConfirmation()
      if stop:
        self.log("Impedance Measurement Stopped")
        self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)
        self.startStopImpedanceButton.setText("Start Impedance Measurement")
    else:
      self.log("Cannot change experiment status in current state")
  
  def start_stop_camera(self):
    if self.status == DeviceStatus.READY_TO_START_EXPERIMENT:
      self.change_status(DeviceStatus.RUNNING_EXPERIMENT)
      self.startStopImpedanceButton.setText("Stop Camera Capture")

      self.camera_thread = ExperimentThread(self.experiment, 'start_camera_capture')
      self.camera_thread.log_signal.connect(self.log)
      self.camera_thread.status_signal.connect(self.change_status)
      self.camera_thread.start()

      # after data collection is complete
      self.startStopImpedanceButton.setText("Start Camera Capture")
    elif self.status == DeviceStatus.RUNNING_EXPERIMENT:
      stop = self.stopConfirmation()
      if stop:
        self.log("Camera Capture Stopped")
        self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)
        self.startStopImpedanceButton.setText("Start Camera Capture")
    else:
      self.log("Cannot change experiment status in current state")

  def stopConfirmation(self):
    reply = QMessageBox.question(self, 'Confirmation',
                                  "Are you sure you want to stop process?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                  QMessageBox.StandardButton.No)
  
    return reply
