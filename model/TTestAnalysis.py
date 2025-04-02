import json
from scipy import stats

class TTest:
    def __init__(self, water_path, spiked_path):
        self.water_data_low = self.get_data_from_path(water_path)[0]
        self.water_data_high = self.get_data_from_path(water_path)[1]
        self.spiked_data_low = self.get_data_from_path(spiked_path)[0]
        self.spiked_data_high = self.get_data_from_path(spiked_path)[1]
  
    def get_data_from_path(self, path):
        with open(path, 'r') as file:
            data = json.load(file)

            impedance_data = data.get("impedanceData", {})

            return [self.calculate_impedance(impedance_data.get("low", [])), self.calculate_impedance(impedance_data.get("high", []))]
    
    def calculate_impedance(self, arr):
        rf_vin = 5600*200

        return [rf_vin/i for i in arr]
    
    def run(self):
        t_low, p_low = stats.ttest_ind(self.water_data_low, self.spiked_data_low)
        t_high, p_high = stats.ttest_ind(self.water_data_high, self.spiked_data_high)

        t_b_low, p_b_low = stats.bartlett(self.water_data_low, self.spiked_data_low)
        t_b_high, p_b_high = stats.bartlett(self.water_data_high, self.spiked_data_high)

        _, p_1 = stats.shapiro(self.water_data_low)
        _, p_2 = stats.shapiro(self.water_data_high)
        _, p_3 = stats.shapiro(self.spiked_data_low)
        _, p_4 = stats.shapiro(self.spiked_data_high)

        print('Low values t = ', t_low, ' p = ', p_low)
        print('High values t = ', t_high, ' p = ', p_high)

        print('Bartlett Low values t = ', t_b_low, ' p = ', p_b_low)
        print('Bartlett High values t = ', t_b_high, ' p = ', p_b_high)

        print((p_1 < 0.05) and (p_2 < 0.05) and (p_3 < 0.05) and (p_4 < 0.05))

water_path = "experiments/trial 2/air or water/20250331_2344_ampd_experiment_data/data.json"
spiked_path = "experiments/trial 2/spiked-little/20250331_2355_ampd_experiment_data/data.json"
tt = TTest(water_path, spiked_path)
tt.run()