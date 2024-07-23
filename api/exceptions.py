import sys


def internal_error_handler(func):

    def wrapper(self, *args, **kwargs):

        while True:
            try:
                func_output = func(self, *args, **kwargs)
                return func_output

            except Exception as e:
                if len(args) > 0:
                    socket = args[0]
                else:
                    socket = kwargs["socket"]
                sys.print_exception(e)
                if self.connection is not None:
                    self._send_internal_error_response(self.connection)
                    socket.close_connection(self.connection)

    return wrapper
