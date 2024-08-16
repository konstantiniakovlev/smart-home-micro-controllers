from utils.timestamp import localtime


class Logger:
    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"
    WARNING = "WARNING"
    TEMPLATE = "{timestamp} [{level}]: {message}"

    def log(func):

        def wrapper(self, *args, **kwargs):
            level, msg = func(*args, **kwargs)
            print(Logger.TEMPLATE.format(
                timestamp=localtime(),
                level=level,
                message=msg,
                ))

        return wrapper

    @log
    def critical(msg = None):
        return Logger.CRITICAL, msg

    @log
    def debug(msg = None):
        return Logger.DEBUG, msg

    @log
    def error(msg = None):
        return Logger.ERROR, msg

    @log
    def info(msg = None):
        return Logger.INFO, msg

    @log
    def warning(msg = None):
        return Logger.WARNING, msg
