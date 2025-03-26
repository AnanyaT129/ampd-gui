import random

class RealTimeAnalysis:
  def __init__(self, data):
    self.low = data[0]
    self.high = data[1]
    self.low_threshold = 240 # experimentally determine a good value
    self.high_threshold = 250  # experimentally determine a good value
    self.significant = 50 # can tweak this
    self.point = (-1, 0)

  def checkThreshold(self):
    return (self.checkArray(self.low, self.threshold) and 
            self.checkArray(self.high, self.threshold))
  
  def checkArray(self, data, threshold) -> bool:
    num_sig = 0
    for d in data:
      if d > threshold:
        num_sig = num_sig + 1
    return num_sig >= self.significant
  
  def checkThresholdMock(self):
    r = random.random()
    location = random.randint(1, len(self.low))
    self.point = (location, self.low_threshold)
    #return r > 0.5
    return True
