from api.application import PicoAPI
from board.board import Board

pico = Board(device_type="Raspberry Pi Pico")
pico.connect_wlan()

if __name__ == "__main__":

    api = PicoAPI(board=pico)
    api.run(host=pico.ip_address, port=80)

    # while True:
    #     _, humidity = pico.sample_humidity()
    #     if humidity < 0.5:
    #         pico.pump_water(10)
    #
    #     time.sleep(20*60)

