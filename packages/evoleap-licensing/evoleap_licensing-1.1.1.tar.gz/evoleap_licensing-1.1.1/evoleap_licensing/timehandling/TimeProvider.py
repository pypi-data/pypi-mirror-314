from datetime import datetime
from .UtcDateTime import UtcDateTime


def Default():
    return SystemTimeProvider()


def Current():
    return SystemTimeProvider()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SystemTimeProvider(metaclass=Singleton):

    def UtcNow(self):
        return UtcDateTime(datetime.utcnow())
