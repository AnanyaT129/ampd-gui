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

        estContentLayout = QHBoxLayout()
        estContentTitleLabel = QLabel("Estimated Microplastic Content: ")
        estContentTitleLabel.setStyleSheet("font-weight: bold")
        self.estContentContentLabel = QLabel("")

        estContentLayout.addWidget(estContentTitleLabel)
        estContentLayout.addWidget(self.estContentContentLabel)

        plasticPresentLayout = QHBoxLayout()
        plasticPresentTitleLabel = QLabel("Plastic Present? ")
        plasticPresentTitleLabel.setStyleSheet("font-weight: bold")
        self.plasticPresentContentLabel = QLabel("")

        plasticPresentLayout.addWidget(plasticPresentTitleLabel)
        plasticPresentLayout.addWidget(self.plasticPresentContentLabel)

        self.layout = QVBoxLayout()
        self.layout.addWidget(resultsTitle)
        self.layout.addLayout(avgScatteredLayout)
        self.layout.addLayout(estContentLayout)
        self.layout.addLayout(plasticPresentLayout)

        self.setLayout(self.layout)
    
    def refresh(self, cameraAnalysis: CameraAnalysis):
        if cameraAnalysis is not None:
            self.avgScatteredContentLabel.setText(str(cameraAnalysis.average_scattered_light))
            self.estContentContentLabel.setText(str(cameraAnalysis.estimatedPlasticContent))
            self.plasticPresentContentLabel.setText(str(cameraAnalysis.plasticPresent))

        else:
            self.avgScatteredContentLabel.setText("")
            self.estContentContentLabel.setText("")
            self.plasticPresentContentLabel.setText("")