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
    
    data = (dLow, dHigh)
  
  def camera_capture(self, length):
    camera_capture = CameraCapture()

    camera_capture.collect_data(length)

    self.frames = camera_capture.data
    
    if len(self.frames) == 0:
      print("NO FRAMES CAPTURED")
      return
    
    midFrame = len(self.frames) // 2
    
    cv2.imwrite("Sample_frame.png", np.array(self.frames[midFrame]))
    print(f"Saved frame {midFrame}")

  def clear(self):
    self.data = []
    self.frames = []
