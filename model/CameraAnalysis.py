from pathlib import Path
import cv2
import numpy as np
import os
import json

class CameraAnalysis:
    def __init__(self, fps = 30, duration = 1):
        self.fps = fps
        self.duration = duration

        self.scattered_light = []
        self.imgs = []

        self.average_scattered_light = 0
        self.plasticPresent = False
        self.estimatedPlasticContent = 500
        self.img_to_save = None

    def add_image(self, image, path_to_img, save=False):
        self.imgs.append(path_to_img)

        # Define the center and radius for the blue circle
        center = (image.shape[1] // 2, image.shape[0] // 2)  # Center of the image
        radius = 50  # Radius of the circle

        # Define the color blue in BGR (OpenCV uses BGR, not RGB)
        blue_color = (255, 0, 0)

        # Draw the circle on the image
        cv2.circle(image, center, radius, blue_color, -1)  # -1 thickness fills the circle

        self.scattered_light.append(np.random.randint(0, 10))

        if save:
            self.img_to_save = image

        return image

    def run_analysis(self):
        self.average_scattered_light = np.average(self.scattered_light)
    
    def write(self, savePath):
        os.makedirs(savePath, exist_ok=True)
        filename = Path(f'{savePath}/cameraAnalysis.json')
        filename.touch(exist_ok=True)  # will create file, if it exists will do nothing

        with open(f'{savePath}/cameraAnalysis.json', 'a') as f:
            dataDict = {
                "metadata": {
                    "fps": self.fps,
                    "duration": self.duration,
                },
                "analysisResults": {
                    "scatteredLight": self.scattered_light,
                    "imgPaths": self.imgs,
                    "averageScatteredLight": self.average_scattered_light,
                    "estPlasticContent": self.estimatedPlasticContent,
                    "plasticPresent": str(self.plasticPresent),
                }
            }
        
            json.dump(dataDict, f, ensure_ascii=False, indent=4)
            f.write("\n")
