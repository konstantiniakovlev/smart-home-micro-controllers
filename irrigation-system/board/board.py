import json
import machine
import network
import time
import ubinascii
import urequests as requests

from board.exceptions import error_handler
from board.logger import logger
from utils.constants import BoardConfig
from utils.constants import HubApiConfig
from utils.constants import MoistureSensorConfig
from utils.constants import RelayConfig
from utils.constants import SensorNames
from utils.secrets import SecretsManager
from utils.timestamp import localtime
from utils.urllib import encode_params


class Board:
    DEVICE_ID: int = None
    DEVICE_TYPE: str = None
    IP_ADDRESS: str = None
    MAC_ADDRESS: str = None

    def __init__(
            self,
            device_type: str = "Raspberry Pi Pico"
    ):
        self.DEVICE_TYPE = device_type

        self.led = None
        self.relay_pump = None
        self.relay_moisture_sensor = None
        self.moisture_sensor = None
        self.wlan = None

        self._set_up()
        self._set_init_state()

    def _set_up(self):
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.relay_pump = machine.Pin(
            BoardConfig.RELAY_PUMP_CTRL_PIN,
            machine.Pin.OUT
        )
        self.relay_moisture_sensor = machine.Pin(
            BoardConfig.RELAY_MOISTURE_SENSOR_CTRL_PIN,
            machine.Pin.OUT
        )
        self.moisture_sensor = machine.ADC(
            machine.Pin(BoardConfig.ADC_PIN)
        )

    def _set_init_state(self):
        self.led.off()
        self.relay_pump.value(RelayConfig.OFF_STATE)
        self.relay_moisture_sensor.value(RelayConfig.OFF_STATE)

    def led_indicator(func):
        def wrapper(self, *args, **kwargs):
            self.led.on()
            func_output = func(self, *args, **kwargs)
            self.led.off()
            return func_output

        return wrapper

    @error_handler
    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(SecretsManager.WIFI_SSID, SecretsManager.WIFI_PASSWORD)

        self._await_connection()
        self._check_connection()

    def _await_connection(self):
        logger.info("Connecting board to network...")
        for _ in range(BoardConfig.CONNECTION_TIMEOUT):
            if self.wlan.isconnected():
                break
            time.sleep(1)

    def _check_connection(self):
        if not self.wlan.isconnected():
            raise Exception("TimeoutError, Board was unable to connect to network.")
        else:
            self.IP_ADDRESS, _, _, _ = self.wlan.ifconfig()
            self.MAC_ADDRESS = ubinascii.hexlify(self.wlan.config("mac"), ":").decode()
            logger.info("Connected.")

    def read_moisture_sensor(self):
        """Separated for calibration purposes
        """
        return self.moisture_sensor.read_u16()

    def register(self):
        base_url = HubApiConfig.URL
        port = HubApiConfig.PORT

        payload = {
            "mac_address": self.MAC_ADDRESS,
            "ip_address": self.IP_ADDRESS,
            "device_type": self.DEVICE_TYPE,
            "description": "Raspberry Pi Pico for watering plants"
        }

        response = requests.post(
            f"{base_url}:{port}/hub/devices/register",
            headers={"content-type": "application/json"},
            data=json.dumps(payload)
        )

        if response.status_code in [200, 201]:
            response_json = response.json()
        else:
            raise Exception(f"ConnectionError, Status code: {response.status_code}")

        if len(response_json) > 0:
            self.DEVICE_ID = int(response_json[0]["device_id"])
        else:
            raise Exception("KeyError, DEVICE_ID was not received.")

        logger.info("Registered.")

    @staticmethod
    def get_sensor_tag(sensor_name: str):
        base_url = HubApiConfig.URL
        port = HubApiConfig.PORT

        params = {"name_filter": sensor_name}

        response = requests.get(
            f"{base_url}:{port}/hub/tags/?{encode_params(params)}",
            headers={"content-type": "application/json"},
        )

        if response.status_code in [200, 201]:
            response_json = response.json()
        else:
            raise Exception(f"ConnectionError, Status code: {response.status_code}")

        if len(response_json) > 0:
            return response_json[0]["tag"]
        return None

    def store_measurement(self, tag, value):
        base_url = HubApiConfig.URL
        port = HubApiConfig.PORT

        payload = {
            "time": localtime(),
            "device_id": self.DEVICE_ID,
            "sensor_tag": tag,
            "value": value
        }

        response = requests.post(
            f"{base_url}:{port}/hub/measurements/",
            headers={"content-type": "application/json"},
            data=json.dumps(payload)
        )

        if response.status_code in [200, 201]:
            logger.info(f"Measurement stored for {tag}.")
        else:
            raise Exception(f"ConnectionError, Status code: {response.status_code}")

    @error_handler
    @led_indicator
    def sample_humidity(self, dry_run=True):
        self.relay_moisture_sensor.value(RelayConfig.ON_STATE)
        time.sleep(RelayConfig.DELAY)

        raw_sample = self.read_moisture_sensor()
        self.relay_moisture_sensor.value(RelayConfig.OFF_STATE)

        humid_perc = self._get_humidity_percentage(raw_sample)

        if not dry_run:
            ms_tag = self.get_sensor_tag(sensor_name=SensorNames.MOISTURE_SENSOR)
            ms_tag_calc = self.get_sensor_tag(sensor_name=SensorNames.MOISTURE_SENSOR_CALC)

            self.store_measurement(tag=ms_tag, value=raw_sample)
            self.store_measurement(tag=ms_tag_calc, value=humid_perc)

        return raw_sample, humid_perc

    @error_handler
    @led_indicator
    def pump_water(self, duration: int = 5):
        self.relay_pump.value(RelayConfig.ON_STATE)
        time.sleep(duration)
        self.relay_pump.value(RelayConfig.OFF_STATE)

    @staticmethod
    def _get_humidity_percentage(sample_value):
        humidity_perc = (
                (MoistureSensorConfig.CALIBRATION_MAX - sample_value)
                / (MoistureSensorConfig.CALIBRATION_MAX - MoistureSensorConfig.CALIBRATION_MIN)
        )
        return humidity_perc
