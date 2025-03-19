import socket
from gpiozero import MCP3008
import time
import matplotlib.pyplot as plt
import numpy as np
from cameratest import CameraTest

# socket setup
server_ip = '10.110.244.42'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# adc setup
sig = MCP3008(0)

# experiment defaults (5 seconds of collection)
datapoints = []
length = 5
end = time.time() + length

# camera setup
camera = CameraTest()

# send intro message to server to prove connection
message = f"Hello from pi"
client_socket.sendto(message.encode(), (server_ip, server_port))

# wait for length
while True:
	response, server_address = client_socket.recvfrom(1024)
	decoded = response.decode()
	
	# if receiving a message to override default length of experiment
	if (decoded.startswith("length")):
		# parse default value from message
		parts = decoded.split("length:")
		length_val = parts[1].strip()
		
		# recalculate experiment values
		length = int(length_val)
		end = time.time() + length
		print("Length: ", length)
		
		break

# sends data to server
while True:
	response, server_address = client_socket.recvfrom(1024)
	decoded = response.decode()
	
	# if experiment has been started
	if (decoded == "start"):
		
		print("Sending data to computer")
	
		# collect data for required duration and stream it to computer
		while time.time() < end:
			data = sig.value * 3300
			
			client_socket.sendto(str(data).encode(), (server_ip, server_port))
			datapoints.append(data)
		
		print("impedance data collected")
		camera.collect_data(5)
		
		break

# tell the server data collection is complete
message = "Data collection complete"
print(message)
client_socket.sendto(message.encode(), (server_ip, server_port))

# close the socket
client_socket.close()

print("camera data: ", len(camera.data))
print("impedance data: ", len(datapoints))
