from helpers.pico import Pico, Pump
from helpers.api import PicoAPI
from tools.hub_client import HubClient
from utils import config


def main():
    client = HubClient()
    pico = Pico()

    pico.connect()
    device_payload = pico.create_device_payload()

    client.register_device(payload=device_payload)
    pico.device_id = client.get_device_id(mac_address=pico.mac_addr)
    print("Device registered")

    program_payload = pico.create_program_payload()
    client.register_program(payload=program_payload)
    print("Program registered")

    pump = Pump(name="Water Pump")
    api = PicoAPI(ctrl_ent=pump)

    api.run(host="0.0.0.0", port=config.PICO_PORT)


def test():
    pump = Pump()
    pump.water(3)


if __name__ == "__main__":
    main()
