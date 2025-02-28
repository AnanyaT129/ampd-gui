import numpy as np
from time import sleep
import time

class ServerMock:
    def __init__(self, log_callback, server_ip='0.0.0.0', server_port=12345):
        self.server_ip = server_ip # 0.0.0.0 means to listen on all available interfaces
        self.server_port = server_port
        self.server_socket = None
        self.datapoints = []
        self.client_address = None
        self.log_callback = log_callback

    def log(self, message):
        """Helper function to log messages through the callback""" 
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def start_server(self, length=5):
        """Start the server and listen for a message from the client"""
        self.log(f"Server listening on {self.server_ip}:{self.server_port}...")

        sleep(5)

        return True

    def start_data_collection(self, length):
        """Start collecting data from the client"""
        if not self.server_socket:
            self.log("Server not started yet.")
            return []

        self.log("Signal sent to start data collection.")
        end = time.time() + length
        while time.time() < end:
            self.datapoints.append(float(np.random.random()))
        
        self.log(f"Received completion signal from client.")

        # Return collected data points
        return self.datapoints

    def close_server(self):
        """Close the server"""
        self.log("Server closed.")
        self.server_socket = None