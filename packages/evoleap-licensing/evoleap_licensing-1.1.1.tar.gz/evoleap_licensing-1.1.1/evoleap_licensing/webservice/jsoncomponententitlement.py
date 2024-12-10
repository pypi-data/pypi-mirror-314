from typing import List, Dict

from ..ComponentEntitlementInfo import TokenUsage, SessionUsage, CurrencyUsage, ComponentEntitlementInfo


class JSONComponentEntitlement:
    __fields = ["id", "components", "tokens_entitled", "tokens_in_use", "tokens_in_use_by_session",
                  "tokens_checked_out", "sessions_entitled", "sessions_in_use", "in_use_by_session",
                  "currency_entitled", "currency_used"]

    def __init__(self, values: Dict[str, object]):
        self.id = 0
        self.components = []
        self.tokens_entitled = 0
        self.tokens_in_use = 0
        self.tokens_in_use_by_session = 0
        self.sessions_entitled = 0
        self.sessions_in_use = 0
        self.currency_entitled = 0
        self.currency_used = 0
        self.in_use_by_session = False
        [self.__setattr__(a, values[a]) for a in self.__class__.__fields if a in values]

    def Deserialize(self) -> ComponentEntitlementInfo:
        info = ComponentEntitlementInfo()
        info.ID = self.id
        info.Components = self.components
        info.TokenUsage = TokenUsage(self.tokens_entitled, self.tokens_in_use, self.tokens_in_use_by_session)
        info.SessionUsage = SessionUsage(self.sessions_entitled, self.sessions_in_use, self.in_use_by_session)
        info.CurrencyUsage = CurrencyUsage(self.currency_entitled, self.currency_used)
        return info
