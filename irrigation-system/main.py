from helpers.pico import Pico, Pump, MoistureSensor
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

    pump = Pump()
    api = PicoAPI(ctrl_ent=pump)

    api.run(host="0.0.0.0", port=config.PICO_PORT)


def calibrate():

    sensor = MoistureSensor()
    sensor.relay.value(config.RELAY_ON)
    max_value, min_value = -10**10, 10**10

    while True:

        try:
            value = sensor.sample()
            max_value = value if value > max_value else max_value
            min_value = value if value < min_value else min_value

        except KeyboardInterrupt:
            sensor.relay.value(config.RELAY_OFF)
            print(f"CALIBRATION_MIN: {min_value}, CALIBRATION_MAX: {max_value}")
            break


if __name__ == "__main__":
    main()
