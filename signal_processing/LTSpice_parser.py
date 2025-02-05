# Justin Bahr
# Capstone C1

import matplotlib.pyplot as plt
import numpy as np
import math

# function to stores transient voltage data from LTSpice in two arrays
def parse_text(file_name):
    col_1 = []
    col_2 = []
    with open(file_name, 'r') as file:
        next(file)
        for line in file:
            parts = line.strip().split()
            col_1.append(float(parts[0]))
            col_2.append(float(parts[1]))
    return col_1, col_2

def main():

    # reads the LTSpice vin data export
    t_in,vin = parse_text('vin_jan31.txt')

    # prompts the user to enter the LTSpice vout data export filename
    print('LTSpice Data Filename: ')
    filename = input()
    t,vout = parse_text(filename)

    # calculates the fft of vin
    vin_fft = np.fft.fft(vin)
    vin_freq = np.fft.fftfreq(len(vin), (t_in[1] - t_in[0]) * math.pi)

    # calculates the fft of vout
    vout_fft = np.fft.fft(vout)
    vout_freq = np.fft.fftfreq(len(vout), (t[1] - t[0]) * math.pi)

    # calculates the impedance based on the fft peaks
    z_1khz = 1500 * (abs(vin_fft[40]) + abs(vin_fft[925])) / (abs(vout_fft[40]) + abs(vout_fft[925]))
    z_10khz = 1500 * (abs(vin_fft[4]) + abs(vin_fft[961])) / (abs(vout_fft[4]) + abs(vout_fft[961]))

    # prints the impedances
    print('Impedance at 1 kHz:', z_1khz)
    print('Impedance at 10 kHz:', z_10khz)

    # plots the transient input voltage
    plt.subplot(2, 2, 1)
    plt.plot(t_in, vin)
    plt.title('Transient Input Voltage')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (V)')

    # plots the fft of vin
    plt.subplot(2, 2, 3)
    plt.plot(vin_freq, np.abs(vin_fft))
    plt.title('FFT of Input Voltage')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('FFT Magnitude')
    plt.xlim(-15000, 15000)

    # plots the transient output voltage
    plt.subplot(2,2,2)
    plt.plot(t,vout)
    plt.title('Transient Output Voltage')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Voltage (V)')

    # plots the fft of vout
    plt.subplot(2,2,4)
    plt.plot(vout_freq, np.abs(vout_fft))
    plt.title('FFT of Output Voltage')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('FFT Magnitude')
    plt.xlim(-15000,15000)
    plt.show()

main()