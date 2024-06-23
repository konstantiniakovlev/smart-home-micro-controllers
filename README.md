# Micro-controllers

## Test locally
To test code on Raspberry Pi Pico while connected to local system, 
we first need to install rshell:\
```pip install rshell```.\
Run ``rshell`` in terminal.\
First, files need to be copied to the board (e.g. ``main.py``):\
```cp main.py /pyboard``` will copy main file to the board's root directory.\
When all necessary files have been copied to the board, you can enter interactive toplevel by running ``repl`` command
which will open console on the board.

#### Useful rshell commands:


#### Useful REPL Commands:
```Ctrl + D``` - soft reboot\
``Ctrl + X`` - exit console\
```ls /pyboard``` - list directory items

