import socket
from gpiozero import MCP3008
import time
import matplotlib.pyplot as plt
import numpy as np

# socket setup
server_ip = '10.110.94.3'
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# adc setup
sig = MCP3008(0)

# experiment defaults (5 seconds of collection)
data = []
length = 5
end = time.time() + length

# send intro message to server to prove connection
message = f"Hello from pi"
client_socket.sendto(message.encode(), (server_ip, server_port))

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
		
		break
	
	# if receiving a message to override default length of experiment
	elif (decoded.startswith("length")):
		# parse default value from message
		parts = decoded.split("length:")
		length_val = parts[1].strip()
		
		# recalculate experiment values
		length = int(length_val)
		end = time.time() + length
		print("Length: ", length)

# tell the server data collection is complete
message = "Data collection complete"
print(message)
client_socket.sendto(message.encode(), (server_ip, server_port))

# close the socket
client_socket.close()
