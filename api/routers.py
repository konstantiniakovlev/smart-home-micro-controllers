from board.board import Board
from helpers.router import Router


class Actions:
    SENSOR_SAMPLE = "sample moisture sensor"
    PUMP_WATER = "pump water"


@Router.get(path="/")
def welcome_msg(*args, **kwargs):
    return {
        "message": "Welcome to the Pico API",
        "device_name": "Raspberry Pi Pico"
    }


@Router.get(path="/sensor/sample")
def sample_moisture_sensor(*args, **kwargs):
    board: Board = kwargs.get("board")
    return {
        "action": Actions.SENSOR_SAMPLE,
        "humidity": board.sample_humidity()
    }


@Router.get(path="/pump/run")
def run_pump(*args, **kwargs):
    request_body = kwargs.get("body")
    board: Board = kwargs.get("board")

    duration = int(request_body.get("duration", 5))
    board.pump_water(duration=duration)
    return {
        "action": Actions.PUMP_WATER,
        "duration": duration
    }

