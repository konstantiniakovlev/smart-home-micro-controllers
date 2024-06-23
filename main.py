import time

from entity.board import Board

pico = Board()

if __name__ == "__main__":

    while True:
        _, humidity = pico.sample_humidity()
        if humidity < 0.5:
            pico.pump_water(10)

        time.sleep(20*60)

