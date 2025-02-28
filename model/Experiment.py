import datetime


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