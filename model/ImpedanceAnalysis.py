import statistics

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



