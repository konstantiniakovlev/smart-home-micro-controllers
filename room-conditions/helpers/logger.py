from utils.timestamp import localtime


class Logger:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    TEMPLATE = "{timestamp} [{level}]: {message}"

    LOG_LEVEL = None

    def log(func):

        def wrapper(self, *args, **kwargs):
            level, msg = func(*args, **kwargs)
            if self._valid_level(level):
                print(
                    Logger.TEMPLATE.format(
                        timestamp=localtime(),
                        level=level,
                        message=msg,
                    )
                )

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

    def set_level(self, level):
        self.LOG_LEVEL = level

    def _valid_level(self, level):
        if self.LOG_LEVEL is None:
            return False

        log_criticality_level = {
            self.DEBUG: 0,
            self.INFO: 1,
            self.WARNING: 2,
            self.ERROR: 3,
            self.CRITICAL: 4
        }

        return log_criticality_level[level] >= log_criticality_level[self.LOG_LEVEL]
