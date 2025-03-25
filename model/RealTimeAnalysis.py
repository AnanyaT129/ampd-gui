class RealTimeAnalysis:
  def __init__(self, data):
    self.low = data[0]
    self.high = data[1]
    self.threshold = 275 # experimentally determine a good value
    self.significant = 50 # can tweak this

  def checkThreshold(self):
    num_sig = 0
    for d in self.data:
      if d > self.threshold:
        num_sig = num_sig + 1
    if num_sig >= self.significant:
      return True
    else:
      return False