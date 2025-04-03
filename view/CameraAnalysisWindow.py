from PyQt6.QtWidgets import (QWidget,
                             QPushButton, 
                             QVBoxLayout,
                             QHBoxLayout,
                             QMessageBox,
                             QFileDialog,
                             QLabel)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

import os
import cv2

from view.components.CameraAnalysisResults import CameraAnalysisResults
from view.components.CameraAnalysisThread import CameraAnalysisThread

class CameraAnalysisWindow(QWidget):
    def __init__(self, cameraAnalysis):
        super().__init__()

        self.setWindowTitle("Camera Analysis")
        self.setGeometry(100, 100, 800, 600)

        self.images = []
        self.cameraAnalysis = cameraAnalysis
        self.savePath = ""

        self.uploadButton = QPushButton("Upload Images", clicked=self.uploadImages)
        self.labelDataFile = QLabel("Data from: ")

        metadataTitle = QLabel("Metadata")
        metadataTitle.setStyleSheet("font-weight: bold")

        fpsLayout = QHBoxLayout()
        fpsTitleLabel = QLabel("FPS: ")
        fpsTitleLabel.setStyleSheet("font-weight: bold")
        self.fpsContentLabel = QLabel(str(self.cameraAnalysis.fps))

        fpsLayout.addWidget(fpsTitleLabel)
        fpsLayout.addWidget(self.fpsContentLabel)

        self.runButton = QPushButton("Run Analysis", clicked=self.run)
        self.runButton.setEnabled(False)

        self.resultsWidget = CameraAnalysisResults()

        uploadLayout = QVBoxLayout()
        uploadLayout.addWidget(self.uploadButton)
        uploadLayout.addWidget(self.labelDataFile)
        uploadLayout.addWidget(metadataTitle)
        uploadLayout.addLayout(fpsLayout)
        uploadLayout.addWidget(self.runButton)
        uploadLayout.addWidget(self.resultsWidget)

        imageLayout = QVBoxLayout()

        self.image_title = QLabel("Image: ")
        self.image_label = QLabel(self)

        imageLayout.addWidget(self.image_title)
        imageLayout.addWidget(self.image_label)

        hlayout = QHBoxLayout()
        hlayout.addLayout(uploadLayout)
        hlayout.addLayout(imageLayout)

        self.closeButton = QPushButton("Save and Close", clicked=self.save_and_close, enabled=False)

        layout = QVBoxLayout()
        layout.addLayout(hlayout)
        layout.addWidget(self.closeButton)
        self.setLayout(layout)

        self.cameraAnalysisThread = CameraAnalysisThread(self.cameraAnalysis, self.images, 'start_camera_analysis')

    def uploadImages(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.FileMode.Directory)  # Allow selecting directories only
        folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)  # Ensure only directories are shown
        if folder_dialog.exec():  # If the dialog is accepted
            folder_path = folder_dialog.selectedFiles()[0]
            png_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(".png")]
            self.images = png_files

            self.savePath = folder_path
        
            self.labelDataFile.setText(f"Data from: {(('...' + folder_path[-47:]) if len(folder_path) > 47 else folder_path)}")
            self.runButton.setEnabled(True)
    
    def resize_image(self, opencv_image, max_width, max_height):
        """Resize the image to fit within the max_width and max_height while maintaining aspect ratio."""
        height, width = opencv_image.shape[:2]

        # Calculate the scaling factor
        scale_factor = min(max_width / width, max_height / height)

        # If the image is larger than the max dimensions, resize it
        if scale_factor < 1:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            opencv_image = cv2.resize(opencv_image, (new_width, new_height))

        return opencv_image
    
    def load_cv2_image(self, image):
        image = self.resize_image(image, max_width=800, max_height=600)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        q_image = QImage(rgb_image.data, width, height, rgb_image.strides[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def update_image_title(self, path):
        self.image_title.setText(f"Image: {(('...' + path[-47:]) if len(path) > 47 else path)}")
    
    def run(self):
        self.images.sort()
        self.cameraAnalysisThread.images = self.images

        self.cameraAnalysisThread.image_signal.connect(self.load_cv2_image)
        self.cameraAnalysisThread.image_path_signal.connect(self.update_image_title)

        self.runButton.setEnabled(False)
        self.cameraAnalysisThread.start()

        self.cameraAnalysisThread.finished.connect(self.refreshResults)
    
    def refreshResults(self):
        self.resultsWidget.refresh(self.cameraAnalysis)
        self.closeButton.setEnabled(True)
    
    def save_and_close(self):
        if self.stopConfirmation() and self.cameraAnalysis is not None:
            self.cameraAnalysis.write(self.savePath)
            self.close()
        else:
            self.close()

    def stopConfirmation(self):
        reply = QMessageBox.question(self, 'Save Analysis',
                                    "Do you want to save before closing?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
    
        return reply