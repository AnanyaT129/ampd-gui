from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout
)

from view.components.AmpdTitle import AmpdTitle
from view.components.experimentMonitor.ExperimentMonitor import ExperimentMonitor
from view.components.experimentMonitor.ExperimentMonitor import ExperimentMonitor

class LayoutLeft(QVBoxLayout):
    def __init__(self, experiment):
        super().__init__()

        self.experiment = experiment

        self.addWidget(AmpdTitle())
        self.addWidget(ExperimentMonitor(experiment))