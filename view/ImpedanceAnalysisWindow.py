from PyQt6.QtWidgets import (QWidget,
                             QPushButton, 
                             QVBoxLayout,
                             QHBoxLayout,
                             QMessageBox,
                             QFileDialog,
                             QLabel,
                             QFormLayout,
                             QLineEdit)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
import pyqtgraph as pg
import numpy as np

from model.ImpedanceAnalysis import ImpedanceAnalysis
from model.Parser import Parser
from view.components.ImpedanceAnalysisMetadata import ImpedanceAnalysisMetadata
from view.components.ImpedanceAnalysisResults import ImpedanceAnalysisResults

class ImpedanceAnalysisWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.data = None
        self.savePath = None
        self.date = None
        self.impedanceAnalysis = None

        self.setWindowTitle("Impedance Analysis")

        self.uploadDataFileButton = QPushButton("Upload Data File", clicked=self.uploadDataFile)
        self.labelDataFile = QLabel("Data from: ")
        
        self.variablesFormWidget = QFormLayout()
        self.numChunksWidget = QLineEdit()
        self.numChunksWidget.setValidator(QIntValidator())
        self.numChunksWidget.setText("10")
        self.numChunksWidget.textChanged.connect(self.numChunksChanged)
        self.variablesFormWidget.addRow("Number of data chunks: ", self.numChunksWidget)

        self.uploadCalibrationFileButton = QPushButton("Upload Calibration File", clicked=self.uploadCalibrationFile)
        self.labelCalibrationFile = QLabel(f"Calibration File: ")

        self.metadata = ImpedanceAnalysisMetadata()

        self.runAnalysisButton = QPushButton("Run Analysis", clicked=self.runAnalysis)
        self.runAnalysisButton.setEnabled(False)
        self.runAnalysisButton.setStyleSheet("background-color: grey")

        self.results = ImpedanceAnalysisResults()
        self.results.refresh(None)

        uploadLayout = QVBoxLayout()
        uploadLayout.addWidget(self.uploadDataFileButton)
        uploadLayout.addWidget(self.labelDataFile)
        uploadLayout.addLayout(self.variablesFormWidget)
        uploadLayout.addWidget(self.uploadCalibrationFileButton)
        uploadLayout.addWidget(self.labelCalibrationFile)
        uploadLayout.addWidget(self.metadata)
        uploadLayout.addWidget(self.runAnalysisButton)
        uploadLayout.addWidget(self.results)

        # Create and set up pyqtgraph plot widget
        self.impedance_widget = pg.PlotWidget()
        self.impedance_widget.addLegend()
        self.capacitance_widget = pg.PlotWidget()
        self.capacitance_widget.addLegend()
        self.conductance_widget = pg.PlotWidget()
        self.conductance_widget.addLegend()

        # Set up plot parameters
        self.impedance_widget.setTitle("Impedance Data (ohms)")
        self.impedance_widget.setLabel("left", "Value")
        self.impedance_widget.setLabel("bottom", "Time", units="s")
        self.impedance_widget.setYRange(5000, 15000)

        # Set up plot parameters
        self.capacitance_widget.setTitle("Capacitance Data (nF)")
        self.capacitance_widget.setLabel("left", "Value")
        self.capacitance_widget.setLabel("bottom", "Time", units="s")
        self.capacitance_widget.setYRange(0, 20)

        # Set up plot parameters
        self.conductance_widget.setTitle("Conductance Data (uS/cm)")
        self.conductance_widget.setLabel("left", "Value")
        self.conductance_widget.setLabel("bottom", "Time", units="s")
        self.conductance_widget.setYRange(0, 250)

        displayLayout = QVBoxLayout()
        # displayLayout.addWidget(self.impedance_widget)
        displayLayout.addWidget(self.capacitance_widget)
        displayLayout.addWidget(self.conductance_widget)

        hLayout = QHBoxLayout()
        hLayout.addLayout(uploadLayout)
        hLayout.addLayout(displayLayout)

        layout = QVBoxLayout()
        layout.addLayout(hLayout)
        layout.addWidget(QPushButton("Save and Close", clicked=self.save_and_close))
        self.setLayout(layout)
    
    def numChunksChanged(self, numChunks):
        if self.impedanceAnalysis is not None:
            self.impedanceAnalysis.numChunks = int(numChunks)
        
        self.metadata.refresh(self.impedanceAnalysis)

    def save_and_close(self):
        if self.stopConfirmation() and self.impedanceAnalysis is not None:
            self.impedanceAnalysis.write(self.savePath)
            self.close()
        else:
            self.close()
    
    def uploadDataFile(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # Allow selecting only existing files
        file_dialog.setNameFilter("JSON Files (*.json)")
        if file_dialog.exec():  # If the dialog is accepted
            file_paths = file_dialog.selectedFiles()[0]
        parser = Parser()
        parser.parse_json(file_paths)

        self.data = parser
        self.runAnalysisButton.setEnabled(True)

        file_label = ''.join(file_paths.split('/')[-2])
        self.date = file_label
        self.savePath = file_label

        self.labelDataFile.setText(f"Data from: {file_label}")

        self.impedanceAnalysis = ImpedanceAnalysis(self.date, self.data.low_impedance, self.data.high_impedance)
        self.labelCalibrationFile.setText(f"Calibration from: {self.impedanceAnalysis.water_path}")

        self.metadata.refresh(self.impedanceAnalysis)
    
    def uploadCalibrationFile(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # Allow selecting only existing files
        file_dialog.setNameFilter("JSON Files (*.json)")
        if file_dialog.exec():  # If the dialog is accepted
            file_paths = file_dialog.selectedFiles()[0]
        parser = Parser()
        parser.parse_json(file_paths)

        self.impedanceAnalysis.water_path = file_paths
        file_label = ''.join(file_paths.split('/')[-2])

        self.labelCalibrationFile.setText(f"Calibration from: ...{file_label}")
    
    def runAnalysis(self):
        if (self.data is None):
            print("No data to analyze")
        else:
            self.runAnalysisButton.setText("Running Analysis")
            self.runAnalysisButton.setEnabled(False)
            self.impedanceAnalysis.run()
            self.runAnalysisButton.setText("Analysis Done")
            self.runAnalysisButton.setEnabled(True)

            self.results.refresh(self.impedanceAnalysis)

            duration = float(self.data.experiment_duration.split()[0])

            '''
            self.graph_impedance_data(duration, 
                                      self.impedanceAnalysis.imp_low_list,
                                      self.impedanceAnalysis.imp_high_list,
                                      self.impedanceAnalysis.water_imp_low,
                                      self.impedanceAnalysis.water_imp_high)
            '''

            self.graph_capacitance_data(duration, self.impedanceAnalysis.cap_list, self.impedanceAnalysis.water_cap)
            self.graph_conductance_data(duration, self.impedanceAnalysis.cond_list, self.impedanceAnalysis.water_cond)

    def graph_impedance_data(self, length, imp_low: list, imp_high: list, water_low, water_high):
        # Extract X (time) and Y (value) for plotting
        x_data_low = np.linspace(0, length, len(imp_low))
        x_data_high = np.linspace(0, length, len(imp_high))
        x_data_water_low = np.linspace(0, length, len(water_low))
        x_data_water_high = np.linspace(0, length, len(water_high))

        # Update the plot with new data
        self.impedance_widget.clear()
        self.impedance_widget.addLegend()
        self.impedance_widget.plot(x_data_low, imp_low, pen='b', symbol='o', symbolBrush='r', name="Low Frequency")
        self.impedance_widget.plot(x_data_high, imp_high, pen='b', symbol='o', symbolBrush='g', name="High Frequency")
        self.impedance_widget.plot(x_data_water_low, water_low, pen='b', symbol='o', symbolBrush='b', name="Base Low Frequency")
        self.impedance_widget.plot(x_data_water_high, water_high, pen='b', symbol='o', symbolBrush='w', name="Base High Frequency")
        self.impedance_widget.enableAutoRange(axis='xy', enable=True)

    def graph_capacitance_data(self, length, cap_list, water_cap):
        # Extract X (time) and Y (value) for plotting
        x_data = np.linspace(0, length, len(cap_list))
        x_data_water = np.linspace(0, length, len(water_cap))

        # Update the plot with new data
        self.capacitance_widget.clear()
        self.capacitance_widget.addLegend()
        self.capacitance_widget.plot(x_data, cap_list, pen='b', symbol='o', symbolBrush='b', name="Capacitance")
        self.capacitance_widget.plot(x_data_water, water_cap, pen='b', symbol='o', symbolBrush='w', name="Base Capacitance")
        self.capacitance_widget.enableAutoRange(axis='xy', enable=True)

    def graph_conductance_data(self, length, cond_list, water_cond):
        # Extract X (time) and Y (value) for plotting
        x_data = np.linspace(0, length, len(cond_list))
        x_data_water = np.linspace(0, length, len(water_cond))

        # Update the plot with new data
        self.conductance_widget.clear()
        self.conductance_widget.addLegend()
        self.conductance.plot(x_data, cond_list, pen='b', symbol='o', symbolBrush='b')
        self.conductance_widget.plot(x_data_water, water_cond, pen='b', symbol='o', symbolBrush='w')
        self.conductance_widget.enableAutoRange(axis='xy', enable=True)

    def stopConfirmation(self):
        reply = QMessageBox.question(self, 'Save Analysis',
                                    "Do you want to save before closing?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
    
        return reply