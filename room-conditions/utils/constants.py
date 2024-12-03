class BoardConfig:
    SCL_PIN = 17
    SDA_PIN = 16
    CONNECTION_TIMEOUT = 24 * 60 * 60


class HubApiConfig:
    URL = "http://home-hub.local"


class Tags:
    TEMPERATURE_TAG = "BME280-TEMP-PV"
    PRESSURE_TAG = "BME280-PRES-PV"
    HUMIDITY_TAG = "BME280-HUMID-PV"
