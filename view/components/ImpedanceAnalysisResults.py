from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from model.ImpedanceAnalysis import ImpedanceAnalysis

class ImpedanceAnalysisResults(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        # meta data labels
        metadataTitle = QLabel("Results")
        metadataTitle.setStyleSheet("font-weight: bold")

        ppmLayout = QHBoxLayout()
        ppmTitleLabel = QLabel("Estimated TDS PPM: ")
        ppmTitleLabel.setStyleSheet("font-weight: bold")
        self.ppmContentLabel = QLabel("")

        ppmLayout.addWidget(ppmTitleLabel)
        ppmLayout.addWidget(self.ppmContentLabel)

        tTesttLayout = QVBoxLayout()
        tTestTitleLabel = QLabel("T Test against Water Control: ")
        tTestTitleLabel.setStyleSheet("font-weight: bold")
        self.tTestContentLabel = QLabel("")

        tTesttLayout.addWidget(tTestTitleLabel)
        tTesttLayout.addWidget(self.tTestContentLabel)

        plasticPresentLayout = QHBoxLayout()
        plasticPresentTitleLabel = QLabel("Plastic Present? ")
        plasticPresentTitleLabel.setStyleSheet("font-weight: bold")
        self.plasticPresentContentLabel = QLabel("")

        plasticPresentLayout.addWidget(plasticPresentTitleLabel)
        plasticPresentLayout.addWidget(self.plasticPresentContentLabel)

        # results labels
        resultsTitle = QLabel("Results")
        resultsTitle.setStyleSheet("font-weight: bold")

        self.layout = QVBoxLayout()
        self.layout.addWidget(metadataTitle)
        self.layout.addLayout(ppmLayout)
        self.layout.addLayout(tTesttLayout)
        self.layout.addLayout(plasticPresentLayout)

        self.setLayout(self.layout)

        # self.addWidget(resultsTitle)
    
    def refresh(self, impedanceAnalysis: ImpedanceAnalysis):
        if impedanceAnalysis is not None:
            self.ppmContentLabel.setText(str(impedanceAnalysis.ppm))
            if impedanceAnalysis.ttestResults is not None:
                tTestStr = f"Low: t={round(impedanceAnalysis.ttestResults[0]['t'], 4)} p={round(impedanceAnalysis.ttestResults[0]['p'], 4)}, High: t={round(impedanceAnalysis.ttestResults[1]['t'], 4)} p={round(impedanceAnalysis.ttestResults[1]['p'], 4)}"
                
            else:
                tTestStr = "Error during calculation"
            self.tTestContentLabel.setText(tTestStr)
            self.plasticPresentContentLabel.setText(str(impedanceAnalysis.plasticPresent))

        else:
            self.ppmContentLabel.setText("")
            self.tTestContentLabel.setText("")
            self.plasticPresentContentLabel.setText("")
