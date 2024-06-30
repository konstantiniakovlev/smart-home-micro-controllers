import json

from helpers.websocket import WebSocket
from board.board import Board
import api.routers as routers


class PicoAPI:

    def __init__(self, board: Board):
        self.board = board

    def run(self, host: str = "0.0.0.0", port: int = 80):
        socket = WebSocket(host, port)

        while True:
            # todo: address /favicon.ico endpoint request
            connection = socket.accept()
            request_obj = self._get_request(connection)
            response = self._handle_request(**request_obj)
            self._send_response(connection, response)
            connection.close()

    @staticmethod
    def _receive_request(connection):
        request = connection.recv(1024)
        return request.decode("utf-8")

    @staticmethod
    def _format_request(request):
        headers = {}
        body = {}

        request_line, headers_str = request.split("\r\n", 1)
        method, request_url, protocol = request_line.split()

        endpoint = request_url.split("?")[0]
        if "?" in request_url:
            for param_value in request_url.split("?")[1].split("&"):
                param, value = param_value.split("=")
                body[param] = value

        request_obj = {
            "method": method,
            "endpoint": endpoint,
            "headers": headers,
            "body": body
        }
        return request_obj

    def _handle_request(self, *args, **kwargs):
        req_response = {}
        for func_def in dir(routers):
            if (not func_def.startswith("__") and
                    # todo: remove redundant functions
                    func_def not in ["get", "Get", "Board", "Methods", "Routers", "Router"]):
                func = getattr(routers, func_def)
                # todo: remove
                print(func_def)
                print(kwargs.get("endpoint"))
                if callable(func):
                     func_response = func(*args, **kwargs, board=self.board)
                     req_response = func_response if func_response is None else req_response

        return req_response

    @staticmethod
    def _format_response():
        pass

    @staticmethod
    def _send_response(connection, response):
        response_str = json.dumps(response)
        connection.sendall("HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n")
        connection.sendall(bytes(response_str, "utf-8"))

    def _get_request(self, connection):
        request = self._receive_request(connection)
        response_obj = self._format_request(request)
        return response_obj
