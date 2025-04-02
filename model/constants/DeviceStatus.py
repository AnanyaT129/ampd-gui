from enum import Enum

class DeviceStatus(Enum):
  READY_TO_START_EXPERIMENT = "Ready to start experiment"
  RUNNING_EXPERIMENT = "Running experiment"
  CAPTURING_IMPEDANCE_DATA = "Capturing impedance data"
  CAPTURING_CAMERA_DATA = "Capturing camera data"
  PERFORMING_ANALYSIS = "Performing analysis"
  UPLOADING_DATA = "Uploading data"

