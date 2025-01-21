from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QLabel
)
import datetime

class Logs(QScrollArea):

    def __init__(self, *args, **kwargs):
        self.logs = []

        QScrollArea.__init__(self, *args, **kwargs)

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        # creating label
        self.label = QLabel(content)

        # setting alignment to the text
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # making label multi-line
        self.label.setWordWrap(True)

        # adding label to the layout
        lay.addWidget(self.label)

    # the setText method
    def setText(self):
        # setting text to the label
        text = "\n".join(self.logs)
        self.label.setText(text)
    
    def appendLog(self, newLog):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logs.append(time + " " + newLog)
        self.setText()
