# Micro-controllers

## Prerequisites
- Raspberry Pi Pico
- [Micropython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) installed on the board.

## Test locally

By default, Raspberry Pi Pico runs `main.py` file in its root directory.

To quickly flash multiple files or entire project directory to the micro-controller, adafruit-ampy module is needed:\
``pip install adafruit-ampy``.

To test code on Raspberry Pi Pico while connected to local system, 
module called rshell is needed. The following steps show how to run main script on Pico.
1. Run ```pip install rshell``` in terminal.
2. Run ``rshell`` in terminal.
3. To copy local files to the board (e.g ``main.py``), run ``cp main.py /pyboard`` in terminal. 
(Alternatively, the files can be flashed to the board sing ``adafruit-ampy``)
4. Run ``repl`` in terminal. This command will open console on the board.
5. Run ``Ctrl + D``. This will perform soft reboot on the board and run ``main.py`` in its root.

In case Pico becomes corrupted, or the program enters a state which is difficult
to enter or nullify using ``rshell``, the board's Flash memory can be reset.
This known as nuking the board. Necessary steps and files needed can be found [here](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#resetting-flash-memory).

### Useful rshell commands:
```ls /pyboard``` - list directory items\
```cp utils/__init__.py /pyboard/utils``` - copy ``__init__.py`` in ``utils/`` 


### Useful REPL Commands:
```Ctrl + D``` - soft reboot\
``Ctrl + X`` - exit console

### Error handling:
Currently, the error handling is configured to behave as follows:
If API has an internal error, the api is (re)run again (``api.run()``) instead of performing soft reboot of the board and
without initiating Api object.

On the other hand, if an exception is raised in functions belonging to the components of the board (including the board
itself within ``board.py``), an entire board is softly rebooted.  

