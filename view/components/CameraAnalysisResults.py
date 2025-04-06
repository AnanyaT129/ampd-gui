from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from model.CameraAnalysis import CameraAnalysis

class CameraAnalysisResults(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        # meta data labels
        resultsTitle = QLabel("Results")
        resultsTitle.setStyleSheet("font-weight: bold")

        avgScatteredLayout = QHBoxLayout()
        avgScatteredTitleLabel = QLabel("Average Scattered Light: ")
        avgScatteredTitleLabel.setStyleSheet("font-weight: bold")
        self.avgScatteredContentLabel = QLabel("")

        avgScatteredLayout.addWidget(avgScatteredTitleLabel)
        avgScatteredLayout.addWidget(self.avgScatteredContentLabel)

        plasticPresentLayout = QHBoxLayout()
        plasticPresentTitleLabel = QLabel("Plastic Present? ")
        plasticPresentTitleLabel.setStyleSheet("font-weight: bold")
        self.plasticPresentContentLabel = QLabel("")

        plasticPresentLayout.addWidget(plasticPresentTitleLabel)
        plasticPresentLayout.addWidget(self.plasticPresentContentLabel)

        self.layout = QVBoxLayout()
        self.layout.addWidget(resultsTitle)
        self.layout.addLayout(avgScatteredLayout)
        self.layout.addLayout(plasticPresentLayout)

        self.setLayout(self.layout)
    
    def refresh(self, cameraAnalysis: CameraAnalysis):
        if cameraAnalysis is not None:
            self.avgScatteredContentLabel.setText(str(cameraAnalysis.average_scattered_light))
            self.plasticPresentContentLabel.setText(str(cameraAnalysis.plasticPresent))

        else:
            self.avgScatteredContentLabel.setText("")
            self.plasticPresentContentLabel.setText("")