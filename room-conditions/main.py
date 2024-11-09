import gc
import json
import time
import urequests as requests

from board.board import Board
from board.logger import logger
from utils.constants import HubApiConfig
from utils.constants import Tags
from utils.timestamp import localtime


SAMPLING_FREQ = 30
BASE_URL = HubApiConfig.URL
PORT = HubApiConfig.PORT

url = f"{BASE_URL}:{PORT}/hub/measurements/"
tags = [Tags.TEMPERATURE_TAG, Tags.PRESSURE_TAG, Tags.HUMIDITY_TAG]


pico = Board()
pico.connect()
pico.register()

# warm up sensor
logger.info("Warming up sensor...")
for _ in range(30):
    time.sleep(1)
    pico.bme.sample()

while True:
    time.sleep(SAMPLING_FREQ)

    temperature, pressure, humidity = pico.bme.sample()
    sample_dt_str = localtime()

    for tag, value in zip(tags, [temperature, pressure, humidity]):

        payload = {
            "time": sample_dt_str,
            "device_id": pico.DEVICE_ID,
            "sensor_tag": tag,
            "value": value
        }
        response = requests.post(
            url,
            headers={"content-type": "application/json"},
            data=json.dumps(payload)
        )

        if response.status_code in [200, 201]:
            logger.info(f"Measurement stored for {tag}.")
        else:
            raise Exception(f"ConnectionError, Status code: {response.status_code}")

        # free up memory after HTTP requests
        gc.collect()
