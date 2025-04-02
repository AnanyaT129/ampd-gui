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
        metadataTitle.setStyleSheet("color: black; font-weight: bold")

        ppmLowLayout = QHBoxLayout()
        ppmLowTitleLabel = QLabel("PPM from Low Freq.: ")
        ppmLowTitleLabel.setStyleSheet("color: black; font-weight: bold")
        self.ppmLowContentLabel = QLabel("")

        ppmLowLayout.addWidget(ppmLowTitleLabel)
        ppmLowLayout.addWidget(self.ppmLowContentLabel)

        ppmHighLayout = QHBoxLayout()
        ppmHighTitleLabel = QLabel("PPM from High Freq.: ")
        ppmHighTitleLabel.setStyleSheet("color: black; font-weight: bold")
        self.ppmHighContentLabel = QLabel("")

        ppmHighLayout.addWidget(ppmHighTitleLabel)
        ppmHighLayout.addWidget(self.ppmHighContentLabel)

        estContentLayout = QHBoxLayout()
        estContentTitleLabel = QLabel("Estimated Microplastic Content: ")
        estContentTitleLabel.setStyleSheet("color: black; font-weight: bold")
        self.estContentContentLabel = QLabel("")

        estContentLayout.addWidget(estContentTitleLabel)
        estContentLayout.addWidget(self.estContentContentLabel)

        tTesttLayout = QVBoxLayout()
        tTestTitleLabel = QLabel("T Test against Water Control: ")
        tTestTitleLabel.setStyleSheet("color: black; font-weight: bold")
        self.tTestContentLabel = QLabel("")

        tTesttLayout.addWidget(tTestTitleLabel)
        tTesttLayout.addWidget(self.tTestContentLabel)

        # results labels
        resultsTitle = QLabel("Results")
        resultsTitle.setStyleSheet("color: black; font-weight: bold")

        self.layout = QVBoxLayout()
        self.layout.addWidget(metadataTitle)
        self.layout.addLayout(ppmLowLayout)
        self.layout.addLayout(ppmHighLayout)
        self.layout.addLayout(tTesttLayout)
        self.layout.addLayout(estContentLayout)

        self.setLayout(self.layout)

        # self.addWidget(resultsTitle)
    
    def refresh(self, impedanceAnalysis: ImpedanceAnalysis):
        if impedanceAnalysis is not None:
            self.ppmLowContentLabel.setText(str(impedanceAnalysis.ppmLow))
            self.ppmHighContentLabel.setText(str(impedanceAnalysis.ppmHigh))
            self.estContentContentLabel.setText(str(impedanceAnalysis.estimatedPlasticContent))
            if impedanceAnalysis.ttestResults is not None:
                tTestStr = f"Low: t={round(impedanceAnalysis.ttestResults[0]["t"], 4)} p={round(impedanceAnalysis.ttestResults[0]["p"], 4)}, High: t={round(impedanceAnalysis.ttestResults[1]["t"], 4)} p={round(impedanceAnalysis.ttestResults[1]["p"], 4)}"
                
            else:
                tTestStr = "Error during calculation"
            self.tTestContentLabel.setText(tTestStr)

        else:
            self.ppmLowContentLabel.setText("")
            self.ppmHighContentLabel.setText("")
            self.estContentContentLabel.setText("")
            self.tTestContentLabel.setText("")