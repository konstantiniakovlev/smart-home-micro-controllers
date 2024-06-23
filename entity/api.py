import socket
import time


class PicoApi:

    def __init__(self):
        self.tcp_socket = None
        self.connection = None
        self.connection_type = "http://"

    def run(self, host: str = "0.0.0.0", port: int = 80):
        self._create_socket(host, port)

        while True:
            self._accept_connection()
            self._get_request()

    def _create_socket(self, host, port):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        address_info = socket.getaddrinfo(host, port)
        self.tcp_socket.bind(address_info[0][-1])
        self.tcp_socket.listen(2)
        print(
            f"Listening on address: {self.connection_type}{address_info[0][-1][0]}:{address_info[0][-1][1]}"
        )

    def _accept_connection(self):
        self.connection, address = self.tcp_socket.accept()
        print(f"Client connected from address {address}")

    def _get_request(self):
        request = self.connection.recv(1024)
        request = request.decode("utf-8")
        print(request)

