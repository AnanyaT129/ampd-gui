from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)
import pyqtgraph as pg
import numpy as np

from model.ImpedanceAnalysis import ImpedanceAnalysis
from model.CameraAnalysis import CameraAnalysis

class RightLayout(QVBoxLayout):
    def __init__(self, experiment):
        super().__init__()
        
        # Create Experiment instance
        self.experiment = experiment

        # Create and set up pyqtgraph plot widget
        self.plot_widget = pg.PlotWidget()
        self.addWidget(self.plot_widget)

        # Set up plot parameters
        self.plot_widget.setTitle("Real-Time Data")
        self.plot_widget.setLabel("left", "Value")
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setYRange(0, 3300)

        # Set up a timer to update the graph every 100 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(100)  # Update every 100 ms

        # setup analysis parameters
        self.impedanceAnalysisButton = QPushButton()
        self.impedanceAnalysisButton.setText("Impedance Analysis")
        self.impedanceAnalysisButton.setStyleSheet("color: black;")
        self.impedanceAnalysisButton.clicked.connect(self.impedance_analysis)

        self.cameraAnalysisButton = QPushButton()
        self.cameraAnalysisButton.setText("Camera Analysis")
        self.cameraAnalysisButton.setStyleSheet("color: black;")
        self.cameraAnalysisButton.clicked.connect(self.camera_analysis)

        self.analysisLayout = QHBoxLayout()
        self.analysisLayout.addWidget(self.impedanceAnalysisButton)
        self.analysisLayout.addWidget(self.cameraAnalysisButton)

        self.addLayout(self.analysisLayout)

    def update_graph(self):
        """
        Get data from the experiment and update the plot.
        """
        # Extract X (time) and Y (value) for plotting
        x_data = np.linspace(0, self.experiment.length, len(self.experiment.data))
        y_data = self.experiment.data

        # Update the plot with new data
        self.plot_widget.clear()
        self.plot_widget.plot(x_data, y_data, pen='b', symbol='o', symbolBrush='r')
    
    def impedance_analysis(self):
        impedance_analysis = ImpedanceAnalysis(self.experiment.data)
        impedance_analysis.run()
    
    def camera_analysis(self):
        camera_analysis = CameraAnalysis(self.experiment.frames)
        camera_analysis.run()
