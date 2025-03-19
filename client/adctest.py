from gpiozero import MCP3008
import time
import matplotlib.pyplot as plt
import numpy as np

sig = MCP3008(0)

data = []

length = 5
end = time.time() + length

while time.time() < end:
	data.append(sig.value)

x = np.linspace(0,length, num=len(data))

print(len(data))

plt.plot(x, data)
plt.ylim(bottom=0,top=1)
plt.grid(True)
plt.show()
