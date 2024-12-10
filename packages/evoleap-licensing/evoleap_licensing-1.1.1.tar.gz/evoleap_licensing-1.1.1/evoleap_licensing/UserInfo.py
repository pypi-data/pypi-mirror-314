class UserInfo(object):
    def __init__(self, name: str, email: str):
        self._name = name
        self._email = email

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value: str):
        self._name = value

    @property
    def Email(self):
        return self._email

    @Email.setter
    def Email(self, value: str):
        self._email = value

    def Verify(self):
        if self._name is None:
            raise ValueError('User name cannot be None')
        if self._email is None:
            raise ValueError('User email cannot be None')
