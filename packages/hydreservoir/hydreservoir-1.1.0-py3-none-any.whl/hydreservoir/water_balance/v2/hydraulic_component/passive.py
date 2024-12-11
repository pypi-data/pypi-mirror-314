from abc import ABC, abstractmethod

from hydreservoir.water_balance.v2.hydraulic_component.core import Core


class Passive(Core, ABC):
    def __init__(
            self, name: str,
            elevation: float,
            gravitational_acceleration: float,
    ):
        super().__init__(name)

        self._elevation = elevation
        self._gravitational_acceleration = gravitational_acceleration
