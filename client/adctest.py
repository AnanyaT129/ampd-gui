from gpiozero import MCP3008, LED
import time
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

import statistics

class ImpedanceAnalysis:
    def __init__(self, impedance_data, numChunks = 10):
        self.impedance_data = impedance_data
        self.total_length = len(self.impedance_data)
        self.num_chunks = numChunks
        self.avg_list = []
        self.imp_list = []

    def run(self):
        self.chunk_avg()
        self.calc_imp()
        
        return self.imp_list

    def chunk_avg(self):
        chunk_size = self.total_length // self.num_chunks
        for i in range(self.num_chunks-1):
            self.avg_list.append(statistics.mean(self.impedance_data[i:i+chunk_size-1]))
        self.avg_list.append(statistics.mean(self.impedance_data[self.num_chunks-1:]))

    def calc_imp(self):
        rf_vin = 5600*200
        for i in range(self.num_chunks):
            self.imp_list.append(rf_vin/self.avg_list[i])

sig = MCP3008(0)
onOffPin = 25
tds = LED(onOffPin)

data = []

length = 5
end = time.time() + length

tds.on()
sleep(1)
print("start")
while time.time() < end:
	data.append(sig.value * 3300)
sleep(1)
tds.off()

ia = ImpedanceAnalysis(data)
imp_list = ia.run()

x = np.linspace(0,length, num=len(data))
x_imp = np.linspace(0, length, num=len(imp_list))

print(len(data))
print(len(imp_list))

fig, axs = plt.subplots(1, 2, figsize=(10,5))

axs[0].plot(x, data, label="Raw data", color="blue")
axs[0].set_title("Raw data")
axs[0].grid(True)
axs[0].set_ylim(0, 3300)

axs[1].plot(x_imp, imp_list, label="Impedance data", color="red")
axs[1].set_title("Impedance data")
axs[1].grid(True)

plt.show()
