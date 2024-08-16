from api.application import PicoAPI
from board.board import Board

if __name__ == "__main__":
    pico = Board(device_type="Raspberry Pi Pico")
    pico.connect()
    pico.register()

    api = PicoAPI(board=pico)
    api.run(host=pico.IP_ADDRESS, port=80)

    # while True:
    #     _, humidity = pico.sample_humidity()
    #     if humidity < 0.5:
    #         pico.pump_water(10)
    #
    #     time.sleep(20*60)

