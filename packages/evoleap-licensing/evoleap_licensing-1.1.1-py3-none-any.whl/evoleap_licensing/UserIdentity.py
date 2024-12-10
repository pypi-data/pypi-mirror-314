from typing import Dict


class UserIdentity(object):

    def __init__(self, data: Dict[str, str]):
        self._data = dict()
        if not (data is None):
            self._data.update(data)

    @property
    def Data(self) -> dict:
        return dict(self._data)
