from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
  QVBoxLayout,
  QHBoxLayout,
  QLabel,
  QWidget,
  QPushButton,
  QMessageBox,
  QLineEdit,
  QFormLayout
)
from PyQt6.QtGui import QColor, QPalette, QIntValidator

import time

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

    # Experiment thread
    self.impedance_thread = ExperimentThread(self.experiment, 'start_data_collection')

    # Experiment title label
    labelTitle = QLabel(f"Title: {self.experiment.savePath}")
    labelTitle.setStyleSheet("color: black; font-weight: bold")

    # Experiment Variables
    self.variablesFormWidget = QFormLayout()

    self.snapshotLengthWidget = QLineEdit()
    self.snapshotLengthWidget.setValidator(QIntValidator())
    self.snapshotLengthWidget.setText("1")
    self.snapshotLengthWidget.textChanged.connect(self.snapshotLengthChanged)
    self.variablesFormWidget.addRow("Snapshot length (s): ", self.snapshotLengthWidget)

    self.snapshotsPerMinuteWidget = QLineEdit()
    self.snapshotsPerMinuteWidget.setValidator(QIntValidator())
    self.snapshotsPerMinuteWidget.setText("2")
    self.snapshotsPerMinuteWidget.textChanged.connect(self.snapshotsPerMinuteChanged)
    self.variablesFormWidget.addRow("Snapshots per minute: ", self.snapshotsPerMinuteWidget)

    self.lengthWidget = QLineEdit()
    self.lengthWidget.setValidator(QIntValidator())
    self.lengthWidget.setText("5")
    self.lengthWidget.textChanged.connect(self.lengthChanged)
    self.variablesFormWidget.addRow("Experiment duration (min): ", self.lengthWidget)

    # Experiment status labels 
    labelConnect = QLabel("Device Status")
    labelConnect.setStyleSheet("color: black; font-weight: bold")

    self.status = DeviceStatus.READY_TO_START_EXPERIMENT
    self.labelStatus = QLabel(self.status.value)
    self.labelStatus.setStyleSheet("color: black;")

    statusLayout = QHBoxLayout()
    statusLayout.addWidget(labelConnect)
    statusLayout.addWidget(self.labelStatus)

    self.startStopCameraButton = QPushButton(self)
    self.startStopCameraButton.setText("Start Camera Capture")
    self.startStopCameraButton.setStyleSheet("color: black; background-color: red")
    self.startStopCameraButton.clicked.connect(self.start_camera)
    self.startStopCameraButton.setEnabled(False)

    self.startExperimentButton = QPushButton(self)
    self.startExperimentButton.setText("Start Experiment")
    self.startExperimentButton.setStyleSheet("color: black;")
    self.startExperimentButton.clicked.connect(self.start_experiment)

    self.stopExperimentButton = QPushButton(self)
    self.stopExperimentButton.setText("Stop Experiment")
    self.stopExperimentButton.setEnabled(False)
    self.stopExperimentButton.setStyleSheet("color: black; background-color: grey")
    self.stopExperimentButton.clicked.connect(self.stop_experiment)

    # data clear button
    self.clearButton = QPushButton()
    self.clearButton.setText("Clear Data")
    self.clearButton.setStyleSheet("color: black")
    self.clearButton.clicked.connect(self.experiment.clear)

    # data collection layout
    self.dataCollectionLayout = QHBoxLayout()
    self.dataCollectionLayout.addWidget(self.startExperimentButton)
    self.dataCollectionLayout.addWidget(self.stopExperimentButton)

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(labelTitle)
    layout.addLayout(self.variablesFormWidget)
    layout.addLayout(statusLayout)
    layout.addLayout(self.dataCollectionLayout)
    layout.addWidget(self.startStopCameraButton)
    layout.addWidget(self.clearButton)
    layout.addWidget(self.logsWidget)
    
    self.setLayout(layout)
  
  def log(self, newLog):
    self.experiment.addLog(newLog)
    self.logsWidget.setText(self.experiment.logs)
  
  def experimentVariableChanged(self, name, text):
    self.log(f"{name} changed to: {text}")

  def snapshotLengthChanged(self, text):
    if (text != ""):
      self.experiment.snapshotLength = int(text)
      self.experimentVariableChanged("Snapshot length", self.experiment.snapshotLength)
  
  def snapshotsPerMinuteChanged(self, text):
    if (text != ""):
      self.experiment.snapshotsPerMinute = int(text)
      self.experimentVariableChanged("Snapshots per minute", self.experiment.snapshotsPerMinute)
  
  def lengthChanged(self, text):
    if (text != ""):
      self.experiment.length = int(text)
      self.experimentVariableChanged("Length", self.experiment.length)
  
  def change_status(self, new_status: DeviceStatus):
    self.status = new_status
    self.labelStatus.setText(self.status.value)
    self.log("Experiment Status: " + self.status.value)
  
  def enable_camera_capture(self, enable):
    if enable:
      self.startStopCameraButton.setEnabled(True)
      self.startStopCameraButton.setStyleSheet("color: black; background-color: green")

      self.start_camera()
    else:
      self.startStopCameraButton.setEnabled(False)
      self.startStopCameraButton.setStyleSheet("color: black; background-color: red")

  def start_experiment(self):
    if self.status == DeviceStatus.READY_TO_START_EXPERIMENT:
      self.change_status(DeviceStatus.RUNNING_EXPERIMENT)

      # disable start button, enable stop button
      self.startExperimentButton.setStyleSheet("color: black; background-color: grey")
      self.startExperimentButton.setEnabled(False)
      self.stopExperimentButton.setStyleSheet("color: black;")
      self.stopExperimentButton.setEnabled(True)

      self.impedance_thread.log_signal.connect(self.log)
      self.impedance_thread.stop_experiment_signal.connect(self.stop_experiment_from_thread)
      self.impedance_thread.enable_signal.connect(self.enable_camera_capture)

      self.impedance_thread.start()
    else:
      self.log("Cannot change experiment status in current state")
  
  def stop_experiment_from_thread(self):
    self.stop_experiment(confirmationOverride = True)

  def stop_experiment(self, confirmationOverride = False):
    if self.status == DeviceStatus.RUNNING_EXPERIMENT:
      if confirmationOverride or self.stopConfirmation():
        self.log("Experiment Stopped")
        self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)

        self.impedance_thread.quit()

        time.sleep(0.5)

        self.log(f"Experiment complete. Writing data to {self.experiment.savePath}")
        self.experiment.write()

        # disable start button, enable stop button
        self.startExperimentButton.setStyleSheet("color: black;")
        self.startExperimentButton.setEnabled(True)
        self.stopExperimentButton.setStyleSheet("color: black; background-color: grey")
        self.stopExperimentButton.setEnabled(False)
    else:
      self.log("Cannot change experiment status in current state")
  
  def start_camera(self):
    if self.status == DeviceStatus.RUNNING_EXPERIMENT:
      self.change_status(DeviceStatus.RUNNING_EXPERIMENT)
      self.startStopCameraButton.setText("Stop Camera Capture")

      self.camera_thread = ExperimentThread(self.experiment, 'start_camera_capture')
      self.camera_thread.log_signal.connect(self.log)
      self.camera_thread.status_signal.connect(self.change_status)
      self.camera_thread.start()
    else:
      self.log("Cannot change experiment status in current state")

  def stopConfirmation(self):
    reply = QMessageBox.question(self, 'Confirmation',
                                  "Are you sure you want to stop process?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                  QMessageBox.StandardButton.No)
  
    return reply
