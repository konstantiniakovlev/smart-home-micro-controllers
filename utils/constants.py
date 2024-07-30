class BoardConfig:
    RELAY_MOISTURE_SENSOR_CTRL_PIN = 0
    RELAY_PUMP_CTRL_PIN = 16
    ADC_PIN = 26
    CONNECTION_TIMEOUT = 30


class RelayConfig:
    ON_STATE = 0
    OFF_STATE = 1
    DELAY = 1


class MoistureSensorConfig:
    CALIBRATION_MIN = 39145
    CALIBRATION_MAX = 65535


class HubApiConfig:
    URL = "http://home-hub.local"
    PORT = 5000


class SensorNames:
    MOISTURE_SENSOR = "Soil Moisture Sensor"
    MOISTURE_SENSOR_CALC = "Soil Moisture Sensor Calculated"
