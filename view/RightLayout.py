from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
)
import pyqtgraph as pg
import numpy as np
import os
from model.CameraAnalysis import CameraAnalysis
from model.Parser import Parser
from view.CameraAnalysisWindow import CameraAnalysisWindow
from view.ImpedanceAnalysisWindow import ImpedanceAnalysisWindow
from view.components.upload.UploadWindow import UploadWindow

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
        self.impedanceAnalysisWindow = None
        self.impedanceAnalysisButton = QPushButton()
        self.impedanceAnalysisButton.setText("Impedance Analysis")
        self.impedanceAnalysisButton.clicked.connect(self.impedance_analysis)

        self.cameraAnalysisWindow = None
        self.cameraAnalysisButton = QPushButton()
        self.cameraAnalysisButton.setText("Camera Analysis")
        self.cameraAnalysisButton.clicked.connect(self.camera_analysis)

        self.uploadWindow = None
        self.analysisLayout = QHBoxLayout()
        self.analysisLayout.addWidget(self.impedanceAnalysisButton)
        self.analysisLayout.addWidget(self.cameraAnalysisButton)
        self.analysisLayout.addWidget(QPushButton("Upload Data", clicked=self.upload))

        self.addLayout(self.analysisLayout)

    def update_graph(self):
        """
        Get data from the experiment and update the plot.
        """
        # Extract X (time) and Y (value) for plotting
        x_data_low = np.linspace(0, self.experiment.length, len(self.experiment.getLatestData()[0]))
        x_data_high = np.linspace(0, self.experiment.length, len(self.experiment.getLatestData()[1]))
        y_data_low = self.experiment.getLatestData()[0]
        y_data_high = self.experiment.getLatestData()[1]

        # Update the plot with new data
        self.plot_widget.clear()
        self.plot_widget.plot(x_data_low, y_data_low, pen='b', symbol='o', symbolBrush='r')
        self.plot_widget.plot(x_data_high, y_data_high, pen='b', symbol='o', symbolBrush='g')
    
    def impedance_analysis(self):
        if self.impedanceAnalysisWindow is None:
            self.impedanceAnalysisWindow = ImpedanceAnalysisWindow()
        self.impedanceAnalysisWindow.show()
    
    def camera_analysis(self):
        if self.cameraAnalysisWindow is None:
            self.cameraAnalysisWindow = CameraAnalysisWindow(CameraAnalysis())
        self.cameraAnalysisWindow.show()
    
    def upload(self):
        if self.uploadWindow is None:
            self.uploadWindow = UploadWindow()
        self.uploadWindow.show()