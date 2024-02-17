import json
import socket
import time


class PicoAPI:

    def __init__(self, ctrl_ent):
        self.pump = ctrl_ent
        self.socket_obj = None
        self.connection = None

    def run(self, host="0.0.0.0", port=80):
        address_info = socket.getaddrinfo(host, port)
        self._create_socket(address_info)

        while True:
            timestamp = self._accept_connection()
            request = self._read_request()
            (
                method,
                endpoint,
                params,
                headers,
                request_body
            ) = self._parse_request(request)
            interaction_params = self._create_interaction_params(endpoint, params, request_body)
            response = self._create_response(timestamp, method, endpoint, interaction_params)
            self._send_response(response)
            self._execute_request(endpoint, params, request_body)

    def _execute_request(self, endpoint, params, request_body):
        if "activate" in endpoint:
            duration = request_body.get("duration", 0)
            if duration >= 1:
                self._activate_pump(duration)

    @staticmethod
    def _create_interaction_params(endpoint, params, request_body):
        if "activate" in endpoint:
            duration = request_body.get("duration", None)
            return {
                "duration": duration
            }
        return {}

    def _create_socket(self, address_info):
        self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_obj.bind(address_info[0][-1])
        self.socket_obj.listen(2)
        print(f"Listening on address: {address_info[0][-1]}\n")

    def _accept_connection(self):
        try:
            self.connection, address = self.socket_obj.accept()
            timestamp = self._custom_strftime(time.localtime())
            print(f"[{timestamp}] Client connected from address {address}")
            return timestamp
        except OSError as e:
            raise Exception(e)

    def _read_request(self):
        try:
            request = self.connection.recv(1024)
            request = request.decode("utf-8")
            print(f"Request:\n{request}")
            return request
        except OSError as e:
            raise Exception(e)

    def _parse_request(self, request):
        try:
            request_line, headers = request.split("\r\n", 1)
            method = self._get_method(request_line)
            endpoint = self._get_endpoint(request_line)
            params = self._get_params(request_line)
            request_body = self._get_request_body(request_line)
            return method, endpoint, params, headers, request_body

        except OSError as e:
            raise Exception(e)

    @staticmethod
    def _create_response(timestamp, method, endpoint, interaction_params):
        response = {
            "timestamp": timestamp,
            "method": method,
            "endpoint": endpoint,
            "interaction_params": interaction_params
        }
        return json.dumps(response)

    def _send_response(self, response):
        try:
            self.connection.sendall("HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n")
            self.connection.sendall(bytes(response, "utf-8"))
            self.connection.close()
        except OSError as e:
            raise Exception(e)

    def _activate_pump(self, duration):
        self.pump.water(duration)

    @staticmethod
    def _get_method(request_line):
        method = request_line.split()[0]
        return method

    @staticmethod
    def _get_endpoint(request_line):
        endpoint = request_line.split()[1].split("?")[0]
        return endpoint

    @staticmethod
    def _get_params(request_line):
        url = request_line.split()[1]
        if "?" not in url:
            return dict()
        else:
            params = dict()
            for kv_str in url.split("?")[1].split("&"):
                key, value = kv_str.split("=")
                params[key] = value
            return params

    def _get_request_body(self, request_line):
        request_body = {}
        method = self._get_method(request_line)
        if method == "POST":
            request_body = self.connection.recv(1024)
            request_body = request_body.decode("utf-8")
            request_body = json.loads(request_body)

        print(f"Request Body:\n {request_body}")
        return request_body

    @staticmethod
    def _custom_strftime(dt):
        year, month, day = dt[0:3]
        hour, minute, second = dt[3:6]
        dt_str = "{:02d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            year, month, day, hour, minute, second
        )
        return dt_str
