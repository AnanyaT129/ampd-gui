import socket
import numpy as np
import matplotlib.pyplot as plt

# Set up the UDP server
server_ip = '0.0.0.0'  # Listen on all available interfaces
server_port = 12345     # Port to listen to

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_ip, server_port))

print(f"Server listening on {server_ip}:{server_port}...")

# experiment defaults
datapoints = []
length = 5

while True:
    # Wait for a message from the client (Raspberry Pi)
    data, client_address = server_socket.recvfrom(1024)  # Buffer size 1024 bytes

    decoded = data.decode()

    # if it recieves introductory message
    if decoded.startswith("Hello from pi"):
        print(f"Received message from {client_address}: {decoded}")
        
        # send length of data collection to the client
        server_socket.sendto(("length: " + str(length)).encode(), client_address)

        # wait for user input to start data collection
        user_input = input("Press s to start experiment: ")
        noInput = True
        while noInput:
            if user_input == "s":
                
                # send signal to client to start collecting data
                server_socket.sendto(b"start", client_address)
                noInput = False
            else:
                user_input == input("Press s to start experiment: ")

        continue
    # if it recieves closing message
    if decoded == "Data collection complete":
        print(f"Received message from {client_address}: {decoded}")
        break
    # data collection
    else:
      # append received datapoint to array
      datapoints.append(float(decoded))

# graph the received data
x = np.linspace(0, length, num=len(datapoints))
print(len(datapoints))

plt.plot(x, datapoints)
# plt.ylim(bottom=200, top=275)
plt.grid(True)
plt.show()