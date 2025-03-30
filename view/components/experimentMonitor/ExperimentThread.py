from PyQt6.QtCore import Qt, QThread, pyqtSignal
import time

from model.DeviceStatus import DeviceStatus

class ExperimentThread(QThread):
    # Define signals to communicate with the main thread
    log_signal = pyqtSignal(str)
    stop_experiment_signal = pyqtSignal(bool)

    def __init__(self, experiment, action, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experiment = experiment
        self.action = action  # The action to be performed (e.g., 'start_data_collection')

    def run(self):
        if self.action == 'start_data_collection':

            if (self.experiment.enable[0]):
                self.log_signal.emit(f"Collecting impdedance data for {self.experiment.length} seconds")
                self.experiment.start_mock_data_collection()

                self.log_signal.emit(f"Data collected: {len(self.experiment.data[-1][0])} low measurements and {len(self.experiment.data[-1][1])} high measurements")
            
            if (self.experiment.enable[1]):
                self.experiment.mock_camera_capture()
                self.log_signal.emit(f"Data collected: {len(self.experiment.frames)} frames")
            
            self.stop_experiment_signal.emit(True)
