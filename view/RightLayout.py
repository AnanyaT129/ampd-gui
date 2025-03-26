from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
)
import pyqtgraph as pg
import numpy as np

# from model.ImpedanceAnalysis import ImpedanceAnalysis
# from model.CameraAnalysis import CameraAnalysis

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
        x_data_low = np.linspace(0, self.experiment.snapshotLength, len(self.experiment.getLatestData()[0]))
        x_data_high = np.linspace(0, self.experiment.snapshotLength, len(self.experiment.getLatestData()[1]))
        y_data_low = self.experiment.getLatestData()[0]
        y_data_high = self.experiment.getLatestData()[1]

        # Update the plot with new data
        self.plot_widget.clear()
        self.plot_widget.plot(x_data_low, y_data_low, pen='b', symbol='o', symbolBrush='r')
        self.plot_widget.plot(x_data_high, y_data_high, pen='b', symbol='o', symbolBrush='g')

        # plot the threshold if it was passed
        t: tuple | None = self.experiment.fetchLatestThreshold()
        if t is not None:
            x = self.experiment.snapshotLength/t[0]
            y = t[1]
            threshold_line = pg.InfiniteLine(pos=x, angle=90, movable=False)
            threshold_point = pg.ScatterPlotItem(pos=[(x, y)], symbol='o', size=10, pen=pg.mkPen(color='r'))
            threshold_label = pg.TextItem(text=f"Threshold pased at ({x}, {y})", anchor=(0.5, 1.5))
            threshold_label.setPos(x, y)

            self.plot_widget.addItem(threshold_line)
            self.plot_widget.addItem(threshold_point)
            self.plot_widget.addItem(threshold_label)
    
    def impedance_analysis(self):
        print("Not implemented")
        # impedance_analysis = ImpedanceAnalysis(self.experiment.data)
        # impedance_analysis.run()
    
    def camera_analysis(self):
        print("not implemented")
        # camera_analysis = CameraAnalysis(self.experiment.frames)
        # camera_analysis.run()
