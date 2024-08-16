class Request:
    method = None
    endpoint = None
    headers = None
    body = None

    def json(self):
        return {
            "method": self.method,
            "endpoint": self.endpoint,
            "headers": self.headers,
            "body": self.body
        }