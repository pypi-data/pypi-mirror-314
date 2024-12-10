from typing import Optional, Dict

DEFAULT_CASE_SENSITIVE: bool = True
DEFAULT_WEIGHT: int = 1
DEFAULT_MAX_ARRAY_VALUE_DIFFERENCE: int = 1
DEFAULT_VERSION = 1
DEFAULT_MAX_MISMATCH_COUNT = 1


class InstanceIdentityValue(object):
    def __init__(self, value: object, case_sensitive: Optional[bool] = DEFAULT_CASE_SENSITIVE,
                 weight: Optional[int] = DEFAULT_WEIGHT,
                 max_array_value_difference: Optional[int] = DEFAULT_MAX_ARRAY_VALUE_DIFFERENCE):
        if value is None:
            raise ValueError('Value cannot be None')
        self._value = value
        self._caseSensitive = case_sensitive
        self._weight = weight
        self._maxArrayValueDifference = max_array_value_difference

    @property
    def Value(self) -> object:
        return self._value

    @property
    def CaseSensitive(self) -> bool:
        return self._caseSensitive

    @property
    def Weight(self) -> int:
        return self._weight

    @property
    def MaxArrayValueDifference(self) -> int:
        return self._maxArrayValueDifference


class InstanceIdentity(object):
    def __init__(self, values: Dict[str, InstanceIdentityValue], version: Optional[int] = DEFAULT_VERSION,
                 maximum_mismatch_count: Optional[int] = DEFAULT_MAX_MISMATCH_COUNT):
        self._values = dict(values)
        self._version = version
        self._maximumMismatchCount = maximum_mismatch_count

    @property
    def Version(self) -> int:
        return self._version

    @property
    def MaximumMismatchCount(self) -> int:
        return self._maximumMismatchCount

    @property
    def Values(self) -> Dict[str, InstanceIdentityValue]:
        return dict(self._values)
