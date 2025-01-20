from enum import Enum

class DeviceStatus(Enum):
  DISCONNECTED = "Disconnected"
  READY_TO_START_EXPERIMENT = "Ready to start experiment"
  RUNNING_EXPERIMENT = "Running experiment"
  PERFORMING_ANALYSIS = "Performing analysis"
  UPLOADING_DATA = "Uploading data"

