import json

class Parser:
    def __init__(self):
        self.date = None
        self.camera_snapshot_length = None
        self.experiment_duration = None
        self.camera_fps = None
        self.low_impedance = []
        self.high_impedance = []
    def parse_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extracting data
        self.date = data.get("date", "N/A")
        metadata = data.get("metadata", {})
        impedance_data = data.get("impedanceData", {})
        
        # Extract metadata details
        self.camera_snapshot_length = metadata.get("cameraSnapshotLength", "N/A")
        self.experiment_duration = metadata.get("experimentDuration", "N/A")
        self.camera_fps = metadata.get("cameraFps", "N/A")
        
        # Extract impedance data
        self.low_impedance = impedance_data.get("low", [])
        self.high_impedance = impedance_data.get("high", [])
#parser = Parser()
#parser.parse_json('20250327_1920_ampd_experiment_data/data.json')