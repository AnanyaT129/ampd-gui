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
# from gpiozero import MCP3008, LED

class Experiment():
  def __init__(self):
    self.logs = []
    self.data = []
    self.frames = []
    self.cameraLength = 1
    self.length = 5
    self.cameraFps = 30
    self.enable = [True, True]

    self.date = datetime.datetime.now().strftime('%Y%m%d_%H%M')

    self.savePath = f"{self.date}_ampd_experiment_data"
    
    self.onOffPinLow = 23
    self.onOffPinHigh = 25
    
    #comment out if you want to run without pins connected
    # self.tdsLow = LED(self.onOffPinLow)
    # self.tdsHigh = LED(self.onOffPinHigh)
    
    os.makedirs(self.savePath, exist_ok=True)

  def addLog(self, newLog):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.logs.append(time + " " + newLog)
  
  def addDatapoint(self, lowHigh: bool):
    print("no pi")
    
    if not lowHigh:
      # get data from low pin
      sig = MCP3008(0)
      d = sig.value * 3300
    
    else:
      # get data from high pin
      sig = MCP3008(1)
      d = sig.value * 3300
    
    # print(d)
    return d
    # return 0

  def start_mock_data_collection(self):
    dLow = []
    dHigh = []

    for i in range(self.length * 10):
      dLow.append(random.randint(0, 3000))
      sleep(0.1)
    
    for i in range(self.length * 10):
      dHigh.append(random.randint(0, 3000))
      sleep(0.1)
    
    self.data.append((dLow, dHigh))
  
  def mock_camera_capture(self):
    mockFrames = []

    for i in range(self.cameraFps * self.cameraLength):
      mockFrames.append(np.random.randint(0, 256, size=(3840, 2160, 3), dtype=np.uint8))
    
    self.frames = mockFrames

    os.makedirs(f"{self.savePath}/frames", exist_ok=True)
    
    if len(self.frames) == 0 or (len(self.frames) != 0 and len(self.frames[-1]) == 0):
      print("NO FRAMES CAPTURED")
      return
    
    print(np.array(self.frames).shape)
    for i in range(len(self.frames)):
      r = cv2.imwrite(f"{self.savePath}/frames/{i}_of_{len(self.frames)}.png", np.array(self.frames[i], dtype=np.uint8))
      print(r)

    print(f"Saved frames to {self.savePath}/frames")
  
  def start_data_collection(self):
    dLow = []
    dHigh = []
    
    print(self.length)
    
    try:
      # get data from low pin
      print("low")
      self.tdsLow.on()
      sleep(1)
      
      end = time.time() + self.length
      print(end)
      while time.time() < end:
        print(time.time())
        print(len(dLow))
        dLow.append(self.addDatapoint(False))
        sleep(0.1)
      self.tdsLow.off()
      print("Done data collection")
      sleep(1)
      
      # get data from high pin
      print("high")
      
      self.tdsHigh.on()
      sleep(1)
      end = time.time() + self.length
      while time.time() < end:
        print(time.time())
        print(len(dHigh))
        dHigh.append(self.addDatapoint(True))
        sleep(0.1)
      sleep(1)
      self.tdsHigh.off()
    except Exception as e:
      print(e)
    finally:
      print("Low: ", dLow, "High: ", dHigh)
      self.data.append((dLow, dHigh))
  
  def camera_capture(self):
    camera_capture = CameraCapture(self.cameraFps)

    camera_capture.collect_data(self.cameraLength)

    self.frames = camera_capture.data
    
    os.makedirs(f"{self.savePath}/frames", exist_ok=True)
    
    if len(self.frames) == 0 or (len(self.frames) != 0 and len(self.frames[-1]) == 0):
      print("NO FRAMES CAPTURED")
      return
    
    print(np.array(self.frames).shape)
    for i in range(len(self.frames)):
      r = cv2.imwrite(f"{self.savePath}/frames/{i}_of_{len(self.frames)}.png", np.array(self.frames[i], dtype=np.uint8))
      print(r)

    print(f"Saved frames to {self.savePath}/frames")

  def clear(self):
    self.data = []
    self.frames = []

  def write(self):
    filename = Path(f'{self.savePath}/data.json')
    filename.touch(exist_ok=True)  # will create file, if it exists will do nothing

    with open(f'{self.savePath}/data.json', 'a') as f:
      dataDict = {
        "date": self.date,
        "metadata": {
          "experimentDuration": f"{self.length} s",
          "cameraFps": self.cameraFps,
          "cameraSnapshotLength": f"{self.cameraLength} s",
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
      return ([],[])
