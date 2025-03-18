from PyQt6.QtCore import Qt, QThread, pyqtSignal

from model.DeviceStatus import DeviceStatus

class ExperimentThread(QThread):
    # Define signals to communicate with the main thread
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(DeviceStatus)

    def __init__(self, experiment, action, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experiment = experiment
        self.action = action  # The action to be performed (e.g., 'start_data_collection')

    def run(self):
        if self.action == 'start_data_collection':
            self.experiment.start_data_collection(5)
            self.log_signal.emit(f"Data collected: {len(self.experiment.data)} measurements")
            self.status_signal.emit(DeviceStatus.READY_TO_START_EXPERIMENT)