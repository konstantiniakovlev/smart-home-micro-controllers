class Methods:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


class Router(object):
    def __init__(self, path):
        self.path = path
        self.method = Methods.GET

    def __call__(self, func):
        self.func = func

        def wrapper(*args, **kwargs):
            print(self.path)
            print(kwargs)
            if self.method in args or self.method == kwargs.get("method"):
                if self.path in args or self.path == kwargs.get("endpoint"):
                    return func(*args, **kwargs)
        return wrapper

    @classmethod
    def get(cls, path):
        cls.path = path
        cls.method = Methods.GET
        return cls(path)

    @classmethod
    def post(cls, path):
        cls.path = path
        cls.method = Methods.POST
        return cls(path)
