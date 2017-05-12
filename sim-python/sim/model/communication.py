import socket
import struct


class Communication:

    def __init__(self, address, port):
        self.socket = None
        self.server_address = (address, port)

    def client_socket(self):

        # Create a socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server.connect(self.server_address)

        return server

    def connect(self):
        self.socket = self.client_socket()

    def send_string(self, csv):
        msg_bytes = "csv".encode()
        msg_len = len(msg_bytes)

        buf = bytes()
        buf += struct.pack('f', msg_len)

        self.sock.sendto(msg_len, self.server_address)
        self.sock.sendto("csv".encode(), self.server_address)

        # look for response
        amount_received = 0
        self.socket.recv(0)