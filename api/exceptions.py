import sys


def internal_error_handler(func):

    def wrapper(self, *args, **kwargs):
        try:
            func_output = func(self, *args, **kwargs)
            return func_output

        except Exception as e:
            sys.print_exception(e)
            if self.connection is not None:
                self._send_internal_error_response(self.connection)
                self.connection.close()
            sys.exit()  # soft reboot

    return wrapper
