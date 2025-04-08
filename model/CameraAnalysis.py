import math
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
        self.estParticles = []

        self.average_scattered_light = 0
        self.plasticPresent = False
        self.img_to_save = None

    def add_image(self, image, path_to_img, save=False):
        self.imgs.append(path_to_img)

        #image = self.detect_scattering(image)
        image = self.mock_detect_scattering(image)

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
                    "estParticles": self.estParticles,
                    "averageScatteredLight": self.average_scattered_light,
                    "plasticPresent": str(self.plasticPresent),
                    "imgToSave": str(self.img_to_save)
                }
            }
        
            json.dump(dataDict, f, ensure_ascii=False, indent=4)
            f.write("\n")
    
    def detect_scattering(self, img, calibration_image_path=None):
        if calibration_image_path:
            calibration_image = cv2.imread(calibration_image_path)
            _, calibration_red_area, _ = self.count_red_area(calibration_image, 0, math.inf)
        else:
            calibration_red_area = 50 # assumed noise threshold
        
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        particle_count, total_area, img_with_contours = self.count_red_area(hsv_image, )

        total_area -= calibration_red_area

        self.scattered_light.append(total_area)
        self.estParticles.append(particle_count)

        self.img_to_save = self.imgs[self.scattered_light.index(max(self.scattered_light))]

        return img_with_contours

    def mock_detect_scattering(self, image):
        # Define the center and radius for the blue circle
        center = (image.shape[1] // 2, image.shape[0] // 2)  # Center of the image
        radius = 50  # Radius of the circle

        # Define the color blue in BGR (OpenCV uses BGR, not RGB)
        blue_color = (255, 0, 0)

        # Draw the circle on the image
        cv2.circle(image, center, radius, blue_color, -1)  # -1 thickness fills the circle

        self.scattered_light.append(np.random.randint(0, 10))
        self.estParticles.append(np.random.randint(0, 10))

        self.img_to_save = self.imgs[self.scattered_light.index(max(self.scattered_light))]

        return image
    
    def count_red_area(self, img, min_blob_size=500, max_blob_size=5000):
        lower_red1 = np.array([0, 120, 70])   # Lower red bound
        upper_red1 = np.array([10, 255, 255]) # Upper red bound
        lower_red2 = np.array([170, 120, 70]) # Lower red bound (second range for red)
        upper_red2 = np.array([180, 255, 255])# Upper red bound (second range for red)

        mask1 = cv2.inRange(img, lower_red1, upper_red1)
        mask2 = cv2.inRange(img, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        particle_count = 0
        total_area = 0

        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_blob_size or area > max_blob_size:
                continue
            
            particle_count += 1
            total_area += area

            cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
    
        return particle_count, total_area, img