from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from model.ImpedanceAnalysis import ImpedanceAnalysis

class ImpedanceAnalysisMetadata(QWidget):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        # meta data labels
        metadataTitle = QLabel("Metadata")
        metadataTitle.setStyleSheet("font-weight: bold")

        dateLayout = QHBoxLayout()
        dateTitleLabel = QLabel("Date: ")
        dateTitleLabel.setStyleSheet("font-weight: bold")
        self.dateContentLabel = QLabel("")

        dateLayout.addWidget(dateTitleLabel)
        dateLayout.addWidget(self.dateContentLabel)

        chunksLayout = QHBoxLayout()
        chunksTitleLabel = QLabel("Number of Data Chunks: ")
        chunksTitleLabel.setStyleSheet("font-weight: bold")
        self.chunksContentLabel = QLabel("")

        chunksLayout.addWidget(chunksTitleLabel)
        chunksLayout.addWidget(self.chunksContentLabel)

        numLowDataLayout = QHBoxLayout()
        numLowDataTitleLabel = QLabel("# Low Freq. Datapoints: ")
        numLowDataTitleLabel.setStyleSheet("font-weight: bold")
        self.numLowDataContentLabel = QLabel("")

        numLowDataLayout.addWidget(numLowDataTitleLabel)
        numLowDataLayout.addWidget(self.numLowDataContentLabel)

        numHighDataLayout = QHBoxLayout()
        numHighDataTitleLabel = QLabel("# High Freq. Datapoints: ")
        numHighDataTitleLabel.setStyleSheet("font-weight: bold")
        self.numHighDataContentLabel = QLabel("")

        numHighDataLayout.addWidget(numHighDataTitleLabel)
        numHighDataLayout.addWidget(self.numHighDataContentLabel)

        self.layout = QVBoxLayout()
        self.layout.addWidget(metadataTitle)
        self.layout.addLayout(dateLayout)
        self.layout.addLayout(chunksLayout)
        self.layout.addLayout(numLowDataLayout)
        self.layout.addLayout(numHighDataLayout)

        self.setLayout(self.layout)
    
    def refresh(self, impedanceAnalysis: ImpedanceAnalysis):
        if impedanceAnalysis is not None:
            self.dateContentLabel.setText(impedanceAnalysis.date)
            self.chunksContentLabel.setText(str(impedanceAnalysis.numChunks))
            self.numLowDataContentLabel.setText(str(len(impedanceAnalysis.low)))
            self.numHighDataContentLabel.setText(str(len(impedanceAnalysis.high)))