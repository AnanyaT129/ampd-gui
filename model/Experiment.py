import datetime
from time import sleep
import random
import time
import cv2
import numpy as np

from model.cameracapture import CameraCapture
from gpiozero import MCP3008

class Experiment():
  def __init__(self):
    self.logs = []
    self.data = []
    self.frames = []
    self.length = 5
  
  def addLog(self, newLog):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.logs.append(time + " " + newLog)
  
  def addDatapoint(self, datapoint):
    self.data.append(datapoint)

  def start_mock_data_collection(self, length):
    for i in range(length):
      self.addDatapoint(random.randint(0, 10))
      sleep(1)
  
  def start_data_collection(self, length=5):
    sig = MCP3008(0)
    
    end = time.time() + length
    
    while time.time() < end:
      d = sig.value * 3300
      self.addDatapoint(d)
  
  def camera_capture(self, length):
    camera_capture = CameraCapture()

    camera_capture.collect_data(length)

    self.frames = camera_capture.data
    
    if len(self.frames) == 0:
      print("ALKSJKLAJSKALJSALKJSA NO FRAMES CAPTURED")
      return
    
    midFrame = len(self.frames) // 2
    
    print("Shape: ", np.array(self.frames[midFrame]).shape)
    print("Type: ", np.array(self.frames[midFrame]).dtype)
    
    cv2.imwrite("Sample_frame.png", np.array(self.frames[midFrame]))
    print(f"Saved frame {midFrame}")

  def clear(self):
    self.data = []
