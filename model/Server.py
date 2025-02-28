import socket
import numpy as np

class Server:
    def __init__(self, experiment, log_callback, server_ip='0.0.0.0', server_port=12345):
        self.server_ip = server_ip # 0.0.0.0 means to listen on all available interfaces
        self.server_port = server_port
        self.server_socket = None
        self.datapoints = []
        self.client_address = None
        self.log_callback = log_callback
        self.experiment = experiment

    def log(self, message):
        """Helper function to log messages through the callback""" 
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def start_server(self, length=5):
        """Start the server and listen for a message from the client"""
        # Create a UDP socket and bind it
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.server_ip, self.server_port))

        self.log(f"Server listening on {self.server_ip}:{self.server_port}...")

        try:
            # Wait for a message from the client (Raspberry Pi)
            data, self.client_address = self.server_socket.recvfrom(1024)  # Buffer size 1024 bytes
            decoded = data.decode()

            # If it receives an introductory message
            if decoded.startswith("Hello from pi"):
                self.log(f"Received message from {self.client_address}: {decoded}")

                # send length of data collection to the client
                self.server_socket.sendto(f"length: {length}".encode(), self.client_address)

                return True
            else:
                self.log("Error: No introductory message received")
                return False
        except Exception as e:
            self.log(f"Error starting server: {e}")

    def start_data_collection(self, length):
        """Start collecting data from the client"""
        if not self.server_socket:
            self.log("Server not started yet.")
            return []

        # wait for gui start to start data collection on the pi
        self.server_socket.sendto(b"start", self.client_address)
        self.log("Signal sent to start data collection.")

        while True:
            # Wait for a message from the client containing data points
            data, _ = self.server_socket.recvfrom(1024)
            decoded = data.decode()

            # if it recieves closing message
            if decoded == "Data collection complete":
                self.log(f"Received completion signal from client.")
                break

            try:
                # Append received datapoint to array (convert to float)
                self.datapoints.append(float(decoded))
                self.experiment.addDatapoint(float(decoded))
            except ValueError:
                self.log(f"Invalid data received: {decoded}")

        # Return collected data points
        return self.datapoints

    def close_server(self):
        """Close the server"""
        if self.server_socket:
            self.server_socket.close()
            self.log("Server closed.")
            self.server_socket = None
        else:
            self.log("Server is not running.")