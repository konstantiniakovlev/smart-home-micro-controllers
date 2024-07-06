from board.board import Board
from helpers.responses import Response
from helpers.router import Router


class Actions:
    SENSOR_SAMPLE = "sample moisture sensor"
    PUMP_WATER = "pump water"


response = Response()


@Router.get(path="/")
def welcome_msg(*args, **kwargs):
    response.message = "Welcome to the Pico API"
    return response


@Router.get(path="/sensor/sample")
def sample_moisture_sensor(*args, **kwargs):
    board: Board = kwargs.get("board")
    _, percentage = board.sample_humidity()
    response.activity = {
        "action": Actions.SENSOR_SAMPLE,
        "description": "humidity percentage",
        "value": percentage
    }
    return response


@Router.get(path="/pump/run")
def run_pump(*args, **kwargs):
    request_body = kwargs.get("body")
    board: Board = kwargs.get("board")

    duration = int(request_body.get("duration", 5))
    board.pump_water(duration=duration)
    response.activity = {
        "action": Actions.PUMP_WATER,
        "description": "duration",
        "value": duration
    }
    return response

