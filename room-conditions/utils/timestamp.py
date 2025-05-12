import ntptime
import time


def localtime():
    dt = time.localtime()
    year, month, day = dt[0:3]
    hour, minute, second = dt[3:6]
    dt_str = "{:02d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        year, month, day, hour, minute, second
    )
    return dt_str


def sync_network_time():
    ntptime.host = 'pool.ntp.org'
    ntptime.settime()
