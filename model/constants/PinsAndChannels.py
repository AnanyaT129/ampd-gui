from enum import Enum

class ADC(Enum):
    LOW_FREQ_PROBE = 0
    HIGH_FREQ_PROBE = 1

class GPIOPins(Enum):
    LOW_FREQ_ON = 23
    HIGH_FREQ_ON = 25
    RELAY_PIN = 17
