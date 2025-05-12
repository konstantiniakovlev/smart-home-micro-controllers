import json
import urequests as requests

from helpers.exceptions import StatusError
from utils.constants import HubApiConfig


class HomeHubClient:

    base_url = HubApiConfig.URL
    headers = {"content-type": "application/json"}

    def __init__(self):
        self.register_device_url = f"{self.base_url}/hub/devices/register/"
        self.store_measurement_url = f"{self.base_url}/hub/measurements/"

    def register_device(self, payload):
        response = requests.post(
            self.register_device_url,
            headers=self.headers,
            data=json.dumps(payload)
        )
        self.validate_response(response)
        return response.json()

    def store_measurement(self, payload):
        response = requests.post(
            self.store_measurement_url,
            headers=self.headers,
            data=json.dumps(payload)
        )
        self.validate_response(response)
        return response.json()

    @staticmethod
    def validate_response(response):
        if response.status_code not in [200, 201]:
            raise StatusError(f"Status code: {response.status_code}")
