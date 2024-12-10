from typing import List
from .ComponentInfo import ComponentInfo
from .ComponentEntitlementInfo import ComponentEntitlementInfo


class ComponentsStatus:
    _success: bool
    _components: List[ComponentInfo]
    _componentEntitlements: List[ComponentEntitlementInfo]

    @property
    def Success(self) -> bool:
        return self._success

    @Success.setter
    def Success(self, value: bool):
        self._success = value

    @property
    def Components(self) -> List[ComponentInfo]:
        return self._components

    @Components.setter
    def Components(self, value: List[ComponentInfo]):
        self._components = value

    @property
    def ComponentEntitlements(self) -> List[ComponentEntitlementInfo]:
        return self._componentEntitlements

    @ComponentEntitlements.setter
    def ComponentEntitlements(self, value: List[ComponentEntitlementInfo]):
        self._componentEntitlements = value
