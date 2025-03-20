from PyQt6.QtCore import Qt, QThread, pyqtSignal
import time

from model.DeviceStatus import DeviceStatus
from model.RealTimeAnalysis import RealTimeAnalysis

class ExperimentThread(QThread):
    # Define signals to communicate with the main thread
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(DeviceStatus)
    enable_signal = pyqtSignal(bool)

    def __init__(self, experiment, action, length=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experiment = experiment
        self.action = action  # The action to be performed (e.g., 'start_data_collection')
        self.length = length
        self.realTimeAnalysis = RealTimeAnalysis()

    def run(self):
        if self.action == 'start_data_collection':
            end = time.time() + self.length

            while time.time() < end:
              d = self.experiment.addDatpoint()
              self.realTimeAnalysis.addData(d)
              threshold = self.realTimeAnalysis.data
              
              if threshold:
                  self.enable_signal.emit(True)

            self.log_signal.emit(f"Data collected: {len(self.experiment.data)} measurements")
            self.status_signal.emit(DeviceStatus.READY_TO_START_EXPERIMENT)
        elif self.action == 'start_camera_capture':
            self.start_camera_capture()
    
    def start_camera_capture(self):
        self.experiment.camera_capture(self.length)
        self.log_signal.emit(f"Data collected: {len(self.experiment.frames)} frames")
        self.status_signal.emit(DeviceStatus.READY_TO_START_EXPERIMENT)
