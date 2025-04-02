from PyQt6.QtWidgets import (QWidget,
                             QPushButton, 
                             QVBoxLayout,
                             QHBoxLayout,
                             QMessageBox,
                             QFileDialog,
                             QLabel,
                             QFormLayout,
                             QLineEdit)
from PyQt6.QtGui import QIntValidator
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

        self.metadata = ImpedanceAnalysisMetadata()

        self.runAnalysisButton = QPushButton("Run Analysis", clicked=self.runAnalysis)
        self.runAnalysisButton.setEnabled(False)
        self.runAnalysisButton.setStyleSheet("color: black; background-color: grey")

        self.results = ImpedanceAnalysisResults()
        self.results.refresh(None)

        uploadLayout = QVBoxLayout()
        uploadLayout.addWidget(self.uploadDataFileButton)
        uploadLayout.addWidget(self.labelDataFile)
        uploadLayout.addLayout(self.variablesFormWidget)
        uploadLayout.addWidget(self.metadata)
        uploadLayout.addWidget(self.runAnalysisButton)
        uploadLayout.addWidget(self.results)

        # Create and set up pyqtgraph plot widget
        self.impedance_widget = pg.PlotWidget()
        self.capacitance_widget = pg.PlotWidget()

        # Set up plot parameters
        self.impedance_widget.setTitle("Impedance Data")
        self.impedance_widget.setLabel("left", "Value")
        self.impedance_widget.setLabel("bottom", "Time", units="s")
        self.impedance_widget.setYRange(0, 3300)

        # Set up plot parameters
        self.capacitance_widget.setTitle("Capacitance Data")
        self.capacitance_widget.setLabel("left", "Value")
        self.capacitance_widget.setLabel("bottom", "Time", units="s")
        self.capacitance_widget.setYRange(0, 3300)
       
        displayLayout = QVBoxLayout()
        displayLayout.addWidget(self.impedance_widget)
        displayLayout.addWidget(self.capacitance_widget)

        hLayout = QHBoxLayout()
        hLayout.addLayout(uploadLayout)
        hLayout.addLayout(displayLayout)

        layout = QVBoxLayout()
        layout.addLayout(hLayout)
        layout.addWidget(QPushButton("Save and Close", clicked=self.save_and_close))
        self.setLayout(layout)
    
    def numChunksChanged(self, numChunks):
        if self.impedanceAnalysis is not None:
            self.impedanceAnalysis.numChunks = numChunks
        
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
        self.runAnalysisButton.setStyleSheet("color: black;")

        file_label = ''.join(file_paths.split('/')[-2])
        self.date = file_label
        self.savePath = file_label

        self.labelDataFile.setText(f"Data from: {file_label}")

        self.impedanceAnalysis = ImpedanceAnalysis(self.date, self.data.low_impedance, self.data.high_impedance)

        self.metadata.refresh(self.impedanceAnalysis)
    
    def runAnalysis(self):
        if (self.data is None):
            print("No data to analyze")
        else:
            self.impedanceAnalysis.run()

            self.results.refresh(self.impedanceAnalysis)

            duration = float(self.data.experiment_duration.split()[0])

            self.graph_impedance_data(duration, self.impedanceAnalysis.imp_low_list, self.impedanceAnalysis.imp_high_list)
            self.graph_capacitance_data(duration, self.impedanceAnalysis.cap_list)
    
    def graph_impedance_data(self, length, imp_low: list, imp_high: list):
        # Extract X (time) and Y (value) for plotting
        x_data_low = np.linspace(0, length, len(imp_low))
        x_data_high = np.linspace(0, length, len(imp_high))

        # Update the plot with new data
        self.impedance_widget.clear()
        self.impedance_widget.plot(x_data_low, imp_low, pen='b', symbol='o', symbolBrush='r')
        self.impedance_widget.plot(x_data_high, imp_high, pen='b', symbol='o', symbolBrush='g')

    def graph_capacitance_data(self, length, cap_list):
        # Extract X (time) and Y (value) for plotting
        x_data = np.linspace(0, length, len(cap_list))

        # Update the plot with new data
        self.capacitance_widget.clear()
        self.capacitance_widget.plot(x_data, cap_list, pen='b', symbol='o', symbolBrush='b')

    def stopConfirmation(self):
        reply = QMessageBox.question(self, 'Save Analysis',
                                    "Do you want to save before closing?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
    
        return reply