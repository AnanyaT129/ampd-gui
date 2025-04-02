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

from model.Experiment import Experiment
from model.Server import Server
from view.components.experimentMonitor.LengthInput import LengthInput
from view.components.experimentMonitor.sockets.WorkerThread import WorkerThread
from view.components.Logs import Logs
from model.constants.DeviceStatus import DeviceStatus

class ExperimentMonitorThreaded(QWidget):
    def __init__(self, experiment: Experiment):
        super().__init__()

        self.setAutoFillBackground(True)

        # Experiment
        self.experiment = experiment

        # Experiment server
        self.server = Server(self.experiment, log_callback=self.log)

        # Experiment status
        self.status = DeviceStatus.DISCONNECTED
        self.labelStatus = QLabel(self.status.value)
        self.labelStatus.setStyleSheet("color: black;")

        # Set up palette for the window
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("White"))
        self.setPalette(palette)

        # Layout for device status
        labelConnect = QLabel("Device Status")
        labelConnect.setStyleSheet("color: black; font-weight: bold")

        statusLayout = QHBoxLayout()
        statusLayout.addWidget(labelConnect)
        statusLayout.addWidget(self.labelStatus)

        # Buttons for controlling server and experiment
        self.startStopServerButton = QPushButton(self)
        self.startStopServerButton.setText("Start Server")
        self.startStopServerButton.setStyleSheet("color: black;")
        self.startStopServerButton.clicked.connect(self.start_stop_server)

        self.startStopExperimentButton = QPushButton(self)
        self.startStopExperimentButton.setText("Start Experiment")
        self.startStopExperimentButton.setStyleSheet("color: black;")
        self.startStopExperimentButton.clicked.connect(self.start_stop_experiment)

        self.lengthInput = LengthInput("Length", initial_value=5)

        # logs widget
        self.logsWidget = Logs()

        # Layout for buttons
        layoutStartStop = QHBoxLayout()
        layoutStartStop.addWidget(self.startStopServerButton)
        layoutStartStop.addWidget(self.startStopExperimentButton)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(statusLayout)
        layout.addWidget(self.lengthInput)
        layout.addLayout(layoutStartStop)
        layout.addWidget(self.logsWidget)

        self.setLayout(layout)

    def log(self, newLog):
        self.experiment.addLog(newLog)
        self.logsWidget.setText(self.experiment.logs)

    def change_status(self, new_status: DeviceStatus):
        self.status = new_status
        self.labelStatus.setText(self.status.value)
        self.log("Experiment Status: " + self.status.value)

    def start_stop_server(self):
        if self.status == DeviceStatus.DISCONNECTED and self.server.server_socket == None:
            # Start server in a worker thread
            self.worker_thread = WorkerThread(self.server, 'start_server')
            self.worker_thread.log_signal.connect(self.log)  # Connect log signal to appendLog
            self.worker_thread.status_signal.connect(self.change_status)  # Connect status signal to change_status
            self.worker_thread.start()

            self.startStopServerButton.setText("Stop Server")
        elif self.status == DeviceStatus.RUNNING_EXPERIMENT:
            self.log("Cannot stop server while experiment is running")
        else:
            stop = self.stopConfirmation()
            if stop:
                # Stop server in a worker thread
                self.worker_thread = WorkerThread(self.server, 'stop_server')
                self.worker_thread.log_signal.connect(self.log)
                self.worker_thread.status_signal.connect(self.change_status)
                self.worker_thread.start()

                self.startStopServerButton.setText("Start Server")

    def start_stop_experiment(self):
        if self.status == DeviceStatus.READY_TO_START_EXPERIMENT:
            self.change_status(DeviceStatus.RUNNING_EXPERIMENT)
            self.startStopExperimentButton.setText("Stop Experiment")

            # Start data collection in a worker thread
            self.worker_thread = WorkerThread(self.server, 'start_data_collection')
            self.worker_thread.log_signal.connect(self.log)
            self.worker_thread.status_signal.connect(self.change_status)
            self.worker_thread.start()
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
        return reply == QMessageBox.StandardButton.Yes

