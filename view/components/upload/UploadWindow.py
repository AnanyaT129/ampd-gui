from PyQt6.QtWidgets import (QWidget,
                             QPushButton,
                             QVBoxLayout,
                             QFileDialog,
                             QLabel,
                             QFormLayout,
                             QLineEdit,
                             QHBoxLayout)
from PyQt6.QtCore import Qt

import json
import re

from view.components.upload.UploadThread import UploadStatus, UploadThread
    
class UploadWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.data = {}
        self.impedanceAnalysisData = {}
        self.cameraAnalysisData = {}

        self.username = ""
        self.password = ""

        self.status = UploadStatus.WAITING_FOR_DATA

        self.setWindowTitle("Upload Experiment Results")

        self.title = "AMPD Experiment"
        self.titleFormWidget = QFormLayout()
        self.titleWidget = QLineEdit()
        self.titleWidget.setText(self.title)
        self.titleWidget.textChanged.connect(self.titleChanged)
        self.titleFormWidget.addRow("Title: ", self.titleWidget)

        self.uploadThread = UploadThread(self.username, self.password, {}, self.title, 'upload')

        self.uploadDataButton = QPushButton("Upload Data", clicked=self.uploadData)
        self.uploadDataPathLabel = QLabel("Data from: ")

        self.uploadImpedanceAnalysis = QPushButton("Upload Impedance Analysis", clicked=self.uploadImpedance)
        self.uploadImpedanceDataPathLabel = QLabel("Data from: ")

        self.uploadCameraAnalysis = QPushButton("Upload Camera Analysis", clicked=self.uploadCamera)
        self.uploadCameraDataPathLabel = QLabel("Data from: ")

        ampdAccountLabel = QLabel("AMP'D Account Information")
        ampdAccountLabel.setStyleSheet("font-weight: bold")

        self.variablesFormWidget = QFormLayout()
        self.usernameWidget = QLineEdit()
        self.usernameWidget.textChanged.connect(self.usernameChanged)

        self.passwordWidget = QLineEdit()
        self.passwordWidget.textChanged.connect(self.passwordChanged)

        self.variablesFormWidget.addRow("Email: ", self.usernameWidget)
        self.variablesFormWidget.addRow("Password: ", self.passwordWidget)

        self.uploadButton = QPushButton("Upload", clicked=self.upload)
        self.uploadButton.setEnabled(False)

        labelConnect = QLabel("Device Status")
        labelConnect.setStyleSheet("font-weight: bold")

        self.labelStatus = QLabel(self.status.value)

        statusLayout = QHBoxLayout()
        statusLayout.addWidget(labelConnect)
        statusLayout.addWidget(self.labelStatus)

        layout = QVBoxLayout()
        layout.addLayout(self.titleFormWidget)
        layout.addWidget(self.uploadDataButton)
        layout.addWidget(self.uploadDataPathLabel)
        layout.addWidget(self.uploadImpedanceAnalysis)
        layout.addWidget(self.uploadImpedanceDataPathLabel)
        layout.addWidget(self.uploadCameraAnalysis)
        layout.addWidget(self.uploadCameraDataPathLabel)
        layout.addWidget(ampdAccountLabel)
        layout.addLayout(self.variablesFormWidget)
        layout.addWidget(self.uploadButton)
        layout.addLayout(statusLayout)

        self.setLayout(layout)
    
    def uploadData(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # Allow selecting only existing files
        file_dialog.setNameFilter("JSON Files (*.json)")
        if file_dialog.exec():  # If the dialog is accepted
            file_path = file_dialog.selectedFiles()[0]
        
            with open(file_path, 'r') as file:
                self.data = json.load(file)
            
            self.uploadDataPathLabel.setText(f"Data from: {(('...' + file_path[-47:]) if len(file_path) > 47 else file_path)}")
            self.titleWidget.setText(''.join(file_path.split('/')[-2]))
        
        if self.checkReady():
            self.change_status(UploadStatus.READY)
        else:
            self.change_status(UploadStatus.WAITING_FOR_DATA)
    
    def uploadImpedance(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # Allow selecting only existing files
        file_dialog.setNameFilter("JSON Files (*.json)")
        if file_dialog.exec():  # If the dialog is accepted
            file_path = file_dialog.selectedFiles()[0]
        
            with open(file_path, 'r') as file:
                self.impedanceAnalysisData = json.load(file)
            
            self.uploadImpedanceDataPathLabel.setText(f"Data from: {(('...' + file_path[-47:]) if len(file_path) > 47 else file_path)}")
        
        if self.checkReady():
            self.change_status(UploadStatus.READY)
        else:
            self.change_status(UploadStatus.WAITING_FOR_DATA)
    
    def uploadCamera(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # Allow selecting only existing files
        file_dialog.setNameFilter("JSON Files (*.json)")
        if file_dialog.exec():  # If the dialog is accepted
            file_path = file_dialog.selectedFiles()[0]
        
            with open(file_path, 'r') as file:
                self.cameraAnalysisData = json.load(file)
            
            self.uploadCameraDataPathLabel.setText(f"Data from: {(('...' + file_path[-47:]) if len(file_path) > 47 else file_path)}")
        
        if self.checkReady():
            self.change_status(UploadStatus.READY)
        else:
            self.change_status(UploadStatus.WAITING_FOR_DATA)
    
    def is_valid_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None
    
    def checkReady(self):
        return (self.data != {} and 
                self.impedanceAnalysisData != {} and
                self.cameraAnalysisData != {} and
                self.is_valid_email(self.username) and
                len(self.password) >= 6)
    
    def usernameChanged(self):
        self.username = self.usernameWidget.text()

        if self.checkReady():
            self.change_status(UploadStatus.READY)
        else:
            self.change_status(UploadStatus.WAITING_FOR_DATA)
    
    def passwordChanged(self):
        self.password = self.passwordWidget.text()

        if self.checkReady():
            self.change_status(UploadStatus.READY)
        else:
            self.change_status(UploadStatus.WAITING_FOR_DATA)

    def titleChanged(self):
        self.title = self.titleWidget.text()
    
    def upload(self):
        data = self.data
        data["impedanceAnalysis"] = self.impedanceAnalysisData
        data["cameraAnalysis"] = self.cameraAnalysisData

        self.uploadThread.username = self.username
        self.uploadThread.password = self.password
        self.uploadThread.title = self.title
        self.uploadThread.data = data
        self.uploadThread.change_status_signal.connect(self.change_status)

        self.uploadThread.start()
    
    def change_status(self, status: UploadStatus):
        self.labelStatus.setText(status.value)
        match status:
            case UploadStatus.WAITING_FOR_DATA:
                self.uploadButton.setEnabled(False)
                self.uploadButton.setText("Upload")
            case UploadStatus.READY:
                self.uploadButton.setEnabled(True)
                self.uploadButton.setText("Upload")
            case UploadStatus.AUTH_ERROR:
                self.uploadButton.setEnabled(True)
                self.uploadButton.setText("Upload")
            case UploadStatus.UPLOAD_ERROR:
                self.uploadButton.setEnabled(True)
                self.uploadButton.setText("Upload")
            case UploadStatus.AUTHENTICATING:
                self.uploadButton.setEnabled(False)
                self.uploadButton.setText("Uploading...")
            case UploadStatus.UPLOADING:
                self.uploadButton.setEnabled(False)
                self.uploadButton.setText("Uploading...")
            case UploadStatus.COMPLETE:
                self.uploadButton.setEnabled(False)
                self.uploadButton.setText("Uploaded")


