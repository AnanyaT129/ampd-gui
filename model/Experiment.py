import datetime
import time
from time import sleep
import random
from gpiozero import MCP3008

class Experiment():
  def __init__(self):
    self.logs = []
    self.data = []
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