class Response:
    message = None
    device_name = "Raspberry Pi Pico"
    activity = {
        "action": None,
        "description": None,
        "value": None
    }

    def json(self):
        return {
            "message": self.message,
            "device_name": self.device_name,
            "activity": self.activity
        }
