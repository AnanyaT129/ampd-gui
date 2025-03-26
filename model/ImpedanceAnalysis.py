import statistics
import random

class ImpedanceAnalysis:
    def __init__(self, impedance_data, numChunks = 10):
        self.impedance_data = impedance_data
        self.total_length = len(self.impedance_data)
        self.numChunks = numChunks
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

def generateRandomVal(base):
    noise = random.random() * 40
    if random.random() < 0.5:
        return base - noise
    else:
        return base + noise

data = [generateRandomVal(200) for i in range(5000)] + [generateRandomVal(300) for i in range(5000)]
print(len(data))

ia = ImpedanceAnalysis(data, 10)
ia.run()