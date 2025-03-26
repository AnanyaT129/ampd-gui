import datetime
from time import sleep
import random
import time
import cv2
import numpy as np
import json
from pathlib import Path
import os

from model.cameracapture import CameraCapture
# from gpiozero import MCP3008

class Experiment():
  def __init__(self):
    self.logs = []
    self.data = []
    self.frames = []
    self.snapshotLength = 1
    self.snapshotsPerMinute = 2
    self.length = 5
    self.cameraFps = 30

    date = datetime.datetime.now().strftime('%Y%m%d_%H:%M')

    self.savePath = f"{date}_ampd_experiment_data"

    # self.createDataFile(date)
    
    onOffPinLow = 24
    onOffPinHigh = 25
    # self.tdsLow = LED(onOffPinLow)
    # self.tdsHigh = LED(onOffPinHigh)
  
  def createDataFile(self, date):
    data = {
      "date": date,
      "metadata": {
        "snapshotLength": f"{self.snapshotLength} s",
        "snapshotsPerMinute": f"{self.snapshotsPerMinute}/min",
        "experimentDuration": f"{self.length} min",
        "cameraFps": self.cameraFps,
      }
    }

    os.makedirs(self.savePath, exist_ok=True)
    filename = Path(f'{self.savePath}/data.json')
    filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
 
    with open(filename, 'a+') as f:
      json.dump(data, f, ensure_ascii=False)

  def addLog(self, newLog):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.logs.append(time + " " + newLog)
  
  def addDatapoint(self, lowHigh: bool):
    print("no pi")
    
    # if not lowHigh:
    #   # get data from low pin
    #   sig = MCP3008(0)
    #   d = sig.value * 3300
    #   self.data.append(d)
    
    # else:
    #   # get data from high pin
    #   sig = MCP3008(1)
    #   d = sig.value * 3300
    #   self.data.append(d)
    
    # return d
    return 0

  def start_mock_data_collection(self, length):
    for i in range(length):
      self.addDatapoint(random.randint(0, 10))
      sleep(1)
  
  def start_data_collection(self, length):
    dLow = []
    dHigh = []
    
    end = time.time() + length
    
    # get data from low pin
    self.tdsLow.on()
    while time.time() < end:
      dLow.append(self.addDatapoint(False))
    self.tdsLow.off()
    
    # get data from high pin
    self.tdsHigh.on()
    while time.time() < end:
      dHigh.append(self.addDatapoint(True))
    self.tdsHigh.off()
    
    self.data.append((dLow, dHigh))
  
  def camera_capture(self, length):
    camera_capture = CameraCapture(self.cameraFps)

    camera_capture.collect_data(length)

    self.frames = camera_capture.data
    
    if len(self.frames) == 0:
      print("NO FRAMES CAPTURED")
      return
    
    for i in range(len(self.frames)):
      cv2.imwrite(f"{self.savePath}/frames/{i}/{len(self.frames)}.png", np.array(self.frames[i]))

    print(f"Saved frames to {self.savePath}/frames")

  def clear(self):
    self.data = []
    self.frames = []

  def write(self):
    with open(f'{self.savePath}/data.json', 'a') as f:
      dataDict = {"impedanceData": {
        "low": [],
        "high": []
      }}
      for i in range(len(self.data)):
        dataDict["impedanceData"]["low"].append(self.data[i][0])
        dataDict["impedanceData"]["high"].append(self.data[i][1])
    
    json.dump(dataDict, f, ensure_ascii=False)

def read_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data