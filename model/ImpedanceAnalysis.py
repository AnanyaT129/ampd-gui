import statistics
import random
import math
import numpy as np
import os
from pathlib import Path
import json

class ImpedanceAnalysis:
    def __init__(self, date, low_data, high_data, numChunks = 10):
        self.date = date
        self.low = low_data
        self.high = high_data
        self.low_length = len(self.low)
        self.high_length = len(self.high)
        self.numChunks = numChunks
        self.avg_low_list = []
        self.avg_high_list = []
        self.imp_low_list = []
        self.imp_high_list = []
        self.cap_list = []
        self.fH = 2390 # high frequency probe
        self.fL = 250 # low frequency probe

    def run(self):
        self.chunk_avg()
        self.calc_imp()
        self.calc_cap()

    def chunk_avg(self):
        # chunks low frequency data into average bins
        low_chunk_size = self.low_length // self.numChunks
        for i in range(self.numChunks-1):
            self.avg_low_list.append(statistics.mean(self.low[i:i+low_chunk_size-1]))
        self.avg_low_list.append(statistics.mean(self.low[self.numChunks-1:]))

        # chunks high frequency data into average bins
        high_chunk_size = self.high_length // self.numChunks
        for i in range(self.numChunks - 1):
            self.avg_high_list.append(statistics.mean(self.high[i:i + high_chunk_size - 1]))
        self.avg_high_list.append(statistics.mean(self.high[self.numChunks - 1:]))

    def calc_imp(self):
        # saves the transimpedance amplifier resistance gain times the input voltage
        rf_vin = 5600*200

        # computes and saves impedances at the low frequency
        for i in range(self.numChunks):
            self.imp_low_list.append(rf_vin/self.avg_low_list[i])

        # computes and stores impedances at the high frequency
        for i in range(self.numChunks):
            self.imp_high_list.append(rf_vin/self.avg_high_list[i])

    def calc_cap(self):
        # saves a frequency ratio for future calculations
        fR = math.sqrt(self.fH**2-self.fL**2) / (2*math.pi*self.fH*self.fL)

        # computes and saves capacitances at each time chunk
        for i in range(self.numChunks):
            self.cap_list.append(fR / math.sqrt(abs(self.imp_low_list[i]**2 - self.imp_high_list[i]**2)))
    
    def write(self, savePath):
        os.makedirs(savePath, exist_ok=True)
        filename = Path(f'{savePath}/impedanceAnalysis.json')
        filename.touch(exist_ok=True)  # will create file, if it exists will do nothing

        with open(f'{savePath}/impedanceAnalysis.json', 'a') as f:
            dataDict = {
                "date": self.date,
                "metadata": {
                    "numChunks": self.numChunks,
                },
                "analysisResults": {
                    "imp_low": self.imp_low_list,
                    "imp_high": self.imp_high_list,
                    "capacitance": self.cap_list
                }
            }
        
            json.dump(dataDict, f, ensure_ascii=False, indent=4)
            f.write("\n")
    
    def lagrange_interpolation(data, x):
        """
        Perform lagrange interpolation on a given set of points.
        :param data: Dictionary where keys are x-values and values are y-values.
        :param x: The x-value to interpolate.
        :return: Interpolated y-value.
        """
        x_vals = np.array(list(data.keys()))
        y_vals = np.array(list(data.values()))
        
        n = len(x_vals)
        L_x = np.ones(n)
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    L_x[i] *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])
        
        y_interp = np.dot(L_x, y_vals)
        return y_interp

def generateRandomVal(base):
    noise = random.random() * 40
    if random.random() < 0.5:
        return base - noise
    else:
        return base + noise

# data = [generateRandomVal(200) for i in range(5000)] + [generateRandomVal(300) for i in range(5000)]
# print(len(data))

# ia = ImpedanceAnalysis(data, 10)
# ia.run()