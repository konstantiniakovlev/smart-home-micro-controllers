import machine
import network
import time
import ubinascii

from utils import config


class Pico:

    def __init__(self):
        self.wlan = None
        self.ip_addr = None
        self.mac_addr = None
        self.device_id = None
        self.device_type = "Raspberry Pi Pico W"
        self.status = "disconnected"

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(config.WIFI_SSID, config.WIFI_PWD)

        self._await_connection()
        self._check_connection()

        self.status = "connected"
        self.ip_addr, _, _, _ = self.wlan.ifconfig()
        self.mac_addr = ubinascii.hexlify(self.wlan.config("mac"), ":").decode()
        print("Connected inet", self.ip_addr)

    def _await_connection(self):
        for _ in range(config.TIMEOUT_TIME):
            if self.wlan.isconnected():
                break
            time.sleep(1)

    def _check_connection(self):
        if not self.wlan.isconnected():
            raise Exception("TimeoutError, pico was not able to connect to network.")

    def create_device_payload(self):
        payload = {
            "mac_address": self.mac_addr,
            "ip_address": self.ip_addr,
            "device_type": self.device_type,
            "description": "Microcontroller with relay "
                           "connected to water pump and moisture "
                           "sensor."
        }
        return payload

    def create_program_payload(self):
        payload = {
            "device_id": self.device_id,
            "port": config.PICO_PORT,
            "program_name": "Irrigation system",
            "description": "API to trigger watering system "
                           "and irrigation system to trigger "
                           "pump automatically.",
        }
        return payload


class Pump:

    def __init__(self):
        self.led = None
        self.relay = None

        self._configure_hardware()
        self._set_initial_state()

    def _configure_hardware(self):
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.relay = machine.Pin(config.PUMP_RELAY_CTRL_PIN, machine.Pin.OUT)

    def _set_initial_state(self):
        self.led.off()
        self.relay.value(config.RELAY_OFF)

    def water(self, water_time):
        self.led.on()
        self.relay.value(config.RELAY_ON)

        time.sleep(water_time)

        self.relay.value(config.RELAY_OFF)
        self.led.off()


class MoistureSensor:

    def __init__(self):
        self.relay = None
        self.sensor = None

        self._configure_hardware()
        self._set_initial_state()

    def _configure_hardware(self):
        self.relay = machine.Pin(config.SENSOR_RELAY_CTRL_PIN, machine.Pin.OUT)
        self.sensor = machine.ADC(machine.Pin(config.ADC_PIN))

    def _set_initial_state(self):
        self.relay(config.RELAY_OFF)

    def sample(self):
        return self.sensor.read_u16()

    def get_soil_humidity(self):
        self.relay.value(config.RELAY_ON)
        time.sleep(config.RELAY_DELAY)

        humid = self._calc_humidity_level(self.sample())

        self.relay.value(config.RELAY_OFF)

        return humid

    @staticmethod
    def _calc_humidity_level(sample_value):

        humid = (
                (config.CALIBRATION_MAX - sample_value)
                / (config.CALIBRATION_MAX - config.CALIBRATION_MIN)
                * 100
        )

        return humid

