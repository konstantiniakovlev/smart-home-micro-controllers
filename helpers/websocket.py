import socket

from api.logger import logger


class WebSocket:
    PROTOCOL = "http"

    def __init__(self, host: str = "0.0.0.0", port: int = 80):
        self.host = host
        self.port = port
        self.tcp_socket: socket.socket = None

        self._init_socket_()

    def _init_socket_(self):
        address_info = self._get_address_info_()

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(address_info[0][-1])
        self.tcp_socket.listen(2)

        address = f"{WebSocket.PROTOCOL}://{address_info[0][-1][0]}:{address_info[0][-1][1]}"
        logger.info(f"Listening on address: {address}")

    def _get_address_info_(self):
        return socket.getaddrinfo(self.host, self.port)

    def accept(self):
        connection, address = self.tcp_socket.accept()
        logger.info(f"Client connected from address {address}")
        return connection

    def close(self):
        self.tcp_socket.close()
        logger.info("Socket closed.")

    @staticmethod
    def close_connection(connection):
        connection.close()
        logger.info("Connection closed.")
