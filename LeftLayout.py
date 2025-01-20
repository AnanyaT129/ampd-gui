from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel
)

from components.AmpdTitle import AmpdTitle
from components.ExperimentMonitor import ExperimentMonitor

class LayoutLeft(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.addWidget(AmpdTitle())
        self.addWidget(ExperimentMonitor())