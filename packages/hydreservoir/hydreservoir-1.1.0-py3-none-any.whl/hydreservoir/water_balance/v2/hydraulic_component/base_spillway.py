from abc import ABC

from hydreservoir.water_balance.v2.hydraulic_component.passive import Passive


class BaseSpillway(Passive, ABC):
    def __init__(
            self, name: str, elevation: float,
            spillway_discharge_coefficient: float,
            gravitational_acceleration: float,
    ):
        super().__init__(name, elevation, gravitational_acceleration)
        self._spillway_discharge_coefficient = spillway_discharge_coefficient
