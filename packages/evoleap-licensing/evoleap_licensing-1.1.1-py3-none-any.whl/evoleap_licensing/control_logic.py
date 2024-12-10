from .timehandling.UtcDateTime import UtcDateTime
from . import ControlStrategy
from datetime import timedelta
from typing import Optional, List, Tuple


class ControlLogic:

    @staticmethod
    def IsFirstLaunchTimeInvalid(first_launch_time: UtcDateTime, current_time: UtcDateTime) -> bool:
        return current_time < first_launch_time

    @staticmethod
    def IsTimeInconsistencyDetected(last_trusted_time: Optional[UtcDateTime], previous_times: List[UtcDateTime],
                                    current_time: UtcDateTime, current_time_is_trusted: bool):
        if last_trusted_time is None:
            return False

        if current_time_is_trusted:
            return False

        return current_time < last_trusted_time or any([current_time < t for t in previous_times])

    @staticmethod
    def IsInGracePeriodForUnregisteredProduct(control_strategy: ControlStrategy, first_launch_time: UtcDateTime,
                                              current_time: UtcDateTime) -> Tuple[bool, UtcDateTime]:

        expiration = first_launch_time + control_strategy.GracePeriodForUnregisteredProduct
        return current_time < expiration, expiration

    @staticmethod
    def IsInGracePeriodForValidationFailures(grace_period_for_validation_failures: timedelta,
                                             last_successful_validation_time: UtcDateTime,
                                             current_time: UtcDateTime) -> Tuple[bool, UtcDateTime]:
        expiration = last_successful_validation_time + grace_period_for_validation_failures
        return current_time < expiration, expiration
