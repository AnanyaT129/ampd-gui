from PyQt6.QtCore import Qt, QThread, pyqtSignal
import time

from model.DeviceStatus import DeviceStatus

class ExperimentThread(QThread):
    # Define signals to communicate with the main thread
    log_signal = pyqtSignal(str)
    stop_experiment_signal = pyqtSignal(bool)
    enable_signal = pyqtSignal(bool)

    def __init__(self, experiment, action, length=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experiment = experiment
        self.action = action  # The action to be performed (e.g., 'start_data_collection')
        self.length = length

    def run(self):
        if self.action == 'start_data_collection':
            wait = 60/self.experiment.snapshotsPerMinute
            iterations = self.experiment.snapshotsPerMinute * self.experiment.length

            for i in range(iterations):
                self.log_signal.emit(f"Collecting data for snapshot {i + 1} of {iterations}")
                self.experiment.start_data_collection(self.length)

                threshold = self.experiment.checkThreshold()
                
                if threshold:
                    self.enable_signal.emit(True)
                    self.log_signal.emit("Microplastic threshold passed - camera snapshot activated")
                else:
                    self.enable_signal.emit(False)
                
                time.sleep(wait)

                self.log_signal.emit(f"Data collected: {len(self.experiment.data[-1][0])} low measurements and {len(self.experiment.data[-1][1])} high measurements")
            
            self.stop_experiment_signal.emit(True)
        elif self.action == 'start_camera_capture':
            self.start_camera_capture()
    
    def start_camera_capture(self):
        self.experiment.camera_capture(self.length)
        self.log_signal.emit(f"Data collected: {len(self.experiment.frames)} frames")
