import statistics
import random
import math
import numpy as np
import os
from pathlib import Path
import json
from scipy import stats
from model.constants.AnalysisConstants import HIGH_FREQUENCY, LOW_FREQUENCY

class ImpedanceAnalysis:
    def __init__(self, date, low_data, high_data, numChunks = 10, water_path = "model/water_data.json"):
        self.date = date
        self.low = low_data
        self.high = high_data
        self.numChunks = numChunks

        self.water_path = water_path
        self.water_imp_low = []
        self.water_imp_high = []
        self.k_list = []
        self.water_cap = []

        self.imp_low_list = []
        self.imp_high_list = []
        self.cap_list = []
        self.res_list = []
        self.ppm = 0
        self.estimatedPlasticContent = 500
        self.plasticPresent = False
        self.ttestResults = None

    def run(self):
        # chunks low frequency data into average bins
        avg_low_list = self.chunk_avg(self.low)

        # chunks high frequency data into average bins
        avg_high_list = self.chunk_avg(self.high)

        # computes and saves impedances for low frequency average
        self.imp_low_list = self.calc_imp(avg_low_list)

        # computes and saves impedances for high frequency average
        self.imp_high_list = self.calc_imp(avg_high_list)

        # computes constant K
        self.k_list = self.calc_k(self.imp_low_list, self.imp_high_list)

        # calculate resistance
        self.res_list = self.calc_res(self.imp_high_list, self.k_list)

        # calculate capacitance
        self.cap_list = self.calc_cap(self.k_list, self.res_list)

        # calculate ppm
        self.ppm = self.calc_ppm(self.high)
        
        # run t test on the raw data
        self.run_ttest()

    def chunk_avg(self, arr):
        avg_arr = []
        low_chunk_size = len(arr) // self.numChunks
        for i in range(self.numChunks-1):
            avg_arr.append(statistics.mean(arr[i:i+low_chunk_size-1]))
        avg_arr.append(statistics.mean(arr[self.numChunks-1:]))

        return avg_arr

    def calc_imp(self, arr):
        # saves the transimpedance amplifier resistance gain times the input voltage
        rf_vin = 5600*200

        # computes and saves impedances
        imp_arr = []
        for i in range(len(arr)):
            imp_arr.append(rf_vin/arr[i])
        
        return imp_arr

    def calc_k(self, imp_low, imp_high):
        k_arr = []
        for i in range(self.numChunks):
            k_arr.append((abs(imp_low[i]*imp_low[i] - imp_high[i]*imp_high[i])) / \
                         (2*math.pi*math.sqrt(abs(imp_high[i]*imp_high[i]*HIGH_FREQUENCY*HIGH_FREQUENCY \
                                              - imp_low[i]*imp_low[i]*LOW_FREQUENCY*LOW_FREQUENCY))))

        return k_arr

    def calc_res(self, imp_high, k):
        # computes and saves resistances at each time chunk
        res_arr = []
        for i in range(self.numChunks):
            res_arr.append(imp_high[i]*math.sqrt(1+4*math.pi*math.pi*HIGH_FREQUENCY*HIGH_FREQUENCY*k[i]))

        return res_arr

    def calc_cap(self, k, res):
        # computes and saves capacitances at each time chunk
        cap_arr = []
        for i in range(self.numChunks):
            cap_arr.append(math.sqrt(k[i]) / res[i])
        
        return cap_arr

    def calc_ppm(self, high):
        avgV = statistics.mean(high)
        ppm = 0.4166*avgV

        return ppm

    def get_water_data(self):
        with open(self.water_path, 'r') as file:
            data = json.load(file)

            impedance_data = data.get("impedanceData", {})

            water_low = self.calc_imp(impedance_data.get("low", []))
            water_high = self.calc_imp(impedance_data.get("high", []))

        avg_low_list = self.chunk_avg(water_low)
        avg_high_list = self.chunk_avg(water_high)

        self.water_imp_low = self.calc_imp(avg_low_list)
        self.water_imp_high = self.calc_imp(avg_high_list)
        self.water_cap = self.calc_cap(self.water_imp_low, self.water_imp_high)

        return [water_low, water_high]

    def run_ttest(self, alpha = 0.05):
        water_low, water_high = self.get_water_data()
        
        sample_low = self.calc_imp(self.low)
        sample_high = self.calc_imp(self.high)

        # step 1: check that data is normal
        # _, p_1 = stats.shapiro(water_low)
        # _, p_2 = stats.shapiro(water_high)
        # _, p_3 = stats.shapiro(sample_low)
        # _, p_4 = stats.shapiro(sample_high)

        # if not ((p_1 < 0.05) and (p_2 < 0.05) and (p_3 < 0.05) and (p_4 < 0.05)):
        #     self.ttestResults = None
        #     return
        
        # step 2: check for equal variance:
        _, p_b_low = stats.bartlett(water_low, sample_low)
        _, p_b_high = stats.bartlett(water_high, sample_high)

        if not ((p_b_low < alpha) and (p_b_high < alpha)):
            self.ttestResults = None
            return

        # step 3: run t test
        t_low, p_low = stats.ttest_ind(water_low, sample_low)
        t_high, p_high = stats.ttest_ind(water_high, sample_high)

        self.ttestResults = [{"t": t_low, "p": p_low}, {"t": t_high, "p": p_high}]

        self.plasticPresent = p_low < alpha and p_high < alpha
    
    def write(self, savePath):
        os.makedirs(savePath, exist_ok=True)
        filename = Path(f'{savePath}/impedanceAnalysis.json')
        filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
        
        ttestResults = self.ttestResults
        if ttestResults is not None:
            ttestResults = {
                "low": {"t": self.ttestResults[0]["t"], "p": self.ttestResults[0]["p"]},
                "high": {"t": self.ttestResults[1]["t"], "p": self.ttestResults[1]["p"]}
            }

        with open(f'{savePath}/impedanceAnalysis.json', 'a') as f:
            dataDict = {
                "date": self.date,
                "metadata": {
                    "numChunks": self.numChunks,
                    "lowFreq": LOW_FREQUENCY,
                    "highFreq": HIGH_FREQUENCY,
                },
                "analysisResults": {
                    "impLow": self.imp_low_list,
                    "impHigh": self.imp_high_list,
                    "capacitance": self.cap_list,
                    "ppm": self.ppm,
                    "estPlasticContent": self.estimatedPlasticContent,
                    "plasticPresent": str(self.plasticPresent),
                    "ttestResults": ttestResults
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
