import datetime
from time import sleep
import random
import time
import cv2
import numpy as np
import json
from pathlib import Path
import os

from model.RealTimeAnalysis import RealTimeAnalysis
from model.cameracapture import CameraCapture
from gpiozero import MCP3008

class Experiment():
  def __init__(self):
    self.logs = []
    self.data = []
    self.frames = []
    self.thresholds = []
    self.snapshotLength = 1
    self.snapshotsPerMinute = 2
    self.length = 5
    self.cameraFps = 30

    self.date = datetime.datetime.now().strftime('%Y%m%d_%H:%M')

    self.savePath = f"{self.date}_ampd_experiment_data"
    
    onOffPinLow = 24
    onOffPinHigh = 25
    self.tdsLow = LED(onOffPinLow)
    self.tdsHigh = LED(onOffPinHigh)

  def addLog(self, newLog):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.logs.append(time + " " + newLog)
  
  def addDatapoint(self, lowHigh: bool):
    # print("no pi")
    
    if not lowHigh:
      # get data from low pin
      sig = MCP3008(0)
      d = sig.value * 3300
      self.data.append(d)
    
    else:
      # get data from high pin
      sig = MCP3008(1)
      d = sig.value * 3300
      self.data.append(d)
    
    return d
    # return 0

  def start_mock_data_collection(self, length):
    dLow = []
    dHigh = []

    for i in range(length * 10):
      dLow.append(random.randint(0, 3000))
      sleep(0.1)
    
    for i in range(length * 10):
      dHigh.append(random.randint(0, 3000))
      sleep(0.1)
    
    self.data.append((dLow, dHigh))
  
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

    self.frames.append(camera_capture.data)
    
    if len(self.frames) == 0 or (len(self.frames) != 0 and len(self.frames[-1]) == 0):
      print("NO FRAMES CAPTURED")
      return
    
    most_recent_frames = self.frames[-1]
    for i in range(len(most_recent_frames)):
      cv2.imwrite(f"{self.savePath}/frames/{len(self.frames)}/{i}.png", np.array(most_recent_frames))

    print(f"Saved frames to {self.savePath}/frames")

  def clear(self):
    self.data = []
    self.frames = []

  def write(self):
    os.makedirs(self.savePath, exist_ok=True)
    filename = Path(f'{self.savePath}/data.json')
    filename.touch(exist_ok=True)  # will create file, if it exists will do nothing

    with open(f'{self.savePath}/data.json', 'a') as f:
      dataDict = {
        "date": self.date,
        "metadata": {
          "snapshotLength": f"{self.snapshotLength} s",
          "snapshotsPerMinute": f"{self.snapshotsPerMinute}/min",
          "experimentDuration": f"{self.length} min",
          "cameraFps": self.cameraFps,
        },
        "impedanceData": {
          "low": [],
          "high": []
        }
      }

      for i in range(len(self.data)):
        dataDict["impedanceData"]["low"].append(self.data[i][0])
        dataDict["impedanceData"]["high"].append(self.data[i][1])
    
      json.dump(dataDict, f, ensure_ascii=False, indent=4)
      f.write("\n")
  
  def getLatestData(self):
    if self.data != []:
      return self.data[-1]
    else:
      return [[],[]]
  
  def checkThreshold(self):
    realTimeAnalysis = RealTimeAnalysis(self.getLatestData())
    threshold = realTimeAnalysis.checkThreshold()
    
    self.thresholds.append({threshold: realTimeAnalysis.point})

    return threshold
  
  def fetchLatestThreshold(self):
    if self.thresholds != []:
      (k, v), = self.thresholds[-1].items()
      if k:
        return v
    else:
      return None