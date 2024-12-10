from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TokenUsage:
    tokens_entitled: int
    tokens_in_use: int
    tokens_in_use_by_session: int


@dataclass(frozen=True)
class SessionUsage:
    sessions_entitled: int
    sessions_in_use: int
    in_use_by_session: bool

@dataclass(frozen=True)
class CurrencyUsage:
    currency_entitled: int
    currency_used: int


class ComponentEntitlementInfo:
    _id: int
    _components: List[str]
    _tokenUsage: TokenUsage
    _sessionUsage: SessionUsage
    _currencyUsage: CurrencyUsage

    @property
    def ID(self) -> int:
        return self._id

    @ID.setter
    def ID(self, value: int):
        self._id = value

    @property
    def Components(self) -> List[str]:
        return self._components

    @Components.setter
    def Components(self, value: List[str]):
        self._components = list(value)

    @property
    def TokenUsage(self):
        return self._tokenUsage

    @TokenUsage.setter
    def TokenUsage(self, value: TokenUsage):
        self._tokenUsage = value

    @property
    def SessionUsage(self) -> SessionUsage:
        return self._sessionUsage

    @SessionUsage.setter
    def SessionUsage(self, value: SessionUsage):
        self._sessionUsage = value

    @property
    def CurrencyUsage(self) -> CurrencyUsage:
        return self._currencyUsage

    @CurrencyUsage.setter
    def CurrencyUsage(self, value: CurrencyUsage):
        self._currencyUsage = value