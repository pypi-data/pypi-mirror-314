from .enumerations.licensing_enumerations import InvalidReason
from datetime import datetime, timedelta
from .timehandling.UtcDateTime import UtcDateTime
from .timehandling import TimeProvider


class SessionValidity:
    _isValid: bool = False
    _invalidReason: InvalidReason = InvalidReason.Unknown
    _isInValidationFailureGracePeriod: bool = False
    _isInUnregisteredGracePeriod: bool = False
    _isOfflineCheckout: bool = False
    _hasExpiredOfflineCheckout: bool = False
    _gracePeriodExpiration: datetime = datetime.min
    _validityDuration: timedelta = timedelta(days=0)

    @property
    def IsValid(self) -> bool:
        return self._isValid

    @IsValid.setter
    def IsValid(self, value: bool):
        self._isValid = value

    @property
    def InvalidReason(self) -> InvalidReason:
        return self._invalidReason

    @InvalidReason.setter
    def InvalidReason(self, value: InvalidReason):
        self._invalidReason = value

    @property
    def IsInValidationFailureGracePeriod(self) -> bool:
        return self._isInValidationFailureGracePeriod

    @IsInValidationFailureGracePeriod.setter
    def IsInValidationFailureGracePeriod(self, value: bool):
        self._isInValidationFailureGracePeriod = value

    @property
    def IsInUnregisteredGracePeriod(self) -> bool:
        return self._isInUnregisteredGracePeriod

    @IsInUnregisteredGracePeriod.setter
    def IsInUnregisteredGracePeriod(self, value: bool):
        self._isInUnregisteredGracePeriod = value

    @property
    def IsOfflineCheckout(self) -> bool:
        return self._isOfflineCheckout

    @IsOfflineCheckout.setter
    def IsOfflineCheckout(self, value: bool):
        self._isOfflineCheckout = value

    @property
    def HasExpiredOfflineCheckout(self) -> bool:
        return self._hasExpiredOfflineCheckout

    @HasExpiredOfflineCheckout.setter
    def HasExpiredOfflineCheckout(self, value: bool):
        self._hasExpiredOfflineCheckout = value

    @property
    def GracePeriodExpiration(self) -> datetime:
        return self._gracePeriodExpiration

    @GracePeriodExpiration.setter
    def GracePeriodExpiration(self, value: datetime):
        self._gracePeriodExpiration = value

    @property
    def ValidityDuration(self) -> timedelta:
        return self._validityDuration

    @ValidityDuration.setter
    def ValidityDuration(self, value: timedelta):
        self._validityDuration = value

    @classmethod
    def Invalid(cls, reason: InvalidReason, has_expired_offline_checkout: bool):
        ret = cls()
        ret.IsValid = False
        ret.InvalidReason = reason
        ret.HasExpiredOfflineCheckout = has_expired_offline_checkout
        return ret

    @classmethod
    def Valid(cls, validity_duration: timedelta):
        ret = cls()
        ret.IsValid = True
        ret.ValidityDuration = validity_duration
        return ret

    @classmethod
    def UnregisteredGracePeriod(cls, expiration: UtcDateTime):
        ret = cls()
        ret.IsValid = True
        ret.ValidityDuration = expiration - TimeProvider.Current().UtcNow()
        ret.IsInUnregisteredGracePeriod = True
        ret.GracePeriodExpiration = expiration.AsDateTime()
        return ret

    @classmethod
    def ValidationFailureGracePeriod(cls, expiration: UtcDateTime):
        ret = cls()
        ret.IsValid = True
        ret.ValidityDuration = expiration - TimeProvider.Current().UtcNow()
        ret.IsInValidationFailureGracePeriod = True
        ret.GracePeriodExpiration = expiration.AsDateTime()
        return ret

    @classmethod
    def OfflineCheckout(cls, expiration: UtcDateTime):
        ret = cls()
        ret.IsValid = True
        ret.ValidityDuration = expiration - TimeProvider.Current().UtcNow()
        ret.IsOfflineCheckout = True
        return ret
