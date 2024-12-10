from datetime import timedelta


class ControlStrategy:
    _locked: bool
    _gracePeriod: timedelta = timedelta(seconds=0)

    def Lock(self):
        self._locked = True

    @property
    def GracePeriodForUnregisteredProduct(self) -> timedelta:
        return self._gracePeriod

    @GracePeriodForUnregisteredProduct.setter
    def GracePeriodForUnregisteredProduct(self, value: timedelta):
        if self._locked:
            raise ValueError('Control strategy cannot be changed after it has been used')
        self._gracePeriod = value
