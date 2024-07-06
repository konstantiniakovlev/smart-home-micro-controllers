import json

import api.routers as routers
from board.board import Board
from helpers.responses import Response
from helpers.requests import Request
from helpers.websocket import WebSocket


class PicoAPI:

    def __init__(self, board: Board):
        self.board = board

    def run(self, host: str = "0.0.0.0", port: int = 80):
        socket = WebSocket(host, port)

        while True:
            # todo: address /favicon.ico endpoint request
            connection = socket.accept()
            request_json = self._get_request(connection)
            response = self._handle_request(**request_json)
            response_json = self._format_response(response)
            self._send_response(connection, response_json)
            socket.close(connection)

    def _get_request(self, connection):
        request = self._receive_request(connection)
        request_json = self._format_request(request)
        return request_json

    @staticmethod
    def _receive_request(connection):
        request = connection.recv(1024)
        return request.decode("utf-8")

    @staticmethod
    def _format_request(request):
        # todo: parse and return headers
        headers = {}
        body = {}

        request_line, headers_str = request.split("\r\n", 1)
        method, request_url, protocol = request_line.split()

        endpoint = request_url.split("?")[0]
        if "?" in request_url:
            for param_value in request_url.split("?")[1].split("&"):
                param, value = param_value.split("=")
                body[param] = value

        request_obj = Request()
        request_obj.method = method
        request_obj.endpoint = endpoint
        request_obj.headers = headers
        request_obj.body = body

        return request_obj.json()

    def _handle_request(self, *args, **kwargs):
        response = Response()
        for func_def in dir(routers):
            if (not func_def.startswith("__") and
                    func_def not in ["Actions", "Board", "Response", "Router", "get", "post", "put"]):
                func = getattr(routers, func_def)
                if callable(func):
                     func_response = func(*args, **kwargs, board=self.board)
                     response = response if func_response is None else func_response

        return response

    @staticmethod
    def _format_response(response):
        return response.json()

    @staticmethod
    def _send_response(connection, response):
        response_str = json.dumps(response)
        connection.sendall("HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n")
        connection.sendall(bytes(response_str, "utf-8"))
