from PyQt6.QtCore import Qt, QThread, pyqtSignal
import cv2
from time import sleep
import numpy as np
    
class CameraAnalysisThread(QThread):
    # Define signals to communicate with the main thread
    image_signal = pyqtSignal(np.ndarray)
    image_path_signal = pyqtSignal(str)

    def __init__(self, cameraAnalysis, images, action, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cameraAnalysis = cameraAnalysis
        self.images = images
        self.action = action  # The action to be performed (e.g., 'start_data_collection')
    
    def run(self):
        if self.action == 'start_camera_analysis':
            halfway_img = len(self.images) // 2
            for i in range(len(self.images)):
                iPath = self.images[i]
                image = cv2.imread(iPath, cv2.IMREAD_UNCHANGED)

                if image is None:
                    print(f"Error: Could not load image {iPath}.")
                    continue
                else:
                    #self.image_signal.emit(image)
                    self.image_path_signal.emit(iPath)

                    result = self.cameraAnalysis.add_image(image, iPath, save=(halfway_img==i))

                    self.image_signal.emit(result)
                
                sleep(1)
            
            self.cameraAnalysis.run_analysis()
