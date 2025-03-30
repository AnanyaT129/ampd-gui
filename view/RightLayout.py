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
from model.Parser import Parser

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
        x_data_low = np.linspace(0, self.experiment.length, len(self.experiment.getLatestData()[0]))
        x_data_high = np.linspace(0, self.experiment.length, len(self.experiment.getLatestData()[1]))
        y_data_low = self.experiment.getLatestData()[0]
        y_data_high = self.experiment.getLatestData()[1]

        # Update the plot with new data
        self.plot_widget.clear()
        self.plot_widget.plot(x_data_low, y_data_low, pen='b', symbol='o', symbolBrush='r')
        self.plot_widget.plot(x_data_high, y_data_high, pen='b', symbol='o', symbolBrush='g')
    
    def impedance_analysis(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # Allow selecting only existing files
        file_dialog.setNameFilter("JSON Files (*.json)")
        if file_dialog.exec():  # If the dialog is accepted
            file_paths = file_dialog.selectedFiles()[0]
        parser = Parser()
        parser.parse_json(file_paths)
        '''
        print(f"Date: {parser.date}")
        print("Metadata:")
        print(f"  Snapshot Length: {parser.snapshot_length}")
        print(f"  Snapshots Per Minute: {parser.snapshots_per_minute}")
        print(f"  Experiment Duration: {parser.experiment_duration}")
        print(f"  Camera FPS: {parser.camera_fps}")
        
        print("Impedance Data:")
        print(f"  Low Impedance: {parser.low_impedance}")
        print(f"  High Impedance: {parser.high_impedance}")
        '''
        
        # impedance_analysis = ImpedanceAnalysis(self.experiment.data)
        # impedance_analysis.run()
    
    def camera_analysis(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)  # Allow selecting directories only
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)  # Ensure only directories are shown
        if folder_dialog.exec():  # If the dialog is accepted
            folder_path = folder_dialog.selectedFiles()[0]
        png_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".png")]
        # print(png_files)
        # camera_analysis = CameraAnalysis(self.experiment.frames)
        # camera_analysis.run()
