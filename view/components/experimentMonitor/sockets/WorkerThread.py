from PyQt6.QtCore import Qt, QThread, pyqtSignal

from model.constants.DeviceStatus import DeviceStatus

class WorkerThread(QThread):
    # Define signals to communicate with the main thread
    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(DeviceStatus)

    def __init__(self, server, action, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = server
        self.action = action  # The action to be performed (e.g., 'start_server', 'stop_server', 'collect_data')

    def run(self):
        if self.action == 'start_server':
            success = self.server.start_server()
            if success:
                self.log_signal.emit("Server started successfully.")
                self.status_signal.emit(DeviceStatus.READY_TO_START_EXPERIMENT)
            else:
                self.log_signal.emit("Failed to start the server.")
        elif self.action == 'stop_server':
            self.server.close_server()
            self.log_signal.emit("Server stopped.")
            self.status_signal.emit(DeviceStatus.DISCONNECTED)
        elif self.action == 'start_data_collection':
            data = self.server.start_data_collection(5)
            self.log_signal.emit(f"Data collected: {data[:10]}")
            self.status_signal.emit(DeviceStatus.READY_TO_START_EXPERIMENT)