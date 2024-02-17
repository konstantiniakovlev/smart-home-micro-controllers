import urequests as requests


class HubClient:

    def __init__(
            self,
            host="home-hub.local",
            port=5000,
    ):
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}"

    def register_device(self, payload):
        endpoint = "/hub/devices/register"
        url = self.base_url + endpoint

        response = requests.post(url=url, json=payload)
        if response.status_code not in [201]:
            raise Exception(f"{response.status_code}, {response.content}")

        return response

    def register_program(self, payload):
        endpoint = "/hub/programs/register"
        url = self.base_url + endpoint

        response = requests.post(url=url, json=payload)
        if response.status_code not in [201]:
            raise Exception(f"{response.status_code}, {response.content}")

        return response

    def get_device_id(self, mac_address):
        params = {"mac_address": mac_address}
        endpoint = "/hub/devices/"

        url = self.base_url + endpoint
        url = url + "?" + "&".join([f"{key}={value}" for key, value in params.items()])

        response = requests.get(url=url)

        if response.status_code not in [200]:
            raise Exception(f"{response.status_code}, {response.content}")

        if len(response.json()) != 0:
            return response.json()[0].get("device_id", None)

        return None

