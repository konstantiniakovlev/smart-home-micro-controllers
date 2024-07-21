import sys


def internal_error_handler(func):

    # todo: test this handler
    def wrapper(self, *args, **kwargs):

        while True:
            try:
                func_output = func(self, *args, **kwargs)
                return func_output

            except Exception as e:
                sys.print_exception(e)
                if self.connection is not None:
                    self._send_internal_error_response(self.connection)
                    self.connection.close()

    return wrapper
