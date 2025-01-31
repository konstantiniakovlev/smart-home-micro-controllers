import json
import urequests as requests

from utils.constants import HubApiConfig


class HomeHubClient:

    base_url = HubApiConfig.URL

    def __init__(self):
        self.register_device_url = f"{self.base_url}/hub/devices/register/"
        self.store_measurement_url = f"{self.base_url}/hub/measurements/"

    def register_device(self, payload):
        response = requests.post(
            self.register_device_url,
            headers={"content-type": "application/json"},
            data=json.dumps(payload)
        )
        self.validate_response(response)
        return response.json()

    def store_measurement(self, payload):
        try:
            response = requests.post(
                self.store_measurement_url,
                headers={"content-type": "application/json"},
                data=json.dumps(payload)
            )
            self.validate_response(response)
            return response.json()
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def validate_response(response):
        if response.status_code not in [200, 201]:
            raise Exception(f"ConnectionError, Status code: {response.status_code}")
