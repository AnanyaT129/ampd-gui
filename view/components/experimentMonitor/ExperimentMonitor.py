from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
  QVBoxLayout,
  QHBoxLayout,
  QLabel,
  QWidget,
  QPushButton,
  QLineEdit,
  QFormLayout,
  QCheckBox
)
from PyQt6.QtGui import QColor, QPalette, QIntValidator

import time

from view.components.Logs import Logs
from model.constants.DeviceStatus import DeviceStatus
from view.components.experimentMonitor.ExperimentThread import ExperimentThread

class ExperimentMonitor(QWidget):
  def __init__(self, experiment, refreshButton: QPushButton):
    super().__init__()
    self.setAutoFillBackground(True)
    self.experiment = experiment

    # Experiment logs
    self.logsWidget = Logs(self)

    palette = self.palette()
    # palette.setColor(QPalette.ColorRole.Window, QColor("White"))
    self.setPalette(palette)

    # Experiment thread
    self.impedance_thread = ExperimentThread(self.experiment, 'start_data_collection')

    # Experiment title label
    labelTitle = QLabel(f"Title: {self.experiment.savePath}")
    labelTitle.setStyleSheet("font-weight: bold")

    # refresh button
    self.clearButton = refreshButton
    self.clearButton.setEnabled(False)

    # Experiment Variables
    self.variablesFormWidget = QFormLayout()

    self.lengthWidget = QLineEdit()
    self.lengthWidget.setValidator(QIntValidator())
    self.lengthWidget.setText("5")
    self.lengthWidget.textChanged.connect(self.lengthChanged)
    self.variablesFormWidget.addRow("Experiment duration (s): ", self.lengthWidget)

    self.cameraLengthWidget = QLineEdit()
    self.cameraLengthWidget.setValidator(QIntValidator())
    self.cameraLengthWidget.setText("1")
    self.cameraLengthWidget.textChanged.connect(self.cameraLengthChanged)
    self.variablesFormWidget.addRow("Camera snapshot length (s): ", self.cameraLengthWidget)

    self.cameraFPSWidget = QLineEdit()
    self.cameraFPSWidget.setValidator(QIntValidator())
    self.cameraFPSWidget.setText("30")
    self.cameraFPSWidget.textChanged.connect(self.fPSChanged)
    self.variablesFormWidget.addRow("Camera FPS (frames/s): ", self.cameraFPSWidget)

    self.experimentEnableLayout = QHBoxLayout()
    self.impedanceEnable = QCheckBox("Impedance", self)
    self.impedanceEnable.setCheckState(Qt.CheckState.Checked)
    self.impedanceEnable.stateChanged.connect(self.impedanceChanged)
    self.cameraEnable = QCheckBox("Camera", self)
    self.cameraEnable.setCheckState(Qt.CheckState.Checked)
    self.cameraEnable.stateChanged.connect(self.cameraChanged)

    self.experimentEnableLayout.addWidget(self.impedanceEnable)
    self.experimentEnableLayout.addWidget(self.cameraEnable)
    self.variablesFormWidget.addRow("Experiment Enable: ", self.experimentEnableLayout)

    # Experiment status labels 
    labelConnect = QLabel("Device Status")
    labelConnect.setStyleSheet("font-weight: bold")

    self.status = DeviceStatus.READY_TO_START_EXPERIMENT
    self.labelStatus = QLabel(self.status.value)

    statusLayout = QHBoxLayout()
    statusLayout.addWidget(labelConnect)
    statusLayout.addWidget(self.labelStatus)

    self.startExperimentButton = QPushButton(self)
    self.startExperimentButton.setText("Start Experiment")
    self.startExperimentButton.clicked.connect(self.start_experiment)

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(labelTitle)
    layout.addLayout(self.variablesFormWidget)
    layout.addLayout(statusLayout)
    layout.addWidget(self.startExperimentButton)
    layout.addWidget(self.logsWidget)
    
    self.setLayout(layout)
  
  def log(self, newLog):
    self.experiment.addLog(newLog)
    self.logsWidget.setText(self.experiment.logs)
  
  def experimentVariableChanged(self, name, text):
    self.log(f"{name} changed to: {text}")

  def cameraLengthChanged(self, text):
    if (text != ""):
      self.experiment.cameraLength = int(text)
      self.experimentVariableChanged("Camera snapshot length", self.experiment.cameraLength)
  
  def fPSChanged(self, text):
    if (text != ""):
      self.experiment.cameraFps = int(text)
      self.experimentVariableChanged("Camera FPS", self.experiment.cameraFps)
  
  def lengthChanged(self, text):
    if (text != ""):
      self.experiment.length = int(text)
      self.experimentVariableChanged("Length", self.experiment.length)

  def impedanceChanged(self, state):
    if state == 2: # Qt.Checked
      self.experiment.enable[0] = True
      self.log("Impedance enabled")
    elif state == 0: # Qt.Unchecked
      self.experiment.enable[0] = False
      self.log("Impedance disabled")
    
    print(self.experiment.enable)
  
  def cameraChanged(self, state):
    if state == 2: # Qt.Checked
      self.experiment.enable[1] = True
      self.log("Camera enabled")
    elif state == 0: # Qt.Unchecked
      self.experiment.enable[1] = False
      self.log("Camera disabled")
    
    print(self.experiment.enable)
  
  def change_status(self, new_status: DeviceStatus):
    self.status = new_status
    self.labelStatus.setText(self.status.value)
    self.log("Experiment Status: " + self.status.value)

  def start_experiment(self):
    if self.status == DeviceStatus.READY_TO_START_EXPERIMENT:
      self.change_status(DeviceStatus.RUNNING_EXPERIMENT)

      # disable start button, enable stop button
      self.startExperimentButton.setStyleSheet("background-color: grey")
      self.startExperimentButton.setEnabled(False)

      self.impedance_thread.log_signal.connect(self.log)
      self.impedance_thread.stop_experiment_signal.connect(self.stop_experiment)
      self.impedance_thread.change_status_signal.connect(self.change_status)

      self.impedance_thread.start()
    else:
      self.log("Cannot change experiment status in current state")

  def stop_experiment(self, stop):
    if (self.status == DeviceStatus.RUNNING_EXPERIMENT or 
        self.status == DeviceStatus.CAPTURING_IMPEDANCE_DATA or 
        self.status == DeviceStatus.CAPTURING_CAMERA_DATA and
        stop):
      self.log("Experiment Stopped")
      self.change_status(DeviceStatus.READY_TO_START_EXPERIMENT)

      self.impedance_thread.quit()

      time.sleep(0.5)

      self.log(f"Experiment complete.")
      
      if self.experiment.enable[0]:
        self.log(f" Writing impedance data to {self.experiment.savePath}")
        self.experiment.write()

      # disable start button, enable stop button
      self.clearButton.setEnabled(True)
    else:
      self.log("Cannot change experiment status in current state")
