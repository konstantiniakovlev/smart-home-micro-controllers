import gc
import machine
import time

from helpers.home_hub_client import HomeHubClient
from helpers.exceptions import SampleError
from helpers.exceptions import StatusError
from board.board import Board
from board.logger import logger
from utils.constants import Tags
from utils.timestamp import localtime


DEVICE_ID = None
SAMPLING_FREQ = 30


def set_up() -> Board:
    pico = Board()
    pico.connect()
    pico.register()

    global DEVICE_ID
    DEVICE_ID = pico.DEVICE_ID

    return pico


def sample(pico: Board) -> (list[str], tuple[float], str):
    tags = [Tags.TEMPERATURE_TAG, Tags.PRESSURE_TAG, Tags.HUMIDITY_TAG]

    try:
        temperature, pressure, humidity = pico.bme.sample()
        sample_time = localtime()
    except Exception as e:
        raise SampleError(e)

    return tags, (temperature, pressure, humidity), sample_time


def post_results(client: HomeHubClient, tags: list[str], values: tuple[float], sample_time: str):
    for tag, value in zip(tags, values):
        payload = {
            "time": sample_time,
            "device_id": DEVICE_ID,
            "sensor_tag": tag,
            "value": value
        }
        client.store_measurement(payload)


def main():
    client = HomeHubClient()
    pico = set_up()

    while True:
        try:
            tags, values, sample_time = sample(pico)
            post_results(client, tags, values, sample_time)
            logger.debug("Sampled and saved results.")
        except (StatusError, SampleError) as e:
            pico = set_up()
            continue
        except Exception as e: 
            logger.critical(f"Critical Error: {e}. Resetting the board.")
            machine.reset()

        gc.collect()  # free up memory after HTTP requests
        time.sleep(SAMPLING_FREQ)


if __name__ == "__main__":
    main()
