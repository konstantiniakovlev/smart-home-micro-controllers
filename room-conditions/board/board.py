import machine
import network
import time
import ubinascii

from board.exceptions import connection_error_handler
from board.logger import logger
from helpers.custom_bme280_driver import BME280
from helpers.exceptions import NetworkError
from helpers.exceptions import RegistrationError
from helpers.home_hub_client import HomeHubClient
from utils.constants import BoardConfig
from utils.secrets import SecretsManager
from utils.timestamp import sync_network_time


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

        self.wlan = None
        self.bme = None
        self.led = None

        self._set_up()

    def _set_up(self):
        i2c = machine.I2C(
            id=0,
            scl=machine.Pin(BoardConfig.SCL_PIN),
            sda=machine.Pin(BoardConfig.SDA_PIN),
            freq=400000
        )

        self.bme = BME280(i2c=i2c, address=0x77)
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led.off()

    @connection_error_handler
    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(SecretsManager.WIFI_SSID, SecretsManager.WIFI_PASSWORD)

        self._await_connection()
        self._check_connection()
        sync_network_time()

    def _await_connection(self):
        logger.debug("Connecting board to network...")
        for _ in range(BoardConfig.CONNECTION_TIMEOUT):
            if self.wlan.isconnected():
                break
            time.sleep(1)

    def _check_connection(self):
        if not self.wlan.isconnected():
            raise NetworkError("TimeoutError, Board was unable to connect to network.")
        else:
            self.IP_ADDRESS, _, _, _ = self.wlan.ifconfig()
            self.MAC_ADDRESS = ubinascii.hexlify(self.wlan.config("mac"), ":").decode()
            logger.debug("Connected.")

    def register(self):
        payload = {
            "mac_address": self.MAC_ADDRESS,
            "ip_address": self.IP_ADDRESS,
            "device_type": self.DEVICE_TYPE,
            "description": "Raspberry Pi Pico for measuring temperature, pressure, and humidity."
        }
        hub_client = HomeHubClient()
        response = hub_client.register_device(payload)

        if len(response) == 0:
            raise RegistrationError("DEVICE_ID was not received.")
        self.DEVICE_ID = int(response[0]["device_id"])

        logger.debug("Registered.")
