from PyQt6.QtWidgets import (QWidget,
                             QPushButton, 
                             QVBoxLayout,
                             QMessageBox)

class ImpedanceAnalysisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Impedance Analysis")
        layout = QVBoxLayout()
        layout.addWidget(QPushButton("Save and Close", clicked=self.save_and_close))
        self.setLayout(layout)
    
    def save_and_close(self):
        if self.stopConfirmation():
            print("saved!")
            self.close
        else:
            self.close

    def stopConfirmation(self):
        reply = QMessageBox.question(self, 'Save Analysis',
                                    "Do you want to save before closing?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
    
        return reply