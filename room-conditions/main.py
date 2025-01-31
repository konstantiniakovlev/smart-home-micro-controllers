import gc
import time

from helpers.home_hub_client import HomeHubClient
from helpers.exceptions import StatusError
from board.board import Board
from board.logger import logger
from utils.constants import Tags
from utils.timestamp import localtime


SAMPLING_FREQ = 30


def set_up_pico():
    pico = Board()
    pico.connect()
    pico.register()

    return pico


def main():
    tags = [Tags.TEMPERATURE_TAG, Tags.PRESSURE_TAG, Tags.HUMIDITY_TAG]

    hub_client = HomeHubClient()
    pico = set_up_pico()

    while True:
        temperature, pressure, humidity = pico.bme.sample()
        sample_dt_str = localtime()

        for tag, value in zip(tags, [temperature, pressure, humidity]):

            payload = {
                "time": sample_dt_str,
                "device_id": pico.DEVICE_ID,
                "sensor_tag": tag,
                "value": value
            }
            try:
                hub_client.store_measurement(payload)
            except StatusError as e:
                raise StatusError(e)
            except Exception as e:
                print(e)
                pico = set_up_pico()
                break

            # free up memory after HTTP requests
            gc.collect()
        time.sleep(SAMPLING_FREQ)


if __name__ == "__main__":
    main()
