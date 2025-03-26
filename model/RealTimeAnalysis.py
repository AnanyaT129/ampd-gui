class RealTimeAnalysis:
  def __init__(self, data):
    self.low = data[0]
    self.high = data[1]
    self.low_threshold = 240 # experimentally determine a good value
    self.high_threshold = 250  # experimentally determine a good value
    self.significant = 50 # can tweak this

  def checkThreshold(self):
    # counts the number of low frequency readings over the low threshold
    num_sig_low = 0
    for d in self.low:
      if d > self.low_threshold:
        num_sig_low = num_sig_low + 1

    # counts the number of high frequency readings over the high threshold
    num_sig_high = 0
    for d in self.high:
      if d > self.high_threshold:
        num_sig_high = num_sig_high + 1

    if num_sig_low+num_sig_high >= self.significant:
      return True
    else:
      return False