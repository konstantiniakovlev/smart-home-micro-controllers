import machine
import network
import time

from board.exceptions import error_handler
from board.logger import logger
from utils.constants import BoardConfig
from utils.constants import MoistureSensorConfig
from utils.constants import RelayConfig
from utils.secrets import SecretsManager


class Board:

    def __init__(
            self,
            identifier: str = None,
            name: str = None,
            device_type: str = None
    ):
        self.identifier = identifier
        self.name = name
        self.device_type = device_type
        self.ip_address = None

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
    def connect_wlan(self):
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
            self.ip_address, _, _, _ = self.wlan.ifconfig()
            logger.info("Connected.")

    def read_moisture_sensor(self):
        """Separated for calibration purposes
        """
        return self.moisture_sensor.read_u16()

    @error_handler
    @led_indicator
    def sample_humidity(self):
        self.relay_moisture_sensor.value(RelayConfig.ON_STATE)
        time.sleep(RelayConfig.DELAY)

        raw_sample = self.read_moisture_sensor()
        self.relay_moisture_sensor.value(RelayConfig.OFF_STATE)

        humid_perc = self._get_humidity_percentage(raw_sample)
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
