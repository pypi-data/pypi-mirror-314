from datetime import datetime, timedelta
import pytz


# noinspection PyProtectedMember
class UtcDateTime(object):
    def __init__(self, datetime_value: datetime):
        self._value = datetime_value.astimezone(pytz.utc)

    @staticmethod
    def Coerce(other):
        if (other is None):
            return None
        elif (isinstance(other, datetime)):
            return UtcDateTime(other)
        elif (isinstance(other, UtcDateTime)):
            return other
        else:
            return None
    def __add__(self, delta: timedelta):
        return UtcDateTime(self._value + delta)

    def __sub__(self, delta_or_other):
        if isinstance(delta_or_other, timedelta):
            return UtcDateTime(self._value - delta_or_other)
        elif isinstance(delta_or_other, UtcDateTime):
            return self._value - delta_or_other._value
        else:
            raise ValueError("delta_or_other must be a timedelta object or UtcDateTime object")

    def __lt__(self, other):
        other = UtcDateTime.Coerce(other)
        return self._value < other._value

    def __gt__(self, other):
        other = UtcDateTime.Coerce(other)
        return self._value > other._value

    def __le__(self, other):
        other = UtcDateTime.Coerce(other)
        return self._value <= other._value

    def __ge__(self, other):
        other = UtcDateTime.Coerce(other)
        return self._value >= other._value

    def __eq__(self, other):
        other = UtcDateTime.Coerce(other)
        return self._value == other._value

    def __ne__(self, other):
        other = UtcDateTime.Coerce(other)
        return self._value != other._value

    def AddDays(self, value):
        return UtcDateTime(self._value + timedelta(days=value))

    def AddMinutes(self, value):
        return UtcDateTime(self._value + timedelta(minutes=value))

    def AsDateTime(self):
        return self._value

    def __hash__(self):
        return hash(self._value)
