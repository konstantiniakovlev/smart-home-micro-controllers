import sys


def error_handler(func):
    def wrapper(self, *args, **kwargs):
        try:
            func_output = func(self, *args, **kwargs)
            return func_output

        except KeyboardInterrupt as e:
            sys.print_exception(e)
            sys.exit()

        except Exception as e:
            sys.print_exception(e)
            raise e

    return wrapper
